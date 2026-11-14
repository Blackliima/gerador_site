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
<div style="text-align:center; margin: 30px auto; width: 100%; max-width: 100%; overflow: hidden; background:var(--card-bg); padding:15px; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px dashed rgba(0,0,0,0.1); box-sizing: border-box;">
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
        <span style="color: var(--text);">🇧🇷 <strong>Salário Mínimo:</strong> R$ 1.520,00</span>
        <span style="color: var(--text);">📈 <strong>Taxa Selic:</strong> 11.25% a.a.</span>
        <span style="color: #16a34a;">💼 <strong>Vagas Home Office:</strong> +4.500 abertas</span>
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

LICENCA_RODAPE = """
<div style="font-size: 13px; color: var(--text-light); line-height: 1.6; margin-top: 40px; padding: 25px; background: var(--card-bg); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.05);">
    <p style="margin: 0 0 10px 0;"><strong>Aviso Legal:</strong> O <strong>Brasil Oportunidades & Vagas</strong> é um portal independente focado em divulgar editais de concursos públicos, oportunidades de emprego e vagas home office para todo o Brasil.</p>
    <p style="margin: 0;"><a href="anuncie.html" style="color: var(--primary); text-decoration: none; font-weight: 600;">Anuncie Vagas</a> | © 2026 Brasil Oportunidades & Vagas. Todos os direitos reservados.</p>
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
    <title>Brasil Oportunidades & Vagas - Concursos, Empregos e Editais</title>
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; width: 100%; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; width: 100%; }
        .nav-container { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; width: 100%; }
        .brand-logo { font-weight: 800; font-size: 18px; color: var(--primary); text-decoration: none; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; width: 100%; }
        header { background: var(--header-bg); color: white; padding: 40px 20px; border-radius: 16px; margin-bottom: 25px; text-align: center; width: 100%; }
        header h1 { margin: 0 0 10px 0; font-size: 32px; font-weight: 800; }
        header p { margin: 0 0 20px 0; opacity: 0.9; font-size: 15px; max-width: 650px; margin-left: auto; margin-right: auto; }
        .section-title { font-size: 22px; font-weight: 700; margin: 45px 0 20px 0; border-left: 5px solid var(--primary); padding-left: 12px; width: 100%; }
        
        /* GRID 100% BLINDADO E ALINHADO */
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
        .state-card:hover { border-color: var(--primary); }
        .state-card h3 { margin: 0 0 4px 0; color: var(--primary); font-size: 17px; font-weight: 700; }
        .state-card p { margin: 0; font-size: 12px; color: var(--text-light); }
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; width: 100%; }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    <div class="navbar">
        <div class="nav-container">
            <a href="index.html" class="brand-logo">💼 Brasil Vagas & Concursos</a>
        </div>
    </div>
    <div class="container">
        {{ ad_banner | safe }}
        <header>
            <h1>Brasil Oportunidades & Vagas</h1>
            <p>O maior portal brasileiro centralizado de editais de concursos públicos, vagas CLT e trabalho Home Office.</p>
        </header>

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

        <h2 class="section-title"><span>🗺️ Concursos e Vagas por Estado (Brasil)</span></h2>
        <div class="states-grid">
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
    <style>
        :root { 
            --primary: #2563eb; --primary-dark: #1d4ed8; --bg-color: #f8fafc; 
            --card-bg: #ffffff; --text: #0f172a; --text-light: #64748b; 
            --header-bg: linear-gradient(135deg, #0f172a, #1e3a8a); --border-color: #e2e8f0;
        }
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 0; width: 100%; }
        .navbar { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 12px 20px; position: sticky; top: 0; z-index: 1000; width: 100%; }
        .nav-container { max-width: 1050px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; width: 100%; }
        .back-link { color: var(--primary); text-decoration: none; font-weight: 600; font-size: 14px; }
        .container { max-width: 1050px; margin: 30px auto; padding: 0 20px; width: 100%; }
        header { background: var(--header-bg); color: white; padding: 40px; border-radius: 16px; margin-bottom: 30px; width: 100%; }
        header h1 { margin: 0 0 10px 0; font-size: 30px; font-weight: 800; }
        .section-title { font-size: 22px; font-weight: 700; margin: 40px 0 20px 0; border-left: 5px solid var(--primary); padding-left: 12px; width: 100%; }
        
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
        footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border-color); padding-top: 20px; width: 100%; }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="nav-container">
            <a href="index.html" class="back-link">← Voltar ao Início</a>
        </div>
    </div>
    <div class="container">
        {{ ad_banner | safe }}
        <header>
            <h1>Oportunidades em {{ estado.name }}</h1>
            <p>Painel dedicado com editais abertos e vagas de emprego regionais em {{ estado.name }}.</p>
        </header>
        
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
</body>
</html>
"""

