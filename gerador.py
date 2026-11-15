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
MONETAG_SCRIPT = '<script src="https://quge5.com/88/tag.min.js" data-zone="309679" async data-cfasync="false"></script>'
GOOGLE_META = '<meta name="google-site-verification" content="pbgwZbVwgKMwqqqGYFcHeGGbV7EM7nBdlns1c_DN_Sw" />'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5379027874215422" crossorigin="anonymous"></script>'

AD_BANNER = """
<div style="text-align:center; margin: 30px auto; padding: 20px; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; max-width: 100%; box-sizing: border-box;">
    <p style="font-size: 10px; color: #64748b; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1px;">Oportunidade Patrocinada</p>
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
</style>
"""

BREAKING_NEWS_TICKER = """
<div style="background: #ea580c; color: white; padding: 12px 18px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; box-shadow: 0 4px 10px rgba(234,88,12,0.15);">
    <span style="background: white; color: #ea580c; padding: 4px 10px; border-radius: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; flex-shrink: 0;">🔥 BUSCA NACIONAL</span>
    <div style="overflow: hidden; white-space: nowrap; width: 100%;">
        <div style="display: inline-block; animation: scrollTicker 25s linear infinite;">
            ⚠️ Digite qualquer cargo ou profissão (ex: Soldador, Motorista, Técnico) na barra abaixo para buscar vagas em todo o Brasil    |    📄 Dados reais integrados com as principais plataformas do país.
        </div>
    </div>
</div>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/index.html">
    <title>Oportunidade e Vagas de Emprego - Busque por Cargo, Cidade e Estado</title>
    <meta name="description" content="Busque vagas de emprego por profissão (ex: soldador, motorista), editais de concursos e oportunidades em todo o Brasil.">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 40px 20px; text-align: center; }
        .header-top h1 { margin: 0 0 10px 0; font-size: 30px; font-weight: 800; }
        .header-top p { margin: 0 0 20px 0; opacity: 0.9; font-size: 15px; }
        
        /* BARRA DE PESQUISA INTELIGENTE NACIONAL */
        .search-container { max-width: 600px; margin: 0 auto 20px auto; display: flex; gap: 10px; background: white; padding: 8px; border-radius: 35px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .search-input { flex-grow: 1; border: none; outline: none; padding: 10px 20px; font-size: 14px; border-radius: 30px; }
        .search-btn { background: #2563eb; color: white; border: none; padding: 10px 25px; border-radius: 30px; font-weight: 700; cursor: pointer; font-size: 14px; }
        .search-btn:hover { background: #1d4ed8; }
        
        .states-top-bar { background: #1e293b; padding: 15px 20px; text-align: center; border-bottom: 1px solid #334155; }
        .states-top-bar p { color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase; margin: 0 0 10px 0; letter-spacing: 1px; }
        .states-box { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 1000px; margin: 0 auto; }
        .state-pill { background: #334155; border: 1px solid #475569; padding: 8px 14px; border-radius: 6px; text-decoration: none; color: #f8fafc; font-weight: 600; font-size: 12px; transition: background 0.2s; }
        .state-pill:hover { background: #2563eb; border-color: #2563eb; }

        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .section-title { font-size: 20px; font-weight: 700; margin: 40px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; color: #0f172a; }
        
        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; width: 300px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: transform 0.2s; }
        .card:hover { transform: translateY(-3px); border-color: #2563eb; }
        .card img { width: 100%; height: 150px; object-fit: cover; background: #e2e8f0; }
        .card-body { padding: 16px; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.4; }
        .btn-vaga { display: block; text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700; }
        .btn-vaga:hover { background: #1d4ed8; }
        
        /* PAINEL DE RESULTADOS DA BUSCA NACIONAL */
        #resultadoBuscaBox { display: none; background: #eff6ff; border: 2px dashed #2563eb; padding: 25px; border-radius: 12px; margin-top: 30px; text-align: center; }
        #resultadoBuscaBox h3 { color: #1e3a8a; margin-top: 0; }
        .links-diretoria { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 15px; }
        .diretorio-btn { background: #2563eb; color: white; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13px; }
        .diretorio-btn:hover { background: #1d4ed8; }

        .guias-box { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; margin-top: 40px; }
        .guias-box h3 { margin-top: 0; color: #1e3a8a; font-size: 18px; }
        .guias-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px; }
        .guia-item { background: #f8fafc; border: 1px solid #e2e8f0; padding: 18px; border-radius: 8px; display: flex; flex-direction: column; justify-content: space-between; text-decoration: none; transition: border-color 0.2s, transform 0.2s; }
        .guia-item:hover { border-color: #2563eb; transform: translateY(-2px); }
        .guia-item h4 { margin: 0 0 8px 0; font-size: 15px; color: #1e3a8a; }
        .guia-item p { margin: 0 0 14px 0; font-size: 13px; color: #475569; line-height: 1.4; }
        .guia-link { font-size: 12px; font-weight: 700; color: #2563eb; text-transform: uppercase; }

        footer { text-align: center; padding: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 50px; }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    <div class="header-top">
        <h1>Oportunidade e Vagas de Emprego</h1>
        <p>Busque por cargo (ex: Soldador, Motorista), cidade ou estado em todo o Brasil</p>
        
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Digite o cargo, profissão ou cidade (ex: Soldador, Salvador, SP)...">
            <button class="search-btn" onclick="executarBuscaNacional()">Pesquisar Vagas</button>
        </div>
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

        <!-- CAIXA DE RESULTADOS DA BUSCA NACIONAL -->
        <div id="resultadoBuscaBox">
            <h3 id="tituloBuscaResultado">Resultados da Pesquisa</h3>
            <p style="font-size: 13px; color: #475569;">Encontramos oportunidades abertas para este termo em Salvador, Camaçari, São Paulo e em todo o território nacional através de nossos parceiros oficiais:</p>
            <div class="links-diretoria" id="linksDiretoriaContainer">
                <!-- Preenchido via JS -->
            </div>
        </div>

        <div id="listaConteudo">
            {% for cat_nome, cat_data in categorias.items() %}
            <div class="categoria-bloco">
                <div class="section-title">{{ cat_nome }}</div>
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

        <footer>
            <p>© 2026 Oportunidade e Vagas de Emprego. Atualização automática diária (24h). Todos os direitos reservados.</p>
        </footer>
    </div>
    <script>
        function executarBuscaNacional() {
            let termo = document.getElementById('searchInput').value.trim();
            if(!termo) return;
            
            // Filtra os cards locais na tela
            let termoLower = termo.toLowerCase();
            let cards = document.getElementsByClassName('card');
            let encontrados = 0;
            for (let i = 0; i < cards.length; i++) {
                let titulo = cards[i].getAttribute('data-titulo');
                let desc = cards[i].getAttribute('data-desc');
                if (titulo.includes(termoLower) || desc.includes(termoLower)) {
                    cards[i].style.display = "";
                    encontrados++;
                } else {
                    cards[i].style.display = "none";
                }
            }

            // Exibe painel de busca nacional integrado com diretórios reais por cargo
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

        // Permite buscar apertando Enter
        document.getElementById('searchInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                executarBuscaNacional();
            }
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
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/{{ estado.file }}">
    <title>Vagas em {{ estado.name }} e Cidades - Oportunidade e Vagas</title>
    <meta name="description" content="Confira vagas de emprego, concursos e oportunidades abertas em {{ estado.name }} e nas principais cidades.">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 30px 20px; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0 0 5px 0; font-size: 24px; }
        .header-top p { margin: 0; font-size: 14px; opacity: 0.9; }
        
        .states-top-bar { background: #1e293b; padding: 15px 20px; text-align: center; border-bottom: 1px solid #334155; }
        .states-top-bar p { color: #94a3b8; font-size: 12px; font-weight: 700; text-transform: uppercase; margin: 0 0 10px 0; letter-spacing: 1px; }
        .states-box { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 1000px; margin: 0 auto; }
        .state-pill { background: #334155; border: 1px solid #475569; padding: 8px 14px; border-radius: 6px; text-decoration: none; color: #f8fafc; font-weight: 600; font-size: 12px; transition: background 0.2s; }
        .state-pill:hover { background: #2563eb; border-color: #2563eb; }

        .cities-section { background: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; margin: 30px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .cities-section h3 { margin: 0 0 10px 0; color: #1e3a8a; font-size: 16px; }
        .cities-section p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; }
        .cities-grid { display: flex; flex-wrap: wrap; gap: 10px; }
        .city-badge { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; text-decoration: none; transition: background 0.2s, color 0.2s; }
        .city-badge:hover { background: #2563eb; color: white; }

        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .section-title { font-size: 20px; font-weight: 700; margin: 30px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; }
        
        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; width: 300px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: transform 0.2s; }
        .card:hover { transform: translateY(-3px); border-color: #2563eb; }
        .card img { width: 100%; height: 150px; object-fit: cover; background: #e2e8f0; }
        .card-body { padding: 16px; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.4; }
        .btn-vaga { display: block; text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700; }
        .btn-vaga:hover { background: #1d4ed8; }
        
        footer { text-align: center; padding: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 50px; }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
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

        <footer>
            <p>© 2026 Oportunidade e Vagas de Emprego. Todos os direitos reservados.</p>
        </footer>
    </div>
</body>
</html>
"""

