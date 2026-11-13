import os
import re
import json
import html
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURAÇÕES GERAIS DO PORTAL (LAYOUT ORIGINAL PRESERVADO)
# ==============================================================================
SITE_NAME = "Global News & Data"
SITE_URL = "https://globalnewsdata.pages.dev"
ADSENSE_PUB_ID = "ca-pub-5379027874215422"
OUTPUT_DIR = "."

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
            "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=pt-BR&gl=BR&ceid=BR:pt-419"
        ]
    },
    "tecnologia": {
        "title": "Tecnologia & IA",
        "icon": "💻",
        "feeds": [
            "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=pt-BR&gl=BR&ceid=BR:pt-419"
        ]
    },
    "vagas": {
        "title": "Vagas & Home Office",
        "icon": "💼",
        "feeds": [
            "https://news.google.com/rss/search?q=vagas+home+office+trabalho+remoto+emprego&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        ]
    },
    "filmes": {
        "title": "Filmes, Séries & Streaming",
        "icon": "🎬",
        "feeds": [
            "https://news.google.com/rss/search?q=filmes+series+netflix+estreias+cinema&hl=pt-BR&gl=BR&ceid=BR:pt-419"
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
        with urllib.request.urlopen(req, timeout=8) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        for item in root.findall('.//item')[:limit]:
            title = item.findtext('title') or "Atualização"
            link = item.findtext('link') or "#"
            pub_date = item.findtext('pubDate') or datetime.now().strftime("%d/%m/%Y")
            desc = clean_html(item.findtext('description') or "")
            source_el = item.find('source')
            source = source_el.text if source_el is not None else "Feed"

            if " - " in title:
                parts = title.rsplit(" - ", 1)
                title = parts[0]
                if source == "Feed":
                    source = parts[1]

            items.append({
                "title": html.escape(title.strip()),
                "link": link.strip(),
                "date": pub_date[:16],
                "desc": html.escape(desc),
                "source": html.escape(source.strip())
            })
    except Exception as e:
        pass
    return items

def collect_all_news():
    news_data = {}
    for cat_key, cat_info in CATEGORIES.items():
        cat_items = []
        seen = set()
        for feed_url in cat_info["feeds"]:
            for art in fetch_rss(feed_url, limit=6):
                if art["title"] not in seen:
                    seen.add(art["title"])
                    cat_items.append(art)
        if not cat_items:
            cat_items.append({
                "title": f"Plantão Global: {cat_info['title']}",
                "link": "#",
                "date": datetime.now().strftime("%d/%m/%Y"),
                "desc": "Acompanhe as principais atualizações e relatórios em tempo real.",
                "source": SITE_NAME
            })
        news_data[cat_key] = cat_items[:8]
    return news_data

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
    <link rel="canonical" href="{SITE_URL}/{canonical_path}">
    
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
    
    <!-- Monetag Multitag Ativa -->
    <script src="https://alwingulla.com/88/tag.min.js" data-zone="90317" async data-cfasync="false"></script>

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
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        a {{ color: inherit; text-decoration: none; }}
        
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
        }}
        .nav-pill:hover {{ border-color: var(--primary); color: var(--primary); }}

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

        .ad-slot {{
            background: var(--surface);
            border: 1px dashed var(--border);
            border-radius: 8px;
            padding: 12px;
            margin: 18px 0;
            text-align: center;
        }}
        .ad-label {{
            font-size: 0.68rem;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}

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
        }}
        .card:hover {{ border-color: var(--primary); }}
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
        }}
        .poll-option:hover {{ border-color: var(--primary); }}
        .poll-bar-bg {{
            height: 6px;
            background: var(--border);
            border-radius: 4px;
            margin-top: 6px;
            overflow: hidden;
        }}
        .poll-bar-fill {{ height: 100%; background: var(--primary); }}
        .country-tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .country-tags a {{
            font-size: 0.8rem;
            background: var(--bg);
            border: 1px solid var(--border);
            padding: 4px 10px;
            border-radius: 6px;
        }}

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

    <div class="container">
        <main>
            {content_html}
        </main>

        <aside>
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

            <div class="ad-slot">
                <span class="ad-label">Publicidade</span>
                <ins class="adsbygoogle"
                     style="display:block; width:100%;"
                     data-ad-client="{ADSENSE_PUB_ID}"
                     data-ad-format="rectangle"
                     data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>

            <div class="widget">
                <h3>🗺️ Dados & Economia por País</h3>
                <div class="country-tags" style="margin-top:8px;">
                    {country_links}
                </div>
            </div>
        </aside>
    </div>

    <footer>
        <p><strong>{SITE_NAME}</strong> — Monitoramento Internacional.</p>
        <p style="margin-top:6px;"><a href="index.html">Início</a> • <a href="sitemap.xml">Sitemap</a> • <a href="privacidade.html">Privacidade</a></p>
    </footer>

    <script type="text/javascript">
        function googleTranslateElementInit() {{
            new google.translate.TranslateElement({{pageLanguage: 'pt', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}}, 'google_translate_element');
        }}
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>

    <script>
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

        async function fetchWeather() {{
            const select = document.getElementById('city-selector');
            const [lat, lon] = select.value.split(',');
            const cityName = select.options[select.selectedIndex].text.split(',')[0];
            try {{
                const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}¤t_weather=true`);
                const data = await res.json();
                document.getElementById('weather-city').innerText = cityName;
                document.getElementById('weather-temp').innerText = `${{Math.round(data.current_weather.temperature)}}°C`;
                document.getElementById('weather-wind').innerText = `Vento: ${{data.current_weather.windspeed}} km/h`;
            }} catch (e) {{
                document.getElementById('weather-temp').innerText = "24°C";
            }}
        }}
        fetchWeather();

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
                        <div class="poll-bar-bg"><div class="poll-bar-fill" style="width:${{pct}}%;"></div></div>
                    </div>
                `;
            }}).join('');
            document.getElementById('poll-status').innerText = `Obrigado pelo voto! Total: ${{total}}.`;
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

