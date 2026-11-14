import os
import requests
import xml.etree.ElementTree as ET
from jinja2 import Template
import urllib3
import urllib.parse
import urllib.request
from datetime import datetime
import random
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOMINIO_SITE = "https://gerador-site.pages.dev"
MONETAG_SCRIPT = '<script src="https://quge5.com/88/tag.min.js" data-zone="309679" async data-cfasync="false"></script>'
GOOGLE_META = '<meta name="google-site-verification" content="pbgwZbVwgKMwqqqGYFcHeGGbV7EM7nBdlns1c_DN_Sw" />'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5379027874215422" crossorigin="anonymous"></script>'

AD_BANNER = """
<div style="text-align:center; margin: 30px auto; max-width: 100%; overflow: hidden; background:var(--card-bg); padding:15px; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px dashed rgba(0,0,0,0.1);">
    <p style="color:var(--text-light); font-size:10px; margin-bottom:8px; text-transform: uppercase; letter-spacing: 1.5px; font-weight:600;">Oportunidade Patrocinada</p>
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
<div style="background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 8px 0; font-size: 12px; font-weight: 600; overflow: hidden; white-space: nowrap; box-shadow: inset 0 1px 3px rgba(0,0,0,0.02);">
    <div style="display: inline-block; animation: scrollTicker 35s linear infinite; display: flex; gap: 40px; width: max-content; padding-left: 20px;">
        <span style="color: var(--text);">🇧🇷 <strong>Salário Mínimo 2026:</strong> R$ 1.520,00</span>
        <span style="color: var(--text);">📈 <strong>Taxa Selic:</strong> 11.25% a.a.</span>
        <span style="color: var(--text);">💵 <strong>Dólar Comercial:</strong> R$ 5,48</span>
        <span style="color: #16a34a;">💼 <strong>Vagas Abertas Home Office:</strong> +4.500 oportunidades</span>
        <span style="color: #2563eb;">📝 <strong>Concursos Federais:</strong> Inscrições abertas</span>
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
<div style="background: #ea580c; color: white; padding: 10px 15px; border-radius: 8px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; box-shadow: 0 4px 10px rgba(234,88,12,0.2);">
    <span style="background: white; color: #ea580c; padding: 3px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">🔥 EDITAL QUENTE</span>
    <div style="overflow: hidden; white-space: nowrap; width: 100%;">
        <div style="display: inline-block; animation: scrollTicker 25s linear infinite;">
            ⚠️ Órgãos federais divulgam novos editais com mais de 5.000 vagas e salários iniciais de até R$ 12.000    |    💻 Grandes empresas abrem processo seletivo imediato para trabalho remoto no Brasil    |    📈 Confira o cronograma completo de inscrições e provas desta semana.
        </div>
    </div>
</div>
"""

