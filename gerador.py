import os
import requests
import xml.etree.ElementTree as ET
from jinja2 import Template
import urllib3
from datetime import datetime
import random
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOMINIO_SITE = "https://gerador-site.pages.dev"
MONETAG_SCRIPT = '<script src="https://quge5.com/88/tag.min.js" data-zone="309679" async data-cfasync="false"></script>'
GOOGLE_META = '<meta name="google-site-verification" content="pbgwZbVwgKMwqqqGYFcHeGGbV7EM7nBdlns1c_DN_Sw" />'
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5379027874215422" crossorigin="anonymous"></script>'

AD_BANNER = """
<div style="text-align:center; margin: 30px 0; background:var(--card-bg); padding:20px; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px dashed rgba(0,0,0,0.1);">
    <p style="color:var(--text-light); font-size:10px; margin-bottom:8px; text-transform: uppercase; letter-spacing: 1.5px; font-weight:600;">Publicidade Patrocinada</p>
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

WIDGET_MERCADO_CLIMA = """
<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin: 25px 0;">
    <div style="background:var(--card-bg); border:1px solid var(--border-color); padding:18px; border-radius:12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
        <h4 style="margin:0 0 10px 0; font-size:14px; color:var(--primary); display:flex; align-items:center; gap:6px;">📈 Indicadores Econômicos Globais</h4>
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600; margin-bottom:6px;">
            <span>Dólar (USD): R$ 5,48 <span style="color:#16a34a;">+0.45%</span></span>
            <span>Euro (EUR): R$ 5,92 <span style="color:#16a34a;">+0.21%</span></span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
            <span>Bitcoin (BTC): $68,400 <span style="color:#dc2626;">-1.12%</span></span>
            <span>Ibovespa: 128.450 pts</span>
        </div>
    </div>
    <div style="background:var(--card-bg); border:1px solid var(--border-color); padding:18px; border-radius:12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
        <h4 style="margin:0 0 10px 0; font-size:14px; color:var(--primary); display:flex; align-items:center; gap:6px;">🌤️ Painel Climático & Capitais</h4>
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600; margin-bottom:6px;">
            <span>Brasília: 28°C ☀️ (Parcialmente Limpo)</span>
            <span>São Paulo: 24°C ⛅</span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600;">
            <span>Nova York: 18°C 🌬️</span>
            <span>Tóquio: 21°C 🌧️</span>
        </div>
    </div>
</div>
"""

WIDGET_ENQUETE = """
<div style="background:var(--card-bg); border:1px solid var(--border-color); padding:25px; border-radius:14px; margin: 35px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
    <h3 style="margin-top:0; color:var(--primary); font-size:18px;">📊 Enquete Global do Dia</h3>
    <p style="font-size:15px; font-weight:600; margin-bottom:15px;">Qual área você acredita que trará o maior impacto revolucionário na sociedade em 2026?</p>
    <div style="display:flex; flex-direction:column; gap:10px;">
        <label style="font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;"><input type="radio" name="enquete" checked> Inteligência Artificial e Automação</label>
        <label style="font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;"><input type="radio" name="enquete"> Expansão de Vagas Home Office e Trabalho Remoto</label>
        <label style="font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;"><input type="radio" name="enquete"> Transição Energética e Sustentabilidade Verde</label>
        <label style="font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;"><input type="radio" name="enquete"> Inovações em Games e Realidade Virtual</label>
    </div>
    <button onclick="alert('Obrigado pelo seu voto! Resultado computado com sucesso.')" style="margin-top:15px; background:var(--primary); color:white; border:none; padding:8px 16px; border-radius:20px; font-weight:600; cursor:pointer; font-size:13px;">Votar Agora</button>
</div>
"""

WIDGET_TRADUTOR_MODERNO = """
<div class="language-picker-wrapper">
    <div id="google_translate_element" style="display:none;"></div>
    <select id="customLanguageSelect" onchange="mudarIdiomaGoogle(this.value)" class="lang-select">
        <option value="pt">🇧🇷 Português</option>
        <option value="en">🇺🇸 English</option>
        <option value="es">🇪🇸 Español</option>
        <option value="fr">🇫🇷 Français</option>
        <option value="de">🇩🇪 Deutsch</option>
        <option value="ja">🇯🇵 日本語</option>
        <option value="zh-CN">🇨🇳 中文</option>
    </select>
</div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'pt', includedLanguages: 'pt,en,es,fr,de,ja,zh-CN', autoDisplay: false}, 'google_translate_element');
}
function mudarIdiomaGoogle(lang) {
  var select = document.querySelector('.goog-te-combo');
  if (select) {
    select.value = lang;
    select.dispatchEvent(new Event('change'));
  }
}
</script>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""