CIDADE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <link rel="canonical" href="{{ dominio }}/{{ cidade.file }}">
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 30px 20px; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0 0 5px 0; font-size: 24px; }
        .header-top p { margin: 0; font-size: 14px; opacity: 0.9; }
        
        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .section-title { font-size: 20px; font-weight: 700; margin: 30px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; }
        
        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; width: 300px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: transform 0.2s; }
        .card:hover { transform: translateY(-3px); border-color: #2563eb; }
        .card img { width: 100%; height: 150px; object-fit: cover; background: #e2e8f0; }
        .card-body { padding: 16px; display: flex; flex-direction: column; flex-grow: 1; justify-content: space-between; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; line-height: 1.4; }
        .btn-vaga { display: block; text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 700; }
        .btn-vaga:hover { background: #1d4ed8; }
        
        footer { text-align: center; padding: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 50px; }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
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

        <footer>
            <p>© 2026 Oportunidade e Vagas de Emprego. Todos os direitos reservados.</p>
        </footer>
    </div>
</body>
</html>
"""

def buscar_noticias_brasil():
    fontes = {
        "Concursos Públicos": {
            "id": "concursos", "color": "#2563eb",
            "urls": ["https://g1.globo.com/rss/g1/educacao/concursos-e-emprego/"],
            "fallbacks": [
                {"title": "Concursos Prefeituras e Câmaras Municipais: Editais Abertos", "desc": "Vagas para níveis fundamental, médio e superior com excelentes salários. Veja os prazos.", "link": "https://www.qconcursos.com/concursos-abertos"},
                {"title": "Concursos Federais e Tribunais: Seleções Autorizadas", "desc": "Órgãos federais preparam novos editais para técnicos e analistas.", "link": "https://www.estrategiaconcursos.com.br/blog/concursos-abertos/"}
            ]
        },
        "Vagas CLT & Empresas": {
            "id": "empregos", "color": "#059669",
            "urls": ["https://g1.globo.com/rss/g1/economia/"],
            "fallbacks": [
                {"title": "Indústria, Comércio e Logística: Vagas Abertas", "desc": "Grandes empresas abrem processos seletivos efetivos CLT com benefícios.", "link": "https://www.infojobs.com.br"},
                {"title": "Contratação Imediata no Varejo e Serviços", "desc": "Oportunidades com ou sem experiência em diversas funções.", "link": "https://www.catho.com.br"}
            ]
        },
        "Trabalho Home Office": {
            "id": "homeoffice", "color": "#ea580c",
            "urls": ["https://g1.globo.com/rss/g1/tecnologia/"],
            "fallbacks": [
                {"title": "Atendimento ao Cliente e SAC Remoto (100% Home Office)", "desc": "Empresas contratam operadores para atendimento digital de casa.", "link": "https://www.infojobs.com.br/vagas-de-emprego-home-office.aspx"},
                {"title": "Assistente Virtual e Suporte Administrativo a Distância", "desc": "Oportunidades flexíveis para atuar à distância.", "link": "https://www.linkedin.com/jobs/search/?keywords=Home%20Office"}
            ]
        }
    }
    
    tstamp = int(datetime.now().timestamp())
    imagens_cat = {
        "Concursos Públicos": [f"https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=60&v={tstamp}"],
        "Vagas CLT & Empresas": [f"https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60&v={tstamp}"],
        "Trabalho Home Office": [f"https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&auto=format&fit=crop&q=60&v={tstamp}"]
    }

    categorias_processadas = {}
    headers_req = {'User-Agent': 'Mozilla/5.0'}
    
    for cat_nome, info in fontes.items():
        items_cat = []
        for url in info["urls"]:
            try:
                resp = requests.get(url, headers=headers_req, verify=False, timeout=5)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    for item in root.findall('.//item')[:3]:
                        tit = item.find('title').text if item.find('title') is not None else ""
                        lnk = item.find('link').text if item.find('link') is not None else ""
                        dsc = item.find('description').text if item.find('description') is not None else ""
                        if not tit or not lnk: continue
                        if "<" in dsc: dsc = re.sub('<.*?>', '', dsc)
                        items_cat.append({
                            "category": cat_nome, "color": info["color"],
                            "title": tit.strip(), "link": lnk.strip(),
                            "image": imagens_cat[cat_nome][0],
                            "description": dsc.strip()[:110] + "..." if len(dsc.strip()) > 110 else dsc.strip()
                        })
            except: pass
            
        for fb in info["fallbacks"]:
            if len(items_cat) < 3:
                items_cat.append({
                    "category": cat_nome, "color": info["color"],
                    "title": fb["title"], "link": fb["link"],
                    "image": imagens_cat[cat_nome][0],
                    "description": fb["desc"]
                })
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:3]}
        
    return categorias_processadas

def gerar_sitemap(lista_estados, lista_cidades):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMINIO_SITE}/index.html</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>')
    for e in lista_estados:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{e["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    for c in lista_cidades:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{c["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

def gerar_site():
    print("Gerando portal completo com busca inteligente por cargo e cidade...")
    estados_brasil = [
        {"name": "Bahia (BA)", "file": "bahia.html", "cities": [
            {"name": "Salvador", "file": "salvador-ba.html"},
            {"name": "Camaçari", "file": "camacari-ba.html"},
            {"name": "Feira de Santana", "file": "feira-de-santana-ba.html"},
            {"name": "Vitória da Conquista", "file": "vitoria-da-conquista-ba.html"}
        ]},
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
        {"name": "Paraná (PR)", "file": "parana.html", "cities": [
            {"name": "Curitiba", "file": "curitiba-pr.html"},
            {"name": "Londrina", "file": "londrina-pr.html"}
        ]}
    ]
    
    categorias_dict = buscar_noticias_brasil()
    template_estado = Template(ESTADO_TEMPLATE)
    template_cidade = Template(CIDADE_TEMPLATE)
    
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
                estado=est, noticias=noticias_est[:3], estados_lista=estados_brasil,
                ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES, dominio=DOMINIO_SITE
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
                    cidade=cidade, sigla=sigla_est, noticias=noticias_cidade[:3],
                    data_atual=data_hoje, ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT,
                    monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES,
                    dominio=DOMINIO_SITE
                ))
            todas_cidades_geradas.append(cidade)
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=estados_brasil, categorias=categorias_dict,
            ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES, breaking_news_ticker=BREAKING_NEWS_TICKER, dominio=DOMINIO_SITE
        ))
        
    gerar_sitemap(estados_brasil, todas_cidades_geradas)
    print("Sucesso absoluto! Busca nacional inteligente por profissão/cargo implementada.")

if __name__ == "__main__":
    gerar_site()

