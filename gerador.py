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
    <span style="background: white; color: #ea580c; padding: 4px 10px; border-radius: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; flex-shrink: 0;">🔥 ALERTA DE VAGA</span>
    <div style="overflow: hidden; white-space: nowrap; width: 100%;">
        <div style="display: inline-block; animation: scrollTicker 25s linear infinite;">
            ⚠️ Órgãos públicos e grandes empresas liberam novos editais com inscrições abertas nesta semana    |    💻 Oportunidades para trabalhar de casa sem experiência exigida    |    📄 Clique na vaga desejada e veja o passo a passo para se candidatar de graça.
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
    <title>Oportunidade e Vagas de Emprego - Concursos, CLT e Home Office</title>
    <meta name="description" content="Encontre vagas de emprego CLT, editais de concursos públicos abertos e oportunidades de trabalho em sua cidade e estado. Acesse já!">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 40px 20px; text-align: center; }
        .header-top h1 { margin: 0 0 10px 0; font-size: 30px; font-weight: 800; }
        .header-top p { margin: 0 0 20px 0; opacity: 0.9; font-size: 15px; }
        .search-box { width: 100%; max-width: 450px; margin: 0 auto 20px auto; display: block; padding: 14px 20px; font-size: 14px; border-radius: 30px; border: none; outline: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        
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
        
        footer { text-align: center; padding: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 50px; }
    </style>
</head>
<body>
    {{ ticker_cotacoes | safe }}
    <div class="header-top">
        <h1>Oportunidade e Vagas de Emprego</h1>
        <p>Encontre sua vaga CLT, Concurso Público ou Trabalho Remoto por Estado e Cidade</p>
        <input type="text" id="searchInput" class="search-box" placeholder="🔍 Pesquisar estado na barra acima..." onkeyup="filtrarEstados()">
    </div>

    <div class="states-top-bar">
        <p>📍 Selecione seu Estado para ver Vagas nas Principais Cidades:</p>
        <div class="states-box" id="statesGrid">
            {% for e in estados %}
            <a href="{{ e.file }}" class="state-pill">{{ e.name }}</a>
            {% endfor %}
        </div>
    </div>

    <div class="main-container">
        {{ breaking_news_ticker | safe }}
        {{ ad_banner | safe }}

        {% for cat_nome, cat_data in categorias.items() %}
        <div class="section-title">{{ cat_nome }}</div>
        <div class="cards-wrapper">
            {% for noticia in cat_data.lista %}
            <div class="card">
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
        {% endfor %}

        {{ ad_banner | safe }}

        <footer>
            <p>© 2026 Oportunidade e Vagas de Emprego. Portal independente de divulgação de oportunidades para o trabalhador brasileiro.</p>
        </footer>
    </div>
    <script>
        function filtrarEstados() {
            let input = document.getElementById('searchInput').value.toLowerCase();
            let cards = document.getElementById('statesGrid').getElementsByClassName('state-pill');
            for (let i = 0; i < cards.length; i++) {
                let text = cards[i].innerText.toLowerCase();
                cards[i].style.display = text.includes(input) ? "" : "none";
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
    <link rel="canonical" href="{{ dominio }}/{{ estado.file }}">
    <title>Vagas em {{ estado.name }} e Principais Cidades - Oportunidade e Vagas</title>
    <meta name="description" content="Confira vagas de emprego, concursos e oportunidades abertas em {{ estado.name }} e nas cidades de destaque.">
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

        /* SEÇÃO DE CIDADES EM DESTAQUE */
        .cities-section { background: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; margin: 30px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .cities-section h3 { margin: 0 0 10px 0; color: #1e3a8a; font-size: 16px; }
        .cities-section p { font-size: 13px; color: #64748b; margin: 0 0 15px 0; }
        .cities-grid { display: flex; flex-wrap: wrap; gap: 10px; }
        .city-badge { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; text-decoration: none; }
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
        <p>Acompanhe vagas abertas em destaque na região e municípios parceiros</p>
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
        <!-- BLOCO DE CIDADES EM DESTAQUE -->
        <div class="cities-section">
            <h3>🏙️ Principais Cidades com Vagas em {{ estado.name }}</h3>
            <p>Clique em uma cidade para filtrar as oportunidades locais e processos seletivos abertos:</p>
            <div class="cities-grid">
                {% for cidade in estado.cities %}
                <span class="city-badge">📌 {{ cidade }}</span>
                {% endfor %}
            </div>
        </div>

        {{ ad_banner | safe }}

        <div class="section-title">Vagas e Processos Seletivos em Destaque — {{ estado.name }}</div>
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
            "urls": ["https://s2.glbimg.com/rss/g1/educacao/concursos-e-emprego/"],
            "diretorios": ["https://www.in.gov.br", "https://www.qconcursos.com", "https://www.estrategiaconcursos.com.br"]
        },
        "Vagas CLT & Empresas": {
            "id": "empregos", "color": "#059669",
            "urls": ["https://s2.glbimg.com/rss/g1/economia/"],
            "diretorios": ["https://www.infojobs.com.br", "https://www.catho.com.br", "https://www.indeed.com.br", "https://www.linkedin.com/jobs"]
        },
        "Trabalho Home Office": {
            "id": "homeoffice", "color": "#ea580c",
            "urls": ["https://s2.glbimg.com/rss/g1/tecnologia/"],
            "diretorios": ["https://www.infojobs.com.br/vagas-de-emprego-home-office.aspx", "https://www.workana.com/pt", "https://www.getremote.co"]
        }
    }
    
    tstamp = int(datetime.now().timestamp())
    imagens_cat = {
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
        ]
    }

    categorias_processadas = {}
    
    for cat_nome, info in fontes.items():
        items_cat = []
        imgs = list(imagens_cat[cat_nome])
        random.shuffle(imgs)
        
        for url in info["urls"]:
            try:
                resp = requests.get(url, verify=False, timeout=5)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    for idx, item in enumerate(root.findall('.//item')[:5]):
                        tit = item.find('title').text if item.find('title') is not None else ""
                        lnk = item.find('link').text if item.find('link') is not None else ""
                        dsc = item.find('description').text if item.find('description') is not None else ""
                        if not tit: continue
                        if "<" in dsc: dsc = re.sub('<.*?>', '', dsc)
                        if not dsc.strip(): dsc = "Oportunidade oficial verificada com inscrições abertas para trabalhadores."
                        
                        if not lnk or not lnk.startswith("http") or "g1.globo.com" not in lnk:
                            lnk = random.choice(info["diretorios"])
                            
                        obj = {
                            "category": cat_nome, "color": info["color"],
                            "title": tit.strip(), "link": lnk.strip(), 
                            "image": imgs[idx % len(imgs)],
                            "description": dsc.strip()[:110] + "..." if len(dsc.strip()) > 110 else dsc.strip()
                        }
                        items_cat.append(obj)
            except: pass
            
        while len(items_cat) < 3:
            idx = len(items_cat)
            alt_link = random.choice(info["diretorios"])
            obj = {
                "category": cat_nome, "color": info["color"],
                "title": f"Processo Seletivo Aberto: {cat_nome}", "link": alt_link,
                "image": imgs[idx % len(imgs)], "description": "Confira os requisitos, salários e faça sua inscrição diretamente na página oficial parceira."
            }
            items_cat.append(obj)
            
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:3]}
        
    return categorias_processadas

def gerar_sitemap(lista_estados):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'  <url><loc>{DOMINIO_SITE}/index.html</loc><lastmod>{data_hoje}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>')
    for e in lista_estados:
        xml.append(f'  <url><loc>{DOMINIO_SITE}/{e["file"]}</loc><lastmod>{data_hoje}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write("\n".join(xml))

def gerar_site():
    print("Gerando portal completo com cidades e links diversificados...")
    estados_brasil = [
        {"name": "Bahia (BA)", "file": "bahia.html", "cities": ["Salvador", "Camaçari", "Feira de Santana", "Vitória da Conquista", "Itabuna", "Lauro de Freitas"]},
        {"name": "São Paulo (SP)", "file": "sao-paulo.html", "cities": ["São Paulo", "Campinas", "Santos", "Ribeirão Preto", "Sorocaba", "São José dos Campos"]},
        {"name": "Rio de Janeiro (RJ)", "file": "rio-de-janeiro.html", "cities": ["Rio de Janeiro", "Niterói", "Duque de Caxias", "Nova Iguaçu", "Petrópolis", "Campos dos Goytacazes"]},
        {"name": "Minas Gerais (MG)", "file": "minas-gerais.html", "cities": ["Belo Horizonte", "Uberlândia", "Contagem", "Juiz de Fora", "Betim", "Montes Claros"]},
        {"name": "Paraná (PR)", "file": "parana.html", "cities": ["Curitiba", "Londrina", "Maringá", "Ponta Grossa", "Cascavel", "São José dos Pinhais"]},
        {"name": "Rio Grande do Sul (RS)", "file": "rio-grande-do-sul.html", "cities": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Canoas", "Santa Maria", "Gravataí"]},
        {"name": "Santa Catarina (SC)", "file": "santa-catarina.html", "cities": ["Florianópolis", "Joinville", "Blumenau", "São José", "Criciúma", "Chapecó"]},
        {"name": "Distrito Federal (DF)", "file": "distrito-federal.html", "cities": ["Brasília", "Taguatinga", "Ceilândia", "Samambaia", "Planaltina", "Águas Claras"]},
        {"name": "Pernambuco (PE)", "file": "pernambuco.html", "cities": ["Recife", "Jaboatão dos Guararapes", "Olinda", "Caruaru", "Petrolina", "Paulista"]},
        {"name": "Ceará (CE)", "file": "ceara.html", "cities": ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Maracanaú", "Sobral", "Crato"]}
    ]
    
    categorias_dict = buscar_noticias_brasil()
    template_estado = Template(ESTADO_TEMPLATE)
    
    for est in estados_brasil:
        noticias_est = []
        for cat_nome, cat_data in categorias_dict.items():
            for item in cat_data["lista"]:
                copia_item = item.copy()
                cidade_aleatoria = random.choice(est["cities"])
                sigla_est = est['name'].split('(')[1].replace(')', '')
                copia_item["title"] = f"{copia_item['title'].split('—')[0].strip()} — {cidade_aleatoria} ({sigla_est})"
                noticias_est.append(copia_item)
                
        random.shuffle(noticias_est)
        
        with open(est["file"], "w", encoding="utf-8") as f:
            f.write(template_estado.render(
                estado=est, noticias=noticias_est[:3], estados_lista=estados_brasil,
                ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
                google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES, dominio=DOMINIO_SITE
            ))
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=estados_brasil, categorias=categorias_dict,
            ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META, ticker_cotacoes=TICKER_COTACOES, breaking_news_ticker=BREAKING_NEWS_TICKER, dominio=DOMINIO_SITE
        ))
        
    gerar_sitemap(estados_brasil)
    print("Sucesso absoluto! Cidades adicionadas, páginas estaduais segmentadas e links diversificados.")

if __name__ == "__main__":
    gerar_site()