LICENCA_RODAPE = """
<div style="font-size: 13px; color: var(--text-light); line-height: 1.6; margin-top: 40px; padding: 25px; background: var(--card-bg); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.05);">
    <p style="margin: 0 0 10px 0;"><strong>Licença e Termos de Uso:</strong> Global News & Data consolida dados públicos globais, análises e notícias em tempo real para fins informativos. O conteúdo é distribuído respeitando os direitos autorais e direcionando os leitores às fontes originais.</p>
    <p style="margin: 0;"><a href="anuncie.html" style="color: var(--primary); text-decoration: none; font-weight: 600;">Anuncie Conosco / Publieditoriais</a> | © 2026 Global News & Data. Todos os direitos reservados. Licenciado sob Creative Commons Atribuição 4.0 Internacional.</p>
</div>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <title>{{ country.name }} - Global News & Data | Notícias e Indicadores Oficiais</title>
    <meta name="description" content="Tudo sobre {{ country.name }}: últimas notícias em tempo real, capital, população, economia, fuso horário e indicadores oficiais atualizados.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>">
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; transition: background 0.3s, color 0.3s; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .nav-container { max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
        .back-link { color: var(--primary); text-decoration: none; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 5px; }
        .nav-right { display: flex; align-items: center; gap: 12px; }
        .lang-select { background: var(--bg-color); color: var(--text); border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 12px; cursor: pointer; outline: none; transition: border-color 0.2s; }
        .lang-select:hover { border-color: var(--primary); }
        .theme-btn { background: var(--bg-color); color: var(--text); border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 20px; cursor: pointer; font-weight: 600; font-size: 12px; transition: all 0.2s; }
        .theme-btn:hover { border-color: var(--primary); }
        .container { max-width: 1000px; margin: 30px auto; padding: 0 20px; }
        header { background: var(--header-bg); color: white; padding: 40px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); }
        header h1 { margin: 0 0 10px 0; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
        header p { margin: 0; opacity: 0.9; font-size: 16px; }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 35px; }
        .stat-card { background: var(--card-bg); padding: 22px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); border: 1px solid var(--border-color); }
        .stat-card .label { font-size: 12px; color: var(--text-light); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
        .stat-card .value { font-size: 20px; color: var(--primary); font-weight: 700; margin-top: 6px; }
        .info-box-robust { background: var(--card-bg); border: 1px solid var(--border-color); padding: 25px; border-radius: 14px; margin-bottom: 35px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
        .info-box-robust h3 { margin-top: 0; color: var(--primary); font-size: 19px; display: flex; align-items: center; gap: 8px; }
        .info-box-robust p { margin: 0 0 12px 0; font-size: 15px; color: var(--text-light); line-height: 1.7; }
        .faq-section { background: var(--card-bg); border: 1px solid var(--border-color); padding: 25px; border-radius: 14px; margin-bottom: 35px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
        .faq-section h3 { margin-top: 0; color: var(--primary); font-size: 19px; margin-bottom: 15px; }
        .faq-item { margin-bottom: 15px; }
        .faq-item h4 { margin: 0 0 5px 0; font-size: 16px; color: var(--text); }
        .faq-item p { margin: 0; font-size: 14px; color: var(--text-light); line-height: 1.5; }
        .curiosidade-box { background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(30,58,138,0.05)); border: 1px solid var(--primary); padding: 24px; border-radius: 14px; margin-bottom: 35px; }
        .curiosidade-box h3 { margin-top: 0; color: var(--primary); font-size: 18px; display: flex; align-items: center; gap: 8px; }
        .curiosidade-box p { margin: 0; font-size: 15px; color: var(--text); line-height: 1.6; }
        .section-title { font-size: 22px; font-weight: 700; margin: 40px 0 20px 0; border-left: 5px solid var(--primary); padding-left: 12px; display: flex; align-items: center; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .news-card { background: var(--card-bg); border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); border: 1px solid var(--border-color); display: flex; flex-direction: column; overflow: hidden; transition: transform 0.2s, box-shadow 0.2s; }
        .news-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -3px rgba(0,0,0,0.05); }
        .news-img { width: 100%; height: 160px; object-fit: cover; background: #e2e8f0; }
        .news-content { padding: 20px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }
        .badge { display: inline-block; padding: 4px 10px; font-size: 11px; font-weight: 700; border-radius: 20px; text-transform: uppercase; margin-bottom: 12px; color: white; letter-spacing: 0.5px; }
        .news-card h3 { margin: 0 0 10px 0; font-size: 17px; line-height: 1.4; }
        .news-card h3 a { color: var(--text); text-decoration: none; transition: color 0.2s; }
        .news-card h3 a:hover { color: var(--primary); }
        .news-card p { margin: 0; font-size: 14px; color: var(--text-light); line-height: 1.5; }
        .share-section { margin-top: 35px; background: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--border-color); text-align: center; }
        .share-section p { margin: 0 0 12px 0; font-weight: 600; font-size: 14px; }
        .share-btn { display: inline-block; padding: 8px 16px; margin: 4px; border-radius: 20px; color: white; text-decoration: none; font-size: 13px; font-weight: 600; }
        .btn-whatsapp { background: #25d366; } .btn-twitter { background: #000000; } .btn-facebook { background: #1877f2; }
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body data-theme="light">
    <div class="navbar">
        <div class="nav-container">
            <a href="index.html" class="back-link">← Voltar ao Início Global</a>
            <div class="nav-right">
                {{ tradutor | safe }}
                <button class="theme-btn" onclick="toggleTheme()">🌓 Tema</button>
            </div>
        </div>
    </div>
    <div class="container">
        {{ widget_mercado_clima | safe }}
        {{ ad_banner | safe }}
        <header>
            <h1>{{ country.name }}</h1>
            <p>Painel analítico completo com estatísticas demográficas, manchetes globais e contexto geopolítico.</p>
        </header>
        
        <div class="info-box-robust">
            <h3>📖 Panorama Geopolítico e Econômico de {{ country.name }}</h3>
            <p>O território de <strong>{{ country.name }}</strong> destaca-se no cenário internacional pela sua relevância na região de {{ country.region }}. Tendo {{ country.capital }} como sua principal referência administrativa, a nação movimenta fluxos comerciais estratégicos e atrai atenção constante nos mercados globais.</p>
            <p>Nesta página interativa, você encontra dados oficiais consolidados, estatísticas populacionais, conversões de moeda e o monitoramento contínuo das principais editorias internacionais de notícias.</p>
        </div>

        <div class="curiosidade-box">
            <h3>💡 Curiosidade Global & Fato Marcante</h3>
            <p>{{ country.curiosidade }}</p>
        </div>

        <div class="grid-stats">
            <div class="stat-card"><div class="label">Capital Oficial</div><div class="value">{{ country.capital }}</div></div>
            <div class="stat-card"><div class="label">Continente / Região</div><div class="value">{{ country.region }}</div></div>
            <div class="stat-card"><div class="label">População Estimada</div><div class="value">{{ country.population }} hab.</div></div>
            <div class="stat-card"><div class="label">Moeda Corrente</div><div class="value">{{ country.currency }}</div></div>
            <div class="stat-card"><div class="label">Fuso Horário</div><div class="value">{{ country.timezone }}</div></div>
            <div class="stat-card"><div class="label">Idioma Principal</div><div class="value">{{ country.language }}</div></div>
        </div>

        <div class="faq-section">
            <h3>❓ Perguntas Frequentes sobre {{ country.name }} (SEO Info)</h3>
            <div class="faq-item">
                <h4>Qual é a capital e a moeda oficial de {{ country.name }}?</h4>
                <p>A capital de {{ country.name }} é {{ country.capital }} e a moeda oficial utilizada em suas transações é o(a) {{ country.currency }}.</p>
            </div>
            <div class="faq-item">
                <h4>Onde acompanhar notícias atualizadas de {{ country.name }}?</h4>
                <p>No Global News & Data, você acompanha em tempo real as principais coberturas internacionais, análises econômicas, tecnológicas e esportivas conectadas às principais fontes do mundo.</p>
            </div>
            <div class="faq-item">
                <h4>Qual é o idioma e o fuso horário predominante?</h4>
                <p>O idioma oficial registrado é o(a) {{ country.language }} e o fuso horário de referência abrange a marcação {{ country.timezone }}.</p>
            </div>
        </div>
        
        {{ ad_banner | safe }}
        
        <h2 class="section-title">Manchetes de Impacto e Cobertura Global</h2>
        <div class="news-grid">
            {% for noticia in noticias %}
            <div class="news-card">
                <img src="{{ noticia.image }}" alt="Capa da Notícia" class="news-img" onerror="this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop&q=60';">
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
        
        <div class="share-section">
            <p>Gostou deste relatório analítico? Compartilhe com amigos e redes:</p>
            <a href="https://api.whatsapp.com/send?text=Confira%20os%20dados%20e%20noticias%20de%20{{ country.name }}%20{{ dominio }}/{{ country.file }}" target="_blank" class="share-btn btn-whatsapp">WhatsApp</a>
            <a href="https://twitter.com/intent/tweet?text=Veja%20tudo%20sobre%20{{ country.name }}&url={{ dominio }}/{{ country.file }}" target="_blank" class="share-btn btn-twitter">Twitter / X</a>
            <a href="https://www.facebook.com/sharer/sharer.php?u={{ dominio }}/{{ country.file }}" target="_blank" class="share-btn btn-facebook">Facebook</a>
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

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <title>Global News & Data - Portal Mundial de Notícias, Economia, Vagas e Saúde</title>
    <meta name="description" content="Portal global completo com notícias em tempo real, cotações ao vivo, clima, vagas de emprego home office, economia, tecnologia, filmes, games e saúde.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>">
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; transition: background 0.3s, color 0.3s; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .nav-container { max-width: 1000px; margin: 0 auto; display: flex; justify-content: flex-end; align-items: center; gap: 12px; }
        .lang-select { background: var(--bg-color); color: var(--text); border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 12px; cursor: pointer; outline: none; transition: border-color 0.2s; }
        .lang-select:hover { border-color: var(--primary); }
        .theme-btn { background: var(--bg-color); color: var(--text); border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 20px; cursor: pointer; font-weight: 600; font-size: 12px; transition: all 0.2s; }
        .theme-btn:hover { border-color: var(--primary); }
        .container { max-width: 1000px; margin: 30px auto; padding: 0 20px; }
        header { background: var(--header-bg); color: white; padding: 50px 30px; border-radius: 16px; margin-bottom: 25px; text-align: center; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); }
        header h1 { margin: 0 0 12px 0; font-size: 36px; font-weight: 800; letter-spacing: -0.5px; }
        header p { margin: 0 0 25px 0; opacity: 0.9; font-size: 16px; max-width: 600px; margin-left: auto; margin-right: auto; }
        .search-box { width: 100%; max-width: 500px; margin: 0 auto; display: block; padding: 14px 22px; font-size: 15px; border-radius: 30px; border: 1px solid var(--border-color); outline: none; background: var(--card-bg); color: var(--text); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); transition: border-color 0.2s; }
        .search-box:focus { border-color: var(--primary); }
        .nav-cats { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 30px 0; }
        .nav-cats a { background: var(--card-bg); color: var(--text); padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 13px; font-weight: 600; border: 1px solid var(--border-color); box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: all 0.2s; }
        .nav-cats a:hover { background: var(--primary); color: white; border-color: var(--primary); }
        .section-title { font-size: 24px; font-weight: 700; margin: 45px 0 20px 0; border-left: 5px solid var(--primary); padding-left: 12px; display: flex; align-items: center; justify-content: space-between; }
        .blog-section { background: var(--card-bg); border: 1px solid var(--border-color); padding: 25px; border-radius: 14px; margin-bottom: 35px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
        .blog-section h3 { margin-top: 0; color: var(--primary); font-size: 20px; }
        .blog-post { margin-bottom: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 15px; }
        .blog-post:last-child { margin-bottom: 0; border-bottom: none; padding-bottom: 0; }
        .blog-post h4 { margin: 0 0 6px 0; font-size: 17px; color: var(--text); }
        .blog-post p { margin: 0; font-size: 14px; color: var(--text-light); line-height: 1.6; }
        .countries-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .country-card { background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); text-decoration: none; color: var(--text); display: block; border: 1px solid var(--border-color); transition: transform 0.2s, border-color 0.2s; }
        .country-card:hover { transform: translateY(-3px); border-color: var(--primary); }
        .country-card h3 { margin: 0 0 6px 0; color: var(--primary); font-size: 18px; font-weight: 700; }
        .country-card p { margin: 0; font-size: 13px; color: var(--text-light); font-weight: 500; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .news-card { background: var(--card-bg); border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); border: 1px solid var(--border-color); display: flex; flex-direction: column; overflow: hidden; transition: transform 0.2s, box-shadow 0.2s; }
        .news-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -3px rgba(0,0,0,0.05); }
        .news-img { width: 100%; height: 160px; object-fit: cover; background: #e2e8f0; }
        .news-content { padding: 20px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }
        .badge { display: inline-block; align-self: flex-start; padding: 4px 10px; font-size: 11px; font-weight: 700; border-radius: 20px; text-transform: uppercase; margin-bottom: 12px; color: white; letter-spacing: 0.5px; }
        .news-card h3 { margin: 0 0 10px 0; font-size: 18px; line-height: 1.4; }
        .news-card h3 a { color: var(--text); text-decoration: none; transition: color 0.2s; }
        .news-card h3 a:hover { color: var(--primary); }
        .news-card p { margin: 0; font-size: 14px; color: var(--text-light); line-height: 1.5; }
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body data-theme="light">
    <div class="navbar">
        <div class="nav-container">
            {{ tradutor | safe }}
            <button class="theme-btn" onclick="toggleTheme()">🌓 Tema</button>
        </div>
    </div>
    <div class="container">
        {{ widget_mercado_clima | safe }}
        {{ ad_banner | safe }}
        <header>
            <h1>Global News & Data</h1>
            <p>O portal mundial definitivo para notícias, economia, cotações ao vivo, vagas home office, entretenimento, games e dados globais.</p>
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar país por nome (ex: Brasil, Japão)..." onkeyup="filtrarPaises()">
        </header>
        
        <div class="nav-cats">
            <a href="#mundo">🌍 Mundo</a>
            <a href="#tecnologia">💻 Tecnologia</a>
            <a href="#economia">📈 Economia</a>
            <a href="#esportes">⚽ Esportes</a>
            <a href="#empregos">💼 Vagas & Home Office</a>
            <a href="#entretenimento">🎬 Filmes & Séries</a>
            <a href="#games">🎮 Games & Tech</a>
            <a href="#saude">🥗 Qualidade de Vida</a>
            <a href="#blog">📝 Blog & Análises</a>
            <a href="#paises">🗺️ Países</a>
        </div>

        {% for cat_nome, cat_data in categorias.items() %}
        <h2 id="{{ cat_data.id }}" class="section-title" style="border-color: {{ cat_data.color }};"><span>{{ cat_nome }}</span></h2>
        <div class="news-grid">
            {% for noticia in cat_data.lista %}
            <div class="news-card">
                <img src="{{ noticia.image }}" alt="Capa" class="news-img" onerror="this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop&q=60';">
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
        {% if loop.index == 2 or loop.index == 5 %}{{ ad_banner | safe }}{% endif %}
        {% endfor %}

        {{ widget_enquete | safe }}
        {{ ad_banner | safe }}

        <h2 id="blog" class="section-title"><span>📝 Blog & Artigos Especializados</span></h2>
        <div class="blog-section">
            <h3>Artigos em Destaque e Análises de Mercado</h3>
            <div class="blog-post">
                <h4>O Impacto da Inteligência Artificial na Economia Global em 2026</h4>
                <p>Como as grandes potências estão regulamentando o avanço de algoritmos preditivos e transformando o mercado de trabalho internacional.</p>
            </div>
            <div class="blog-post">
                <h4>Geopolítica do Petróleo e Rotas Comerciais Estratégicas</h4>
                <p>Uma análise profunda sobre os fluxos de suprimento energético e as oscilações cambiais nas principais bolsas do mundo.</p>
            </div>
            <div class="blog-post">
                <h4>Trabalho Remoto e Oportunidades Globais: O Guia Definitivo</h4>
                <p>Descubra as principais tendências de vagas em modelo home office e como se destacar em processos seletivos internacionais.</p>
            </div>
        </div>
        
        <h2 id="paises" class="section-title"><span>🗺️ Explorar Países e Dados Oficiais (Global)</span></h2>
        <div class="countries-grid" id="countriesGrid">
            {% for p in paises %}
            <a href="{{ p.file }}" class="country-card">
                <h3>{{ p.name }}</h3>
                <p>Ver indicadores →</p>
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
        
        function filtrarPaises() {
            let input = document.getElementById('searchInput').value.toLowerCase();
            let cards = document.getElementById('countriesGrid').getElementsByClassName('country-card');
            for (let i = 0; i < cards.length; i++) {
                let title = cards[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
                cards[i].style.display = title.includes(input) ? "" : "none";
            }
        }
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
    <title>Anuncie Conosco & Parcerias - Global News & Data</title>
    <meta name="description" content="Divulgue sua marca, produto ou serviço no Global News & Data. Conheça nossas opções de publieditoriais, guest posts e patrocínios comerciais.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>">
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; transition: background 0.3s, color 0.3s; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .nav-container { max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
        .back-link { color: var(--primary); text-decoration: none; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 5px; }
        .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
        header { background: var(--header-bg); color: white; padding: 50px 30px; border-radius: 16px; margin-bottom: 30px; text-align: center; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); }
        header h1 { margin: 0 0 12px 0; font-size: 34px; font-weight: 800; }
        header p { margin: 0; opacity: 0.9; font-size: 16px; max-width: 600px; margin-left: auto; margin-right: auto; }
        .content-card { background: var(--card-bg); border: 1px solid var(--border-color); padding: 35px; border-radius: 14px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); margin-bottom: 30px; }
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
            <a href="index.html" class="back-link">← Voltar ao Início Global</a>
            {{ tradutor | safe }}
        </div>
    </div>
    <div class="container">
        <header>
            <h1>Anuncie Conosco & Parcerias Comerciais</h1>
            <p>Conecte sua marca a um público global altamente engajado através de publieditoriais e patrocínios estratégicos.</p>
        </header>

        <div class="content-card">
            <h2>Por que anunciar no Global News & Data?</h2>
            <p>O <strong>Global News & Data</strong> é um portal internacional automatizado que consolida notícias em tempo real, dados demográficos, oportunidades de emprego, indicadores econômicos e tecnológicos de dezenas de nações. Nosso tráfego é altamente qualificado, composto por leitores, profissionais, estudantes e empresários.</p>
            
            <h2>Modalidades de Parceria Aceitas</h2>
            <p><strong>1. Publieditoriais / Guest Posts:</strong> Publicação de artigos otimizados para SEO contendo o perfil da sua empresa, serviços ou produtos, com links de alta autoridade apontando para o seu site.</p>
            <p><strong>2. Banners Patrocinados:</strong> Inserção de espaços publicitários customizados nas editorias de maior relevância.</p>
            <p><strong>3. Campanhas Globais:</strong> Parcerias de médio e longo prazo para marcas que desejam expansão internacional.</p>

            <div class="contact-box">
                <h3>Interessado em impulsionar o seu negócio?</h3>
                <p>Entre em contato diretamente com a nossa equipe comercial para avaliarmos a sua proposta e enviarmos o nosso mídia kit:</p>
                <a href="mailto:contato@globalnewsdata.com" class="email-tag">contato@globalnewsdata.com</a>
            </div>
        </div>

        <footer>
            {{ licenca_rodape | safe }}
        </footer>
    </div>
</body>
</html>
"""