def build_index(news_data):
    sections_html = []
    for idx, (cat_key, cat_info) in enumerate(CATEGORIES.items()):
        articles = news_data.get(cat_key, [])
        cards_html = "".join([
            f"""
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
            """ for art in articles
        ])
        
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
        """ if idx in [1, 4] else ""

        sections_html.append(f"""
        <section class="section-block" id="{cat_key}">
            <div class="section-header">
                <h2>{cat_info['icon']} {cat_info['title']}</h2>
            </div>
            <div class="news-grid">{cards_html}</div>
        </section>
        {ad_divider}
        """)

    html_out = get_base_template(
        page_title="Notícias Globais, Economia, Vagas e Dados",
        meta_desc="Portal internacional com notícias em tempo real, clima, vagas e indicadores.",
        canonical_path="index.html",
        content_html="\n".join(sections_html)
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    print("✔ index.html gerado mantendo o layout original.")

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
              "acceptedAnswer": {{"@type": "Answer", "text": "A capital de {c['name']} é {c['capital']} e a moeda é {c['currency']}."}}
            }}
          ]
        }}
        </script>
        """
        content = f"""
        <section class="section-block">
            <div class="section-header"><h2>🏳️ Perfil Econômico: {c['name']}</h2></div>
            <table class="data-table" style="width:100%; border-collapse:collapse; margin-bottom:20px;">
                <tr><th style="padding:10px; border-bottom:1px solid var(--border); text-align:left;">Indicador</th><th style="padding:10px; border-bottom:1px solid var(--border); text-align:left;">Dado</th></tr>
                <tr><td style="padding:10px; border-bottom:1px solid var(--border);">Capital</td><td style="padding:10px; border-bottom:1px solid var(--border);">{c['capital']}</td></tr>
                <tr><td style="padding:10px; border-bottom:1px solid var(--border);">Moeda</td><td style="padding:10px; border-bottom:1px solid var(--border);">{c['currency']}</td></tr>
                <tr><td style="padding:10px; border-bottom:1px solid var(--border);">PIB</td><td style="padding:10px; border-bottom:1px solid var(--border);">{c['gdp']}</td></tr>
            </table>
            <h3 style="margin-bottom:12px;">🌍 Manchetes Internacionais</h3>
            <div class="news-grid">{news_cards}</div>
        </section>
        """
        html_out = get_base_template(f"{c['name']} - Dados", f"Indicadores de {c['name']}", filename, content, faq_schema)
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html_out)
    print("✔ Páginas de países geradas.")

def build_privacy_page():
    content = """<section class="section-block"><div class="section-header"><h2>Privacidade</h2></div><p>Conteúdo protegido e em conformidade.</p></section>"""
    html_out = get_base_template("Privacidade", "Privacidade", "privacidade.html", content)
    with open(os.path.join(OUTPUT_DIR, "privacidade.html"), "w", encoding="utf-8") as f:
        f.write(html_out)

def build_seo_files():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"{SITE_URL}/index.html", f"{SITE_URL}/privacidade.html"] + [f"{SITE_URL}/pais-{c['slug']}.html" for c in COUNTRIES]
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join([f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls]) + '</urlset>'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f: f.write(sitemap)
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f: f.write("User-agent: *\nAllow: /\n")

if __name__ == "__main__":
    news = collect_all_news()
    build_index(news)
    build_country_pages(news)
    build_privacy_page()
    build_seo_files()
    print("=== Atualização concluída com sucesso mantendo o design original! ===")

