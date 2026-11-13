import os
import requests
import xml.etree.ElementTree as ET
from jinja2 import Template
import urllib3
from datetime import datetime
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DOMINIO_SITE = "https://guia-dados-globais.lkliima1950.workers.dev"

AD_BANNER = """
<div style="text-align:center; margin: 25px 0; background:var(--card-bg); padding:15px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px dashed #ccc;">
    <p style="color:#888; font-size:11px; margin-bottom:5px; text-transform: uppercase; letter-spacing: 1px;">Publicidade</p>
    <!-- COLE SEU CÓDIGO DA ADSTERRA / ADSENSE AQUI -->
    <div style="color:var(--text-light); font-size:13px; font-weight: bold;">[ Espaço para Anúncio - Banner Responsivo ]</div>
</div>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ country.name }} - Portal de Notícias e Dados Globais</title>
    <meta name="description" content="Acompanhe as últimas manchetes, estatísticas completas, fuso horário e economia de {{ country.name }}.">
    
    <meta property="og:type" content="article">
    <meta property="og:title" content="{{ country.name }} - Portal de Notícias e Dados">
    <meta property="og:description" content="Veja capital, população, moeda, fuso horário e cobertura em tempo real sobre {{ country.name }}.">
    <meta property="og:url" content="{{ dominio }}/{{ country.file }}">

    <style>
        :root { --primary: #2563eb; --bg-color: #f3f4f6; --card-bg: #ffffff; --text: #1f2937; --text-light: #4b5563; --header-bg: linear-gradient(135deg, #1e3a8a, #2563eb); }
        [data-theme="dark"] { --primary: #3b82f6; --bg-color: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --text-light: #94a3b8; --header-bg: linear-gradient(135deg, #090d16, #1e3a8a); }
        
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 20px; transition: background 0.3s, color 0.3s; }
        .container { max-width: 900px; margin: 0 auto; }
        
        .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .theme-btn { background: var(--card-bg); color: var(--text); border: 1px solid #ccc; padding: 8px 14px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 13px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        
        header { background: var(--header-bg); color: white; padding: 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        header h1 { margin: 0 0 10px 0; font-size: 28px; }
        header p { margin: 0; opacity: 0.9; font-size: 15px; }
        
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-card { background: var(--card-bg); padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .stat-card .label { font-size: 13px; color: var(--text-light); text-transform: uppercase; font-weight: bold; }
        .stat-card .value { font-size: 18px; color: var(--primary); font-weight: bold; margin-top: 5px; }
        
        .section-title { font-size: 20px; margin: 30px 0 15px 0; border-left: 4px solid var(--primary); padding-left: 10px; }
        .news-grid { display: grid; grid-template-columns: 1fr; gap: 15px; }
        .news-card { background: var(--card-bg); padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s; }
        .news-card:hover { transform: translateY(-3px); }
        .badge { display: inline-block; padding: 3px 10px; font-size: 11px; font-weight: bold; border-radius: 20px; text-transform: uppercase; margin-bottom: 8px; color: white; }
        .news-card h3 { margin: 0 0 8px 0; font-size: 17px; }
        .news-card h3 a { color: var(--text); text-decoration: none; }
        .news-card h3 a:hover { color: var(--primary); text-decoration: underline; }
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
            <p>Painel informativo oficial com dados populacionais, fuso horário e cobertura global em tempo real.</p>
        </header>

        <div class="grid-stats">
            <div class="stat-card">
                <div class="label">Capital</div>
                <div class="value">{{ country.capital }}</div>
            </div>
            <div class="stat-card">
                <div class="label">Região / Sub-região</div>
                <div class="value">{{ country.region }}</div>
            </div>
            <div class="stat-card">
                <div class="label">População</div>
                <div class="value">{{ country.population }} hab.</div>
            </div>
            <div class="stat-card">
                <div class="label">Moeda</div>
                <div class="value">{{ country.currency }}</div>
            </div>
            <div class="stat-card">
                <div class="label">Fuso Horário</div>
                <div class="value">{{ country.timezone }}</div>
            </div>
            <div class="stat-card">
                <div class="label">Idioma Principal</div>
                <div class="value">{{ country.language }}</div>
            </div>
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
            <p>© 2026 Portal Global de Notícias e Dados. Todos os direitos reservados.</p>
        </footer>
    </div>

    <script>
        function toggleTheme() {
            const body = document.body;
            if (body.getAttribute('data-theme') === 'light') {
                body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                body.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        }
        if (localStorage.getItem('theme') === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
        }
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
    <title>Portal Global - Mundo, Tecnologia, Economia e Esportes</title>
    <meta name="description" content="Seu portal completo de notícias internacionais divididas por categorias, estatísticas de mais de 190 países e atualizações em tempo real.">
    
    <meta property="og:type" content="website">
    <meta property="og:title" content="Portal Global - Notícias, Países e Atualizações">
    <meta property="og:description" content="Explore estatísticas de centenas de nações e acompanhe manchetes internacionais.">
    <meta property="og:url" content="{{ dominio }}/index.html">

    <style>
        :root { --primary: #2563eb; --bg-color: #f3f4f6; --card-bg: #ffffff; --text: #1f2937; --text-light: #4b5563; --header-bg: linear-gradient(135deg, #1e3a8a, #2563eb); }
        [data-theme="dark"] { --primary: #3b82f6; --bg-color: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --text-light: #94a3b8; --header-bg: linear-gradient(135deg, #090d16, #1e3a8a); }

        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: var(--text); background: var(--bg-color); margin: 0; padding: 20px; transition: background 0.3s, color 0.3s; }
        .container { max-width: 900px; margin: 0 auto; }
        
        .top-bar { display: flex; justify-content: flex-end; align-items: center; margin-bottom: 15px; }
        .theme-btn { background: var(--card-bg); color: var(--text); border: 1px solid #ccc; padding: 8px 14px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 13px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

        header { background: var(--header-bg); color: white; padding: 40px 30px; border-radius: 12px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        header h1 { margin: 0 0 10px 0; font-size: 32px; }
        header p { margin: 0; opacity: 0.9; font-size: 16px; }
        
        .search-box { width: 100%; max-width: 500px; margin: 20px auto 0 auto; display: block; padding: 12px 20px; font-size: 16px; border-radius: 30px; border: 1px solid #ccc; outline: none; background: var(--card-bg); color: var(--text); box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

        .nav-cats { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 25px 0; }
        .nav-cats a { background: var(--card-bg); color: var(--text); padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 14px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: all 0.2s; }
        .nav-cats a:hover { background: var(--primary); color: white; }
        
        .section-title { font-size: 22px; margin: 35px 0 15px 0; border-left: 5px solid var(--primary); padding-left: 12px; }
        
        .countries-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .country-card { background: var(--card-bg); padding: 18px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-decoration: none; color: var(--text); display: block; transition: transform 0.2s, border-color 0.2s; border: 1px solid transparent; }
        .country-card:hover { transform: translateY(-3px); border-color: var(--primary); }
        .country-card h3 { margin: 0 0 5px 0; color: var(--primary); font-size: 18px; }
        .country-card p { margin: 0; font-size: 13px; color: var(--text-light); }
        
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 15px; }
        .news-card { background: var(--card-bg); padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; }
        .badge { display: inline-block; align-self: flex-start; padding: 3px 10px; font-size: 11px; font-weight: bold; border-radius: 20px; text-transform: uppercase; margin-bottom: 10px; color: white; }
        .news-card h3 { margin: 0 0 8px 0; font-size: 17px; }
        .news-card h3 a { color: var(--text); text-decoration: none; }
        .news-card h3 a:hover { color: var(--primary); text-decoration: underline; }
        .news-card p { margin: 0; font-size: 14px; color: var(--text-light); }
        
        footer { text-align: center; margin-top: 40px; font-size: 13px; color: var(--text-light); padding: 20px 0; border-top: 1px solid var(--card-bg); }
    </style>
</head>
<body data-theme="light">
    <div class="container">
        <div class="top-bar">
            <button class="theme-btn" onclick="toggleTheme()">🌓 Alternar Tema</button>
        </div>

        {{ ad_banner | safe }}
        
        <header>
            <h1>Portal Global de Notícias & Dados</h1>
            <p>Cobertura em tempo real por categorias e estatísticas detalhadas de nações do mundo inteiro.</p>
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar país no portal..." onkeyup="filtrarPaises()">
        </header>

        <div class="nav-cats">
            <a href="#mundo">🌍 Mundo</a>
            <a href="#tecnologia">💻 Tecnologia</a>
            <a href="#economia">📈 Economia</a>
            <a href="#esportes">⚽ Esportes</a>
            <a href="#paises">🗺️ Países</a>
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
        {% if loop.index == 2 %}
            {{ ad_banner | safe }}
        {% endif %}
        {% endfor %}

        {{ ad_banner | safe }}

        <h2 id="paises" class="section-title">Explorar Países e Dados (Global)</h2>
        <div class="countries-grid" id="countriesGrid">
            {% for p in paises %}
            <a href="{{ p.file }}" class="country-card">
                <h3>{{ p.name }}</h3>
                <p>Ver estatísticas e notícias →</p>
            </a>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}

        <footer>
            <p>© 2026 Portal Global. Todos os direitos reservados.</p>
        </footer>
    </div>

    <script>
        function toggleTheme() {
            const body = document.body;
            if (body.getAttribute('data-theme') === 'light') {
                body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                body.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        }
        if (localStorage.getItem('theme') === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
        }

        function filtrarPaises() {
            let input = document.getElementById('searchInput').value.toLowerCase();
            let grid = document.getElementById('countriesGrid');
            let cards = grid.getElementsByClassName('country-card');

            for (let i = 0; i < cards.length; i++) {
                let title = cards[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
                if (title.includes(input)) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
        }
    </script>
</body>
</html>
"""

