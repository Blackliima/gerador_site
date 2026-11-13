import os
import requests
import xml.etree.ElementTree as ET
from jinja2 import Template
import urllib3
from datetime import datetime
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOMINIO_SITE = "https://gerador-site.pages.dev"
MONETAG_META = '<meta name="monetag" content="60579baab4bd2ab620a4e0fdf532170a">'

AD_BANNER = """
<div style="text-align:center; margin: 25px 0; background:var(--card-bg); padding:15px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px dashed #ccc;">
    <p style="color:#888; font-size:11px; margin-bottom:5px; text-transform: uppercase; letter-spacing: 1px;">Publicidade</p>
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

LICENCA_RODAPE = """
<div style="font-size: 12px; color: var(--text-light); line-height: 1.5; margin-top: 20px; padding: 15px; background: var(--card-bg); border-radius: 8px; border: 1px solid rgba(0,0,0,0.05);">
    <p style="margin: 0 0 8px 0;"><strong>Licença e Termos de Uso:</strong> Este portal consolida dados públicos globais e notícias em tempo real para fins informativos. O conteúdo de notícias é distribuído através de feeds RSS públicos de parceiros de mídia, respeitando os direitos de autoria e direcionando os leitores às fontes originais.</p>
    <p style="margin: 0;">© 2026 Portal Global de Notícias & Dados. Todos os direitos reservados. Licenciado sob Creative Commons Atribuição 4.0 Internacional.</p>