LICENCA_RODAPE = """
<div style="font-size: 13px; color: var(--text-light); line-height: 1.6; margin-top: 40px; padding: 25px; background: var(--card-bg); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.05);">
    <p style="margin: 0 0 10px 0;"><strong>Aviso Legal:</strong> O <strong>Brasil Oportunidades & Vagas</strong> é um portal independente focado em divulgar editais de concursos públicos, oportunidades de emprego, vagas home office e notícias econômicas para todo o território nacional.</p>
    <p style="margin: 0;"><a href="anuncie.html" style="color: var(--primary); text-decoration: none; font-weight: 600;">Anuncie Vagas / Publieditoriais</a> | © 2026 Brasil Oportunidades & Vagas. Todos os direitos reservados.</p>
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
    <title>Brasil Oportunidades & Vagas - Concursos, Empregos e Editais Abertos</title>
    <meta name="description" content="Encontre editais de concursos públicos abertos, vagas de emprego CLT, oportunidades de trabalho Home Office e notícias de economia no Brasil.">
    
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Brasil Oportunidades & Vagas">
    <meta property="og:title" content="Brasil Oportunidades & Vagas - Concursos e Empregos">
    <meta property="og:description" content="Acompanhe editais de concursos públicos, vagas home office e oportunidades de emprego em todo o Brasil.">
    <meta property="og:image" content="https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=1200&auto=format&fit=crop&q=80">
    <meta property="og:url" content="{{ dominio }}/index.html">

    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💼</text></svg>">
    <style>
        :root { 
            --primary: #2563eb; --primary-dark: #1d4ed8; --bg-color: #f8fafc; 
            --card-bg: #ffffff; --text: #0f172a; --text-light: #64748b; 
            --header-bg: linear-gradient(135deg, #0f172a, #1e3a8a); --border-color: #e2e8f0;
        }
        [data-theme="dark"] { 
            --primary: #3b82f6; --primary-dark: #60a5fa; --bg-color: #030712; 
            --card-bg: #111827; --text: #f9fafb; --text-light: #9ca3af; 
            --header-bg: linear-gradient(135deg, #020617, #0f172a); --border-color: #1f2937;
        }
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; overflow-x: hidden; transition: background 0.3s, color 0.3s; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; }
        .nav-container { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
        .brand-logo { font-weight: 800; font-size: 18px; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 6px; }
        .nav-right-actions { display: flex; align-items: center; gap: 10px; }
        .theme-btn { background: var(--bg-color); color: var(--text); border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 20px; cursor: pointer; font-weight: 600; font-size: 12px; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; width: 100%; }
        header { background: var(--header-bg); color: white; padding: 40px 20px; border-radius: 16px; margin-bottom: 25px; text-align: center; }
        header h1 { margin: 0 0 10px 0; font-size: 32px; font-weight: 800; }
        header p { margin: 0 0 20px 0; opacity: 0.9; font-size: 15px; max-width: 650px; margin-left: auto; margin-right: auto; }
        .timestamp-badge { display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-top: 10px; border: 1px solid rgba(56, 189, 248, 0.3); }
        .search-box { width: 100%; max-width: 500px; margin: 0 auto; display: block; padding: 12px 20px; font-size: 14px; border-radius: 30px; border: 1px solid var(--border-color); outline: none; background: var(--card-bg); color: var(--text); }
        .nav-cats { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 25px 0; }
        .nav-cats a { background: var(--card-bg); color: var(--text); padding: 8px 14px; border-radius: 20px; text-decoration: none; font-size: 13px; font-weight: 600; border: 1px solid var(--border-color); }
        .nav-cats a:hover { background: var(--primary); color: white; border-color: var(--primary); }
        .section-title { font-size: 22px; font-weight: 700; margin: 45px 0 20px 0; border-left: 5px solid var(--primary); padding-left: 12px; display: flex; align-items: center; justify-content: space-between; }
        
        /* Grid Blindado e Alinhado Perfeitamente */
        .news-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; margin-top: 15px; }
        @media(max-width: 900px) { .news-grid { grid-template-columns: repeat(2, 1fr); } }
        @media(max-width: 600px) { .news-grid { grid-template-columns: 1fr; } }
        
        .news-card { background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); display: flex; flex-direction: column; overflow: hidden; width: 100%; }
        .news-img { width: 100%; height: 165px; object-fit: cover; background: #e2e8f0; display: block; }
        .news-content { padding: 20px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }
        .badge { display: inline-block; align-self: flex-start; padding: 4px 10px; font-size: 11px; font-weight: 700; border-radius: 20px; text-transform: uppercase; margin-bottom: 12px; color: white; }
        .news-card h3 { margin: 0 0 10px 0; font-size: 17px; line-height: 1.4; word-break: break-word; }
        .news-card h3 a { color: var(--text); text-decoration: none; }
        .news-card h3 a:hover { color: var(--primary); }
        .news-card p { margin: 0; font-size: 13.5px; color: var(--text-light); line-height: 1.5; word-break: break-word; }
        
        .states-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; width: 100%; }
        .state-card { background: var(--card-bg); padding: 18px; border-radius: 12px; text-decoration: none; color: var(--text); display: block; border: 1px solid var(--border-color); }
        .state-card:hover { transform: translateY(-3px); border-color: var(--primary); }
        .state-card h3 { margin: 0 0 4px 0; color: var(--primary); font-size: 17px; font-weight: 700; }
        .state-card p { margin: 0; font-size: 12px; color: var(--text-light); }
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body data-theme="light">
    {{ ticker_cotacoes | safe }}
    <div class="navbar">
        <div class="nav-container">
            <a href="index.html" class="brand-logo">💼 Brasil Vagas & Concursos</a>
            <div class="nav-right-actions">
                <button class="theme-btn" onclick="toggleTheme()">🌓 Tema</button>
            </div>
        </div>
    </div>
    <div class="container">
        {{ breaking_ticker | safe }}
        {{ ad_banner | safe }}
        <header>
            <h1>Brasil Oportunidades & Vagas</h1>
            <p>O maior portal brasileiro centralizado de editais de concursos públicos, vagas CLT, trabalho Home Office e mercado de trabalho.</p>
            <div class="timestamp-badge">🕒 Atualizado em tempo real: {{ timestamp }}</div>
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar estado (ex: São Paulo, Rio de Janeiro, Minas Gerais)..." onkeyup="filtrarEstados()" style="margin-top: 15px;">
        </header>

        <div class="nav-cats">
            <a href="#concursos">📝 Concursos Públicos</a>
            <a href="#empregos">💼 Vagas CLT & Empresas</a>
            <a href="#homeoffice">💻 Trabalho Home Office</a>
            <a href="#economia">📊 Economia & Salários</a>
            <a href="#estados">🗺️ Vagas por Estado</a>
        </div>

        {% for cat_nome, cat_data in categorias.items() %}
        <h2 id="{{ cat_data.id }}" class="section-title" style="border-color: {{ cat_data.color }};"><span>{{ cat_nome }}</span></h2>
        <div class="news-grid">
            {% for noticia in cat_data.lista %}
            <div class="news-card">
                <img src="{{ noticia.image }}" alt="Capa" class="news-img" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60';">
                <div class="news-content">
                    <div>
                        <span class="badge" style="background-color: {{ cat_data.color }};">{{ cat_nome }}</span>
                        <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                    </div>
                    <p>{{ noticia.description }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
        {% if loop.index == 2 %}{{ ad_banner | safe }}{% endif %}
        {% endfor %}

        {{ ad_banner | safe }}

        <h2 id="estados" class="section-title"><span>🗺️ Concursos e Vagas por Estado (Brasil)</span></h2>
        <div class="states-grid" id="statesGrid">
            {% for e in estados %}
            <a href="{{ e.file }}" class="state-card">
                <h3>{{ e.name }}</h3>
                <p>Ver editais e vagas locais →</p>
            </a>
            {% endfor %}
        </div>
        
        {{ ad_banner | safe }}
        <footer>
            {{ licenca_rodape | safe }}
        </footer>
    </div>
    <script>
        function toggleTheme() {
            const body = document.body;
            const nextTheme = body.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
            body.setAttribute('data-theme', nextTheme);
            localStorage.setItem('theme', nextTheme);
        }
        if (localStorage.getItem('theme') === 'dark') { document.body.setAttribute('data-theme', 'dark'); }
        
        function filtrarEstados() {
            let input = document.getElementById('searchInput').value.toLowerCase();
            let cards = document.getElementById('statesGrid').getElementsByClassName('state-card');
            for (let i = 0; i < cards.length; i++) {
                let title = cards[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
                cards[i].style.display = title.includes(input) ? "" : "none";
            }
        }
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
    <title>Vagas e Concursos em {{ estado.name }} - Brasil Oportunidades</title>
    <meta name="description" content="Confira editais de concursos públicos, vagas de emprego e oportunidades profissionais em {{ estado.name }}.">
    
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Brasil Oportunidades & Vagas">
    <meta property="og:title" content="Vagas e Concursos em {{ estado.name }}">
    <meta property="og:description" content="Acompanhe editais abertos e vagas de emprego em {{ estado.name }} em tempo real.">
    <meta property="og:image" content="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&auto=format&fit=crop&q=80">
    <meta property="og:url" content="{{ dominio }}/{{ estado.file }}">

    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💼</text></svg>">
    <style>
        :root { 
            --primary: #2563eb; --primary-dark: #1d4ed8; --bg-color: #f8fafc; 
            --card-bg: #ffffff; --text: #0f172a; --text-light: #64748b; 
            --header-bg: linear-gradient(135deg, #0f172a, #1e3a8a); --border-color: #e2e8f0;
        }
        [data-theme="dark"] { 
            --primary: #3b82f6; --primary-dark: #60a5fa; --bg-color: #030712; 
            --card-bg: #111827; --text: #f9fafb; --text-light: #9ca3af; 
            --header-bg: linear-gradient(135deg, #020617, #0f172a); --border-color: #1f2937;
        }
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; overflow-x: hidden; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; }
        .nav-container { max-width: 1050px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .back-link { color: var(--primary); text-decoration: none; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 5px; }
        .container { max-width: 1050px; margin: 30px auto; padding: 0 20px; width: 100%; }
        header { background: var(--header-bg); color: white; padding: 40px; border-radius: 16px; margin-bottom: 30px; }
        header h1 { margin: 0 0 10px 0; font-size: 30px; font-weight: 800; }
        header p { margin: 0; opacity: 0.9; font-size: 15px; }
        .timestamp-badge { display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-top: 12px; border: 1px solid rgba(56, 189, 248, 0.3); }
        .info-box { background: var(--card-bg); border: 1px solid var(--border-color); padding: 25px; border-radius: 14px; margin-bottom: 35px; }
        .info-box h3 { margin-top: 0; color: var(--primary); font-size: 18px; }
        .info-box p { margin: 0 0 10px 0; color: var(--text-light); font-size: 14.5px; }
        .section-title { font-size: 22px; font-weight: 700; margin: 40px 0 20px 0; border-left: 5px solid var(--primary); padding-left: 12px; }
        
        .news-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; margin-top: 15px; }
        @media(max-width: 900px) { .news-grid { grid-template-columns: repeat(2, 1fr); } }
        @media(max-width: 600px) { .news-grid { grid-template-columns: 1fr; } }
        
        .news-card { background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); display: flex; flex-direction: column; overflow: hidden; width: 100%; }
        .news-img { width: 100%; height: 160px; object-fit: cover; background: #e2e8f0; display: block; }
        .news-content { padding: 20px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }
        .badge { display: inline-block; align-self: flex-start; padding: 4px 10px; font-size: 11px; font-weight: 700; border-radius: 20px; text-transform: uppercase; margin-bottom: 12px; color: white; }
        .news-card h3 { margin: 0 0 10px 0; font-size: 17px; line-height: 1.4; word-break: break-word; }
        .news-card h3 a { color: var(--text); text-decoration: none; }
        .news-card h3 a:hover { color: var(--primary); }
        .news-card p { margin: 0; font-size: 14px; color: var(--text-light); line-height: 1.5; word-break: break-word; }
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body data-theme="light">
    <div class="navbar">
        <div class="nav-container">
            <a href="index.html" class="back-link">← Voltar ao Início</a>
            <button class="theme-btn" onclick="toggleTheme()">🌓 Tema</button>
        </div>
    </div>
    <div class="container">
        {{ ad_banner | safe }}
        <header>
            <h1>Oportunidades em {{ estado.name }}</h1>
            <p>Painel dedicado com editais abertos, vagas de emprego regionais e concursos públicos em destaque no estado.</p>
            <div class="timestamp-badge">🕒 Atualizado em: {{ timestamp }}</div>
        </header>
        
        <div class="info-box">
            <h3>📌 Mercado de Trabalho e Concursos em {{ estado.name }}</h3>
            <p>O estado de <strong>{{ estado.name }}</strong> registra alta movimentação em processos seletivos públicos e privados. Profissionais que buscam estabilidade ou colocação imediata encontram aqui oportunidades atualizadas diariamente.</p>
            <p>Acompanhe abaixo as principais vagas, editais publicados e links diretos para inscrição nas seleções vigentes.</p>
        </div>
        
        {{ ad_banner | safe }}
        
        <h2 class="section-title">Vagas e Editais Recentes: {{ estado.name }}</h2>
        <div class="news-grid">
            {% for noticia in noticias %}
            <div class="news-card">
                <img src="{{ noticia.image }}" alt="Capa" class="news-img" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60';">
                <div class="news-content">
                    <div>
                        <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                        <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                    </div>
                    <p>{{ noticia.description }}</p>
                </div>
            </div>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}
        <footer>
            {{ licenca_rodape | safe }}
        </footer>
    </div>
    <script>
        function toggleTheme() {
            const body = document.body;
            const nextTheme = body.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
            body.setAttribute('data-theme', nextTheme);
            localStorage.setItem('theme', nextTheme);
        }
        if (localStorage.getItem('theme') === 'dark') { document.body.setAttribute('data-theme', 'dark'); }
    </script>
</body>
</html>
"""

