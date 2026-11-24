import os
import re
import json
import random
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
import urllib3
from jinja2 import Template

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOMINIO_SITE = "https://gerador-site.pages.dev"
NOME_MARCA = "Oportunidade e Vagas de Emprego"

GOOGLE_META = '<meta name="google-site-verification" content="pbgwZbVwgKMwqqqGYFcHeGGbV7EM7nBdlns1c_DN_Sw" />'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5379027874215422" crossorigin="anonymous"></script>'

# Mantenha scripts de outras redes de anuncios desativados durante a revisao do AdSense:
MONETAG_SCRIPT = '<!-- <script src="https://quge5.com/88/tag.min.js" data-zone="309679" async data-cfasync="false"></script> -->'

ADS_TXT_CONTENT = "google.com, pub-5379027874215422, DIRECT, f08c47fec0942fa0"

FAVICON_TAG = (
    '<link rel="icon" type="image/svg+xml" href="'
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<rect width='100' height='100' rx='20' fill='%231e3a8a'/>"
    "<text x='50%' y='55%' dominant-baseline='middle' text-anchor='middle' "
    "fill='%2338bdf8' font-family='Arial, sans-serif' font-size='65' font-weight='bold'>O</text>"
    '</svg>">'
)

AD_BANNER = """
<!-- Bloco de anuncio opcional desativado durante revisao do AdSense -->
"""

TICKER_COTACOES = """
<div style="background: #0f172a; color: #f8fafc; border-bottom: 1px solid #1e293b; padding: 10px 0; font-size: 12px; font-weight: 600; overflow: hidden; white-space: nowrap;">
    <div style="display: flex; animation: scrollTicker 35s linear infinite; gap: 40px; width: max-content; padding-left: 20px;">
        <span>📋 <strong>Guia do Candidato:</strong> Currículo objetivo e preparo para entrevistas</span>
        <span>🏛️ <strong>Concursos Públicos:</strong> Leitura de editais, prazos e provas</span>
        <span>💼 <strong>Mercado CLT:</strong> Indústria, comércio, logística e serviços</span>
        <span style="color: #4ade80;">💻 <strong>Trabalho Remoto:</strong> Boas práticas para rotinas digitais</span>
        <span style="color: #60a5fa;">✅ <strong>Portal Informativo:</strong> Orientação profissional e curadoria de fontes</span>
    </div>
</div>
<style>
@keyframes scrollTicker {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.nav-link { color: #cbd5e1; text-decoration: none; font-size: 13px; font-weight: 600; transition: color 0.2s; }
.nav-link:hover { color: #60a5fa; }
</style>
"""

NAV_BAR = """
<nav style="background: #0f172a; border-bottom: 1px solid #1e293b; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
    <a href="index.html" style="color: #ffffff; text-decoration: none; font-size: 18px; font-weight: 800; letter-spacing: -0.5px;">Oportunidade<span style="color: #38bdf8;">Vagas</span></a>
    <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center;">
        <a href="index.html" class="nav-link">Início</a>
        <a href="sobre.html" class="nav-link">Sobre</a>
        <a href="termos.html" class="nav-link">Termos de Uso</a>
        <a href="privacidade.html" class="nav-link">Privacidade</a>
        <a href="contato.html" class="nav-link">Contato</a>
    </div>
</nav>
"""

BREAKING_NEWS_TICKER = """
<div style="background: #ea580c; color: white; padding: 12px 18px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; box-shadow: 0 4px 10px rgba(234,88,12,0.15); box-sizing: border-box; flex-wrap: wrap;">
    <span style="background: white; color: #ea580c; padding: 4px 10px; border-radius: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; flex-shrink: 0;">🔥 ORIENTAÇÃO</span>
    <div style="overflow: hidden; white-space: nowrap; flex: 1; min-width: 200px;">
        <div style="display: inline-block; animation: scrollTicker 25s linear infinite;">
            📌 Guias práticos para candidaturas, leitura de editais e organização de estudos    |    ⚠️ Nunca pague taxas indevidas para participar de seleções ou enviar currículo.
        </div>
    </div>
</div>
"""

GUIA_EDITORIAL_SECTION = """
<div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 12px; margin-top: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
    <h3 style="margin-top: 0; color: #1e3a8a; font-size: 18px;">📌 Boas Práticas para Candidaturas e Concursos</h3>
    <p style="font-size: 13px; color: #475569; line-height: 1.6; margin-bottom: 20px;">
        Organizar a busca por emprego ou a preparação para concursos exige atenção a detalhes práticos que fazem diferença na triagem de currículos e no cumprimento de prazos oficiais:
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; font-size: 13px; color: #334155; line-height: 1.6;">
        <div style="background: #f8fafc; padding: 18px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 15px;">1. Currículo direto ao ponto</h4>
            <p style="margin: 0;">Destaque o objetivo profissional, um breve resumo das suas competências, experiências recentes com atividades claras e cursos concluídos. Mantenha a formatação limpa, legível e atualizada em PDF.</p>
        </div>
        <div style="background: #f8fafc; padding: 18px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 15px;">2. Leitura atenta do edital ou vaga</h4>
            <p style="margin: 0;">Confira escolaridade exigida, regime de contratação, escala de trabalho, localização e prazos de inscrição. Em concursos públicos, acompanhe retificações e cronogramas diretamente no site da banca.</p>
        </div>
        <div style="background: #f8fafc; padding: 18px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 15px;">3. Segurança digital na seleção</h4>
            <p style="margin: 0;">Desconfie de cobranças antecipadas para exames, uniformes, materiais ou inscrição fora de canais oficiais. Verifique sempre a autenticidade da empresa ou órgão antes de compartilhar documentos.</p>
        </div>
    </div>
</div>
"""

GUIA_ENTREVISTA_SECTION = """
<div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 12px; margin-top: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
    <h3 style="margin-top: 0; color: #1e3a8a; font-size: 18px;">🎯 Preparação para Entrevistas e Rotina de Estudos</h3>
    <p style="font-size: 13px; color: #475569; line-height: 1.6; margin-bottom: 18px;">
        Tanto em processos seletivos de empresas quanto na preparação para concursos públicos, consistência e clareza na comunicação ajudam a evitar erros comuns:
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; font-size: 13px; color: #334155; line-height: 1.6;">
        <div style="background: #f8fafc; padding: 18px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 15px;">Na entrevista de emprego</h4>
            <p style="margin: 0;">Prepare exemplos reais de situações em que resolveu problemas, cumpriu metas ou trabalhou em equipe. Seja objetivo ao falar sobre sua última experiência e revise os requisitos da vaga antes da conversa.</p>
        </div>
        <div style="background: #f8fafc; padding: 18px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h4 style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 15px;">Na rotina de concursos e cursos</h4>
            <p style="margin: 0;">Divida o tempo de estudo entre leitura do conteúdo base, revisão periódica e resolução de questões. Pequenos blocos diários bem executados costumam ser mais sustentáveis do que maratonas irregulares.</p>
        </div>
    </div>
</div>
"""

