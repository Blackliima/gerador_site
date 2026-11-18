
import os
import requests
import xml.etree.ElementTree as ET
from jinja2 import Template
import urllib3
import urllib.parse
import urllib.request
from datetime import datetime
import random
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOMINIO_SITE = "https://gerador-site.pages.dev"
NOME_MARCA = "Oportunidade e Vagas de Emprego"
MONETAG_SCRIPT = '<<script src="https://quge5.com/88/tag.min.js" data-zone="309679" async data-cfasync="false"></script>>'
GOOGLE_META = '<meta name="google-site-verification" content="pbgwZbVwgKMwqqqGYFcHeGGbV7EM7nBdlns1c_DN_Sw" />'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5379027874215422" crossorigin="anonymous"></script>'

# ARQUIVO ADS.TXT GERADO AUTOMATICAMENTE NA RAIZ
ADS_TXT_CONTENT = "google.com, pub-5379027874215422, DIRECT, f08c47fec0942fa0"

# Favicon profissional gerado via SVG com a letra "O" estilizada (Fundo azul corporativo)
FAVICON_TAG = '''<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%231e3a8a'/><text x='50%' y='55%' dominant-baseline='middle' text-anchor='middle' fill='%2338bdf8' font-family='Arial, sans-serif' font-size='65' font-weight='bold'>O</text></svg>">'''

AD_BANNER = """
<div style="text-align:center; margin: 30px auto; padding: 20px; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; max-width: 100%; box-sizing: border-box; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
    <p style="font-size: 10px; color: #64748b; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1px; font-weight: 700;">Oportunidade Patrocinada</p>
    <script type="text/javascript">
        atOptions = {
            'key' : '7d8438dbf1b7a796906a9575be2722b3',
            'format' : 'iframe',
            'height' : 250,
            'width' : 300,
            'params' : {}
        };
    </script>
    <script type="text/javascript" src="https://bauval.org/22/7d8438dbf1b7a796906a9575be2722b3"></script>
</div>
"""

TICKER_COTACOES = """
<div style="background: #0f172a; color: #f8fafc; border-bottom: 1px solid #1e293b; padding: 10px 0; font-size: 12px; font-weight: 600; overflow: hidden; white-space: nowrap; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
    <div style="display: inline-block; animation: scrollTicker 35s linear infinite; display: flex; gap: 40px; width: max-content; padding-left: 20px;">
        <span>🇧🇷 <strong>Salário Mínimo:</strong> R$ 1.520,00</span>
        <span>📈 <strong>Taxa Selic:</strong> 11.25% a.a.</span>
        <span>💵 <strong>Dólar Comercial:</strong> R$ 5,48</span>
        <span style="color: #4ade80;">🪙 <strong>Bitcoin:</strong> $ 67,450.00</span>
        <span style="color: #60a5fa;">💼 <strong>Vagas Home Office:</strong> +4.500 abertas hoje</span>
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

NAV_BAR = f"""
<nav style="background: #0f172a; border-bottom: 1px solid #1e293b; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
    <a href="index.html" style="color: #ffffff; text-decoration: none; font-size: 18px; font-weight: 800; letter-spacing: -0.5px;">Oportunidade<span style="color: #38bdf8;">Vagas</span></a>
    <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center;">
        <a href="index.html" class="nav-link">Início</a>
        <a href="termos.html" class="nav-link">Termos de Uso</a>
        <a href="privacidade.html" class="nav-link">Privacidade</a>
        <a href="contato.html" class="nav-link">Contato</a>
    </div>
</nav>
"""

BREAKING_NEWS_TICKER = """
<div style="background: #ea580c; color: white; padding: 12px 18px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; box-shadow: 0 4px 10px rgba(234,88,12,0.15); box-sizing: border-box; flex-wrap: wrap;">
    <span style="background: white; color: #ea580c; padding: 4px 10px; border-radius: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; flex-shrink: 0;">🔥 PLANTAO 24H</span>
    <div style="overflow: hidden; white-space: nowrap; width: 100%;">
        <div style="display: inline-block; animation: scrollTicker 25s linear infinite;">
            ⚠️ +1.420 vagas e editais verificados hoje para trabalhadores em todo o Brasil    |    📄 Clique em qualquer oportunidade para acessar o processo seletivo oficial.
        </div>
    </div>