def buscar_noticias_brasil():
    fontes = {
        "Concursos Públicos": {
            "id": "concursos", "color": "#2563eb",
            "urls": ["https://s2.glbimg.com/rss/g1/educacao/concursos-e-emprego/"]
        },
        "Vagas CLT & Empresas": {
            "id": "empregos", "color": "#059669",
            "urls": ["https://s2.glbimg.com/rss/g1/economia/", "https://www.infomoney.com.br/feed/"]
        },
        "Trabalho Home Office": {
            "id": "homeoffice", "color": "#ea580c",
            "urls": ["https://s2.glbimg.com/rss/g1/tecnologia/"]
        }
    }
    
    tstamp = int(datetime.now().timestamp())
    imagens = [
        f"https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=60&v={tstamp}",
        f"https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60&v={tstamp}",
        f"https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&auto=format&fit=crop&q=60&v={tstamp}"
    ]

    categorias_processadas, todas_noticias = {}, []
    
    for cat_nome, info in fontes.items():
        items_cat = []
        for url in info["urls"]:
            try:
                resp = requests.get(url, verify=False, timeout=5)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    for item in root.findall('.//item')[:3]:
                        tit = item.find('title').text if item.find('title') is not None else ""
                        lnk = item.find('link').text if item.find('link') is not None else "https://news.google.com"
                        dsc = item.find('description').text if item.find('description') is not None else ""
                        if not tit: continue
                        if "<" in dsc: dsc = re.sub('<.*?>', '', dsc)
                        
                        obj = {
                            "category": cat_nome, "color": info["color"],
                            "title": tit.strip(), "link": lnk.strip(), "image": random.choice(imagens),
                            "description": dsc.strip()[:140] + "..." if len(dsc.strip()) > 140 else dsc.strip()
                        }
                        items_cat.append(obj)
                        todas_noticias.append(obj)
            except: pass
            
        while len(items_cat) < 3:
            obj = {
                "category": cat_nome, "color": info["color"],
                "title": f"Oportunidade Verificada em {cat_nome}", "link": f"#{info['id']}",
                "image": random.choice(imagens), "description": "Confira os detalhes desta oportunidade com inscrições abertas."
            }
            items_cat.append(obj)
            todas_noticias.append(obj)
            
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:3]}
        
    return categorias_processadas, todas_noticias

def gerar_sitemap(lista_estados):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMINIO_SITE}/index.html</loc><lastmod>{data_hoje}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>')
    for e in lista_estados:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{e["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write("\n".join(xml))

def gerar_site():
    print("Gerando novo portal do zero...")
    estados_brasil = [
        {"name": "São Paulo (SP)", "file": "sao-paulo.html"},
        {"name": "Rio de Janeiro (RJ)", "file": "rio-de-janeiro.html"},
        {"name": "Minas Gerais (MG)", "file": "minas-gerais.html"},
        {"name": "Bahia (BA)", "file": "bahia.html"},
        {"name": "Paraná (PR)", "file": "parana.html"}
    ]
    
    categorias_dict, todas_noticias = buscar_noticias_brasil()
    template_estado = Template(ESTADO_TEMPLATE)
    lista_estados_gerados = []
    
    for est in estados_brasil:
        random.shuffle(todas_noticias)
        noticias_est = todas_noticias[:3]
        with open(est["file"], "w", encoding="utf-8") as f:
            f.write(template_estado.render(
                estado=est, noticias=noticias_est,
                ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE
            ))
        lista_estados_gerados.append(est)
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=lista_estados_gerados, categorias=categorias_dict,
            ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE
        ))
        
    gerar_sitemap(lista_estados_gerados)
    print("Sucesso absoluto! Portal refeito do zero limpo e alinhado.")

if __name__ == "__main__":
    gerar_site()