def buscar_noticias_por_categoria():
    fontes = {
        "Mundo": {
            "id": "mundo", "color": "#2563eb",
            "url": "https://g1.globo.com/rss/g1/mundo/",
            "fallbacks": [
                {"title": "Cúpula internacional debate novos acordos globais de comércio", "link": "#", "description": "Líderes mundiais definem diretrizes econômicas para o próximo ciclo."},
                {"title": "Missões diplomáticas reforçam cooperações multilaterais", "link": "#", "description": "Encontros estratégicos buscam estabilidade geopolítica regional."}
            ]
        },
        "Tecnologia": {
            "id": "tecnologia", "color": "#7c3aed",
            "url": "https://g1.globo.com/rss/g1/tecnologia/",
            "fallbacks": [
                {"title": "Inovações em inteligência artificial transformam ecossistemas web", "link": "#", "description": "Novas ferramentas otimizam portais automatizados e indexação."},
                {"title": "Avanços em infraestrutura de rede prometem maior velocidade global", "link": "#", "description": "Especialistas avaliam impacto das novas tecnologias de conectividade."}
            ]
        },
        "Economia": {
            "id": "economia", "color": "#059669",
            "url": "https://g1.globo.com/rss/g1/economia/",
            "fallback": [{"title": "Mercados globais operam com foco em indicadores fiscais", "link": "#", "description": "Investidores acompanham taxas de câmbio e inflação."}]
        },
        "Esportes": {
            "id": "esportes", "color": "#dc2626",
            "url": "https://ge.globo.com/rss/ge/",
            "fallback": [{"title": "Competições internacionais movimentam o calendário esportivo", "link": "#", "description": "Confira os resultados e análises das principais disputas."}]
        }
    }

    categorias_processadas = {}
    todas_noticias = []

    for cat_nome, info in fontes.items():
        items_cat = []
        try:
            resp = requests.get(info["url"], verify=False, timeout=6)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for item in root.findall('.//item')[:4]:
                    title = item.find('title').text if item.find('title') is not None else "Atualização"
                    link = item.find('link').text if item.find('link') is not None else "#"
                    noticia_obj = {
                        "category": cat_nome, "color": info["color"],
                        "title": title, "link": link,
                        "description": f"Cobertura especial da editoria de {cat_nome} em tempo real."
                    }
                    items_cat.append(noticia_obj)
                    todas_noticias.append(noticia_obj)
        except:
            pass

        # Rotação dinâmica e Fallback inteligente caso o RSS falhe
        if not items_cat:
            fb_list = info.get("fallbacks", info.get("fallback", []))
            for fb in fb_list:
                fb_obj = {"category": cat_nome, "color": info["color"], "title": fb["title"], "link": fb["link"], "description": fb["description"]}
                items_cat.append(fb_obj)
                todas_noticias.append(fb_obj)

        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat}

    return categorias_processadas, todas_noticias