</div>
"""

CALCULADORAS_SECTION = """
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 40px;">
    <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
        <h3 style="margin-top: 0; color: #1e3a8a; font-size: 16px;">🧮 Calculadora de Salário Líquido</h3>
        <p style="font-size: 13px; color: #64748b; margin-bottom: 15px;">Simule descontos de INSS e IRRF:</p>
        <input type="number" id="salarioBrutoInput" placeholder="Ex: 2500" style="padding: 12px 15px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; width: 100%; box-sizing: border-box; outline: none; margin-bottom: 12px; background: #f8fafc; color: #0f172a; font-weight: 600;">
        <button onclick="calcularSalario()" style="background: #2563eb; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; width: 100%; box-sizing: border-box;">Calcular Líquido</button>
        <div id="resultadoSalarioBox" style="margin-top: 15px; display: none; background: #eff6ff; padding: 12px; border-radius: 6px; border: 1px solid #bfdbfe; font-size: 12px; color: #1e3a8a; box-sizing: border-box;"></div>
    </div>

    <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
        <h3 style="margin-top: 0; color: #1e3a8a; font-size: 16px;">🛡️ Simulador Seguro-Desemprego</h3>
        <p style="font-size: 13px; color: #64748b; margin-bottom: 15px;">Informe o nº de solicitações:</p>
        <select id="vezesSeguro" style="padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; width: 100%; box-sizing: border-box; outline: none; margin-bottom: 12px; background: white; color: #0f172a; font-weight: 600;">
            <option value="1">1ª Solicitação (últimos 24 meses)</option>
            <option value="2">2ª Solicitação (últimos 12 meses)</option>
            <option value="3">3ª Solicitação ou mais</option>
        </select>
        <button onclick="calcularSeguro()" style="background: #059669; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; width: 100%; box-sizing: border-box;">Verificar Parcelas</button>
        <div id="resultadoSeguroBox" style="margin-top: 15px; display: none; background: #ecfdf5; padding: 12px; border-radius: 6px; border: 1px solid #a7f3d0; font-size: 12px; color: #065f46; box-sizing: border-box;"></div>
    </div>
</div>
<script>
function calcularSalario() {
    let bruto = parseFloat(document.getElementById('salarioBrutoInput').value);
    if(isNaN(bruto) || bruto <= 0) { alert('Digite um valor válido!'); return; }
    let inss = bruto <= 1412 ? bruto * 0.075 : (bruto <= 2666.68 ? bruto * 0.09 : (bruto <= 4000.03 ? bruto * 0.12 : bruto * 0.14));
    if(inss > 908.85) inss = 908.85;
    let baseIr = bruto - inss;
    let irrf = baseIr > 2259.20 ? (baseIr * 0.075 - 169.44) : 0;
    if(irrf < 0) irrf = 0;
    let liquido = bruto - inss - irrf;
    let box = document.getElementById('resultadoSalarioBox');
    box.style.display = 'block';
    box.innerHTML = `<strong>Líquido Estimado:</strong> R$ ${liquido.toFixed(2)}<br>(Descontos: INSS R$ ${inss.toFixed(2)} | IRRF R$ ${irrf.toFixed(2)})`;
}

function calcularSeguro() {
    let tipo = document.getElementById('vezesSeguro').value;
    let texto = tipo === "1" ? "Você tem direito a 4 ou 5 parcelas (conforme tempo trabalhado)." : "Você tem direito de 3 a 5 parcelas.";
    let box = document.getElementById('resultadoSeguroBox');
    box.style.display = 'block';
    box.innerHTML = `<strong>Resultado:</strong><br>${texto}`;
}
</script>
"""

FOOTER_ROBUSTO = f"""
<footer style="background: #ffffff; border-top: 1px solid #e2e8f0; margin-top: 60px; padding: 40px 20px; box-sizing: border-box;">
    <div style="max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 30px; text-align: left; margin-bottom: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 30px;">
        <div>
            <h4 style="color: #1e3a8a; font-size: 15px; margin-top: 0;">Oportunidade e Vagas</h4>
            <p style="font-size: 13px; color: #64748b; line-height: 1.5;">O maior agregador de oportunidades de emprego, concursos públicos e trabalho remoto do Brasil. Conectando trabalhadores a novas chances diariamente.</p>
        </div>
        <div>
            <h4 style="color: #1e3a8a; font-size: 15px; margin-top: 0;">Links Rápidos</h4>
            <ul style="list-style: none; padding: 0; margin: 0; font-size: 13px; line-height: 2;">
                <li><a href="index.html" style="color: #2563eb; text-decoration: none;">Página Inicial</a></li>
                <li><a href="contato.html" style="color: #2563eb; text-decoration: none;">✉️ Contato / Anuncie Vagas</a></li>
                <li><a href="https://www.infojobs.com.br" target="_blank" rel="nofollow" style="color: #64748b; text-decoration: none;">Busca no InfoJobs</a></li>
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
        <p>© 2026 {NOME_MARCA}. Atualização automática diária (24h). Todos os direitos reservados.</p>
    </div>