CALCULADORAS_SECTION = """
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 40px;">
    <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
        <h3 style="margin-top: 0; color: #1e3a8a; font-size: 16px;">🧮 Simulador Educativo de Salário Líquido</h3>
        <p style="font-size: 13px; color: #64748b; margin-bottom: 15px;">Estimativa simplificada apenas para fins educativos (não substitui cálculo oficial ou holerite):</p>
        <input type="number" id="salarioBrutoInput" placeholder="Ex: 2500" style="padding: 12px 15px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; width: 100%; box-sizing: border-box; outline: none; margin-bottom: 12px; background: #f8fafc; color: #0f172a; font-weight: 600;">
        <button type="button" onclick="calcularSalario()" style="background: #2563eb; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; width: 100%; box-sizing: border-box;">Simular Líquido</button>
        <div id="resultadoSalarioBox" style="margin-top: 15px; display: none; background: #eff6ff; padding: 12px; border-radius: 6px; border: 1px solid #bfdbfe; font-size: 12px; color: #1e3a8a; box-sizing: border-box;"></div>
    </div>

    <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
        <h3 style="margin-top: 0; color: #1e3a8a; font-size: 16px;">🛡️ Orientação sobre Seguro-Desemprego</h3>
        <p style="font-size: 13px; color: #64748b; margin-bottom: 15px;">Selecione o histórico de solicitações para ver orientações gerais:</p>
        <select id="vezesSeguro" style="padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; width: 100%; box-sizing: border-box; outline: none; margin-bottom: 12px; background: white; color: #0f172a; font-weight: 600;">
            <option value="1">1ª Solicitação</option>
            <option value="2">2ª Solicitação</option>
            <option value="3">3ª Solicitação ou mais</option>
        </select>
        <button type="button" onclick="calcularSeguro()" style="background: #059669; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; width: 100%; box-sizing: border-box;">Ver Orientação</button>
        <div id="resultadoSeguroBox" style="margin-top: 15px; display: none; background: #ecfdf5; padding: 12px; border-radius: 6px; border: 1px solid #a7f3d0; font-size: 12px; color: #065f46; box-sizing: border-box;"></div>
    </div>
</div>
<script>
function calcularSalario() {
    let bruto = parseFloat(document.getElementById('salarioBrutoInput').value);
    if (isNaN(bruto) || bruto <= 0) {
        alert('Digite um valor válido maior que zero!');
        return;
    }
    let inss = bruto <= 1412 ? bruto * 0.075 : (bruto <= 2666.68 ? bruto * 0.09 : (bruto <= 4000.03 ? bruto * 0.12 : bruto * 0.14));
    if (inss > 908.85) inss = 908.85;
    let baseIr = bruto - inss;
    let irrf = baseIr > 2259.20 ? (baseIr * 0.075 - 169.44) : 0;
    if (irrf < 0) irrf = 0;
    let liquido = bruto - inss - irrf;
    let box = document.getElementById('resultadoSalarioBox');
    box.style.display = 'block';
    box.innerHTML = `<strong>Estimativa Líquida:</strong> R$ ${liquido.toFixed(2)}<br>(Simulação simplificada: INSS ~R$ ${inss.toFixed(2)} | IRRF ~R$ ${irrf.toFixed(2)})`;
}

function calcularSeguro() {
    let tipo = document.getElementById('vezesSeguro').value;
    let texto = tipo === "1"
        ? "Na 1ª solicitação, o número de parcelas depende do tempo de trabalho exigido e comprovado nos períodos de referência previstos em lei."
        : "Nas solicitações seguintes, a quantidade de parcelas varia conforme o tempo de serviço acumulado dentro das regras trabalhistas vigentes.";
    let box = document.getElementById('resultadoSeguroBox');
    box.style.display = 'block';
    box.innerHTML = `<strong>Orientação:</strong><br>${texto}`;
}
</script>
"""

FOOTER_ROBUSTO = f"""
<footer style="background: #ffffff; border-top: 1px solid #e2e8f0; margin-top: 60px; padding: 40px 20px; box-sizing: border-box;">
    <div style="max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 30px; text-align: left; margin-bottom: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 30px;">
        <div>
            <h4 style="color: #1e3a8a; font-size: 15px; margin-top: 0;">Oportunidade e Vagas</h4>
            <p style="font-size: 13px; color: #64748b; line-height: 1.5;">Portal informativo com guias práticos, orientações sobre concursos públicos, carreira e atalhos para plataformas externas.</p>
        </div>
        <div>
            <h4 style="color: #1e3a8a; font-size: 15px; margin-top: 0;">Links Rápidos</h4>
            <ul style="list-style: none; padding: 0; margin: 0; font-size: 13px; line-height: 2;">
                <li><a href="index.html" style="color: #2563eb; text-decoration: none;">Página Inicial</a></li>
                <li><a href="sobre.html" style="color: #2563eb; text-decoration: none;">ℹ️ Sobre o Portal</a></li>
                <li><a href="contato.html" style="color: #2563eb; text-decoration: none;">✉️ Contato</a></li>
            </ul>
        </div>
        <div>
            <h4 style="color: #1e3a8a; font-size: 15px; margin-top: 0;">Institucional & FAQ</h4>
            <ul style="list-style: none; padding: 0; margin: 0; font-size: 13px; line-height: 2;">
                <li><a href="#faqSection" style="color: #64748b; text-decoration: none;">❓ Perguntas Frequentes (FAQ)</a></li>
                <li><a href="termos.html" style="color: #64748b; text-decoration: none;">📄 Termos de Uso</a></li>
                <li><a href="privacidade.html" style="color: #64748b; text-decoration: none;">🔒 Política de Privacidade</a></li>
            </ul>
        </div>
    </div>
    <div style="max-width: 1000px; margin: 0 auto; text-align: center; color: #64748b; font-size: 13px;">
        <p>© 2026 {NOME_MARCA}. Todos os direitos reservados.</p>
    </div>
</footer>
"""