def baixar_paises():
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url, verify=False, timeout=15)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return [
        {"name": {"common": "Brasil"}, "capital": ["Brasília"], "region": "Americas", "population": 212000000, "currencies": {"BRL": {"name": "Real"}}, "timezones": ["UTC-3"], "languages": {"por": "Português"}}
    ]

def gerar_sitemap(lista_paises, output_dir):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    xml_content.append('  <url>')
    xml_content.append(f'    <loc>{DOMINIO_SITE}/index.html</loc>')
    xml_content.append(f'    <lastmod>{data_hoje}</lastmod>')
    xml_content.append('    <changefreq>hourly</changefreq>')
    xml_content.append('    <priority>1.0</priority>')
    xml_content.append('  </url>')

    for p in lista_paises:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{DOMINIO_SITE}/{p["file"]}</loc>')
        xml_content.append(f'    <lastmod>{data_hoje}</lastmod>')
        xml_content.append('    <changefreq>daily</changefreq>')
        xml_content.append('    <priority>0.8</priority>')
        xml_content.append('  </url>')

    xml_content.append('</urlset>')
    
    sitemap_path = os.path.join(output_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    print("Sitemap global atualizado com sucesso!")

def gerar_site():
    print("Iniciando geração inteligente do portal global...")
    paises = baixar_paises()
    categorias_dict, todas_noticias = buscar_noticias_por_categoria()
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    template = Template(HTML_TEMPLATE)
    lista_paises = []

    for item in paises:
        try:
            name = item.get('name', {}).get('common', 'Desconhecido')
            capital = item.get('capital', ['N/A'])[0]
            region = item.get('region', 'N/A')
            subregion = item.get('subregion', '')
            if subregion:
                region = f"{region} ({subregion})"
            
            population = f"{item.get('population', 0):,}".replace(',', '.')
            currencies = item.get('currencies', {})
            currency_name = list(currencies.values())[0]['name'] if currencies else 'N/A'
            
            timezones = item.get('timezones', ['UTC'])
            timezone_str = ", ".join(timezones)
            
            languages = item.get('languages', {})
            lang_name = list(languages.values())[0] if languages else 'N/A'

            file_name = name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '') + ".html"
            
            country_data = {
                "name": name, "capital": capital, "region": region,
                "population": population, "currency": currency_name, 
                "timezone": timezone_str, "language": lang_name,
                "file": file_name
            }

            # Embaralha levemente as notícias para rotação dinâmica por país
            noticias_pais = list(todas_noticias)
            random.shuffle(noticias_pais)

            with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
                f.write(template.render(country=country_data, noticias=noticias_pais[:8], ad_banner=AD_BANNER, dominio=DOMINIO_SITE))
            
            lista_paises.append({"name": name, "file": file_name})
        except:
            continue

    index_template = Template(INDEX_TEMPLATE)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_template.render(paises=lista_paises, categorias=categorias_dict, ad_banner=AD_BANNER, dominio=DOMINIO_SITE))

    gerar_sitemap(lista_paises, output_dir)
    print(f"Sucesso! {len(lista_paises)} países gerados com dados enriquecidos, rotação e sitemap.")

if __name__ == "__main__":
    gerar_site()