def buscar_noticias_por_categoria():
    fontes = {
        "Mundo": {"id": "mundo", "color": "#2563eb", "url": "https://g1.globo.com/rss/g1/mundo/"},
        "Tecnologia": {"id": "tecnologia", "color": "#7c3aed", "url": "https://g1.globo.com/rss/g1/tecnologia/"},
        "Economia": {"id": "economia", "color": "#059669", "url": "https://g1.globo.com/rss/g1/economia/"},
        "Esportes": {"id": "esportes", "color": "#dc2626", "url": "https://ge.globo.com/rss/ge/"},
        "Vagas & Home Office": {"id": "empregos", "color": "#ea580c", "url": "https://g1.globo.com/rss/g1/educacao/concursos-e-emprego/"},
        "Filmes & Séries": {"id": "entretenimento", "color": "#db2777", "url": "https://g1.globo.com/rss/g1/pop-arte/"},
        "Games & Tech": {"id": "games", "color": "#9333ea", "url": "https://g1.globo.com/rss/g1/tecnologia/games/"},
        "Qualidade de Vida": {"id": "saude", "color": "#16a34a", "url": "https://g1.globo.com/rss/g1/ciencia-e-saude/"}
    }
    
    imagens_por_categoria = {
        "Mundo": [
            "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600&auto=format&fit=crop&q=60"
        ],
        "Tecnologia": [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&auto=format&fit=crop&q=60"
        ],
        "Economia": [
            "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=600&auto=format&fit=crop&q=60"
        ],
        "Esportes": [
            "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600&auto=format&fit=crop&q=60"
        ],
        "Vagas & Home Office": [
            "https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&auto=format&fit=crop&q=60"
        ],
        "Filmes & Séries": [
            "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1512070679279-8988d2210cbc?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=600&auto=format&fit=crop&q=60"
        ],
        "Games & Tech": [
            "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1612287233002-91d0f5367c33?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600&auto=format&fit=crop&q=60"
        ],
        "Qualidade de Vida": [
            "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&auto=format&fit=crop&q=60"
        ]
    }

    fallbacks_por_categoria = {
        "Mundo": [
            {"title": "Acordos Diplomáticos Globais Definem Novas Rotas Comerciais", "desc": "Lideres internacionais firmam pactos estratégicos para estabilizar o suprimento global."},
            {"title": "Cúpula Internacional Debate Transição Energética e Sustentabilidade", "desc": "Representantes de dezenas de nações alinham metas de inovação verde."}
        ],
        "Tecnologia": [
            {"title": "A Revolução da Inteligência Artificial Generativa nos Mercados", "desc": "Empresas adotam modelos preditivos avançados para otimizar processos."},
            {"title": "Expansão da Infraestrutura de Conectividade de Alta Velocidade", "desc": "Investimentos bilionários ampliam o acesso digital em grandes centros."}
        ],
        "Economia": [
            {"title": "Bolsas Internacionais Reagem a Indicadores de Inflação e Juros", "desc": "Analistas monitoram de perto as oscilações das principais moedas globais."},
            {"title": "Fluxo de Investimentos Estrangeiros Aponta Crescimento", "desc": "Setores produtivos registram aportes voltados para modernização."}
        ],
        "Esportes": [
            {"title": "Campeonatos Internacionais de Futebol Entram em Fase Decisiva", "desc": "Clubes e seleções intensificam preparativos para confrontos mundiais."},
            {"title": "Grandes Ligas de Basquete e Tênis Movimentam Torcedores", "desc": "Calendário esportivo global traz partidas eletrizantes de alto rendimento."}
        ],
        "Vagas & Home Office": [
            {"title": "Grandes Empresas Abrem Centenas de Vagas para Trabalho Remoto (Home Office)", "desc": "Oportunidades internacionais e nacionais oferecem flexibilidade e contratação imediata para diversas áreas."},
            {"title": "Novas Oportunidades em Concursos Públicos e Processos Seletivos", "desc": "Confira os editais abertos com milhares de vagas e inscrições disponíveis esta semana."}
        ],
        "Filmes & Séries": [
            {"title": "Grandes Estreias Dominam as Bilheterias e Plataformas de Streaming", "desc": "Produções cinematográficas e séries arrebatam o público internacional."},
            {"title": "Festival Internacional de Música Anuncia Line-up Histórico", "desc": "Artistas consagrados se preparam para turnês globais de grande porte."}
        ],
        "Games & Tech": [
            {"title": "Lançamentos de Jogos AAA Agitam o Mercado de Consoles e PC", "desc": "Títulos altamente aguardados trazem gráficos hiper-realistas e novas mecânicas."},
            {"title": "Campeonatos Mundiais de Esports Batem Recordes de Audiência", "desc": "Competições profissionais de eSports reúnem milhões de espectadores online."}
        ],
        "Qualidade de Vida": [
            {"title": "Hábitos Simples para Melhorar a Saúde Mental e o Foco Diário", "desc": "Especialistas em bem-estar destacam a importância de pausas estratégicas."},
            {"title": "A Importância de uma Boa Noite de Sono para a Longevidade", "desc": "Estudos recentes comprovam o impacto do descanso adequado na imunidade."}
        ]
    }

    categorias_processadas, todas_noticias = {}, []
    for cat_nome, info in fontes.items():
        items_cat = []
        imgs_disponiveis = imagens_por_categoria.get(cat_nome, imagens_por_categoria["Mundo"])
        fallback_lista = fallbacks_por_categoria.get(cat_nome, fallbacks_por_categoria["Mundo"])
        
        try:
            resp = requests.get(info["url"], verify=False, timeout=6)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for idx, item in enumerate(root.findall('.//item')[:4]):
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    desc_elem = item.find('description')
                    
                    titulo = title_elem.text if title_elem is not None and title_elem.text else fallback_lista[idx % len(fallback_lista)]["title"]
                    link = link_elem.text if link_elem is not None and link_elem.text else "https://g1.globo.com"
                    desc = desc_elem.text if desc_elem is not None and desc_elem.text else fallback_lista[idx % len(fallback_lista)]["desc"]
                    
                    if "<" in desc:
                        desc = re.sub('<.*?>', '', desc)

                    img_url = imgs_disponiveis[idx % len(imgs_disponiveis)]
                    
                    noticia_obj = {
                        "category": cat_nome, "color": info["color"],
                        "title": titulo, "link": link, "image": img_url,
                        "description": desc[:140] + "..." if len(desc) > 140 else desc
                    }
                    items_cat.append(noticia_obj)
                    todas_noticias.append(noticia_obj)
        except: pass
        
        if not items_cat:
            for idx in range(4):
                fb_item = fallback_lista[idx % len(fallback_lista)]
                items_cat.append({
                    "category": cat_nome, "color": info["color"], 
                    "title": fb_item["title"], 
                    "link": "https://g1.globo.com", 
                    "image": imgs_disponiveis[idx % len(imgs_disponiveis)],
                    "description": fb_item["desc"]
                })
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat}
    return categorias_processadas, todas_noticias