</div>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ monetag_meta | safe }}
    <title>{{ country.name }} - Portal de Notícias e Dados Globais</title>
    <meta name="description" content="Acompanhe as últimas manchetes e estatísticas de {{ country.name }}.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>">
    <style>
        :root { --primary: #2563eb; --bg-color: #f3f4f6; --card-bg: #ffffff; --text: #1f2937; --text-light: #4b5563; --header-bg: linear-gradient(135deg, #1e3a8a, #2563eb); }
        [data-theme="dark"] { --primary: #3b82f6; --bg-color: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --text-light: #94a3b8; --header-bg: linear-gradient(135deg, #090d16, #1e3a8a); }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 20px; transition: background 0.3s, color 0.3s; }
        .container { max-width: 900px; margin: 0 auto; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .theme-btn { background: var(--card-bg); color: var(--text); border: 1px solid #ccc; padding: 8px 14px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 13px; }
        header { background: var(--header-bg); color: white; padding: 30px; border-radius: 12px; margin-bottom: 25px; }
        header h1 { margin: 0 0 10px 0; font-size: 28px; }
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-card { background: var(--card-bg); padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .stat-card .label { font-size: 13px; color: var(--text-light); text-transform: uppercase; font-weight: bold; }
        .stat-card .value { font-size: 18px; color: var(--primary); font-weight: bold; margin-top: 5px; }
        .section-title { font-size: 20px; margin: 30px 0 15px 0; border-left: 4px solid var(--primary); padding-left: 10px; }
        .news-grid { display: grid; grid-template-columns: 1fr; gap: 15px; }
        .news-card { background: var(--card-bg); padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .badge { display: inline-block; padding: 3px 10px; font-size: 11px; font-weight: bold; border-radius: 20px; text-transform: uppercase; margin-bottom: 8px; color: white; }
        .news-card h3 { margin: 0 0 8px 0; font-size: 17px; }
        .news-card h3 a { color: var(--text); text-decoration: none; }
        .news-card p { margin: 0; font-size: 14px; color: var(--text-light); }
        .back-link { display: inline-block; margin-top: 30px; color: var(--primary); text-decoration: none; font-weight: bold; }
        footer { text-align: center; margin-top: 40px; font-size: 13px; color: var(--text-light); padding: 20px 0; border-top: 1px solid var(--card-bg); }
    </style>
</head>
<body data-theme="light">
    <div class="container">
        <div class="top-bar">
            <a href="index.html" class="back-link" style="margin:0;">← Voltar para a Página Inicial</a>
            <button class="theme-btn" onclick="toggleTheme()">🌓 Alternar Tema</button>
        </div>
        {{ ad_banner | safe }}
        <header>
            <h1>{{ country.name }}</h1>
            <p>Painel informativo oficial com dados populacionais, fuso horário e cobertura global.</p>
        </header>
        <div class="grid-stats">
            <div class="stat-card"><div class="label">Capital</div><div class="value">{{ country.capital }}</div></div>
            <div class="stat-card"><div class="label">Região</div><div class="value">{{ country.region }}</div></div>
            <div class="stat-card"><div class="label">População</div><div class="value">{{ country.population }} hab.</div></div>
            <div class="stat-card"><div class="label">Moeda</div><div class="value">{{ country.currency }}</div></div>
            <div class="stat-card"><div class="label">Fuso Horário</div><div class="value">{{ country.timezone }}</div></div>
            <div class="stat-card"><div class="label">Idioma</div><div class="value">{{ country.language }}</div></div>
        </div>
        {{ ad_banner | safe }}
        <h2 class="section-title">Cobertura Global e Internacional</h2>
        <div class="news-grid">
            {% for noticia in noticias %}
            <div class="news-card">
                <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                <p>{{ noticia.description }}</p>
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
            body.setAttribute('data-theme', body.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
            localStorage.setItem('theme', body.getAttribute('data-theme'));
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
    {{ monetag_meta | safe }}
    <title>Portal Global - Notícias, Tecnologia, Economia e Esportes</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>">
    <style>
        :root { --primary: #2563eb; --bg-color: #f3f4f6; --card-bg: #ffffff; --text: #1f2937; --text-light: #4b5563; --header-bg: linear-gradient(135deg, #1e3a8a, #2563eb); }
        [data-theme="dark"] { --primary: #3b82f6; --bg-color: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --text-light: #94a3b8; --header-bg: linear-gradient(135deg, #090d16, #1e3a8a); }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 20px; transition: background 0.3s, color 0.3s; }
        .container { max-width: 900px; margin: 0 auto; }
        .top-bar { display: flex; justify-content: flex-end; align-items: center; margin-bottom: 15px; }
        .theme-btn { background: var(--card-bg); color: var(--text); border: 1px solid #ccc; padding: 8px 14px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 13px; }
        header { background: var(--header-bg); color: white; padding: 40px 30px; border-radius: 12px; margin-bottom: 20px; text-align: center; }
        header h1 { margin: 0 0 10px 0; font-size: 32px; }
        .search-box { width: 100%; max-width: 500px; margin: 20px auto 0 auto; display: block; padding: 12px 20px; font-size: 16px; border-radius: 30px; border: 1px solid #ccc; outline: none; background: var(--card-bg); color: var(--text); }
        .nav-cats { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 25px 0; }
        .nav-cats a { background: var(--card-bg); color: var(--text); padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 14px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .nav-cats a:hover { background: var(--primary); color: white; }
        .section-title { font-size: 22px; margin: 35px 0 15px 0; border-left: 5px solid var(--primary); padding-left: 12px; }
        .countries-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .country-card { background: var(--card-bg); padding: 18px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-decoration: none; color: var(--text); display: block; border: 1px solid transparent; }
        .country-card:hover { border-color: var(--primary); }
        .country-card h3 { margin: 0 0 5px 0; color: var(--primary); font-size: 18px; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 15px; }
        .news-card { background: var(--card-bg); padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; }
        .badge { display: inline-block; align-self: flex-start; padding: 3px 10px; font-size: 11px; font-weight: bold; border-radius: 20px; text-transform: uppercase; margin-bottom: 10px; color: white; }
        .news-card h3 { margin: 0 0 8px 0; font-size: 17px; }
        .news-card h3 a { color: var(--text); text-decoration: none; }
        footer { text-align: center; margin-top: 40px; font-size: 13px; color: var(--text-light); padding: 20px 0; border-top: 1px solid var(--card-bg); }
    </style>
</head>
<body data-theme="light">
    <div class="container">
        <div class="top-bar"><button class="theme-btn" onclick="toggleTheme()">🌓 Alternار Tema</button></div>
        {{ ad_banner | safe }}
        <header>
            <h1>Portal Global de Notícias & Dados</h1>
            <p>Cobertura em tempo real e estatísticas detalhadas de nações do mundo inteiro.</p>
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar país..." onkeyup="filtrarPaises()">
        </header>
        <div class="nav-cats">
            <a href="#mundo">🌍 Mundo</a><a href="#tecnologia">💻 Tecnologia</a><a href="#economia">📈 Economia</a><a href="#esportes">⚽ Esportes</a><a href="#paises">🗺️ Países</a>
        </div>
        {% for cat_nome, cat_data in categorias.items() %}
        <h2 id="{{ cat_data.id }}" class="section-title" style="border-color: {{ cat_data.color }};">{{ cat_nome }}</h2>
        <div class="news-grid">
            {% for noticia in cat_data.lista %}
            <div class="news-card">
                <div>
                    <span class="badge" style="background-color: {{ cat_data.color }};">{{ cat_nome }}</span>
                    <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                </div>
                <p>{{ noticia.description }}</p>
            </div>
            {% endfor %}
        </div>
        {% if loop.index == 2 %}{{ ad_banner | safe }}{% endif %}
        {% endfor %}
        {{ ad_banner | safe }}
        <h2 id="paises" class="section-title">Explorar Países e Dados (Global)</h2>
        <div class="countries-grid" id="countriesGrid">
            {% for p in paises %}
            <a href="{{ p.file }}" class="country-card">
                <h3>{{ p.name }}</h3>
                <p>Ver estatísticas →</p>
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
            body.setAttribute('data-theme', body.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
            localStorage.setItem('theme', body.getAttribute('data-theme'));
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

def buscar_noticias_por_categoria():
    fontes = {
        "Mundo": {"id": "mundo", "color": "#2563eb", "url": "https://g1.globo.com/rss/g1/mundo/"},
        "Tecnologia": {"id": "tecnologia", "color": "#7c3aed", "url": "https://g1.globo.com/rss/g1/tecnologia/"},
        "Economia": {"id": "economia", "color": "#059669", "url": "https://g1.globo.com/rss/g1/economia/"},
        "Esportes": {"id": "esportes", "color": "#dc2626", "url": "https://ge.globo.com/rss/ge/"}
    }
    categorias_processadas, todas_noticias = {}, []
    for cat_nome, info in fontes.items():
        items_cat = []
        try:
            resp = requests.get(info["url"], verify=False, timeout=6)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for item in root.findall('.//item')[:4]:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    desc_elem = item.find('description')
                    
                    titulo = title_elem.text if title_elem is not None and title_elem.text else f"Últimas notícias de {cat_nome}"
                    link = link_elem.text if link_elem is not None and link_elem.text else f"https://ge.globo.com" if cat_nome == "Esportes" else "https://g1.globo.com"
                    desc = desc_elem.text if desc_elem is not None and desc_elem.text else f"Acompanhe as principais atualizações e coberturas da editoria de {cat_nome}."
                    
                    # Limpeza simples de tags HTML no resumo se houver
                    if "<" in desc:
                        import re
                        desc = re.sub('<.*?>', '', desc)

                    noticia_obj = {
                        "category": cat_nome, "color": info["color"],
                        "title": titulo,
                        "link": link,
                        "description": desc[:150] + "..." if len(desc) > 150 else desc
                    }
                    items_cat.append(noticia_obj)
                    todas_noticias.append(noticia_obj)
        except: pass
        
        if not items_cat:
            fallback_link = "https://ge.globo.com" if cat_nome == "Esportes" else "https://g1.globo.com"
            items_cat.append({
                "category": cat_nome, "color": info["color"], 
                "title": f"Cobertura especial de {cat_nome} em tempo real", 
                "link": fallback_link, 
                "description": f"Clique para acessar a cobertura completa e atualizada da editoria de {cat_nome}."
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
    for p in lista_paises:
        xml_content.append(f'  <url><loc>{DOMINIO_SITE}/{p["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    xml_content.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write("\n".join(xml_content))

def gerar_site():
    print("Iniciando geração com correção de links e notícias...")
    paises = baixar_paises()
    categorias_dict, todas_noticias = buscar_noticias_por_categoria()
    
    template = Template(HTML_TEMPLATE)
    lista_paises = []
    for item in paises:
        try:
            name = item.get('name', {}).get('common', 'Desconhecido')
            file_name = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '') + ".html"
            country_data = {
                "name": name, "capital": item.get('capital', ['N/A'])[0],
                "region": item.get('region', 'N/A'), "population": f"{item.get('population', 0):,}".replace(',', '.'),
                "currency": list(item.get('currencies', {}).values())[0]['name'] if item.get('currencies') else 'N/A',
                "timezone": ", ".join(item.get('timezones', ['UTC'])) if isinstance(item.get('timezones'), list) else str(item.get('timezones', 'UTC')),
                "language": list(item.get('languages', {}).values())[0] if item.get('languages') else 'N/A',
                "file": file_name
            }
            noticias_pais = list(todas_noticias)
            random.shuffle(noticias_pais)
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(template.render(country=country_data, noticias=noticias_pais[:8], ad_banner=AD_BANNER, monetag_meta=MONETAG_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE))
            lista_paises.append({"name": name, "file": file_name})
        except: continue

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(paises=lista_paises, categorias=categorias_dict, ad_banner=AD_BANNER, monetag_meta=MONETAG_META, licenca_rodape=LICENCA_RODAPE, dominio=DOMINIO_SITE))
    
    gerar_sitemap(lista_paises)
    print(f"Sucesso! {len(lista_paises)} países gerados com notícias corrigidas.")

if __name__ == "__main__":
    gerar_site()