FAQ_SECTION = """
<div id="faqSection" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 12px; margin-top: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
    <h3 style="margin-top: 0; color: #1e3a8a; font-size: 18px;">❓ Perguntas Frequentes (FAQ do Candidato)</h3>
    <div style="margin-top: 20px; font-size: 13px; color: #334155; line-height: 1.6;">
        <p><strong>1. Como faço para consultar oportunidades ou editais?</strong><br>Clique no botão "Acessar Fonte →" no cartão escolhido para abrir o portal ou fonte externa correspondente e verificar requisitos, prazos e regras oficiais.</p>
        <p><strong>2. O site cobra alguma taxa?</strong><br>Não. A leitura dos guias, orientações e simuladores educativos do portal é gratuita e não cobramos taxas de inscrição ou intermediação.</p>
        <p><strong>3. Posso filtrar o conteúdo da página inicial?</strong><br>Sim! Utilize os botões de categoria no topo ou digite um termo na barra de pesquisa para filtrar os cartões exibidos e abrir atalhos em sites externos.</p>
        <p><strong>4. Os valores dos simuladores são definitivos?</strong><br>Não. Os simuladores servem apenas como referência educativa inicial e não substituem cálculos oficiais ou conferência em documentos formais.</p>
    </div>
</div>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ favicon_tag | safe }}
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/index.html">
    <meta property="og:title" content="Oportunidade e Vagas de Emprego - Concursos, CLT e Home Office">
    <meta property="og:description" content="Guias práticos, orientações sobre concursos públicos, trabalho remoto e atalhos para plataformas de carreira.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ dominio }}/index.html">
    <title>Oportunidade e Vagas de Emprego - Concursos, CLT e Home Office</title>
    <meta name="description" content="Orientações sobre emprego, concursos públicos, trabalho remoto, preparação para entrevistas e simuladores educativos.">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; box-sizing: border-box; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 45px 20px; text-align: center; box-sizing: border-box; }
        .header-top h1 { margin: 0 0 10px 0; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
        .header-top p { margin: 0 auto 25px auto; opacity: 0.9; font-size: 15px; max-width: 600px; line-height: 1.5; }

        .search-container { max-width: 600px; margin: 0 auto; display: flex; gap: 10px; background: white; padding: 8px; border-radius: 35px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); box-sizing: border-box; }
        .search-input { flex-grow: 1; border: none; outline: none; padding: 12px 20px; font-size: 14px; border-radius: 30px; width: 100%; box-sizing: border-box; }
        .search-btn { background: #2563eb; color: white; border: none; padding: 12px 28px; border-radius: 30px; font-weight: 700; cursor: pointer; font-size: 14px; transition: background 0.2s; flex-shrink: 0; }
        .search-btn:hover { background: #1d4ed8; }

        .filter-nav { background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 12px 20px; text-align: center; position: sticky; top: 0; z-index: 100; display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; box-sizing: border-box; }
        .filter-btn { background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 13px; cursor: pointer; transition: all 0.2s; }
        .filter-btn:hover, .filter-btn.active { background: #2563eb; color: white; border-color: #2563eb; }

        .states-top-bar { background: #1e293b; padding: 15px 20px; text-align: center; border-bottom: 1px solid #334155; box-sizing: border-box; }
        .states-top-bar p { color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase; margin: 0 0 10px 0; letter-spacing: 1px; }
        .states-box { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 1000px; margin: 0 auto; box-sizing: border-box; }
        .state-pill { background: #334155; border: 1px solid #475569; padding: 8px 14px; border-radius: 6px; text-decoration: none; color: #f8fafc; font-weight: 600; font-size: 12px; transition: background 0.2s; box-sizing: border-box; }
        .state-pill:hover { background: #2563eb; border-color: #2563eb; }

        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; box-sizing: border-box; }
        .section-title { font-size: 20px; font-weight: 700; margin: 40px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; color: #0f172a; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }

        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; box-sizing: border-box; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; width: 300px; max-width: 100%; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.03); transition: transform 0.2s, box-shadow 0.2s; box-sizing: border-box; }
        .card:hover { transform: translateY(-4px); box-shadow: 0 10px 15px rgba(0,0,0,0.08); border-color: #2563eb; }
        .card img { width: 100%; height: 160px; object-fit: cover; background: #e2e8f0; }
        .card-body { padding: 18px; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; box-sizing: border-box; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 10px; width: fit-content; text-transform: uppercase; letter-spacing: 0.5px; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.4; }
        .btn-vaga { display: block; text-align: center; background: #2563eb; color: white; padding: 11px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 700; transition: background 0.2s; box-sizing: border-box; }
        .btn-vaga:hover { background: #1d4ed8; }

        #resultadoBuscaBox { display: none; background: #eff6ff; border: 2px dashed #2563eb; padding: 25px; border-radius: 12px; margin-top: 30px; text-align: center; box-sizing: border-box; }
        #resultadoBuscaBox h3 { color: #1e3a8a; margin-top: 0; }
        .links-diretoria { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 15px; box-sizing: border-box; }
        .diretorio-btn { background: #2563eb; color: white; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13px; transition: background 0.2s; box-sizing: border-box; }
        .diretorio-btn:hover { background: #1d4ed8; }

        .guias-box { background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 12px; margin-top: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box; }
        .guias-box h3 { margin-top: 0; color: #1e3a8a; font-size: 18px; }
        .guias-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px; box-sizing: border-box; }
        .guia-item { background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; justify-content: space-between; text-decoration: none; transition: all 0.2s; box-sizing: border-box; }
        .guia-item:hover { border-color: #2563eb; transform: translateY(-2px); }
        .guia-item h4 { margin: 0 0 8px 0; font-size: 15px; color: #1e3a8a; }
        .guia-item p { margin: 0 0 14px 0; font-size: 13px; color: #475569; line-height: 1.4; }
        .guia-link { font-size: 12px; font-weight: 700; color: #2563eb; text-transform: uppercase; }

        @media (max-width: 768px) {
            .header-top { padding: 30px 15px; }
            .header-top h1 { font-size: 24px; }
            .search-container { flex-direction: column; background: transparent; box-shadow: none; padding: 0; gap: 10px; }
            .search-input { border-radius: 30px; padding: 14px 20px; border: 1px solid #cbd5e1; }
            .search-btn { width: 100%; border-radius: 30px; padding: 14px; }
            .main-container { padding: 15px; }
            .card { width: 100%; }
        }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    {{ nav_bar | safe }}
    <div class="header-top">
        <h1>Oportunidade e Vagas de Emprego</h1>
        <p>Guias práticos, orientações sobre concursos, trabalho remoto e atalhos de pesquisa</p>

        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Digite o cargo, profissão ou área...">
            <button type="button" class="search-btn" onclick="executarBuscaNacional()">Pesquisar</button>
        </div>
    </div>

    <div class="filter-nav">
        <button type="button" class="filter-btn active" onclick="filtrarCategoria('todas', this)">🏢 Todas as Seções</button>
        <button type="button" class="filter-btn" onclick="filtrarCategoria('concursos', this)">🏛️ Concursos Públicos</button>
        <button type="button" class="filter-btn" onclick="filtrarCategoria('empregos', this)">💼 Vagas CLT & Empresas</button>
        <button type="button" class="filter-btn" onclick="filtrarCategoria('homeoffice', this)">💻 Trabalho Home Office</button>
    </div>

    <div class="states-top-bar">
        <p>📍 Selecione um Estado para ver Orientações Regionais e Municípios:</p>
        <div class="states-box" id="statesGrid">
            {% for e in estados %}
            <a href="{{ e.file }}" class="state-pill">{{ e.name }}</a>
            {% endfor %}
        </div>
    </div>

    <div class="main-container">
        {{ breaking_news_ticker | safe }}
        {{ ad_banner | safe }}

        <div id="resultadoBuscaBox">
            <h3 id="tituloBuscaResultado">Resultados da Pesquisa</h3>
            <p style="font-size: 13px; color: #475569;">Filtramos os itens exibidos na página e reunimos atalhos de busca em plataformas externas:</p>
            <div class="links-diretoria" id="linksDiretoriaContainer"></div>
        </div>

        <div id="listaConteudo">
            {% for cat_nome, cat_data in categorias.items() %}
            <div class="categoria-bloco" data-catid="{{ cat_data.id }}">
                <div class="section-title">
                    <span>{{ cat_nome }}</span>
                    <span style="font-size: 12px; font-weight: 600; color: #64748b; background: #e2e8f0; padding: 2px 10px; border-radius: 12px;">{{ cat_data.lista | length }} Itens</span>
                </div>
                <div class="cards-wrapper">
                    {% for noticia in cat_data.lista %}
                    <div class="card" data-titulo="{{ noticia.title | lower }}" data-desc="{{ noticia.description | lower }}">
                        <img src="{{ noticia.image }}" alt="{{ noticia.title }}" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                        <div class="card-body">
                            <div>
                                <span class="badge" style="background-color: {{ cat_data.color }};">{{ cat_nome }}</span>
                                <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow noopener">{{ noticia.title }}</a></h3>
                                <p>{{ noticia.description }}</p>
                            </div>
                            <a href="{{ noticia.link }}" target="_blank" rel="nofollow noopener" class="btn-vaga">Acessar Fonte →</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}
        {{ guia_editorial_section | safe }}
        {{ guia_entrevista_section | safe }}
        {{ calculadoras_section | safe }}

        <div class="guias-box">
            <h3>📖 Ferramentas e Materiais de Apoio</h3>
            <p>Recursos úteis para montar currículo, revisar questões de provas e desenvolver habilidades:</p>
            <div class="guias-list">
                <a href="https://www.canva.com/pt_br/criar/curriculos/" target="_blank" rel="nofollow noopener" class="guia-item">
                    <div>
                        <h4>📝 Modelos de Currículo</h4>
                        <p>Organize suas experiências e formação em um layout limpo e legível para recrutadores.</p>
                    </div>
                    <span class="guia-link">Abrir Ferramenta →</span>
                </a>
                <a href="https://www.qconcursos.com/questoes-de-concursos" target="_blank" rel="nofollow noopener" class="guia-item">
                    <div>
                        <h4>🏛️ Questões de Concursos</h4>
                        <p>Pratique com questões organizadas por banca, órgão e disciplina para provas públicas.</p>
                    </div>
                    <span class="guia-link">Ver Questões →</span>
                </a>
                <a href="https://www.ev.org.br/" target="_blank" rel="nofollow noopener" class="guia-item">
                    <div>
                        <h4>💻 Cursos Gratuitos Online</h4>
                        <p>Aprimore conhecimentos básicos de informática, organização e atendimento para o mercado de trabalho.</p>
                    </div>
                    <span class="guia-link">Conhecer Cursos →</span>
                </a>
            </div>
        </div>

        {{ faq_section | safe }}
    </div>

    {{ footer_robusto | safe }}

    <script>
        function filtrarCategoria(catId, btnEl) {
            let btns = document.getElementsByClassName('filter-btn');
            for (let b of btns) { b.classList.remove('active'); }
            if (btnEl) { btnEl.classList.add('active'); }

            let blocos = document.getElementsByClassName('categoria-bloco');
            for (let bloco of blocos) {
                if (catId === 'todas' || bloco.getAttribute('data-catid') === catId) {
                    bloco.style.display = "";
                } else {
                    bloco.style.display = "none";
                }
            }
        }

        function executarBuscaNacional() {
            let termo = document.getElementById('searchInput').value.trim();
            if (!termo) return;
            let termoLower = termo.toLowerCase();
            let cards = document.getElementsByClassName('card');
            for (let i = 0; i < cards.length; i++) {
                let titulo = cards[i].getAttribute('data-titulo') || "";
                let desc = cards[i].getAttribute('data-desc') || "";
                if (titulo.includes(termoLower) || desc.includes(termoLower)) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
            let box = document.getElementById('resultadoBuscaBox');
            let tituloRes = document.getElementById('tituloBuscaResultado');
            let containerLinks = document.getElementById('linksDiretoriaContainer');
            tituloRes.textContent = `Resultados filtrados para: "${termo}"`;
            let termoEncoded = encodeURIComponent(termo);
            containerLinks.innerHTML = `
                <a href="https://www.infojobs.com.br/vagas-de-emprego-${termoEncoded}.aspx" target="_blank" rel="nofollow noopener" class="diretorio-btn">💼 InfoJobs (${termo})</a>
                <a href="https://www.catho.com.br/vagas/${termoEncoded}/" target="_blank" rel="nofollow noopener" class="diretorio-btn">📄 Catho (${termo})</a>
                <a href="https://br.indeed.com/jobs?q=${termoEncoded}&l=Brasil" target="_blank" rel="nofollow noopener" class="diretorio-btn">🔍 Indeed (${termo})</a>
                <a href="https://www.linkedin.com/jobs/search/?keywords=${termoEncoded}&location=Brasil" target="_blank" rel="nofollow noopener" class="diretorio-btn">🌐 LinkedIn (${termo})</a>
            `;
            box.style.display = "block";
            box.scrollIntoView({ behavior: 'smooth' });
        }

        document.getElementById('searchInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') { executarBuscaNacional(); }
        });
    </script>
</body>
</html>
"""

