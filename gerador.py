import os
import re
import json
import html
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURAÇÕES GERAIS DO PORTAL
# ==============================================================================
SITE_NAME = "Global News & Data"
SITE_URL = "https://gerador-site.pages.dev"  # Atualize aqui quando migrar o domínio
ADSENSE_PUB_ID = "ca-pub-5379027874215422"
OUTPUT_DIR = "."  # Gera na raiz para deploy direto no Cloudflare Pages

# Feeds RSS Reais e Estáveis por Editoria
CATEGORIES = {
    "mundo": {
        "title": "Mundo & Geopolítica",
        "icon": "🌍",
        "feeds": [
            "https://news.google.com/rss/headlines/section/topic/WORLD?hl=pt-BR&gl=BR&ceid=BR:pt-419",
            "https://feeds.bbci.co.uk/portuguese/rss.xml"
        ]
    },
    "economia": {
        "title": "Economia & Mercados",
        "icon": "📈",
        "feeds": [
            "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=pt-BR&gl=BR&ceid=BR:pt-419",
            "https://g1.globo.com/rss/g1/economia/"
        ]
    },
    "tecnologia": {
        "title": "Tecnologia & IA",
        "icon": "💻",
        "feeds": [
            "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=pt-BR&gl=BR&ceid=BR:pt-419",
            "https://www.tecmundo.com.br/rss"
        ]
    },
    "vagas": {
        "title": "Vagas & Home Office",
        "icon": "💼",
        "feeds": [
            "https://news.google.com/rss/search?q=vagas+home+office+trabalho+remoto+emprego&hl=pt-BR&gl=BR&ceid=BR:pt-419",
            "https://news.google.com/rss/search?q=remote+jobs+hiring+tech+careers&hl=en-US&gl=US&ceid=US:en"
        ]
    },
    "filmes": {
        "title": "Filmes, Séries & Streaming",
        "icon": "🎬",
        "feeds": [
            "https://news.google.com/rss/search?q=filmes+series+netflix+estreias+cinema&hl=pt-BR&gl=BR&ceid=BR:pt-419",
            "https://www.omelete.com.br/rss"
        ]
    },
    "games": {
        "title": "Games & E-Sports",
        "icon": "🎮",
        "feeds": [
            "https://news.google.com/rss/search?q=games+playstation+xbox+nintendo+pc+gaming&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        ]
    },
    "esportes": {
        "title": "Esportes Globais",
        "icon": "⚽",
        "feeds": [
            "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=pt-BR&gl=BR&ceid=BR:pt-419"
        ]
    },
    "saude": {
        "title": "Qualidade de Vida & Saúde",
        "icon": "🧬",
        "feeds": [
            "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=pt-BR&gl=BR&ceid=BR:pt-419"
        ]
    }
}

# Base de Dados de Países para Páginas Programáticas de SEO + FAQ
COUNTRIES = [
    {"slug": "brasil", "name": "Brasil", "capital": "Brasília", "currency": "Real (BRL)", "pop": "216,4 milhões", "continent": "América do Sul", "gdp": "US$ 2,17 trilhões"},
    {"slug": "estados-unidos", "name": "Estados Unidos", "capital": "Washington, D.C.", "currency": "Dólar Americano (USD)", "pop": "334,9 milhões", "continent": "América do Norte", "gdp": "US$ 27,36 trilhões"},
    {"slug": "portugal", "name": "Portugal", "capital": "Lisboa", "currency": "Euro (EUR)", "pop": "10,5 milhões", "continent": "Europa", "gdp": "US$ 287 bilhões"},
    {"slug": "reino-unido", "name": "Reino Unido", "capital": "Londres", "currency": "Libra Esterlina (GBP)", "pop": "67,7 milhões", "continent": "Europa", "gdp": "US$ 3,34 trilhões"},
    {"slug": "japao", "name": "Japão", "capital": "Tóquio", "currency": "Iene (JPY)", "pop": "124,5 milhões", "continent": "Ásia", "gdp": "US$ 4,21 trilhões"},
    {"slug": "alemanha", "name": "Alemanha", "capital": "Berlim", "currency": "Euro (EUR)", "pop": "84,4 milhões", "continent": "Europa", "gdp": "US$ 4,46 trilhões"},
    {"slug": "canada", "name": "Canadá", "capital": "Ottawa", "currency": "Dólar Canadense (CAD)", "pop": "40,1 milhões", "continent": "América do Norte", "gdp": "US$ 2,14 trilhões"},
    {"slug": "emirados-arabes", "name": "Emirados Árabes Unidos", "capital": "Abu Dhabi", "currency": "Dirham (AED)", "pop": "9,5 milhões", "continent": "Ásia", "gdp": "US$ 509 bilhões"}
]

# ==============================================================================
# MOTOR DE COLETA RSS COM TRATAMENTO DE ERROS
# ==============================================================================
def clean_html(raw_html):
    if not raw_html:
        return ""
    text = re.sub(r'<[^>]+>', '', raw_html)
    text = html.unescape(text)
    return " ".join(text.split())[:220] + "..."

def fetch_rss(url, limit=6):
    items = []
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GlobalNewsBot/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        for item in root.findall('.//item')[:limit]:
            title = item.findtext('title') or "Atualização Global"
            link = item.findtext('link') or "#"
            pub_date = item.findtext('pubDate') or datetime.now().strftime("%d/%m/%Y")
            desc = clean_html(item.findtext('description') or "")
            source_el = item.find('source')
            source = source_el.text if source_el is not None else "Global Feed"

            # Limpa sufixo repetitivo do Google News
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                title = parts[0]
                if source == "Global Feed":
                    source = parts[1]

            items.append({
                "title": html.escape(title.strip()),
                "link": link.strip(),
                "date": pub_date[:16],
                "desc": html.escape(desc),
                "source": html.escape(source.strip())
            })
    except Exception as e:
        print(f"[Aviso] Falha ao ler feed {url}: {e}")
    return items

def collect_all_news():
    news_data = {}
    for cat_key, cat_info in CATEGORIES.items():
        print(f"Coletando editoria: {cat_info['title']}...")
        cat_items = []
        seen_titles = set()
        for feed_url in cat_info["feeds"]:
            fetched = fetch_rss(feed_url, limit=6)
            for art in fetched:
                if art["title"] not in seen_titles:
                    seen_titles.add(art["title"])
                    cat_items.append(art)
        if not cat_items:
            cat_items.append({
                "title": f"Monitoramento ativo em {cat_info['title']}",
                "link": "#",
                "date": datetime.now().strftime("%d/%m/%Y"),
                "desc": "Atualização contínua de indicadores, manchetes internacionais e relatórios em tempo real.",
                "source": SITE_NAME
            })
        news_data[cat_key] = cat_items[:8]
    return news_data

# ==============================================================================
# TEMPLATE BASE HTML (CSS + WIDGETS INTERATIVOS + MONETIZAÇÃO + TRADUTOR)
# ==============================================================================
def get_base_template(page_title, meta_desc, canonical_path, content_html, extra_schema=""):
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    nav_links = "".join([
        f'<a href="index.html#{k}" class="nav-pill">{v["icon"]} {v["title"].split(" & ")[0]}</a>'
        for k, v in CATEGORIES.items()
    ])
    country_links = "".join([
        f'<a href="pais-{c["slug"]}.html">{c["name"]}</a>'
        for c in COUNTRIES
    ])

    return f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | {SITE_NAME}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/{canonical_path}">
    
    <!-- Google AdSense Verification & Auto Ads -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
    
    <!-- ESPAÇO RESERVADO PARA MULTITAG MONETAG (Cole sua tag Monetag logo abaixo se desejar atualizar) -->
    <!-- <script src="https://..." data-zone="..." async data-cfasync="false"></script> -->

    {extra_schema}

    <style>
        :root {{
            --bg: #0b0f19;
            --surface: #131a2a;
            --surface-hover: #1b2438;
            --border: #243049;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
            --primary: #3b82f6;
            --accent: #10b981;
            --danger: #ef4444;
        }}
        [data-theme="light"] {{
            --bg: #f8fafc;
            --surface: #ffffff;
            --surface-hover: #f1f5f9;
            --border: #e2e8f0;
            --text: #0f172a;
            --text-muted: #475569;
            --primary: #2563eb;
            --accent: #059669;
            --danger: #dc2626;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            transition: background 0.25s, color 0.25s;
        }}
        a {{ color: inherit; text-decoration: none; }}
        
        /* Ticker Financeiro Ao Vivo */
        .ticker-bar {{
            background: #060911;
            color: #e2e8f0;
            font-size: 0.82rem;
            padding: 8px 16px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .ticker-items {{ display: flex; gap: 18px; flex-wrap: wrap; font-weight: 600; }}
        .ticker-up {{ color: #34d399; }}
        .ticker-down {{ color: #f87171; }}

        /* Header */
        header {{
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header-top {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 14px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .brand {{
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .brand span {{ color: var(--primary); }}
        .controls {{ display: flex; align-items: center; gap: 10px; }}
        .btn-control {{
            background: var(--surface-hover);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .nav-scroll {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 20px 12px;
            display: flex;
            gap: 8px;
            overflow-x: auto;
            scrollbar-width: none;
        }}
        .nav-pill {{
            background: var(--bg);
            border: 1px solid var(--border);
            padding: 6px 13px;
            border-radius: 999px;
            font-size: 0.84rem;
            font-weight: 600;
            white-space: nowrap;
            transition: 0.2s;
        }}
        .nav-pill:hover {{ border-color: var(--primary); color: var(--primary); }}

        /* Layout Principal */
        .container {{
            max-width: 1280px;
            margin: 24px auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: 1fr 330px;
            gap: 28px;
        }}
        @media (max-width: 960px) {{
            .container {{ grid-template-columns: 1fr; }}
        }}

        /* Blocos de Anúncio Responsivos */
        .ad-slot {{
            background: var(--surface);
            border: 1px dashed var(--border);
            border-radius: 8px;
            padding: 12px;
            margin: 18px 0;
            text-align: center;
            min-height: 95px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .ad-label {{
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}

        /* Cards e Seções */
        .section-block {{ margin-bottom: 36px; }}
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }}
        .section-header h2 {{ font-size: 1.25rem; display: flex; align-items: center; gap: 8px; }}
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
            gap: 16px;
        }}
        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card:hover {{ transform: translateY(-2px); border-color: var(--primary); }}
        .card-meta {{
            font-size: 0.75rem;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}
        .card h3 {{ font-size: 1.02rem; margin-bottom: 8px; line-height: 1.4; }}
        .card p {{ font-size: 0.86rem; color: var(--text-muted); margin-bottom: 12px; }}
        .card-footer {{
            font-size: 0.76rem;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            border-top: 1px solid var(--border);
            padding-top: 8px;
        }}

        /* Widgets Laterais */
        .widget {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 20px;
        }}
        .widget h3 {{ font-size: 1.05rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
        .weather-select {{
            width: 100%;
            padding: 8px;
            border-radius: 6px;
            background: var(--bg);
            color: var(--text);
            border: 1px solid var(--border);
            margin-bottom: 12px;
        }}
        .weather-display {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg);
            padding: 12px;
            border-radius: 8px;
        }}
        .poll-option {{
            display: block;
            width: 100%;
            text-align: left;
            padding: 10px 12px;
            margin-bottom: 8px;
            background: var(--bg);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.88rem;
            transition: 0.2s;
        }}
        .poll-option:hover {{ border-color: var(--primary); }}
        .poll-bar-bg {{
            height: 6px;
            background: var(--border);
            border-radius: 4px;
            margin-top: 6px;
            overflow: hidden;
        }}
        .poll-bar-fill {{
            height: 100%;
            background: var(--primary);
            transition: width 0.4s ease;
        }}
        .country-tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .country-tags a {{
            font-size: 0.8rem;
            background: var(--bg);
            border: 1px solid var(--border);
            padding: 4px 10px;
            border-radius: 6px;
        }}
        .country-tags a:hover {{ border-color: var(--accent); color: var(--accent); }}

        /* Tabela Dados Países & FAQ */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            background: var(--surface);
            border-radius: 8px;
            overflow: hidden;
        }}
        .data-table th, .data-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            text-align: left;
        }}
        .faq-item {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 10px;
        }}
        .faq-item h4 {{ margin-bottom: 6px; color: var(--primary); }}

        footer {{
            background: var(--surface);
            border-top: 1px solid var(--border);
            padding: 32px 20px;
            margin-top: 40px;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <!-- Barra de Cotações em Tempo Real -->
    <div class="ticker-bar">
        <div class="ticker-items" id="live-ticker">
            <span>💵 USD/BRL: Carregando...</span>
            <span>💶 EUR/BRL: Carregando...</span>
            <span>₿ BTC/USD: Carregando...</span>
            <span>Ξ ETH/USD: Carregando...</span>
        </div>
        <div>Atualizado: {now_str}</div>
    </div>

    <!-- Cabeçalho & Navegação -->
    <header>
        <div class="header-top">
            <a href="index.html" class="brand">🌐 Global<span>News</span> & Data</a>
            <div class="controls">
                <div id="google_translate_element"></div>
                <button class="btn-control" onclick="toggleTheme()" id="theme-btn">☀️ Modo Claro</button>
            </div>
        </div>
        <nav class="nav-scroll">
            <a href="index.html" class="nav-pill">🏠 Início</a>
            {nav_links}
        </nav>
    </header>

    <!-- Banner Superior Monetização -->
    <div style="max-width: 1280px; margin: 0 auto; padding: 0 20px;">
        <div class="ad-slot">
            <span class="ad-label">Publicidade</span>
            <ins class="adsbygoogle"
                 style="display:block; width:100%;"
                 data-ad-client="{ADSENSE_PUB_ID}"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>
    </div>

    <!-- Conteúdo Principal + Barra Lateral de Widgets -->
    <div class="container">
        <main>
            {content_html}
        </main>

        <aside>
            <!-- Widget 1: Clima Global em Tempo Real -->
            <div class="widget">
                <h3>🌦️ Clima Global Ao Vivo</h3>
                <select class="weather-select" id="city-selector" onchange="fetchWeather()">
                    <option value="-23.55,-46.63">🇧🇷 São Paulo, Brasil</option>
                    <option value="40.71,-74.00">🇺🇸 Nova York, EUA</option>
                    <option value="51.50,-0.12">🇬🇧 Londres, Reino Unido</option>
                    <option value="35.67,139.65">🇯🇵 Tóquio, Japão</option>
                    <option value="38.72,-9.13">🇵🇹 Lisboa, Portugal</option>
                    <option value="25.20,55.27">🇦🇪 Dubai, EAU</option>
                </select>
                <div class="weather-display" id="weather-box">
                    <div>
                        <strong id="weather-city">São Paulo</strong>
                        <div style="font-size:0.8rem; color:var(--text-muted);" id="weather-wind">Vento: -- km/h</div>
                    </div>
                    <div style="font-size:1.6rem; font-weight:800; color:var(--primary);" id="weather-temp">--°C</div>
                </div>
            </div>

            <!-- Widget 2: Enquete Interativa -->
            <div class="widget">
                <h3>📊 Enquete do Leitor</h3>
                <p style="font-size:0.88rem; margin-bottom:12px; color:var(--text-muted);">
                    Qual setor vai gerar mais oportunidades globais nos próximos 12 meses?
                </p>
                <div id="poll-container">
                    <button class="poll-option" onclick="votePoll(0)">🤖 Inteligência Artificial & Tech</button>
                    <button class="poll-option" onclick="votePoll(1)">💼 Trabalho Remoto Internacional</button>
                    <button class="poll-option" onclick="votePoll(2)">📈 Mercado Financeiro & Cripto</button>
                    <button class="poll-option" onclick="votePoll(3)">🌱 Energia Verde & Sustentabilidade</button>
                </div>
                <div id="poll-status" style="font-size:0.78rem; color:var(--accent); margin-top:8px;"></div>
            </div>

            <!-- Espaço AdSense Lateral -->
            <div class="ad-slot">
                <span class="ad-label">Patrocinado</span>
                <ins class="adsbygoogle"
                     style="display:block; width:100%;"
                     data-ad-client="{ADSENSE_PUB_ID}"
                     data-ad-format="rectangle"
                     data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>

            <!-- Widget 3: Indicadores por País (SEO Interno) -->
            <div class="widget">
                <h3>🗺️ Dados & Economia por País</h3>
                <p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:10px;">
                    Acesse indicadores econômicos, PIB, moeda e perguntas frequentes:
                </p>
                <div class="country-tags">
                    {country_links}
                </div>
            </div>
        </aside>
    </div>

    <footer>
        <p><strong>{SITE_NAME}</strong> — Monitoramento Internacional de Notícias, Economia, Carreiras e Dados.</p>
        <p style="margin-top:6px;">
            <a href="index.html">Início</a> • 
            <a href="sitemap.xml">Sitemap XML</a> • 
            <a href="privacidade.html">Política de Privacidade & Termos</a>
        </p>
    </footer>

    <!-- Google Translate Widget -->
    <script type="text/javascript">
        function googleTranslateElementInit() {{
            new google.translate.TranslateElement({{pageLanguage: 'pt', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}}, 'google_translate_element');
        }}
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>

    <!-- Scripts Interativos: Tema, Cotações, Clima e Enquete -->
    <script>
        // 1. Alternar Tema Claro/Escuro
        function toggleTheme() {{
            const htmlEl = document.documentElement;
            const current = htmlEl.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            htmlEl.setAttribute('data-theme', next);
            localStorage.setItem('gnd_theme', next);
            document.getElementById('theme-btn').innerText = next === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Escuro';
        }}
        (function initTheme() {{
            const saved = localStorage.getItem('gnd_theme');
            if (saved) {{
                document.documentElement.setAttribute('data-theme', saved);
                document.getElementById('theme-btn').innerText = saved === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Escuro';
            }}
        }})();

        // 2. Cotações Financeiras ao Vivo (AwesomeAPI)
        async function fetchMarketRates() {{
            try {{
                const res = await fetch('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-USD,ETH-USD');
                const data = await res.json();
                const usd = parseFloat(data.USDBRL.bid).toFixed(2);
                const eur = parseFloat(data.EURBRL.bid).toFixed(2);
                const btc = parseFloat(data.BTCUSD.bid).toLocaleString('en-US', {{maximumFractionDigits: 0}});
                const eth = parseFloat(data.ETHUSD.bid).toLocaleString('en-US', {{maximumFractionDigits: 0}});
                document.getElementById('live-ticker').innerHTML = `
                    <span>💵 USD/BRL: <strong class="ticker-up">R$ ${{usd}}</strong></span>
                    <span>💶 EUR/BRL: <strong class="ticker-up">R$ ${{eur}}</strong></span>
                    <span>₿ BTC/USD: <strong class="ticker-up">$ ${{btc}}</strong></span>
                    <span>Ξ ETH/USD: <strong class="ticker-up">$ ${{eth}}</strong></span>
                `;
            }} catch (e) {{
                document.getElementById('live-ticker').innerHTML = `
                    <span>💵 USD/BRL: R$ 5,75</span>
                    <span>💶 EUR/BRL: R$ 6,18</span>
                    <span>₿ BTC/USD: $ 91.400</span>
                    <span>📊 Mercados Globais Ativos</span>
                `;
            }}
        }}
        fetchMarketRates();

        // 3. Clima Global ao Vivo (Open-Meteo API - Gratuita sem chave)
        async function fetchWeather() {{
            const select = document.getElementById('city-selector');
            const [lat, lon] = select.value.split(',');
            const cityName = select.options[select.selectedIndex].text.split(',')[0];
            try {{
                const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}¤t_weather=true`);
                const data = await res.json();
                const temp = Math.round(data.current_weather.temperature);
                const wind = data.current_weather.windspeed;
                document.getElementById('weather-city').innerText = cityName;
                document.getElementById('weather-temp').innerText = `${{temp}}°C`;
                document.getElementById('weather-wind').innerText = `Vento: ${{wind}} km/h`;
            }} catch (e) {{
                document.getElementById('weather-temp').innerText = "24°C";
            }}
        }}
        fetchWeather();

        // 4. Enquete Interativa com Persistência
        const pollLabels = [
            "🤖 Inteligência Artificial & Tech",
            "💼 Trabalho Remoto Internacional",
            "📈 Mercado Financeiro & Cripto",
            "🌱 Energia Verde & Sustentabilidade"
        ];
        let pollVotes = JSON.parse(localStorage.getItem('gnd_poll_votes')) || [142, 98, 76, 54];
        let hasVoted = localStorage.getItem('gnd_has_voted') === 'true';

        function renderPoll() {{
            if (!hasVoted) return;
            const total = pollVotes.reduce((a, b) => a + b, 0);
            const container = document.getElementById('poll-container');
            container.innerHTML = pollLabels.map((label, idx) => {{
                const pct = Math.round((pollVotes[idx] / total) * 100);
                return `
                    <div style="margin-bottom:10px; font-size:0.85rem;">
                        <div style="display:flex; justify-content:space-between;">
                            <span>${{label}}</span>
                            <strong>${{pct}}%</strong>
                        </div>
                        <div class="poll-bar-bg">
                            <div class="poll-bar-fill" style="width:${{pct}}%;"></div>
                        </div>
                    </div>
                `;
            }}).join('');
            document.getElementById('poll-status').innerText = `Obrigado pelo voto! Total: ${{total}} participações.`;
        }}

        function votePoll(index) {{
            if (hasVoted) return;
            pollVotes[index] += 1;
            hasVoted = true;
            localStorage.setItem('gnd_poll_votes', JSON.stringify(pollVotes));
            localStorage.setItem('gnd_has_voted', 'true');
            renderPoll();
        }}
        if (hasVoted) renderPoll();
    </script>
</body>
</html>"""

# ==============================================================================
# GERADORES DE PÁGINAS (HOME, PAÍSES, PRIVACIDADE, SITEMAP & ROBOTS)
# ==============================================================================
def build_index(news_data):
    sections_html = []
    for idx, (cat_key, cat_info) in enumerate(CATEGORIES.items()):
        articles = news_data.get(cat_key, [])
        cards_html = ""
        for art in articles:
            cards_html += f"""
            <article class="card">
                <div>
                    <div class="card-meta">{art['source']}</div>
                    <h3><a href="{art['link']}" target="_blank" rel="noopener noreferrer">{art['title']}</a></h3>
                    <p>{art['desc']}</p>
                </div>
                <div class="card-footer">
                    <span>🕒 {art['date']}</span>
                    <a href="{art['link']}" target="_blank" rel="noopener noreferrer" style="color:var(--primary); font-weight:600;">Ler matéria →</a>
                </div>
            </article>
            """
        
        ad_divider = ""
        if idx in [1, 4]:
            ad_divider = f"""
            <div class="ad-slot">
                <span class="ad-label">Publicidade</span>
                <ins class="adsbygoogle"
                     style="display:block; width:100%;"
                     data-ad-client="{ADSENSE_PUB_ID}"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
            """

        sections_html.append(f"""
        <section class="section-block" id="{cat_key}">
            <div class="section-header">
                <h2>{cat_info['icon']} {cat_info['title']}</h2>
            </div>
            <div class="news-grid">
                {cards_html}
            </div>
        </section>
        {ad_divider}
        """)

    html_out = get_base_template(
        page_title="Notícias Globais, Economia, Vagas Home Office, Filmes e Dados",
        meta_desc="Portal internacional com notícias em tempo real, cotações de moedas, clima global, vagas home office, filmes, séries e indicadores econômicos.",
        canonical_path="index.html",
        content_html="\n".join(sections_html)
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    print("✔ index.html gerado com sucesso.")

def build_country_pages(news_data):
    world_news = news_data.get("mundo", [])[:4]
    news_cards = "".join([
        f"""
        <article class="card">
            <div>
                <div class="card-meta">{art['source']}</div>
                <h3><a href="{art['link']}" target="_blank" rel="noopener noreferrer">{art['title']}</a></h3>
                <p>{art['desc']}</p>
            </div>
            <div class="card-footer"><span>🕒 {art['date']}</span><span>Global</span></div>
        </article>
        """ for art in world_news
    ])

    for c in COUNTRIES:
        filename = f"pais-{c['slug']}.html"
        faq_schema = f"""
        <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": [
            {{
              "@type": "Question",
              "name": "Qual é a capital e a moeda oficial de {c['name']}?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "A capital de {c['name']} é {c['capital']} e a moeda oficial utilizada na economia local é {c['currency']}."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Qual é a população e o PIB estimado de {c['name']}?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "{c['name']} possui uma população estimada em {c['pop']} e um Produto Interno Bruto (PIB) de aproximadamente {c['gdp']}."
              }}
            }}
          ]
        }}
        </script>
        """

        content = f"""
        <section class="section-block">
            <div class="section-header">
                <h2>🏳️ Perfil Econômico e Dados: {c['name']}</h2>
            </div>
            <p style="color:var(--text-muted); margin-bottom:16px;">
                Resumo atualizado dos principais indicadores demográficos, monetários e geopolíticos de <strong>{c['name']}</strong> ({c['continent']}).
            </p>
            <table class="data-table">
                <tr><th>Indicador</th><th>Informação Oficial</th></tr>
                <tr><td><strong>Capital</strong></td><td>{c['capital']}</td></tr>
                <tr><td><strong>Continente</strong></td><td>{c['continent']}</td></tr>
                <tr><td><strong>Moeda Oficial</strong></td><td>{c['currency']}</td></tr>
                <tr><td><strong>População Estimada</strong></td><td>{c['pop']}</td></tr>
                <tr><td><strong>PIB Nominal Estimado</strong></td><td>{c['gdp']}</td></tr>
            </table>

            <h3 style="margin: 24px 0 12px;">❓ Perguntas Frequentes sobre {c['name']}</h3>
            <div class="faq-item">
                <h4>Qual é a moeda oficial de {c['name']}?</h4>
                <p>A moeda utilizada oficialmente em transações comerciais e financeiras em {c['name']} é o <strong>{c['currency']}</strong>.</p>
            </div>
            <div class="faq-item">
                <h4>Onde fica localizada a capital de {c['name']}?</h4>
                <p>O centro administrativo e capital oficial do país é <strong>{c['capital']}</strong>, situado na região de {c['continent']}.</p>
            </div>

            <h3 style="margin: 28px 0 14px;">🌍 Últimas Manchetes Internacionais</h3>
            <div class="news-grid">{news_cards}</div>
        </section>
        """

        html_out = get_base_template(
            page_title=f"{c['name']}: Economia, Moeda, População e Notícias",
            meta_desc=f"Dados completos sobre {c['name']}: capital {c['capital']}, moeda {c['currency']}, PIB {c['gdp']} e notícias internacionais atualizadas.",
            canonical_path=filename,
            content_html=content,
            extra_schema=faq_schema
        )
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html_out)
    print(f"✔ {len(COUNTRIES)} páginas de países geradas com FAQ Schema.")

def build_privacy_page():
    content = f"""
    <section class="section-block">
        <div class="section-header">
            <h2>🔒 Política de Privacidade e Termos de Uso</h2>
        </div>
        <div class="card" style="gap:12px;">
            <p>O portal <strong>{SITE_NAME}</strong> respeita a privacidade de seus visitantes e opera em conformidade com as diretrizes internacionais de proteção de dados e políticas de publicidade do Google AdSense.</p>
            <p><strong>Cookies e Publicidade:</strong> Utilizamos fornecedores terceiros, incluindo o Google, que usam cookies para veicular anúncios com base em visitas anteriores dos usuários a este ou a outros sites. Você pode desativar a publicidade personalizada acessando as Configurações de Anúncios do Google.</p>
            <p><strong>Fontes de Dados:</strong> As notícias exibidas são agregadas automaticamente via feeds públicos RSS com atribuição direta e link para os veículos originais. Os dados climáticos e de câmbio são fornecidos por APIs públicas informativas.</p>
        </div>
    </section>
    """
    html_out = get_base_template(
        page_title="Política de Privacidade",
        meta_desc=f"Política de privacidade, uso de cookies e termos do portal {SITE_NAME}.",
        canonical_path="privacidade.html",
        content_html=content
    )
    with open(os.path.join(OUTPUT_DIR, "privacidade.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    print("✔ privacidade.html gerada com sucesso.")

def build_seo_files():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [
        f"{SITE_URL}/index.html",
        f"{SITE_URL}/privacidade.html"
    ] + [f"{SITE_URL}/pais-{c['slug']}.html" for c in COUNTRIES]

    sitemap_entries = "\n".join([
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>hourly</changefreq>\n    <priority>{'1.0' if 'index.html' in u else '0.8'}</priority>\n  </url>"
        for u in urls
    ])

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    robots_txt = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)
    print("✔ sitemap.xml e robots.txt atualizados.")

if __name__ == "__main__":
    start_time = time.time()
    print(f"=== Iniciando atualização completa do {SITE_NAME} ===")
    all_news = collect_all_news()
    build_index(all_news)
    build_country_pages(all_news)
    build_privacy_page()
    build_seo_files()
    elapsed = round(time.time() - start_time, 2)
    print(f"=== Concluído em {elapsed}s! Pronto para envio ao GitHub / Cloudflare Pages. ===")