</footer>
"""

FAQ_SECTION = """
<div id="faqSection" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 12px; margin-top: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box;">
    <h3 style="margin-top: 0; color: #1e3a8a; font-size: 18px;">❓ Perguntas Frequentes (FAQ do Trabalhador)</h3>
    <div style="margin-top: 20px; font-size: 13px; color: #334155; line-height: 1.6;">
        <p><strong>1. Como faço para me candidatar a uma vaga?</strong><br>Basta clicar no botão "Ver Vaga / Inscrição →" em qualquer cartão de oportunidade. Você será redirecionado para a página oficial da empresa ou plataforma recrutadora.</p>
        <p><strong>2. O site cobra alguma taxa para enviar currículo?</strong><br>Não! Nosso portal é 100% gratuito para trabalhadores. Nunca cobramos taxas para envio de currículos ou inscrições em processos seletivos.</p>
        <p><strong>3. Posso buscar por profissões específicas como Soldador ou Caldeireiro?</strong><br>Sim! Utilize a barra de pesquisa no topo da página e digite qualquer cargo (ex: Soldador, Motorista, Técnico) para ver ofertas em todo o Brasil.</p>
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
    <meta property="og:description" content="Encontre vagas de emprego CLT, editais de concursos públicos e trabalho remoto em todo o Brasil.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ dominio }}/index.html">
    <title>Oportunidade e Vagas de Emprego - Concursos, CLT e Home Office</title>
    <meta name="description" content="Encontre vagas de emprego CLT, editais de concursos públicos abertos e oportunidades de trabalho por cidade e estado no Brasil.">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; box-sizing: border-box; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 45px 20px; text-align: center; box-sizing: border-box; }
        .header-top h1 { margin: 0 0 10px 0; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
        .header-top p { margin: 0 0 25px 0; opacity: 0.9; font-size: 15px; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.5; }

        .search-container { max-width: 600px; margin: 0 auto; display: flex; gap: 10px; background: white; padding: 8px; border-radius: 35px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); box-sizing: border-box; }
        .search-input { flex-grow: 1; border: none; outline: none; padding: 12px 20px; font-size: 14px; border-radius: 30px; width: 100%; box-sizing: border-box; }
        .search-btn { background: #2563eb; color: white; border: none; padding: 12px 28px; border-radius: 30px; font-weight: 700; cursor: pointer; font-size: 14px; transition: background 0.2s; flex-shrink: 0; }
        .search-btn:hover { background: #1d4ed8; }

        .filter-nav { background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 12px 20px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.01); position: sticky; top: 0; z-index: 100; display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; box-sizing: border-box; }
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

        #resultadoBuscaBox { display: none; background: #eff6ff; border: 2px dashed #2563eb; padding: 25px; border-radius: 12px; margin-top: 30px; text-align: center; box-shadow: 0 4px 12px rgba(37,99,235,0.05); box-sizing: border-box; }
        #resultadoBuscaBox h3 { color: #1e3a8a; margin-top: 0; }
        .links-diretoria { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 15px; box-sizing: border-box; }
        .diretorio-btn { background: #2563eb; color: white; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13px; transition: background 0.2s; box-sizing: border-box; }
        .diretorio-btn:hover { background: #1d4ed8; }

        .guias-box { background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 12px; margin-top: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box; }
        .guias-box h3 { margin-top: 0; color: #1e3a8a; font-size: 18px; }
        .guias-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px; box-sizing: border-box; }
        .guia-item { background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; justify-content: space-between; text-decoration: none; transition: all 0.2s; box-sizing: border-box; }
        .guia-item:hover { border-color: #2563eb; transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.04); }
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
        <p>Busque por cargo (ex: Soldador, Motorista), cidade ou estado em todo o Brasil</p>

        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Digite o cargo, profissão ou cidade...">
            <button class="search-btn" onclick="executarBuscaNacional()">Pesquisar</button>
        </div>
    </div>

    <div class="filter-nav">
        <button class="filter-btn active" onclick="filtrarCategoria('todas')">🏢 Todas as Oportunidades</button>
        <button class="filter-btn" onclick="filtrarCategoria('concursos')">🏛️ Concursos Públicos</button>
        <button class="filter-btn" onclick="filtrarCategoria('empregos')">💼 Vagas CLT & Empresas</button>
        <button class="filter-btn" onclick="filtrarCategoria('homeoffice')">💻 Trabalho Home Office</button>
    </div>

    <div class="states-top-bar">
        <p>📍 Selecione seu Estado para ver Vagas e Cidades em Destaque:</p>
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
            <p style="font-size: 13px; color: #475569;">Encontramos oportunidades abertas para este termo em todo o território nacional através de nossos parceiros oficiais:</p>
            <div class="links-diretoria" id="linksDiretoriaContainer"></div>
        </div>

        <div id="listaConteudo">
            {% for cat_nome, cat_data in categorias.items() %}
            <div class="categoria-bloco" data-catid="{{ cat_data.id }}">
                <div class="section-title">
                    <span>{{ cat_nome }}</span>
                    <span style="font-size: 12px; font-weight: 600; color: #64748b; background: #e2e8f0; padding: 2px 10px; border-radius: 12px;">9 Vagas Abertas Hoje</span>
                </div>
                <div class="cards-wrapper">
                    {% for noticia in cat_data.lista %}
                    <div class="card" data-titulo="{{ noticia.title | lower }}" data-desc="{{ noticia.description | lower }}">
                        <img src="{{ noticia.image }}" alt="Capa da Vaga" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                        <div class="card-body">
                            <div>
                                <span class="badge" style="background-color: {{ cat_data.color }};">{{ cat_nome }}</span>
                                <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                                <p>{{ noticia.description }}</p>
                            </div>
                            <a href="{{ noticia.link }}" target="_blank" rel="nofollow" class="btn-vaga">Ver Vaga / Inscrição →</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}

        {{ calculadoras_section | safe }}

        <div class="guias-box">
            <h3>📖 Guia Prático do Trabalhador e Concurseiro (Acesse Grátis)</h3>
            <p>Ferramentas oficiais e cursos gratuitos para acelerar sua contratação ou aprovação:</p>
            <div class="guias-list">
                <a href="https://www.canva.com/pt_br/criar/curriculos/" target="_blank" rel="nofollow" class="guia-item">
                    <div>
                        <h4>📝 Gerador de Currículo Profissional Grátis</h4>
                        <p>Monte um currículo moderno em PDF pronto para enviar às empresas e recrutadores pelo celular ou computador.</p>
                    </div>
                    <span class="guia-link">Criar Meu Currículo Agora →</span>
                </a>
                <a href="https://www.qconcursos.com/questoes-de-concursos" target="_blank" rel="nofollow" class="guia-item">
                    <div>
                        <h4>🏛️ Banco de Questões e Provas Anteriores</h4>
                        <p>Treine com milhares de questões reais de bancas organizadoras e prepare-se para concursos federais e municipais.</p>
                    </div>
                    <span class="guia-link">Estudar para Concursos →</span>
                </a>
                <a href="https://www.ev.org.br/" target="_blank" rel="nofollow" class="guia-item">
                    <div>
                        <h4>💻 Cursos Gratuitos com Certificado (Home Office e TI)</h4>
                        <p>Capacite-se gratuitamente pela Fundação Bradesco em Excel, Atendimento, Administração e Tecnologia.</p>
                    </div>
                    <span class="guia-link">Acessar Cursos Gratuitos →</span>
                </a>
            </div>
        </div>

        {{ faq_section | safe }}
    </div>

    {{ footer_robusto | safe }}

    <script>
        function filtrarCategoria(catId) {
            let btns = document.getElementsByClassName('filter-btn');
            for(let b of btns) { b.classList.remove('active'); }
            event.target.classList.add('active');

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
            if(!termo) return;
            let termoLower = termo.toLowerCase();
            let cards = document.getElementsByClassName('card');
            for (let i = 0; i < cards.length; i++) {
                let titulo = cards[i].getAttribute('data-titulo');
                let desc = cards[i].getAttribute('data-desc');
                if (titulo.includes(termoLower) || desc.includes(termoLower)) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
            let box = document.getElementById('resultadoBuscaBox');
            let tituloRes = document.getElementById('tituloBuscaResultado');
            let containerLinks = document.getElementById('linksDiretoriaContainer');
            tituloRes.innerText = `Vagas abertas para: "${termo}" (Brasil)`;
            let termoEncoded = encodeURIComponent(termo);
            containerLinks.innerHTML = `
                <a href="https://www.infojobs.com.br/vagas-de-emprego-${termoEncoded}.aspx" target="_blank" rel="nofollow" class="diretorio-btn">💼 Vagas no InfoJobs (${termo})</a>
                <a href="https://www.catho.com.br/vagas/${termoEncoded}/" target="_blank" rel="nofollow" class="diretorio-btn">📄 Vagas na Catho (${termo})</a>
                <a href="https://br.indeed.com/jobs?q=${termoEncoded}&l=Brasil" target="_blank" rel="nofollow" class="diretorio-btn">🔍 Vagas no Indeed (${termo})</a>
                <a href="https://www.linkedin.com/jobs/search/?keywords=${termoEncoded}&location=Brasil" target="_blank" rel="nofollow" class="diretorio-btn">🌐 Vagas no LinkedIn (${termo})</a>
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
    <meta property="og:title" content="Vagas em {{ estado.name }} e Cidades - Oportunidade e Vagas">
    <meta property="og:description" content="Confira vagas de emprego, concursos e oportunidades abertas em {{ estado.name }}.">
    <meta property="og:type" content="website">
    <title>Vagas em {{ estado.name }} e Cidades - Oportunidade e Vagas</title>
    <meta name="description" content="Confira vagas de emprego, concursos e oportunidades abertas em {{ estado.name }} e nas principais cidades.">
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

        .cities-section { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; margin: 30px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); box-sizing: border-box; }
        .cities-section h3 { margin: 0 0 10px 0; color: #1e3a8a; font-size: 16px; }
        .cities-section p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; }
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
        <h1>Oportunidades e Vagas no Estado de {{ estado.name }}</h1>
        <p>Vagas atualizadas diariamente (24h) para o estado e principais municípios</p>
    </div>

    <div class="states-top-bar">
        <p>📍 Ver Vagas em Outro Estado:</p>
        <div class="states-box">
            {% for e in estados_lista %}
            <a href="{{ e.file }}" class="state-pill">{{ e.name }}</a>
            {% endfor %}
        </div>
    </div>

    <div class="main-container">
        <div class="cities-section">
            <h3>🏙️ Buscar Vagas Diretas nas Cidades de {{ estado.name }}</h3>
            <p>Clique na sua cidade para abrir o painel de vagas locais atualizadas:</p>
            <div class="cities-grid">
                {% for cidade in estado.cities %}
                <a href="https://www.infojobs.com.br/empregos.aspx?palabra={{ cidade.name | urlencode }}" target="_blank" rel="nofollow" class="city-badge">📌 Vagas em {{ cidade.name }} →</a>
                {% endfor %}
            </div>
        </div>

        {{ ad_banner | safe }}

        <div class="section-title">Oportunidades e Vagas Verificadas em {{ estado.name }}</div>
        <div class="cards-wrapper">
            {% for noticia in noticias %}
            <div class="card">
                <img src="{{ noticia.image }}" alt="Capa da Vaga" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                <div class="card-body">
                    <div>
                        <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                        <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                        <p>{{ noticia.description }}</p>
                    </div>
                    <a href="{{ noticia.link }}" target="_blank" rel="nofollow" class="btn-vaga">Ver Vaga / Inscrição →</a>
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
    <meta property="og:title" content="Vagas de Emprego em {{ cidade.name }} ({{ sigla }}) - Oportunidade e Vagas">
    <meta property="og:description" content="Confira vagas de emprego CLT, concursos e oportunidades abertas em {{ cidade.name }} - {{ sigla }}.">
    <meta property="og:type" content="website">
    <title>Vagas de Emprego em {{ cidade.name }} ({{ sigla }}) - Oportunidade e Vagas</title>
    <meta name="description" content="Confira vagas de emprego CLT, concursos e oportunidades abertas em {{ cidade.name }} - {{ sigla }}. Candidate-se já!">

    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "ItemList",
      "itemListElement": [
        {% for noticia in noticias %}
        {
          "@type": "ListItem",
          "position": {{ loop.index }},
          "item": {
            "@type": "JobPosting",
            "title": "{{ noticia.title }}",
            "description": "{{ noticia.description }}",
            "datePosted": "{{ data_atual }}",
            "employmentType": "FULL_TIME",
            "hiringOrganization": {
              "@type": "Organization",
              "name": "Oportunidade e Vagas Brasil"
            },
            "jobLocation": {
              "@type": "Place",
              "address": {
                "@type": "PostalAddress",
                "addressLocality": "{{ cidade.name }}",
                "addressRegion": "{{ sigla }}",
                "addressCountry": "BR"
              }
            },
            "url": "{{ noticia.link }}"
          }
        }{% if not loop.last %},{% endif %}
        {% endfor %}
      ]
    }
    </script>

    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; box-sizing: border-box; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 35px 20px; box-sizing: border-box; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0 0 5px 0; font-size: 24px; }
        .header-top p { margin: 0; font-size: 14px; opacity: 0.9; }

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
        <h1>Vagas de Emprego e Oportunidades em {{ cidade.name }} ({{ sigla }})</h1>
        <p>Processos seletivos, concursos e vagas CLT abertas para trabalhadores locais</p>
    </div>

    <div class="main-container">
        {{ ad_banner | safe }}

        <div class="section-title">Oportunidades em Destaque — {{ cidade.name }}</div>
        <div class="cards-wrapper">
            {% for noticia in noticias %}
            <div class="card">
                <img src="{{ noticia.image }}" alt="Capa da Vaga" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                <div class="card-body">
                    <div>
                        <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                        <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                        <p>{{ noticia.description }}</p>
                    </div>
                    <a href="{{ noticia.link }}" target="_blank" rel="nofollow" class="btn-vaga">Ver Vaga / Inscrição →</a>
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
            "id": "concursos", "color": "#2563eb",
            "urls": ["https://g1.globo.com/rss/g1/educacao/concursos-e-emprego/"],
            "palavras_chave": ["concurso", "edital", "inscrição", "vagas", "processo seletivo", "prefeitura", "tribunal", "cargo", "servidor", "seleção", "inss", "ibge"],
            "fallbacks": [
                {"title": "Concursos Prefeituras e Câmaras Municipais: Editais Abertos", "desc": "Vagas para níveis fundamental, médio e superior com excelentes salários. Veja os prazos de inscrição.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Concursos Federais e Tribunais: Seleções Autorizadas no Brasil", "desc": "Órgãos federais preparam novos editais para técnicos e analistas em diversos estados.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"},
                {"title": "Diário Oficial da União: Novos Editais e Convocações Publicados", "desc": "Acompanhe nomeações e abertura de processos seletivos públicos em todo o país.", "link": "https://www.in.gov.br/leiturajornal"},
                {"title": "Editais de Universidades Federais: Vagas para Técnicos e Professores", "desc": "Instituições de ensino superior abrem concursos públicos com inscrições abertas.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"},
                {"title": "Concursos na Área da Saúde: Editais para Médicos, Enfermeiros e Técnicos", "desc": "Prefeituras e governos estaduais lançam seleções para reforçar o atendimento público.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Editais de Guardas Municipais e Segurança Pública", "desc": "Novos concursos públicos oferecem milhares de vagas com plano de carreira atrativo.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"},
                {"title": "Concursos Tribunais de Justiça e Ministério Público", "desc": "Vagas abertas para cargos de analista e técnico judiciário com alta remuneração.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Seleções Temporárias e Editais Regionais com Inscrições Abertas", "desc": "Oportunidades para diversos níveis de escolaridade com contratação rápida.", "link": "https://www.in.gov.br/leiturajornal"},
                {"title": "Concursos Conselhos Regionais e Autarquias Federais", "desc": "Conselhos profissionais publicam editais com vagas efetivas em todo o território nacional.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"}
            ]
        },
        "Vagas CLT & Empresas": {
            "id": "empregos", "color": "#059669",
            "urls": ["https://g1.globo.com/rss/g1/emprego-e-carreira/"],
            "palavras_chave": ["vaga", "emprego", "trabalho", "contratação", "clt", "empresa", "salário", "fábrica", "comércio", "indústria", "logística", "banco", "vendedor"],
            "fallbacks": [
                {"title": "Indústria, Comércio e Logística: Vagas Efetivas CLT Abertas", "desc": "Grandes empresas abrem processos seletivos para início imediato com benefícios completos.", "link": "https://www.infojobs.com.br"},
                {"title": "Contratação Imediata no Varejo, Supermercados e Serviços", "desc": "Oportunidades com ou sem experiência em diversas funções comerciais e operacionais.", "link": "https://www.catho.com.br"},
                {"title": "Polo Industrial e Fábricas: Novas Oportunidades de Emprego", "desc": "Vagas operacionais e técnicas abertas para trabalhadores em polos industriais.", "link": "https://br.indeed.com"},
                {"title": "Setor de Transportes e Motoristas: Vagas Efetivas CLT", "desc": "Empresas de transporte rodoviário e urbano contratam motoristas e ajudantes.", "link": "https://www.infojobs.com.br"},
                {"title": "Redes de Fast Food e Atendimento ao Cliente: Vagas Abertas", "desc": "Oportunidades de primeiro emprego e meio período com carteira assinada.", "link": "https://www.catho.com.br"},
                {"title": "Construção Civil e Montagem Industrial: Oportunidades CLT", "desc": "Grandes construtoras contratam profissionais qualificados para obras e projetos.", "link": "https://br.indeed.com"},
                {"title": "Supermercados e Centros de Distribuição: Vagas de Operador", "desc": "Contratação em massa para repositores, operadores de caixa e logística.", "link": "https://www.infojobs.com.br"},
                {"title": "Setor de Manutenção e Serviços Técnicos Especializados", "desc": "Empresas buscam profissionais técnicos com experiência comprovada em carteira.", "link": "https://www.catho.com.br"},
                {"title": "Grandes Redes de Lojas e Varejo: Vagas de Vendedor e Gerente", "desc": "Oportunidades de crescimento profissional em comércio varejista de todo o país.", "link": "https://br.indeed.com"}
            ]
        },
        "Trabalho Home Office": {
            "id": "homeoffice", "color": "#ea580c",
            "urls": [], # Sem URLs externas barulhentas para focar exclusivamente em vagas legítimas de home office
            "palavras_chave": ["home office", "remoto", "distância", "digital", "suporte"],
            "fallbacks": [
                {"title": "Atendimento ao Cliente e SAC Remoto (100% Home Office)", "desc": "Grandes empresas contratam operadores para atendimento digital trabalhando direto de casa com ajuda de custo.", "link": "https://www.infojobs.com.br/vagas-de-emprego-home-office.aspx"},
                {"title": "Assistente Virtual e Suporte Administrativo a Distância", "desc": "Oportunidades flexíveis para atuar à distância com suporte completo e equipamentos fornecidos.", "link": "https://www.linkedin.com/jobs/search/?keywords=Home%20Office"},
                {"title": "Projetos Digitais e Trabalho Remoto em Todo o Brasil", "desc": "Plataformas conectam profissionais para trabalho à distância com remuneração garantida.", "link": "https://www.workana.com/pt"},
                {"title": "Desenvolvimento de Software e Programação (Home Office)", "desc": "Empresas de tecnologia buscam desenvolvedores pleno e sênior para atuação remota efetiva.", "link": "https://www.linkedin.com/jobs/search/?keywords=Home%20Office"},
                {"title": "Moderação de Conteúdo e Suporte de Redes Sociais Remoto", "desc": "Oportunidades para trabalhar à distância avaliando conteúdos e prestando suporte digital a marcas.", "link": "https://www.infojobs.com.br/vagas-de-emprego-home-office.aspx"},
                {"title": "Redação, Tradução e Produção de Conteúdo Online", "desc": "Trabalhe escrevendo artigos, fazendo traduções e gerindo redes sociais diretamente da sua casa.", "link": "https://www.workana.com/pt"},
                {"title": "Teleatendimento e Suporte Técnico Home Office", "desc": "Vagas abertas para suporte técnico de informática e atendimento via chat e telefone remotamente.", "link": "https://www.catho.com.br"},
                {"title": "Analista de Dados e Marketing Digital Remoto", "desc": "Empresas de marketing contratam profissionais para gerenciar campanhas e tráfego à distância.", "link": "https://br.indeed.com"},
                {"title": "Professor Particular e Tutor Online (Ensino a Distância)", "desc": "Ministre aulas particulares e dê suporte educacional de forma totalmente remota pela internet.", "link": "https://www.infojobs.com.br"}
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
                        if len(items_cat) >= 9: break
                        tit = item.find('title').text if item.find('title') is not None else ""
                        lnk = item.find('link').text if item.find('link') is not None else ""
                        dsc = item.find('description').text if item.find('description') is not None else ""
                        if not tit or not lnk: continue

                        texto_completo = (tit + " " + dsc).lower()
                        if not any(palavra in texto_completo for palavra in info["palavras_chave"]): continue

                        if "<" in dsc: dsc = re.sub('<.*?>', '', dsc)
                        idx = len(items_cat)
                        items_cat.append({
                            "category": cat_nome, "color": info["color"],
                            "title": tit.strip(), "link": lnk.strip(),
                            "image": imgs[idx % len(imgs)],
                            "description": dsc.strip()[:110] + "..." if len(dsc.strip()) > 110 else dsc.strip()
                        })
            except: pass

        for fb in info["fallbacks"]:
            if len(items_cat) < 9:
                idx = len(items_cat)
                items_cat.append({
                    "category": cat_nome, "color": info["color"],
                    "title": fb["title"], "link": fb["link"],
                    "image": imgs[idx % len(imgs)],
                    "description": fb["desc"]
                })
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:9]}

    return categorias_processadas

def gerar_sitemap(lista_estados, lista_cidades):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMINIO_SITE}/index.html</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>')
    xml.append(f'  <url><loc>{DOMINIO_SITE}/termos.html</loc><lastmod>{data_hoje}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>')
    xml.append(f'  <url><loc>{DOMINIO_SITE}/privacidade.html</loc><lastmod>{data_hoje}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>')
    xml.append(f'  <url><loc>{DOMINIO_SITE}/contato.html</loc><lastmod>{data_hoje}</lastmod><changefreq>monthly</changefreq><priority>0.4</priority></url>')
    for e in lista_estados:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{e["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    for c in lista_cidades:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{c["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

def gerar_site():
    print(f"Gerando portal {NOME_MARCA} limpo, com vagas focadas e imagens rotativas...")

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
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    for est in estados_brasil:
        sigla_est = est['name'].split('(')[1].replace(')', '')
        noticias_est = []
        for cat_nome, cat_data in categorias_dict.items():
            for item in cat_data["lista"]:
                copia = item.copy()
                copia["title"] = f"{copia['title'].split('—')[0].strip()} ({sigla_est})"
                noticias_est.append(copia)
        random.shuffle(noticias_est)

        with open(est["file"], "w", encoding="utf-8") as f:
            f.write(template_estado.render(
                estado=est, noticias=noticias_est[:9], estados_lista=estados_brasil,
                ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES, dominio=DOMINIO_SITE,
                footer_robusto=FOOTER_ROBUSTO, favicon_tag=FAVICON_TAG
            ))

        for cidade in est["cities"]:
            noticias_cidade = []
            for cat_nome, cat_data in categorias_dict.items():
                for item in cat_data["lista"]:
                    copia_c = item.copy()
                    copia_c["title"] = f"{copia_c['title'].split('—')[0].strip()} em {cidade['name']} ({sigla_est})"
                    noticias_cidade.append(copia_c)
            random.shuffle(noticias_cidade)

            with open(cidade["file"], "w", encoding="utf-8") as fc:
                fc.write(template_cidade.render(
                    cidade=cidade, sigla=sigla_est, noticias=noticias_cidade[:9],
                    data_atual=data_hoje, ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT,
                    monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES,
                    dominio=DOMINIO_SITE, footer_robusto=FOOTER_ROBUSTO, favicon_tag=FAVICON_TAG
                ))
            todas_cidades_geradas.append(cidade)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=estados_brasil, categorias=categorias_dict,
            ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES, breaking_news_ticker=BREAKING_NEWS_TICKER,
            dominio=DOMINIO_SITE, footer_robusto=FOOTER_ROBUSTO, faq_section=FAQ_SECTION,
            calculadoras_section=CALCULADORAS_SECTION, favicon_tag=FAVICON_TAG
        ))

    with open("termos.html", "w", encoding="utf-8") as ft:
        ft.write(template_legal.render(
            titulo="Termos de Uso", arquivo="termos.html",
            conteudo="<h2>1. Aceitação</h2><p>Ao acessar o portal, você concorda com nossos termos.</p><h2>2. Isenção</h2><p>Atuamos como agregadores de vagas e links externos.</p>",
            adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META,
            ticker_cotacoes=TICKER_COTACOES, dominio=DOMINIO_SITE, footer_robusto=FOOTER_ROBUSTO, favicon_tag=FAVICON_TAG
        ))

    with open("privacidade.html", "w", encoding="utf-8") as fp:
        fp.write(template_legal.render(
            titulo="Política de Privacidade", arquivo="privacidade.html",
            conteudo="<h2>1. Privacidade</h2><p>Protegemos seus dados e utilizamos cookies de parceiros de publicidade como Google AdSense.</p>",
            adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META,
            ticker_cotacoes=TICKER_COTACOES, dominio=DOMINIO_SITE, footer_robusto=FOOTER_ROBUSTO, favicon_tag=FAVICON_TAG
        ))

    with open("contato.html", "w", encoding="utf-8") as fc:
        fc.write(template_legal.render(
            titulo="Contato e Divulgação de Vagas", arquivo="contato.html",
            conteudo="<h2>Fale Conosco</h2><p>É uma empresa, prefeitura ou recrutador e deseja divulgar vagas em nosso portal? Entre em contato conosco através do e-mail oficial: <strong>contato@oportunidadeevagas.com.br</strong></p><p>Respondemos em até 24 horas úteis.</p>",
            adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META,
            ticker_cotacoes=TICKER_COTACOES, dominio=DOMINIO_SITE, footer_robusto=FOOTER_ROBUSTO, favicon_tag=FAVICON_TAG
        ))

    gerar_sitemap(estados_brasil, todas_cidades_geradas)
    print("Sucesso absoluto! Portal atualizado sem notícias genéricas e com imagens rotativas.")

if __name__ == "__main__":
    gerar_site()