ESTADO_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ favicon_tag | safe }}
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/{{ estado.file }}">
    <meta property="og:title" content="Guia de Orientação Profissional em {{ estado.name }} - Oportunidade e Vagas">
    <meta property="og:description" content="Orientações regionais, municípios em destaque e atalhos de pesquisa em {{ estado.name }}.">
    <meta property="og:type" content="website">
    <title>Guia em {{ estado.name }} - Oportunidade e Vagas</title>
    <meta name="description" content="Orientações regionais, municípios em destaque e atalhos de pesquisa em {{ estado.name }}.">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; box-sizing: border-box; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 35px 20px; box-sizing: border-box; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0 0 5px 0; font-size: 24px; }
        .header-top p { margin: 0; font-size: 14px; opacity: 0.9; }

        .states-top-bar { background: #1e293b; padding: 15px 20px; text-align: center; border-bottom: 1px solid #334155; box-sizing: border-box; }
        .states-top-bar p { color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase; margin: 0 0 10px 0; letter-spacing: 1px; }
        .states-box { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 1000px; margin: 0 auto; box-sizing: border-box; }
        .state-pill { background: #334155; border: 1px solid #475569; padding: 8px 14px; border-radius: 6px; text-decoration: none; color: #f8fafc; font-weight: 600; font-size: 12px; transition: background 0.2s; box-sizing: border-box; }
        .state-pill:hover { background: #2563eb; border-color: #2563eb; }

        .info-panel { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; margin: 25px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box; }
        .info-panel h2 { margin: 0 0 10px 0; color: #1e3a8a; font-size: 18px; }
        .info-panel p { font-size: 14px; color: #475569; margin: 0 0 12px 0; line-height: 1.6; }
        .checklist { margin: 0; padding-left: 20px; font-size: 13px; color: #334155; line-height: 1.7; }

        .cities-section { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; margin: 25px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box; }
        .cities-section h3 { margin: 0 0 10px 0; color: #1e3a8a; font-size: 16px; }
        .cities-section p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.5; }
        .cities-grid { display: flex; flex-wrap: wrap; gap: 10px; box-sizing: border-box; }
        .city-badge { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; text-decoration: none; transition: all 0.2s; box-sizing: border-box; }
        .city-badge:hover { background: #2563eb; color: white; }

        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; box-sizing: border-box; }
        .section-title { font-size: 20px; font-weight: 700; margin: 30px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; }

        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; box-sizing: border-box; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; width: 300px; max-width: 100%; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.03); transition: transform 0.2s; box-sizing: border-box; }
        .card:hover { transform: translateY(-4px); border-color: #2563eb; }
        .card img { width: 100%; height: 160px; object-fit: cover; background: #e2e8f0; }
        .card-body { padding: 18px; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; box-sizing: border-box; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 10px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.4; }
        .btn-vaga { display: block; text-align: center; background: #2563eb; color: white; padding: 11px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 700; transition: background 0.2s; box-sizing: border-box; }
        .btn-vaga:hover { background: #1d4ed8; }

        @media (max-width: 768px) {
            .header-top { padding: 25px 15px; }
            .main-container { padding: 15px; }
            .card { width: 100%; }
        }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    {{ nav_bar | safe }}
    <div class="header-top">
        <a href="index.html">← Voltar para a Página Inicial</a>
        <h1>Panorama Profissional em {{ estado.name }}</h1>
        <p>Orientações regionais, municípios em destaque e recursos de apoio para {{ estado.name }}</p>
    </div>

    <div class="states-top-bar">
        <p>📍 Ver Outro Estado:</p>
        <div class="states-box">
            {% for e in estados_lista %}
            <a href="{{ e.file }}" class="state-pill">{{ e.name }}</a>
            {% endfor %}
        </div>
    </div>

    <div class="main-container">
        <div class="info-panel">
            <h2>Como Organizar a Busca em {{ estado.name }}</h2>
            <p>
                Ao acompanhar oportunidades e seleções em <strong>{{ estado.name }}</strong>, considere a distância entre bairros ou municípios vizinhos, os horários de transporte público e os requisitos específicos de cada setor econômico estadual.
            </p>
            <ul class="checklist">
                <li><strong>Documentação e registro:</strong> mantenha documentos pessoais, comprovantes de escolaridade e registros profissionais em ordem.</li>
                <li><strong>Editais e bancas:</strong> em concursos estaduais ou municipais em {{ sigla }}, confira sempre o cronograma oficial e possíveis retificações.</li>
                <li><strong>Triagem de propostas:</strong> avalie remuneração, benefícios, escala e canais oficiais antes de avançar.</li>
                <li><strong>Segurança contra golpes:</strong> evite pagamentos antecipados por supostas inscrições, exames ou materiais.</li>
            </ul>
        </div>

        <div class="cities-section">
            <h3>🏙️ Municípios em Destaque em {{ estado.name }}</h3>
            <p>Acesse a página de cada município para ver orientações locais e atalhos de busca:</p>
            <div class="cities-grid">
                {% for cidade in estado.cities %}
                <a href="{{ cidade.file }}" class="city-badge">📌 {{ cidade.name }} ({{ sigla }}) →</a>
                {% endfor %}
            </div>
        </div>

        {{ ad_banner | safe }}

        <div class="section-title">Guias e Leituras de Apoio</div>
        <div class="cards-wrapper">
            {% for noticia in noticias %}
            <div class="card">
                <img src="{{ noticia.image }}" alt="{{ noticia.title }}" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                <div class="card-body">
                    <div>
                        <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                        <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow noopener">{{ noticia.title }}</a></h3>
                        <p>{{ noticia.description }}</p>
                    </div>
                    <a href="{{ noticia.link }}" target="_blank" rel="nofollow noopener" class="btn-vaga">Acessar Fonte →</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}
    </div>

    {{ footer_robusto | safe }}
</body>
</html>
"""

CIDADE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ favicon_tag | safe }}
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/{{ cidade.file }}">
    <meta property="og:title" content="Guia Profissional de {{ cidade.name }} ({{ sigla }}) - Oportunidade e Vagas">
    <meta property="og:description" content="Atalhos de busca e dicas práticas de recolocação em {{ cidade.name }} - {{ sigla }}.">
    <meta property="og:type" content="website">
    <title>Guia de {{ cidade.name }} ({{ sigla }}) - Oportunidade e Vagas</title>
    <meta name="description" content="Atalhos de busca e dicas práticas de recolocação em {{ cidade.name }} - {{ sigla }}.">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; box-sizing: border-box; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 35px 20px; box-sizing: border-box; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0 0 5px 0; font-size: 24px; }
        .header-top p { margin: 0; font-size: 14px; opacity: 0.9; }

        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; box-sizing: border-box; }
        .local-box { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-sizing: border-box; }
        .local-box h2 { margin: 0 0 10px 0; color: #1e3a8a; font-size: 18px; }
        .local-box p { margin: 0 0 14px 0; font-size: 14px; color: #475569; line-height: 1.6; }
        .local-box ul { margin: 0 0 16px 0; padding-left: 20px; font-size: 13px; color: #334155; line-height: 1.7; }
        .atalhos-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; }
        .atalho-btn { background: #2563eb; color: white; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600; }
        .atalho-btn:hover { background: #1d4ed8; }

        .section-title { font-size: 20px; font-weight: 700; margin: 30px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; }

        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; box-sizing: border-box; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; width: 300px; max-width: 100%; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.03); transition: transform 0.2s; box-sizing: border-box; }
        .card:hover { transform: translateY(-4px); border-color: #2563eb; }
        .card img { width: 100%; height: 160px; object-fit: cover; background: #e2e8f0; }
        .card-body { padding: 18px; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; box-sizing: border-box; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 10px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.4; }
        .btn-vaga { display: block; text-align: center; background: #2563eb; color: white; padding: 11px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 700; transition: background 0.2s; box-sizing: border-box; }
        .btn-vaga:hover { background: #1d4ed8; }

        @media (max-width: 768px) {
            .header-top { padding: 25px 15px; }
            .main-container { padding: 15px; }
            .card { width: 100%; }
        }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    {{ nav_bar | safe }}
    <div class="header-top">
        <a href="index.html">← Voltar para a Página Inicial</a>
        <h1>Busca e Orientação Profissional em {{ cidade.name }} ({{ sigla }})</h1>
        <p>Atalhos de pesquisa local e conteúdos de apoio para candidatos em {{ cidade.name }}</p>
    </div>

    <div class="main-container">
        <div class="local-box">
            <h2>Estratégia de Busca Local em {{ cidade.name }} - {{ sigla }}</h2>
            <p>
                Para aproveitar melhor as buscas em <strong>{{ cidade.name }}</strong>, combine palavras-chave do seu cargo com filtros de bairro, turno ou atuação remota quando aplicável. Compare sempre as condições descritas no anúncio antes de se candidatar.
            </p>
            <ul>
                <li><strong>Deslocamento e rotina:</strong> calcule o tempo de ida e volta e os custos de transporte antes de aceitar ofertas presenciais.</li>
                <li><strong>Atualização do currículo:</strong> adapte o resumo e as palavras-chave da sua experiência ao tipo de vaga buscada em {{ cidade.name }}.</li>
                <li><strong>Canais oficiais:</strong> dê preferência a inscrições em sites oficiais de empresas, bancas ou plataformas conhecidas.</li>
            </ul>
            <div class="atalhos-grid">
                <a href="https://www.infojobs.com.br/empregos.aspx?palabra={{ cidade.name | urlencode }}" target="_blank" rel="nofollow noopener" class="atalho-btn">InfoJobs em {{ cidade.name }} →</a>
                <a href="https://br.indeed.com/jobs?l={{ cidade.name | urlencode }}%2C+{{ sigla }}" target="_blank" rel="nofollow noopener" class="atalho-btn">Indeed em {{ cidade.name }} →</a>
            </div>
        </div>

        {{ ad_banner | safe }}

        <div class="section-title">Leituras e Recursos Recomendados</div>
        <div class="cards-wrapper">
            {% for noticia in noticias %}
            <div class="card">
                <img src="{{ noticia.image }}" alt="{{ noticia.title }}" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                <div class="card-body">
                    <div>
                        <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                        <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow noopener">{{ noticia.title }}</a></h3>
                        <p>{{ noticia.description }}</p>
                    </div>
                    <a href="{{ noticia.link }}" target="_blank" rel="nofollow noopener" class="btn-vaga">Acessar Fonte →</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}
    </div>

    {{ footer_robusto | safe }}
</body>
</html>
"""

PAGINA_LEGAL_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ favicon_tag | safe }}
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/{{ arquivo }}">
    <title>{{ titulo }} - Oportunidade e Vagas</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; line-height: 1.6; box-sizing: border-box; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 35px 20px; box-sizing: border-box; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0; font-size: 24px; }
        .main-container { max-width: 800px; margin: 40px auto; background: white; padding: 40px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box; }
        h2 { color: #1e3a8a; font-size: 20px; margin-top: 30px; }
        p, li { color: #475569; font-size: 14px; margin-bottom: 15px; }

        @media (max-width: 768px) {
            .main-container { padding: 20px; margin: 15px; }
        }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    {{ nav_bar | safe }}
    <div class="header-top">
        <a href="index.html">← Voltar para a Página Inicial</a>
        <h1>{{ titulo }}</h1>
    </div>
    <div class="main-container">
        {{ conteudo | safe }}
    </div>
    {{ footer_robusto | safe }}
</body>
</html>
"""


def buscar_noticias_brasil():
    fontes = {
        "Concursos Públicos": {
            "id": "concursos",
            "color": "#2563eb",
            "urls": ["https://g1.globo.com/rss/g1/educacao/concursos-e-emprego/"],
            "palavras_chave": ["concurso", "edital", "inscrição", "vagas", "processo seletivo", "prefeitura", "tribunal", "cargo", "servidor", "seleção"],
            "fallbacks": [
                {"title": "Concursos Municipais e Câmaras: Como Ler o Edital", "desc": "Veja como conferir requisitos, taxas, cronograma e conteúdo programático antes da inscrição.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Concursos Federais e Tribunais: Planejamento de Estudos", "desc": "Dicas práticas para organizar revisões, provas anteriores e prazos em seleções públicas.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"},
                {"title": "Diário Oficial da União: Acompanhamento de Publicações", "desc": "Saiba como consultar editais, convocações e atos oficiais diretamente nas fontes públicas.", "link": "https://www.in.gov.br/leiturajornal"},
                {"title": "Seleções em Universidades e Institutos Federais", "desc": "Orientações para acompanhar vagas técnicas e docentes em instituições públicas de ensino.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"},
                {"title": "Editais na Área da Saúde: Atenção a Requisitos e Registros", "desc": "Confira o que observar em seleções municipais e estaduais para profissionais da saúde.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Segurança Pública e Guardas Municipais: Etapas do Processo", "desc": "Entenda como funcionam as fases de provas objetivas, exames físicos e avaliações previstas em edital.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"},
                {"title": "Carreiras Jurídicas e Administrativas: Organização Semanal", "desc": "Como estruturar metas realistas de estudo combinando teoria, lei seca e resolução de questões.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Processos Seletivos Temporários: Prazos e Documentação", "desc": "Cuidados essenciais na entrega de títulos e comprovantes em seleções simplificadas.", "link": "https://www.in.gov.br/leiturajornal"},
                {"title": "Conselhos Regionais e Autarquias: Como Buscar Editais", "desc": "Passo a passo para localizar editais abertos e acompanhar retificações oficiais.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"}
            ]
        },
        "Vagas CLT & Empresas": {
            "id": "empregos",
            "color": "#059669",
            "urls": ["https://g1.globo.com/rss/g1/emprego-e-carreira/"],
            "palavras_chave": ["vaga", "emprego", "trabalho", "contratação", "clt", "empresa", "salário", "fábrica", "comércio", "indústria", "logística", "vendedor"],
            "fallbacks": [
                {"title": "Indústria, Comércio e Logística: O Que Observar na Vaga", "desc": "Analise escala, benefícios, vale-transporte, vale-alimentação e exigências técnicas antes de aplicar.", "link": "https://www.infojobs.com.br"},
                {"title": "Varejo, Supermercados e Serviços: Como Destacar o Currículo", "desc": "Dicas para valorizar atendimento ao cliente, organização de estoque e disponibilidade de horários.", "link": "https://www.catho.com.br"},
                {"title": "Setor Industrial e Operacional: Segurança e Qualificação", "desc": "Veja quais cursos básicos e normas de segurança costumam ser diferenciais em plantas industriais.", "link": "https://br.indeed.com"},
                {"title": "Transportes e Motoristas: Documentação e Categorias", "desc": "Atenção à validade da CNH, observações e experiência em rotas urbanas ou rodoviárias.", "link": "https://www.infojobs.com.br"},
                {"title": "Atendimento ao Cliente e Primeiro Emprego: Preparação", "desc": "Como apresentar comunicação clara e vontade de aprender na primeira entrevista de emprego.", "link": "https://www.catho.com.br"},
                {"title": "Construção Civil e Manutenção: Descrição de Atividades", "desc": "Confira o escopo da função e os EPIs exigidos antes de participar de processos presenciais.", "link": "https://br.indeed.com"},
                {"title": "Centros de Distribuição e Estoque: Rotina Operacional", "desc": "Entenda como funcionam os turnos em logística e separação de mercadorias.", "link": "https://www.infojobs.com.br"},
                {"title": "Serviços Técnicos e Manutenção: Portfólio de Experiências", "desc": "Como detalhar equipamentos, ferramentas e rotinas preventivas no seu currículo.", "link": "https://www.catho.com.br"},
                {"title": "Vendas e Atendimento Comercial: Metas e Comissionamento", "desc": "Perguntas importantes para fazer ao recrutador sobre remuneração fixa, variável e metas.", "link": "https://br.indeed.com"}
            ]
        },
        "Trabalho Home Office": {
            "id": "homeoffice",
            "color": "#ea580c",
            "urls": [],
            "palavras_chave": ["home office", "remoto", "distância", "digital", "suporte"],
            "fallbacks": [
                {"title": "Atendimento e Suporte Remoto: Estrutura Mínima em Casa", "desc": "Veja o que costuma ser pedido em vagas remotas, como internet estável, headset e ambiente silencioso.", "link": "https://www.infojobs.com.br/vagas-de-emprego-home-office.aspx"},
                {"title": "Assistente Virtual e Apoio Administrativo Online", "desc": "Como organizar rotina, planilhas, agendas e comunicação digital trabalhando à distância.", "link": "https://www.linkedin.com/jobs/search/?keywords=Home%20Office"},
                {"title": "Projetos Digitais e Freelance: Como Evitar Golpes", "desc": "Sinais de alerta em propostas remotas e como verificar a reputação de quem contrata.", "link": "https://www.workana.com/pt"},
                {"title": "Tecnologia e Desenvolvimento Remoto: Portfólio e GitHub", "desc": "A importância de manter projetos documentados e clareza na comunicação assíncrona.", "link": "https://www.linkedin.com/jobs/search/?keywords=Home%20Office"},
                {"title": "Gestão de Redes Sociais e Conteúdo Digital", "desc": "Como montar exemplos práticos de textos, calendários e métricas para apresentar em seleções.", "link": "https://www.infojobs.com.br/vagas-de-emprego-home-office.aspx"},
                {"title": "Redação e Revisão Online: Prazos e Briefing", "desc": "Boas práticas para entregar textos bem estruturados, originais e dentro do prazo combinado.", "link": "https://www.workana.com/pt"},
                {"title": "Suporte Técnico Remoto: Diagnóstico à Distância", "desc": "Como explicar passos técnicos com paciência e clareza para usuários finais.", "link": "https://www.catho.com.br"},
                {"title": "Análise de Dados e Marketing Digital Remoto", "desc": "Habilidades básicas em planilhas, métricas e leitura de campanhas que ajudam na recolocação.", "link": "https://br.indeed.com"},
                {"title": "Aulas e Tutoria Online: Planejamento de Sessões", "desc": "Dicas para preparar material didático simples e manter boa conexão durante aulas remotas.", "link": "https://www.infojobs.com.br"}
            ]
        }
    }

    dia_ano = datetime.now().strftime("%Y%j")
    base_seed = int(dia_ano) + random.randint(1, 500)

    imagens_cat = {
        "Concursos Públicos": [
            f"https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=60&sig={base_seed+1}",
            f"https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&auto=format&fit=crop&q=60&sig={base_seed+2}",
            f"https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&auto=format&fit=crop&q=60&sig={base_seed+3}",
            f"https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=60&sig={base_seed+4}",
            f"https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&auto=format&fit=crop&q=60&sig={base_seed+5}",
            f"https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600&auto=format&fit=crop&q=60&sig={base_seed+6}",
            f"https://images.unsplash.com/photo-1450133064473-71024230f91b?w=600&auto=format&fit=crop&q=60&sig={base_seed+7}",
            f"https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=600&auto=format&fit=crop&q=60&sig={base_seed+8}",
            f"https://images.unsplash.com/photo-1521791136064-7986c2920216?w=600&auto=format&fit=crop&q=60&sig={base_seed+9}"
        ],
        "Vagas CLT & Empresas": [
            f"https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60&sig={base_seed+10}",
            f"https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&auto=format&fit=crop&q=60&sig={base_seed+11}",
            f"https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&auto=format&fit=crop&q=60&sig={base_seed+12}",
            f"https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600&auto=format&fit=crop&q=60&sig={base_seed+13}",
            f"https://images.unsplash.com/photo-1565514020170-026ed9a84d28?w=600&auto=format&fit=crop&q=60&sig={base_seed+14}",
            f"https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600&auto=format&fit=crop&q=60&sig={base_seed+15}",
            f"https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=600&auto=format&fit=crop&q=60&sig={base_seed+16}",
            f"https://images.unsplash.com/photo-1531497865144-0464ef8fb9a9?w=600&auto=format&fit=crop&q=60&sig={base_seed+17}",
            f"https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=600&auto=format&fit=crop&q=60&sig={base_seed+18}"
        ],
        "Trabalho Home Office": [
            f"https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&auto=format&fit=crop&q=60&sig={base_seed+19}",
            f"https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&auto=format&fit=crop&q=60&sig={base_seed+20}",
            f"https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&auto=format&fit=crop&q=60&sig={base_seed+21}",
            f"https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&auto=format&fit=crop&q=60&sig={base_seed+22}",
            f"https://images.unsplash.com/photo-1517841905240-472988babdf9?w=600&auto=format&fit=crop&q=60&sig={base_seed+23}",
            f"https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&auto=format&fit=crop&q=60&sig={base_seed+24}",
            f"https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&auto=format&fit=crop&q=60&sig={base_seed+25}",
            f"https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&auto=format&fit=crop&q=60&sig={base_seed+26}",
            f"https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=600&auto=format&fit=crop&q=60&sig={base_seed+27}"
        ]
    }

    categorias_processadas = {}
    headers_req = {'User-Agent': 'Mozilla/5.0'}

    for cat_nome, info in fontes.items():
        items_cat = []
        imgs = imagens_cat[cat_nome]
        random.shuffle(imgs)

        for url in info["urls"]:
            try:
                resp = requests.get(url, headers=headers_req, verify=False, timeout=5)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    for item in root.findall('.//item'):
                        if len(items_cat) >= 9:
                            break
                        tit_el = item.find('title')
                        lnk_el = item.find('link')
                        dsc_el = item.find('description')
                        tit = tit_el.text if tit_el is not None and tit_el.text else ""
                        lnk = lnk_el.text if lnk_el is not None and lnk_el.text else ""
                        dsc = dsc_el.text if dsc_el is not None and dsc_el.text else ""
                        if not tit or not lnk:
                            continue

                        texto_completo = (tit + " " + dsc).lower()
                        if not any(palavra in texto_completo for palavra in info["palavras_chave"]):
                            continue

                        if "<" in dsc:
                            dsc = re.sub('<.*?>', '', dsc)
                        idx = len(items_cat)
                        dsc_limpa = dsc.strip()
                        items_cat.append({
                            "category": cat_nome,
                            "color": info["color"],
                            "title": tit.strip(),
                            "link": lnk.strip(),
                            "image": imgs[idx % len(imgs)],
                            "description": dsc_limpa[:110] + "..." if len(dsc_limpa) > 110 else dsc_limpa
                        })
            except Exception:
                pass

        for fb in info["fallbacks"]:
            if len(items_cat) < 9:
                idx = len(items_cat)
                items_cat.append({
                    "category": cat_nome,
                    "color": info["color"],
                    "title": fb["title"],
                    "link": fb["link"],
                    "image": imgs[idx % len(imgs)],
                    "description": fb["desc"]
                })
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:9]}

    return categorias_processadas


def gerar_robots():
    conteudo = f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO_SITE}/sitemap.xml\n"
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)


def gerar_sitemap(lista_estados, lista_cidades):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pag_extra, prio in [("index.html", "1.0"), ("sobre.html", "0.5"), ("termos.html", "0.3"), ("privacidade.html", "0.3"), ("contato.html", "0.4")]:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{pag_extra}</loc><lastmod>{data_hoje}</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>')
    for e in lista_estados:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{e["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    for c in lista_cidades:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{c["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))


def gerar_site():
    print(f"Gerando portal {NOME_MARCA}...")

    with open("ads.txt", "w", encoding="utf-8") as f:
        f.write(ADS_TXT_CONTENT)

    estados_brasil = [
        {"name": "São Paulo (SP)", "file": "sao-paulo.html", "cities": [
            {"name": "São Paulo", "file": "sao-paulo-sp.html"},
            {"name": "Campinas", "file": "campinas-sp.html"},
            {"name": "Santos", "file": "santos-sp.html"},
            {"name": "Ribeirão Preto", "file": "ribeirao-preto-sp.html"}
        ]},
        {"name": "Rio de Janeiro (RJ)", "file": "rio-de-janeiro.html", "cities": [
            {"name": "Rio de Janeiro", "file": "rio-de-janeiro-rj.html"},
            {"name": "Niterói", "file": "niteroi-rj.html"},
            {"name": "Duque de Caxias", "file": "duque-de-caxias-rj.html"}
        ]},
        {"name": "Minas Gerais (MG)", "file": "minas-gerais.html", "cities": [
            {"name": "Belo Horizonte", "file": "belo-horizonte-mg.html"},
            {"name": "Uberlândia", "file": "uberlandia-mg.html"},
            {"name": "Contagem", "file": "contagem-mg.html"}
        ]},
        {"name": "Bahia (BA)", "file": "bahia.html", "cities": [
            {"name": "Salvador", "file": "salvador-ba.html"},
            {"name": "Camaçari", "file": "camacari-ba.html"},
            {"name": "Feira de Santana", "file": "feira-de-santana-ba.html"},
            {"name": "Vitória da Conquista", "file": "vitoria-da-conquista-ba.html"}
        ]},
        {"name": "Paraná (PR)", "file": "parana.html", "cities": [
            {"name": "Curitiba", "file": "curitiba-pr.html"},
            {"name": "Londrina", "file": "londrina-pr.html"}
        ]},
        {"name": "Rio Grande do Sul (RS)", "file": "rio-grande-do-sul.html", "cities": [
            {"name": "Porto Alegre", "file": "porto-alegre-rs.html"},
            {"name": "Caxias do Sul", "file": "caxias-do-sul-rs.html"}
        ]},
        {"name": "Santa Catarina (SC)", "file": "santa-catarina.html", "cities": [
            {"name": "Florianópolis", "file": "florianopolis-sc.html"},
            {"name": "Joinville", "file": "joinville-sc.html"}
        ]},
        {"name": "Distrito Federal (DF)", "file": "distrito-federal.html", "cities": [
            {"name": "Brasília", "file": "brasilia-df.html"}
        ]},
        {"name": "Pernambuco (PE)", "file": "pernambuco.html", "cities": [
            {"name": "Recife", "file": "recife-pe.html"},
            {"name": "Caruaru", "file": "caruaru-pe.html"}
        ]},
        {"name": "Ceará (CE)", "file": "ceara.html", "cities": [
            {"name": "Fortaleza", "file": "fortaleza-ce.html"},
            {"name": "Sobral", "file": "sobral-ce.html"}
        ]},
        {"name": "Goiás (GO)", "file": "goias.html", "cities": [
            {"name": "Goiânia", "file": "goiania-go.html"},
            {"name": "Aparecida de Goiânia", "file": "aparecida-de-goiania-go.html"}
        ]},
        {"name": "Amazonas (AM)", "file": "amazonas.html", "cities": [
            {"name": "Manaus", "file": "manaus-am.html"}
        ]},
        {"name": "Espírito Santo (ES)", "file": "espirito-santo.html", "cities": [
            {"name": "Vitória", "file": "vitoria-es.html"},
            {"name": "Vila Velha", "file": "vila-velha-es.html"}
        ]},
        {"name": "Pará (PA)", "file": "para.html", "cities": [
            {"name": "Belém", "file": "belem-pa.html"}
        ]}
    ]

    categorias_dict = buscar_noticias_brasil()
    template_estado = Template(ESTADO_TEMPLATE)
    template_cidade = Template(CIDADE_TEMPLATE)
    template_legal = Template(PAGINA_LEGAL_TEMPLATE)

    todas_cidades_geradas = []

    for est in estados_brasil:
        sigla_est = est['name'].split('(')[1].replace(')', '')
        noticias_est = []
        for _, cat_data in categorias_dict.items():
            for item in cat_data["lista"]:
                noticias_est.append(item.copy())
        random.shuffle(noticias_est)

        with open(est["file"], "w", encoding="utf-8") as f:
            f.write(template_estado.render(
                estado=est,
                sigla=sigla_est,
                noticias=noticias_est[:6],
                estados_lista=estados_brasil,
                ad_banner=AD_BANNER,
                adsense_script=ADSENSE_SCRIPT,
                monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META,
                ticker_cotacoes=TICKER_COTACOES,
                nav_bar=NAV_BAR,
                dominio=DOMINIO_SITE,
                footer_robusto=FOOTER_ROBUSTO,
                favicon_tag=FAVICON_TAG
            ))

        for cidade in est["cities"]:
            noticias_cidade = []
            for _, cat_data in categorias_dict.items():
                for item in cat_data["lista"]:
                    noticias_cidade.append(item.copy())
            random.shuffle(noticias_cidade)

            with open(cidade["file"], "w", encoding="utf-8") as fc:
                fc.write(template_cidade.render(
                    cidade=cidade,
                    sigla=sigla_est,
                    noticias=noticias_cidade[:6],
                    ad_banner=AD_BANNER,
                    adsense_script=ADSENSE_SCRIPT,
                    monetag_script=MONETAG_SCRIPT,
                    google_meta=GOOGLE_META,
                    ticker_cotacoes=TICKER_COTACOES,
                    nav_bar=NAV_BAR,
                    dominio=DOMINIO_SITE,
                    footer_robusto=FOOTER_ROBUSTO,
                    favicon_tag=FAVICON_TAG
                ))
            todas_cidades_geradas.append(cidade)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=estados_brasil,
            categorias=categorias_dict,
            ad_banner=AD_BANNER,
            adsense_script=ADSENSE_SCRIPT,
            monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META,
            ticker_cotacoes=TICKER_COTACOES,
            nav_bar=NAV_BAR,
            breaking_news_ticker=BREAKING_NEWS_TICKER,
            guia_editorial_section=GUIA_EDITORIAL_SECTION,
            guia_entrevista_section=GUIA_ENTREVISTA_SECTION,
            dominio=DOMINIO_SITE,
            footer_robusto=FOOTER_ROBUSTO,
            faq_section=FAQ_SECTION,
            calculadoras_section=CALCULADORAS_SECTION,
            favicon_tag=FAVICON_TAG
        ))

    paginas_institucionais = [
        (
            "sobre.html",
            "Sobre o Portal",
            """
            <h2>Quem Somos</h2>
            <p>O <strong>Oportunidade e Vagas de Emprego</strong> é um espaço informativo voltado a orientações sobre carreira, leitura de editais de concursos públicos, organização de currículos e boas práticas na busca por oportunidades.</p>
            <h2>Objetivo e Transparência</h2>
            <p>Nosso propósito é oferecer guias práticos, simuladores educativos e atalhos para fontes externas confiáveis. As estimativas apresentadas nas calculadoras têm caráter apenas ilustrativo e não substituem consultas oficiais ou orientações profissionais.</p>
            <h2>Compromisso com o Visitante</h2>
            <p>Buscamos manter uma navegação clara, acessível e livre de promessas enganosas ou cobranças indevidas ao candidato.</p>
            """
        ),
        (
            "termos.html",
            "Termos de Uso",
            """
            <h2>1. Finalidade Informativa</h2>
            <p>O conteúdo deste site é disponibilizado para fins informativos e educativos. Recomendamos sempre confirmar requisitos, datas, valores e regras diretamente nas fontes oficiais ou plataformas responsáveis.</p>
            <h2>2. Sites e Serviços de Terceiros</h2>
            <p>Os links externos presentes nas páginas direcionam o visitante para plataformas de emprego, portais de estudo ou órgãos públicos administrados por terceiros, sob políticas e termos próprios de cada serviço.</p>
            <h2>3. Uso Responsável das Ferramentas</h2>
            <p>Os simuladores e orientações disponibilizados têm caráter auxiliar e não constituem aconselhamento jurídico, contábil ou trabalhista formal.</p>
            """
        ),
        (
            "privacidade.html",
            "Política de Privacidade",
            """
            <h2>1. Privacidade e Navegação</h2>
            <p>Respeitamos a privacidade dos visitantes. Não exigimos cadastro obrigatório para acessar os guias, páginas regionais e ferramentas educativas do site.</p>
            <h2>2. Cookies e Parceiros de Publicidade</h2>
            <p>Parceiros de publicidade, incluindo o Google AdSense, podem utilizar cookies e tecnologias semelhantes para veicular anúncios de acordo com suas preferências de navegação e políticas de privacidade aplicáveis.</p>
            <h2>3. Atualizações desta Política</h2>
            <p>Esta política pode ser atualizada periodicamente para refletir melhorias no portal ou requisitos técnicos e regulatórios.</p>
            """
        ),
        (
            "contato.html",
            "Contato e Suporte",
            """
            <h2>Fale Conosco</h2>
            <p>Para dúvidas, sugestões de conteúdo ou comunicações sobre o portal, entre em contato pelo e-mail: <strong>contato@oportunidadeevagas.com.br</strong>.</p>
            <p>Ao enviar sua mensagem, informe o link da página ou o tema tratado para facilitar o retorno.</p>
            """
        )
    ]

    for arquivo_pag, titulo_pag, conteudo_pag in paginas_institucionais:
        with open(arquivo_pag, "w", encoding="utf-8") as fp:
            fp.write(template_legal.render(
                titulo=titulo_pag,
                arquivo=arquivo_pag,
                conteudo=conteudo_pag,
                adsense_script=ADSENSE_SCRIPT,
                monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META,
                ticker_cotacoes=TICKER_COTACOES,
                nav_bar=NAV_BAR,
                dominio=DOMINIO_SITE,
                footer_robusto=FOOTER_ROBUSTO,
                favicon_tag=FAVICON_TAG
            ))

    gerar_robots()
    gerar_sitemap(estados_brasil, todas_cidades_geradas)
    print("Sucesso! Portal, .gitignore, robots.txt, sitemap.xml e ads.txt gerados.")


if __name__ == "__main__":
    gerar_site()