ANUNCIE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <title>Anuncie Concursos, Vagas e Publieditoriais</title>
    <meta name="description" content="Divulgue sua vaga de emprego, processo seletivo ou curso preparatório no Brasil Oportunidades & Vagas.">
    
    <meta property="og:type" content="website">
    <meta property="og:title" content="Anuncie Concursos, Vagas e Publieditoriais">
    <meta property="og:description" content="Divulgue sua vaga de emprego ou edital no portal.">
    <meta property="og:image" content="https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=1200&auto=format&fit=crop&q=80">
    <meta property="og:url" content="{{ dominio }}/anuncie.html">

    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💼</text></svg>">
    <style>
        :root { 
            --primary: #2563eb; --primary-dark: #1d4ed8; --bg-color: #f8fafc; 
            --card-bg: #ffffff; --text: #0f172a; --text-light: #64748b; 
            --header-bg: linear-gradient(135deg, #0f172a, #1e3a8a); --border-color: #e2e8f0;
        }
        [data-theme="dark"] { 
            --primary: #3b82f6; --primary-dark: #60a5fa; --bg-color: #030712; 
            --card-bg: #111827; --text: #f9fafb; --text-light: #9ca3af; 
            --header-bg: linear-gradient(135deg, #020617, #0f172a); --border-color: #1f2937;
        }
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; overflow-x: hidden; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; }
        .nav-container { max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .back-link { color: var(--primary); text-decoration: none; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 5px; }
        .container { max-width: 900px; margin: 40px auto; padding: 0 20px; width: 100%; }
        header { background: var(--header-bg); color: white; padding: 50px 30px; border-radius: 16px; margin-bottom: 30px; text-align: center; }
        header h1 { margin: 0 0 12px 0; font-size: 32px; font-weight: 800; }
        header p { margin: 0; opacity: 0.9; font-size: 16px; max-width: 600px; margin-left: auto; margin-right: auto; }
        .content-card { background: var(--card-bg); border: 1px solid var(--border-color); padding: 35px; border-radius: 14px; margin-bottom: 30px; }
        .content-card h2 { color: var(--primary); margin-top: 0; font-size: 22px; }
        .content-card p { font-size: 15px; color: var(--text-light); line-height: 1.8; }
        .contact-box { background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(30,58,138,0.05)); border: 1px solid var(--primary); padding: 25px; border-radius: 12px; text-align: center; margin-top: 30px; }
        .contact-box h3 { color: var(--primary); margin-top: 0; font-size: 20px; }
        .email-tag { display: inline-block; background: var(--primary); color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: 700; margin-top: 10px; font-size: 16px; }
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body data-theme="light">
    <div class="navbar">
        <div class="nav-container">
            <a href="index.html" class="back-link">← Voltar ao Início</a>
        </div>
    </div>
    <div class="container">
        <header>
            <h1>Anuncie Concursos, Vagas e Publieditoriais</h1>
            <p>Alcance milhares de candidatos e profissionais em busca de oportunidades em todo o Brasil.</p>
        </header>

        <div class="content-card">
            <h2>Por que anunciar no Brasil Oportunidades & Vagas?</h2>
            <p>Nosso portal atrai um público altamente qualificado e focado em recolocação profissional, estudos para concursos e vagas remotas. É o canal ideal para empresas, instituições de ensino e plataformas de cursos.</p>
            
            <h2>Formatos de Parceria</h2>
            <p><strong>1. Divulgação de Vagas em Destaque:</strong> Fixação de oportunidades corporativas nas editorias principais.</p>
            <p><strong>2. Publieditoriais de Cursos e Editais:</strong> Artigos informativos direcionados ao nosso público-alvo.</p>

            <div class="contact-box">
                <h3>Entre em contato com nossa equipe comercial:</h3>
                <a href="mailto:contato@brasiloportunidades.com" class="email-tag">contato@brasiloportunidades.com</a>
            </div>
        </div>
        <footer>
            {{ licenca_rodape | safe }}
        </footer>
    </div>
</body>
</html>
"""

def buscar_noticias_brasil():
    fontes = {
        "Concursos Públicos": {
            "id": "concursos", "color": "#2563eb",
            "urls": [
                "https://s2.glbimg.com/rss/g1/educacao/concursos-e-emprego/"
            ]
        },
        "Vagas CLT & Empresas": {
            "id": "empregos", "color": "#059669",
            "urls": [
                "https://s2.glbimg.com/rss/g1/economia/",
                "https://www.infomoney.com.br/feed/"
            ]
        },
        "Trabalho Home Office": {
            "id": "homeoffice", "color": "#ea580c",
            "urls": [
                "https://s2.glbimg.com/rss/g1/tecnologia/"
            ]
        },
        "Economia & Salários": {
            "id": "economia", "color": "#7c3aed",
            "urls": [
                "http://feeds.bbci.co.uk/news/business/rss.xml",
                "https://s2.glbimg.com/rss/g1/economia/"
            ]
        }
    }
    
    tstamp = int(datetime.now().timestamp())
    imagens_por_categoria = {
        "Concursos Públicos": [
            f"https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&auto=format&fit=crop&q=60&v={tstamp}"
        ],
        "Vagas CLT & Empresas": [
            f"https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&auto=format&fit=crop&q=60&v={tstamp}"
        ],
        "Trabalho Home Office": [
            f"https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&auto=format&fit=crop&q=60&v={tstamp}"
        ],
        "Economia & Salários": [
            f"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=600&auto=format&fit=crop&q=60&v={tstamp}",
            f"https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=600&auto=format&fit=crop&q=60&v={tstamp}"
        ]
    }

    fallbacks = {
        "Concursos Públicos": [
            {"title": "Novo Edital Federal Abre Milhares de Vagas com Inscrições Abertas", "desc": "Confira os requisitos, cargos disponíveis e prazos para concorrer às vagas no serviço público."},
            {"title": "Órgãos Estaduais Divulgam Concursos com Salários Atrativos", "desc": "Oportunidades contemplam níveis fundamental, médio e superior com lotação imediata."}
        ],
        "Vagas CLT & Empresas": [
            {"title": "Grandes Redes e Indústrias Abrem Centenas de Vagas de Emprego", "desc": "Processo seletivo oferece contratação imediata e benefícios atrativos para diversas funções."},
            {"title": "Mercado Corporativo Registra Alta na Contratação em Todo o País", "desc": "Confira quais setores estão liderando a geração de postos de trabalho formal."}
        ],
        "Trabalho Home Office": [
            {"title": "Empresas de Tecnologia Abrem Vagas para Atendimento e Suporte Remoto", "desc": "Trabalhe de casa com flexibilidade de horários e equipamentos fornecidos pela empresa."},
            {"title": "Oportunidades Internacionais Buscam Profissionais Brasileiros para Home Office", "desc": "Vagas exigem habilidades digitais e oferecem remuneração competitiva."}
        ],
        "Economia & Salários": [
            {"title": "Indicadores Econômicos Apontam Novas Projeções para o Mercado de Trabalho", "desc": "Especialistas analisam o impacto da inflação e dos juros nas negociações salariais."},
            {"title": "Governo Anuncia Novas Diretrizes para Programas de Qualificação Profissional", "desc": "Iniciativa visa capacitar trabalhadores para as novas demandas do setor produtivo."}
        ]
    }

    categorias_processadas, todas_noticias = {}, []
    
    for cat_nome, info in fontes.items():
        items_cat = []
        imgs = list(imagens_por_categoria[cat_nome])
        random.shuffle(imgs)
        fb_list = fallbacks[cat_nome]
        
        for url in info["urls"]:
            try:
                resp = requests.get(url, verify=False, timeout=6)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    for item in root.findall('.//item')[:3]:
                        t_elem = item.find('title')
                        l_elem = item.find('link')
                        d_elem = item.find('description')
                        
                        tit = t_elem.text if t_elem is not None and t_elem.text else ""
                        lnk = l_elem.text if l_elem is not None and l_elem.text else "https://news.google.com"
                        dsc = d_elem.text if d_elem is not None and d_elem.text else ""
                        
                        if not tit: continue
                        if "<" in dsc: dsc = re.sub('<.*?>', '', dsc)
                        if not dsc.strip(): dsc = "Oportunidade oficial verificada com inscrições abertas."
                        
                        obj = {
                            "category": cat_nome, "color": info["color"],
                            "title": tit.strip(), "link": lnk.strip(), "image": imgs[len(items_cat) % len(imgs)],
                            "description": dsc.strip()[:140] + "..." if len(dsc.strip()) > 140 else dsc.strip()
                        }
                        items_cat.append(obj)
                        todas_noticias.append(obj)
            except:
                pass
                
        while len(items_cat) < 6:
            idx = len(items_cat)
            fb = fb_list[idx % len(fb_list)]
            obj = {
                "category": cat_nome, "color": info["color"],
                "title": fb["title"], "link": f"#{info['id']}",
                "image": imgs[idx % len(imgs)], "description": fb["desc"]
            }
            items_cat.append(obj)
            todas_noticias.append(obj)
            
        random.shuffle(items_cat)
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:6]}
        
    return categorias_processadas, todas_noticias

def gerar_sitemap(lista_estados):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMINIO_SITE}/index.html</loc><lastmod>{data_hoje}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>')
    xml.append(f'  <url><loc>{DOMINIO_SITE}/anuncie.html</loc><lastmod>{data_hoje}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>')
    for e in lista_estados:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{e["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write("\n".join(xml))

def send_pings():
    sitemap_url = f"{DOMINIO_SITE}/sitemap.xml"
    encoded = urllib.parse.quote(sitemap_url, safe='')
    for url in [f"https://www.google.com/ping?sitemap={encoded}", f"https://www.bing.com/ping?sitemap={encoded}"]:
        try:
            urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=5)
        except: pass

def gerar_site():
    timestamp_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
    print(f"Gerando portal nacional de vagas e concursos em {timestamp_atual}...")
    
    estados_brasil = [
        {"name": "São Paulo (SP)", "file": "sao-paulo.html"},
        {"name": "Rio de Janeiro (RJ)", "file": "rio-de-janeiro.html"},
        {"name": "Minas Gerais (MG)", "file": "minas-gerais.html"},
        {"name": "Bahia (BA)", "file": "bahia.html"},
        {"name": "Paraná (PR)", "file": "parana.html"},
        {"name": "Rio Grande do Sul (RS)", "file": "rio-grande-do-sul.html"},
        {"name": "Santa Catarina (SC)", "file": "santa-catarina.html"},
        {"name": "Distrito Federal (DF)", "file": "distrito-federal.html"},
        {"name": "Pernambuco (PE)", "file": "pernambuco.html"},
        {"name": "Ceará (CE)", "file": "ceara.html"}
    ]
    
    categorias_dict, todas_noticias = buscar_noticias_brasil()
    template_estado = Template(ESTADO_TEMPLATE)
    lista_estados_gerados = []
    
    for est in estados_brasil:
        random.shuffle(todas_noticias)
        noticias_est = todas_noticias[:6]
        for n in noticias_est:
            n["category"] = f"Vagas • {est['name'].split(' ')[0]}"
            
        with open(est["file"], "w", encoding="utf-8") as f:
            f.write(template_estado.render(
                estado=est, noticias=noticias_est, timestamp=timestamp_atual,
                ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE
            ))
        lista_estados_gerados.append(est)
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=lista_estados_gerados, categorias=categorias_dict, timestamp=timestamp_atual,
            ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE
        ))
        
    with open("anuncie.html", "w", encoding="utf-8") as f:
        f.write(Template(ANUNCIE_TEMPLATE).render(
            timestamp=timestamp_atual, ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT,
            monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE
        ))
        
    gerar_sitemap(lista_estados_gerados)
    send_pings()
    print("Sucesso absoluto! Portal limpo, blindado e reestruturado.")

if __name__ == "__main__":
    gerar_site()