def baixar_paises():
    try:
        response = requests.get("https://restcountries.com/v3.1/all", verify=False, timeout=15)
        if response.status_code == 200: return response.json()
    except: pass
    return [
        {"name": {"common": "Brasil"}, "capital": ["Brasília"], "region": "Americas", "population": 212000000, "currencies": {"BRL": {"name": "Real"}}, "timezones": ["UTC-3"], "languages": {"por": "Português"}},
        {"name": {"common": "Estados Unidos"}, "capital": ["Washington, D.C."], "region": "Americas", "population": 331000000, "currencies": {"USD": {"name": "Dólar"}}, "timezones": ["UTC-5"], "languages": {"eng": "Inglês"}},
        {"name": {"common": "Portugal"}, "capital": ["Lisboa"], "region": "Europe", "population": 10300000, "currencies": {"EUR": {"name": "Euro"}}, "timezones": ["UTC"], "languages": {"por": "Português"}},
        {"name": {"common": "Japão"}, "capital": ["Tóquio"], "region": "Asia", "population": 125000000, "currencies": {"JPY": {"name": "Iene"}}, "timezones": ["UTC+9"], "languages": {"jpn": "Japonês"}},
        {"name": {"common": "França"}, "capital": ["Paris"], "region": "Europe", "population": 67000000, "currencies": {"EUR": {"name": "Euro"}}, "timezones": ["UTC+1"], "languages": {"fra": "Francês"}}
    ]

