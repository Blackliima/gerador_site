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

# Banner unificado seguro e centralizado
AD_BANNER = """
<div style="text-align:center; margin: 40px auto; padding: 20px; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; max-width: 100%; box-sizing: border-box;">
    <p style="font-size: 10px; color: #64748b; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1px;">Publicidade</p>
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

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {{ adsense_script | safe }}
    {{ monetag_script | safe }}
    {{ google_meta | safe }}
    <title>Brasil Oportunidades & Vagas - Concursos e Empregos</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 40px 20px; text-align: center; }
        .header-top h1 { margin: 0 0 10px 0; font-size: 28px; }
        .header-top p { margin: 0; opacity: 0.9; font-size: 14px; }
        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .section-title { font-size: 20px; font-weight: 700; margin: 40px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; color: #0f172a; }
        
        /* Grid simples em tabela flexível para nunca quebrar */
        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; width: 300px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .card img { width: 100%; height: 150px; object-fit: cover; }
        .card-body { padding: 15px; display: flex; flex-direction: column; flex-grow: 1; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0; line-height: 1.4; }
        
        .states-box { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 30px; }
        .state-pill { background: #ffffff; border: 1px solid #e2e8f0; padding: 10px 15px; border-radius: 8px; text-decoration: none; color: #0f172a; font-weight: 600; font-size: 13px; }
        .state-pill:hover { border-color: #2563eb; color: #2563eb; }
        
        footer { text-align: center; padding: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 50px; }
    </style>
</head>
<body>
    <div class="header-top">
        <h1>Brasil Oportunidades & Vagas</h1>
        <p>Editais de Concursos Públicos, Vagas CLT e Trabalho Home Office</p>
    </div>

    <div class="main-container">
        {{ ad_banner | safe }}

        {% for cat_nome, cat_data in categorias.items() %}
        <div class="section-title">{{ cat_nome }}</div>
        <div class="cards-wrapper">
            {% for noticia in cat_data.lista %}
            <div class="card">
                <img src="{{ noticia.image }}" alt="Capa" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                <div class="card-body">
                    <span class="badge" style="background-color: {{ cat_data.color }};">{{ cat_nome }}</span>
                    <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                    <p>{{ noticia.description }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}

        {{ ad_banner | safe }}

        <div class="section-title">Vagas e Concursos por Estado</div>
        <div class="states-box">
            {% for e in estados %}
            <a href="{{ e.file }}" class="state-pill">{{ e.name }}</a>
            {% endfor %}
        </div>

        <footer>
            <p>© 2026 Brasil Oportunidades & Vagas. Todos os direitos reservados.</p>
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
    <title>Vagas em {{ estado.name }} - Brasil Oportunidades</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 0; }
        .header-top { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 30px 20px; }
        .header-top a { color: #93c5fd; text-decoration: none; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
        .header-top h1 { margin: 0; font-size: 24px; }
        .main-container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .section-title { font-size: 20px; font-weight: 700; margin: 30px 0 20px 0; border-left: 4px solid #2563eb; padding-left: 10px; }
        
        .cards-wrapper { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; width: 300px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .card img { width: 100%; height: 150px; object-fit: cover; }
        .card-body { padding: 15px; display: flex; flex-direction: column; flex-grow: 1; }
        .badge { background: #2563eb; color: white; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; width: fit-content; text-transform: uppercase; }
        .card h3 { font-size: 15px; margin: 0 0 8px 0; line-height: 1.4; }
        .card h3 a { color: #0f172a; text-decoration: none; }
        .card h3 a:hover { color: #2563eb; }
        .card p { font-size: 13px; color: #64748b; margin: 0; line-height: 1.4; }
        
        footer { text-align: center; padding: 30px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 50px; }
    </style>
</head>
<body>
    <div class="header-top">
        <a href="index.html">← Voltar ao Início</a>
        <h1>Oportunidades em {{ estado.name }}</h1>
    </div>

    <div class="main-container">
        {{ ad_banner | safe }}

        <div class="section-title">Editais e Vagas Recentes</div>
        <div class="cards-wrapper">
            {% for noticia in noticias %}
            <div class="card">
                <img src="{{ noticia.image }}" alt="Capa" onerror="this.src='https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60'">
                <div class="card-body">
                    <span class="badge" style="background-color: {{ noticia.color }};">{{ noticia.category }}</span>
                    <h3><a href="{{ noticia.link }}" target="_blank" rel="nofollow">{{ noticia.title }}</a></h3>
                    <p>{{ noticia.description }}</p>
                </div>
            </div>
            {% endfor %}
        </div>

        {{ ad_banner | safe }}

        <footer>
            <p>© 2026 Brasil Oportunidades & Vagas. Todos os direitos reservados.</p>
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
            "urls": ["https://s2.glbimg.com/rss/g1/economia/"]
        },
        "Trabalho Home Office": {
            "id": "homeoffice", "color": "#ea580c",
            "urls": ["https://s2.glbimg.com/rss/g1/tecnologia/"]
        }
    }
    
    tstamp = int(datetime.now().timestamp())
    imagens_cat = {
        "Concursos Públicos": f"https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&auto=format&fit=crop&q=60&v={tstamp}",
        "Vagas CLT & Empresas": f"https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=600&auto=format&fit=crop&q=60&v={tstamp}",
        "Trabalho Home Office": f"https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600&auto=format&fit=crop&q=60&v={tstamp}"
    }

    categorias_processadas, todas_noticias = {}, []
    
    for cat_nome, info in fontes.items():
        items_cat = []
        img_default = imagens_cat[cat_nome]
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
                            "title": tit.strip(), "link": lnk.strip(), "image": img_default,
                            "description": dsc.strip()[:120] + "..." if len(dsc.strip()) > 120 else dsc.strip()
                        }
                        items_cat.append(obj)
                        todas_noticias.append(obj)
            except: pass
            
        while len(items_cat) < 3:
            obj = {
                "category": cat_nome, "color": info["color"],
                "title": f"Oportunidade Verificada em {cat_nome}", "link": f"#{info['id']}",
                "image": img_default, "description": "Confira os detalhes desta oportunidade com inscrições abertas."
            }
            items_cat.append(obj)
            todas_noticias.append(obj)
            
        categorias_processadas[cat_nome] = {"id": info["id"], "color": info["color"], "lista": items_cat[:3]}
        
    return categorias_processadas, todas_noticias

def gerar_site():
    print("Gerando site limpo sem falhas estruturais...")
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
                google_meta=GOOGLE_META, dominio=DOMINIO_SITE
            ))
        lista_estados_gerados.append(est)
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(Template(INDEX_TEMPLATE).render(
            estados=lista_estados_gerados, categorias=categorias_dict,
            ad_banner=AD_BANNER, adsense_script=ADSENSE_SCRIPT, monetag_script=MONETAG_SCRIPT,
            google_meta=GOOGLE_META, dominio=DOMINIO_SITE
        ))
        
    print("Sucesso absoluto! Script reescrito de forma simplificada e direta.")

if __name__ == "__main__":
    gerar_site()