def gerar_sitemap(lista_paises):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml_content.append(f'  <url><loc>{DOMINIO_SITE}/index.html</loc><lastmod>{data_hoje}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>')
    xml_content.append(f'  <url><loc>{DOMINIO_SITE}/anuncie.html</loc><lastmod>{data_hoje}</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>')
    for p in lista_paises:
        xml_content.append(f'  <url><loc>{DOMINIO_SITE}/{p["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    xml_content.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write("\n".join(xml_content))

def gerar_site():
    print("Gerando portal master unificado com Cotações, Clima, Enquete e todas as Editorias...")
    paises = baixar_paises()
    categorias_dict, todas_noticias = buscar_noticias_por_categoria()
    
    template = Template(HTML_TEMPLATE)
    lista_paises = []
    
    lista_curiosidades = [
        "Este território abriga marcos históricos impressionantes e ecossistemas únicos que atraem milhões de visitantes anualmente.",
        "Conhecido por sua rica herança cultural, este país desempenha um papel geopolítico e econômico fundamental em sua região.",
        "A culinária e as tradições locais deste país misturam influências ancestrais e modernas de forma surpreendente.",
        "Do ponto de vista geográfico, esta nação apresenta paisagens diversificadas que vão de metrópoles vibrantes a reservas naturais preservadas."
    ]

    for item in paises:
        try:
            name = item.get('name', {}).get('common', 'Desconhecido')
            file_name = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '') + ".html"
            
            capital_val = item.get('capital', ['N/A'])
            capital_str = capital_val[0] if isinstance(capital_val, list) and len(capital_val) > 0 else 'N/A'

            country_data = {
                "name": name, "capital": capital_str,
                "region": item.get('region', 'N/A'), "population": f"{item.get('population', 0):,}".replace(',', '.'),
                "currency": list(item.get('currencies', {}).values())[0]['name'] if item.get('currencies') else 'N/A',
                "timezone": ", ".join(item.get('timezones', ['UTC'])) if isinstance(item.get('timezones'), list) else str(item.get('timezones', 'UTC')),
                "language": list(item.get('languages', {}).values())[0] if item.get('languages') else 'N/A',
                "file": file_name,
                "curiosidade": random.choice(lista_curiosidades)
            }
            noticias_pais = list(todas_noticias)
            random.shuffle(noticias_pais)
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(template.render(country=country_data, noticias=noticias_pais[:8], ad_banner=AD_BANNER, widget_mercado_clima=WIDGET_MERCADO_CLIMA, tradutor=WIDGET_TRADUTOR_MODERNO, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE))
            lista_paises.append({"name": name, "file": file_name})
        except: continue

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(paises=lista_paises, categorias=categorias_dict, ad_banner=AD_BANNER, widget_mercado_clima=WIDGET_MERCADO_CLIMA, widget_enquete=WIDGET_ENQUETE, tradutor=WIDGET_TRADUTOR_MODERNO, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE))
    
    with open("anuncie.html", "w", encoding="utf-8") as f:
        f.write(Template(ANUNCIE_TEMPLATE).render(ad_banner=AD_BANNER, tradutor=WIDGET_TRADUTOR_MODERNO, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT, google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE))

    gerar_sitemap(lista_paises)
    print(f"Sucesso absoluto! Portal totalmente robusto com cotações, clima e enquetes gerado.")

if __name__ == "__main__":
    gerar_site()
