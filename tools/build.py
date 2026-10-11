#!/usr/bin/env python3
"""Easy.Finance static site generator. Run: python3 tools/build.py  (outputs to repo root)."""
import os, json, html, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from guides import GUIDES
from calcs import CALCS

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAIN = "https://easy.finance"
TODAY = datetime.date.today()
UPDATED = TODAY.strftime("%B %Y")
INQ = "https://web.works/contact"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
SEARCH = []
PAGES = []

LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#0b1f33"/><path d="M10 27l7-7 5 5 8-10" fill="none" stroke="#3cc9a4" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="30" cy="15" r="3" fill="#c99a2e"/></svg>'

NAV = [("calculators/","Calculators"),("guides/","Guides"),("videos.html","Videos"),("tools.html","Tools"),("support.html","Support Us")]

def esc(s): return html.escape(s, quote=True)

def layout(path, title, desc, body, active="", schema=None, extra_js="", og_type="website", root=None, head_extra=""):
    depth = path.count("/")
    root = "../" * depth if root is None else root
    url = DOMAIN + "/" + (path[:-10] if path.endswith("index.html") else path)
    nav = "".join(f'<a href="{root}{h}"{" aria-current=\"page\"" if active==h else ""}>{t}</a>' for h,t in NAV)
    sch = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    full_title = title if "Easy.Finance" in title else f"{title} | Easy.Finance"
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{head_extra}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Easy.Finance">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1f33">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
{ADS}
{sch}
</head>
<body data-root="{root}">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar" role="note">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership — <a href="{INQ}" target="_blank" rel="noopener">contact us here</a></div>
<header class="site-head"><div class="wrap head-row">
<a class="logo" href="{root}index.html" aria-label="Easy.Finance home">{LOGO}<span>Easy<span class="dot">.</span>Finance</span></a>
<button class="icon-btn menu-btn" aria-label="Open menu" aria-expanded="false">☰</button>
<nav class="nav" aria-label="Main">{nav}<button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode" title="Toggle dark mode"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button><a class="btn btn-primary" href="{root}get-help.html">Get free help</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div id="foot-rich"></div>
<nav class="pill-list" aria-label="Legal" style="margin-top:8px"><a href="{root}about.html">About</a><a href="{root}contact.html">Contact</a><a href="{root}privacy.html">Privacy policy</a><a href="{root}terms.html">Terms</a><a href="{root}disclaimer.html">Disclaimer</a><a href="{root}how-we-make-money.html">How we make money</a><a href="{root}trademark.html">Trademark & copyright</a><a href="{root}sitemap.html">Sitemap</a></nav>
<div class="fine">
<p><b>Disclaimer:</b> Easy.Finance provides general educational information and calculators. It is not financial, investment, tax or legal advice, and we are not a bank, lender, broker or registered adviser. Results are estimates. Some links and referrals may earn us compensation.</p>
<p><b>Trademark notice:</b> Easy.Finance is an independent publication, not affiliated with easyGroup Ltd, easyJet, or any company trading as "EasyFinance", "Easy Finance" or similar. Third-party trademarks and videos belong to their owners.</p>
<p>© <span data-year>{TODAY.year}</span> Easy.Finance. All rights reserved.</p>
</div></div></footer>
<script src="{root}assets/js/config.js"></script>
<script src="{root}assets/js/chrome.js"></script>
<script src="{root}assets/js/search-index.js"></script>
<script src="{root}assets/js/main.js"></script>
{extra_js.replace("{root}", root)}
</body>
</html>'''
    dest = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f: f.write(page)
    PAGES.append(path)

def crumbs(root, items):
    parts = [f'<a href="{root}index.html">Home</a>'] + [f'<a href="{root}{h}">{t}</a>' if h else t for h,t in items]
    return '<div class="breadcrumb">' + " › ".join(parts) + '</div>'

def bc_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":DOMAIN+"/"+h} for i,(h,t) in enumerate([("", "Home")]+items)]}

def faq_html(faq):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q,a in faq)

def faq_schema(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

def video(vid, title, channel, root=""):
    return f'''<button class="video" data-yt="{vid}" aria-label="Play video: {esc(title)}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="play"></span></button>
<div class="video-meta">▶ {esc(title)} — <i>{esc(channel)}</i> · embedded via YouTube</div>'''

CMAP = {c[0]: c for c in CALCS}
GMAP = {g["slug"]: g for g in GUIDES}

def newsletter(root):
    return f'''<section class="section-tight"><div class="wrap"><div class="band">
<div><span class="eyebrow" style="color:#7fe0c4">Free weekly email</span><h2>One money win, every Sunday.</h2><p>A 3-minute email with one practical tip, one calculator trick and one thing to avoid. No spam, unsubscribe anytime, and we never sell your email.</p></div>
<form data-ef-form="Newsletter signup" data-ok="You're in! Watch your inbox on Sunday."><input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="email" name="email" required placeholder="you@example.com" aria-label="Email address"><button class="btn btn-gold" type="submit">Subscribe free</button><div class="form-msg" style="width:100%"></div></form>
</div></div></section>'''

# ---------------- HOME ----------------
def build_home():
    cards = "".join(f'<a class="card" href="calculators/{c[0]}.html"><div class="ico">{c[2]}</div><h3>{c[1].replace(" Calculator","")}</h3><p>{c[4]}</p><span class="more">Calculate →</span></a>' for c in CALCS[:8])
    guides = "".join(f'<a class="card" href="guides/{g["slug"]}.html"><span class="tag">{g["cat"]}</span><h3 style="margin-top:10px">{g["title"]}</h3><p>{g["desc"]}</p><span class="more">Read guide →</span></a>' for g in GUIDES[:6])
    faq = [("Is Easy.Finance really free?","Yes. Every calculator, guide and video is free. We're supported by advertising, optional reader donations, sponsorships and — only if you ask for help — referral fees from partners. See how we make money."),
           ("Is my data saved when I use the calculators?","No. Calculators run entirely in your browser. Nothing you type into a calculator is sent to us."),
           ("Do you give personalised financial advice?","No. We publish education and tools. If you want personalised help, our free request form connects you with relevant professionals or services; you choose whether to proceed."),
           ("Which countries is this for?","Our tools work in multiple currencies (USD, CAD, EUR, GBP, AUD, INR, LKR) and our guides explain principles that apply everywhere, with country notes where rules differ.")]
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Money, made easy</span>
<h1>Smart money decisions, <em>without the jargon.</em></h1>
<p class="lede">Free calculators, plain-English guides and expert help for loans, mortgages, debt, saving, investing and retirement — in your currency.</p>
<form class="search-wrap" role="search"><div class="hero-search"><input data-search type="search" placeholder="Try “mortgage”, “EMI”, “pay off debt”…" aria-label="Search calculators and guides"><button class="btn btn-primary" type="submit">Search</button></div><div class="search-results"></div></form>
<div class="trust-row"><span>100% free</span><span>No sign-up</span><span>Private: runs in your browser</span><span>7 currencies</span></div>
</div>
<div class="hero-card"><h3>Quick mortgage estimate</h3><div data-calc="mortgage" data-compact class="calc" style="grid-template-columns:1fr;gap:12px"></div></div>
</div></section>

<section class="section-tight alt"><div class="wrap">
<div class="center"><span class="eyebrow">Start here</span><h2>What's your next money move?</h2></div>
<div class="chooser" style="margin-top:24px">
<a class="card" href="calculators/home-affordability.html"><div class="ico">🏡</div><h3>Buy a home</h3><p>See what you can afford, estimate payments and compare loan terms.</p><span class="more">Start →</span></a>
<a class="card" href="calculators/debt-payoff.html"><div class="ico">⛰️</div><h3>Get out of debt</h3><p>Build an avalanche or snowball plan and find your debt-free date.</p><span class="more">Start →</span></a>
<a class="card" href="calculators/retirement.html"><div class="ico">🌱</div><h3>Grow my money</h3><p>Plan retirement, model SIPs and see the power of compounding.</p><span class="more">Start →</span></a>
</div></div></section>

<section><div class="wrap">
<div class="stats"><div><b>12+</b><span>free calculators</span></div><div><b>7</b><span>currencies supported</span></div><div><b>0</b><span>sign-ups required</span></div><div><b>100%</b><span>independent & ad-supported</span></div></div>
</div></section>

<section class="alt"><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap"><div><span class="eyebrow">Most-used tools</span><h2>Financial calculators</h2><p class="lede">Instant answers with charts and year-by-year schedules.</p></div><a class="btn btn-ghost" href="calculators/">See all calculators</a></div>
<div class="grid g4" style="margin-top:28px">{cards}</div>
</div></section>

<section><div class="wrap">
<div class="center"><span class="eyebrow">Free expert matching</span><h2>Get help in three simple steps</h2><p class="lede">Tell us what you need. We review every request and point you to a vetted professional or service that fits — at no cost to you.</p></div>
<ol class="steps" style="margin-top:28px"><li><h3>Answer 6 quick questions</h3><p class="notice">About 90 seconds. No credit check and no documents.</p></li><li><h3>We review your request</h3><p class="notice">A real person reads it and identifies the right type of help.</p></li><li><h3>Get your options</h3><p class="notice">We reply within 1 business day. You decide whether to proceed — no obligation.</p></li></ol>
<div class="center" style="margin-top:28px"><a class="btn btn-primary btn-lg" href="get-help.html">Start my free request →</a><p class="notice" style="margin-top:10px">🔒 Encrypted (HTTPS) · We never sell your data without consent</p></div>
</div></section>

<section class="alt"><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap"><div><span class="eyebrow">Learn</span><h2>Plain-English money guides</h2></div><a class="btn btn-ghost" href="guides/">All guides</a></div>
<div class="grid g3" style="margin-top:28px">{guides}</div>
</div></section>

<section><div class="wrap grid g2" style="align-items:center;gap:40px">
<div><span class="eyebrow">Watch & learn</span><h2>Money lessons in minutes</h2><p class="lede">Hand-picked videos from respected educators, paired with our guides and calculators so you can apply each idea immediately.</p><a class="btn btn-primary" href="videos.html">Open the video library</a></div>
<div>{video("Rm6UdfRs3gw","Compound interest introduction","Khan Academy")}</div>
</div></section>

<section class="alt"><div class="wrap grid g2" style="gap:40px;align-items:center">
<div><span class="eyebrow">2-minute quiz</span><h2>How healthy are your finances?</h2><p class="lede">Answer 8 questions and get a score with your top three priorities — and the exact tools to fix them.</p><a class="btn btn-primary" href="money-checkup.html">Take the money check-up</a></div>
<div class="card"><div class="score-ring">78<span style="font-size:1.2rem">/100</span></div><p class="notice">Sample result: “Strong saver — next step: cut card interest and automate investing.”</p><div class="bar"><i style="width:78%;background:var(--brand)"></i></div></div>
</div></section>

<section><div class="wrap">
<div class="grid g3">
<div class="card"><div class="ico">💚</div><h3>Support free finance education</h3><p>Reader support keeps our tools free and ad-light. Every contribution funds new calculators, guides and contests.</p><a class="more" href="support.html">Become a supporter →</a></div>
<div class="card"><div class="ico">🏆</div><h3>Contests & prizes</h3><p>Join our money challenges — share a budget win or a savings tip and compete for prizes.</p><a class="more" href="contests.html">See current challenge →</a></div>
<div class="card"><div class="ico">🤝</div><h3>Partner or advertise</h3><p>Reach readers actively making money decisions with sponsorships, featured placements and partnerships.</p><a class="more" href="advertise.html">Partnership options →</a></div>
</div></div></section>

<section class="alt"><div class="wrap" style="max-width:860px"><div class="center"><span class="eyebrow">FAQ</span><h2>Questions, answered</h2></div><div style="margin-top:24px">{faq_html(faq)}</div></div></section>
{newsletter("")}
'''
    schema = [{"@context":"https://schema.org","@type":"WebSite","name":"Easy.Finance","url":DOMAIN+"/","potentialAction":{"@type":"SearchAction","target":DOMAIN+"/?q={search_term_string}","query-input":"required name=search_term_string"}},
              {"@context":"https://schema.org","@type":"Organization","name":"Easy.Finance","url":DOMAIN+"/","logo":DOMAIN+"/assets/img/favicon.svg"}, faq_schema(faq)]
    layout("index.html","Easy.Finance — Free Financial Calculators, Guides & Expert Help","Free mortgage, loan/EMI, compound interest, retirement and debt payoff calculators, plain-English money guides, and free expert help. Money, made easy.",body,schema=schema,extra_js='<script src="{root}assets/js/calc.js"></script>')
    SEARCH.append({"t":"Home","d":"Easy.Finance home","k":"","u":"index.html"})

# ---------------- CALCULATORS ----------------
def build_calcs():
    cats = {}
    for c in CALCS: cats.setdefault(c[3],[]).append(c)
    blocks = ""
    for cat, items in cats.items():
        blocks += f'<h2 style="margin-top:36px">{cat}</h2><div class="grid g3">' + "".join(f'<a class="card" href="{c[0]}.html"><div class="ico">{c[2]}</div><h3>{c[1]}</h3><p>{c[4]}</p></a>' for c in items) + "</div>"
    body = f'''<div class="wrap">{crumbs("../",[(None,"Calculators")])}</div>
<section class="section-tight"><div class="wrap"><span class="eyebrow">Free tools</span><h1>Financial calculators</h1><p class="lede">Fast, private calculators for every big money decision. Everything runs in your browser — nothing you enter is stored or sent anywhere.</p>{blocks}
<div class="card" style="margin-top:40px;display:flex;gap:20px;align-items:center;flex-wrap:wrap;justify-content:space-between"><div><h3>Numbers done — need a human?</h3><p>Get matched with a relevant professional or service for free.</p></div><a class="btn btn-primary" href="../get-help.html">Get free help →</a></div>
</div></section>{newsletter("../")}'''
    layout("calculators/index.html","Free Financial Calculators","Free mortgage, EMI, compound interest, retirement, SIP, debt payoff, budget, inflation and emergency fund calculators.",body,active="calculators/",schema=[bc_schema([("calculators/","Calculators")])])
    SEARCH.append({"t":"All calculators","d":"Every free financial calculator","k":"tools calculators","u":"calculators/"})
    for slug,title,icon,cat,desc,content,faq in CALCS:
        rel_g = [g for g in GUIDES if slug in g["calcs"]][:3]
        others = [c for c in CALCS if c[3]==cat and c[0]!=slug][:2] + [c for c in CALCS if c[3]!=cat][:4]
        rg = "".join(f'<a class="card" href="../guides/{g["slug"]}.html"><span class="tag">{g["cat"]}</span><h3 style="margin-top:8px;font-size:1.05rem">{g["title"]}</h3></a>' for g in rel_g)
        oc = "".join(f'<a href="{c[0]}.html">{c[2]} {c[1].replace(" Calculator","")}</a>' for c in others[:6])
        body = f'''<div class="wrap">{crumbs("../",[("calculators/","Calculators"),(None,title)])}</div>
<section class="section-tight" style="padding-top:12px"><div class="wrap">
<span class="eyebrow">{icon} {cat} calculator</span><h1>{title}</h1><p class="lede">{desc}</p>
<div class="calc" data-calc="{slug}" style="margin-top:24px"></div>
<div class="article" style="margin-top:56px"><article class="prose"><h2>How this calculator works</h2>{content}
<h2>Frequently asked questions</h2>{faq_html(faq)}
<p class="disclaimer-note">Results are estimates for educational purposes and depend on the assumptions you enter. They are not an offer of credit or financial advice. Last reviewed {UPDATED}.</p></article>
<aside class="toc"><div class="card"><h3 style="font-size:1.05rem">Related guides</h3><div class="grid" style="gap:12px">{rg or '<p class="notice">More guides coming soon.</p>'}</div></div>
<div class="card" style="margin-top:16px;text-align:center"><h3 style="font-size:1.05rem">Want a second opinion?</h3><p class="notice">Free, no-obligation help from a relevant professional.</p><a class="btn btn-primary" style="margin-top:10px" href="../get-help.html?topic={slug}">Get free help</a></div></aside></div>
<h2 style="margin-top:40px;font-size:1.3rem">More calculators</h2><div class="pill-list">{oc}</div>
</div></section>'''
        sch = [bc_schema([("calculators/","Calculators"),(f"calculators/{slug}.html",title)]), faq_schema(faq),
               {"@context":"https://schema.org","@type":"WebApplication","name":title,"applicationCategory":"FinanceApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0"},"url":f"{DOMAIN}/calculators/{slug}.html"}]
        layout(f"calculators/{slug}.html", f"{title} — Free & Instant", desc, body, active="calculators/", schema=sch, extra_js='<script src="{root}assets/js/calc.js"></script>')
        SEARCH.append({"t":title,"d":desc,"k":cat+" "+slug.replace("-"," "),"u":f"calculators/{slug}.html"})

# ---------------- GUIDES ----------------
def build_guides():
    cards = "".join(f'<a class="card" href="{g["slug"]}.html"><div class="ico">{g["icon"]}</div><span class="tag">{g["cat"]}</span><h3 style="margin-top:10px">{g["title"]}</h3><p>{g["desc"]}</p><span class="more">Read →</span></a>' for g in GUIDES)
    body = f'''<div class="wrap">{crumbs("../",[(None,"Guides")])}</div>
<section class="section-tight"><div class="wrap"><span class="eyebrow">Learn</span><h1>Money guides</h1><p class="lede">Clear, practical guides written in plain English. Each one pairs with a calculator so you can apply it to your own numbers.</p>
<div class="grid g3" style="margin-top:28px">{cards}</div></div></section>{newsletter("../")}'''
    layout("guides/index.html","Personal Finance Guides","Plain-English guides on budgeting, credit scores, emergency funds, index funds, mortgages, debt payoff, retirement and compound interest.",body,active="guides/",schema=[bc_schema([("guides/","Guides")])])
    SEARCH.append({"t":"All guides","d":"Plain-English money guides","k":"learn articles","u":"guides/"})
    for g in GUIDES:
        import re
        heads = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', g["body"])
        toc = "".join(f'<a href="#{i}">{t}</a>' for i,t in heads)
        calcs = "".join(f'<a class="card" href="../calculators/{s}.html" style="padding:16px"><b>{CMAP[s][2]} {CMAP[s][1]}</b></a>' for s in g["calcs"])
        vid, vt, vc = g["video"]
        others = "".join(f'<a href="{o["slug"]}.html">{o["icon"]} {o["title"].split(":")[0]}</a>' for o in GUIDES if o is not g)
        words = len(re.sub("<[^>]+>"," ",g["body"]).split())
        body = f'''<div class="wrap">{crumbs("../",[("guides/","Guides"),(None,g["title"].split(":")[0])])}</div>
<section class="section-tight" style="padding-top:12px"><div class="wrap article">
<article class="prose"><span class="eyebrow">{g["icon"]} {g["cat"]}</span><h1>{g["title"]}</h1><p class="lede">{g["desc"]}</p>
<div class="byline"><span>By the Easy.Finance Editorial Team</span><span>Updated {UPDATED}</span><span>{max(3,round(words/220))} min read</span><span><a href="../editorial-guidelines.html">Editorial standards</a></span></div>
<div class="takeaways"><h2>Key takeaways</h2><ul>{"".join(f"<li>{t}</li>" for t in g["take"])}</ul></div>
{g["body"]}
<h2 id="watch">Watch: the 5-minute version</h2>{video(vid,vt,vc)}
<h2 id="faq">FAQ</h2>{faq_html(g["faq"])}
<div class="card" style="margin-top:32px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;justify-content:space-between"><div><h3 style="margin:0">Want help applying this?</h3><p>Get a free, no-obligation match with a relevant expert.</p></div><a class="btn btn-primary" href="../get-help.html?topic={g["calcs"][0]}">Get free help →</a></div>
<p class="disclaimer-note">This guide is general education, not personal financial, tax or legal advice. Rules, rates and limits vary by country and change over time — confirm with official sources or a licensed professional.</p>
<h2 style="font-size:1.3rem">Keep learning</h2><div class="pill-list">{others}</div>
</article>
<aside class="toc"><div class="card"><h3 style="font-size:1rem">On this page</h3><nav>{toc}<a href="#watch">Watch</a><a href="#faq">FAQ</a></nav></div>
<div style="margin-top:16px" class="grid">{calcs}</div></aside>
</div></section>{newsletter("../")}'''
        sch = [bc_schema([("guides/","Guides"),(f"guides/{g['slug']}.html",g["title"])]), faq_schema(g["faq"]),
               {"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["desc"],"dateModified":TODAY.isoformat(),"author":{"@type":"Organization","name":"Easy.Finance Editorial Team"},"publisher":{"@type":"Organization","name":"Easy.Finance"},"mainEntityOfPage":f"{DOMAIN}/guides/{g['slug']}.html"},
               {"@context":"https://schema.org","@type":"VideoObject","name":vt,"description":f"{vt} by {vc}","thumbnailUrl":f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg","embedUrl":f"https://www.youtube-nocookie.com/embed/{vid}","uploadDate":"2020-01-01"}]
        layout(f"guides/{g['slug']}.html", g["title"], g["desc"], body, active="guides/", schema=sch, og_type="article")
        SEARCH.append({"t":g["title"],"d":g["desc"],"k":g["cat"],"u":f"guides/{g['slug']}.html"})

# ---------------- VIDEOS ----------------
def build_videos():
    items = "".join(f'<div class="card" style="padding:16px">{video(*g["video"])}<h3 style="margin-top:12px;font-size:1.05rem">{g["cat"]}</h3><a class="more" href="guides/{g["slug"]}.html">Read the companion guide →</a></div>' for g in GUIDES)
    body = f'''<div class="wrap">{crumbs("",[(None,"Videos")])}</div>
<section class="section-tight"><div class="wrap"><span class="eyebrow">Watch & learn</span><h1>Money video library</h1><p class="lede">Short, trustworthy lessons from respected educators, each paired with an Easy.Finance guide and calculator. Videos load only when you press play, using YouTube's privacy-enhanced mode.</p>
<div class="grid g2" style="margin-top:28px">{items}</div>
<p class="notice" style="margin-top:28px">Videos are embedded with YouTube's official player and remain the property of their creators. Easy.Finance is not affiliated with these channels. Creators who prefer not to be featured can <a href="contact.html">contact us</a>.</p>
</div></section>{newsletter("")}'''
    layout("videos.html","Personal Finance Video Library","Short personal finance video lessons on budgeting, credit, investing, mortgages, debt and retirement — paired with free calculators.",body,active="videos.html")
    SEARCH.append({"t":"Video library","d":"Watch short money lessons","k":"youtube video watch","u":"videos.html"})

# ---------------- GET HELP (lead gen) ----------------
def build_lead():
    needs = [("🏠","Mortgage / home loan"),("💳","Personal or auto loan"),("⛰️","Debt relief & consolidation"),("📈","Credit score repair"),("🌱","Investing & retirement"),("🛡️","Insurance (life, health, home, auto)"),("🧾","Tax filing & planning"),("🧭","Budget & money coaching")]
    amts = ["Under 5,000","5,000 – 25,000","25,000 – 100,000","100,000 – 500,000","500,000+","Not sure yet"]
    credit = [("🌟","Excellent"),("👍","Good"),("🙂","Fair"),("🛠️","Needs work"),("❔","Not sure")]
    when = [("⚡","As soon as possible"),("📅","Within 1–3 months"),("🗓️","3–6 months"),("🔎","Just researching")]
    o = lambda lst: "".join(f'<button type="button" class="opt" data-v="{t}"><span>{i}</span>{t}</button>' for i,t in lst)
    countries = ["United States","Canada","India","United Kingdom","Australia","Sri Lanka","United Arab Emirates","Singapore","Other"]
    body = f'''<section class="hero" style="padding-bottom:24px"><div class="wrap center">
<span class="eyebrow">Free · No obligation · No credit check</span><h1>Get matched with the right money expert</h1><p class="lede">Answer six quick questions. A real person reviews every request and replies within one business day with options from vetted professionals and services.</p></div></section>
<section class="section-tight" style="padding-top:0"><div class="wrap">
<div class="lead" data-lead>
<div class="progress"><i></i></div><div class="step-label"></div>
<div class="lead-body">
<div class="step" data-name="need" data-auto><h2>What can we help you with?</h2><div class="options">{o(needs)}</div></div>
<div class="step" data-name="amount" data-auto><h2>Roughly how much money is involved?</h2><p class="notice">In your local currency.</p><div class="options">{o([("💰",a) for a in amts])}</div></div>
<div class="step" data-name="credit" data-auto><h2>How would you describe your credit?</h2><p class="notice">An estimate is fine — we never pull your credit.</p><div class="options">{o(credit)}</div></div>
<div class="step" data-name="timeline" data-auto><h2>When do you want to act?</h2><div class="options">{o(when)}</div></div>
<div class="step"><h2>Where are you located?</h2><p class="notice">So we only suggest services available to you.</p>
<div class="field"><label for="ld-country">Country</label><select id="ld-country" name="country" required><option value="">Select…</option>{"".join(f"<option>{c}</option>" for c in countries)}</select></div>
<div class="field"><label for="ld-zip">City or postal / ZIP / PIN code</label><input id="ld-zip" name="location" type="text" required maxlength="60" autocomplete="postal-code"></div></div>
<div class="step"><h2>Where should we send your options?</h2>
<div class="grid g2" style="gap:0 16px"><div class="field"><label for="ld-name">Full name</label><input id="ld-name" name="name" type="text" required autocomplete="name" maxlength="80"></div>
<div class="field"><label for="ld-email">Email</label><input id="ld-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="ld-phone">Phone (optional)</label><input id="ld-phone" name="phone" type="tel" autocomplete="tel" maxlength="25"></div>
<div class="field"><label for="ld-time">Best time to reach you</label><select id="ld-time" name="best_time"><option>Any time</option><option>Morning</option><option>Afternoon</option><option>Evening</option><option>Email only, please</option></select></div></div>
<div class="field"><label for="ld-notes">Anything else? (optional)</label><textarea id="ld-notes" name="notes" rows="3" maxlength="1000"></textarea></div>
<label class="consent"><input type="checkbox" name="consent" required> <span>I agree that Easy.Finance may contact me about this request and share my details with up to three relevant partners so they can contact me. I can withdraw consent any time. See the <a href="privacy.html">privacy policy</a>.</span></label>
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true"></div>
</div>
<div class="lead-nav"><button type="button" class="btn btn-ghost" data-back>← Back</button><button type="button" class="btn btn-primary btn-lg" data-next>Continue →</button></div>
<div class="form-msg"></div>
<div class="reassure"><span>🔒 Sent over HTTPS</span><span>✓ 100% free to you</span><span>✓ No credit check</span><span>✓ No obligation</span></div>
</div>
<div class="grid g3" style="margin-top:48px">
<div class="card"><h3>Why use Easy.Finance?</h3><p>We're independent. We don't push one lender or product — we look at what you asked for and suggest options that fit.</p></div>
<div class="card"><h3>How we're paid</h3><p>Some partners pay us a referral fee if you choose to work with them. It never costs you more. <a href="how-we-make-money.html">Details</a>.</p></div>
<div class="card"><h3>Your data</h3><p>We use your details only for this request and share them only with the partners you consent to. We never sell your data to list brokers.</p></div>
</div>
<div style="max-width:860px;margin:48px auto 0"><h2 class="center">Before you submit</h2>{faq_html([("Will this affect my credit score?","No. We never pull your credit. If you later apply with a lender, that lender may run its own check — they'll tell you first."),("How fast will I hear back?","Within one business day, by email (and phone if you asked)."),("Do I have to accept any offer?","No. Every suggestion is optional and there's no obligation."),("Are you a lender or adviser?","No. Easy.Finance is an independent education and referral service. Partners are responsible for their own licensed advice and products.")])}</div>
</div></section>'''
    layout("get-help.html","Get Free Expert Help — Loans, Debt, Mortgages & Investing","Free, no-obligation matching with vetted professionals for mortgages, loans, debt relief, credit repair, investing, insurance and tax. No credit check.",body,active="get-help.html",extra_js='<script src="{root}assets/js/lead.js"></script>')
    SEARCH.append({"t":"Get free expert help","d":"Free matching with vetted professionals","k":"lead help advisor loan quote expert","u":"get-help.html"})

# ---------------- SUPPORT / DONATE ----------------
def build_support():
    body = f'''<section class="hero"><div class="wrap center"><span class="eyebrow">Reader-supported</span><h1>Keep finance education free for everyone</h1><p class="lede">Easy.Finance is independent. Your support funds new calculators, better guides, translation, community contests and the talented people who build them.</p></div></section>
<section class="section-tight" style="padding-top:0"><div class="wrap">
<div class="tiers" id="tiers">
<div class="card tier" data-amt="5"><div class="ico" style="margin:0 auto 10px">☕</div><h3>Coffee</h3><div class="amt">5</div><p>Covers a day of hosting and tools.</p></div>
<div class="card tier sel" data-amt="25"><div class="ico" style="margin:0 auto 10px">📘</div><h3>Supporter</h3><div class="amt">25</div><p>Funds research for one new guide.</p></div>
<div class="card tier" data-amt="100"><div class="ico" style="margin:0 auto 10px">🧮</div><h3>Builder</h3><div class="amt">100</div><p>Helps ship a new calculator.</p></div>
<div class="card tier" data-amt="500"><div class="ico" style="margin:0 auto 10px">🏆</div><h3>Champion</h3><div class="amt">500</div><p>Funds a full contest prize pool. Listed on our supporters wall (optional).</p></div>
</div>
<div class="card" style="margin-top:24px;max-width:760px;margin-left:auto;margin-right:auto">
<h2 style="font-size:1.5rem">Make your contribution</h2>
<div class="amount-row" id="freq"><button type="button" class="sel" data-f="one-time">One-time</button><button type="button" data-f="monthly">Monthly</button></div>
<div class="grid g2" style="gap:0 16px">
<div class="field"><label for="d-amt">Amount</label><input id="d-amt" type="number" min="1" value="25"></div>
<div class="field"><label for="d-cur">Currency</label><select id="d-cur"><option>USD</option><option>CAD</option><option>INR</option><option>EUR</option><option>GBP</option><option>AUD</option><option>LKR</option></select></div>
<div class="field"><label for="d-use">Direct my support to</label><select id="d-use"><option>Where it's needed most</option><option>Day-to-day operations</option><option>Promotion & marketing</option><option>Hiring writers & talent</option><option>Contests & prizes</option></select></div>
<div class="field"><label for="d-name">Name for the supporters wall (optional)</label><input id="d-name" type="text" maxlength="60" placeholder="Anonymous"></div></div>
<div id="pay-buttons" style="display:flex;flex-wrap:wrap;gap:10px"></div>
<form id="pledge" data-ef-form="Donation pledge" data-ok="Thank you! We've received your pledge and will email you a secure payment link within 24 hours." style="margin-top:14px">
<p class="notice" id="pledge-note">Online checkout is being set up. Pledge now and we'll email you a secure payment link — nothing is charged until you confirm.</p>
<input type="hidden" name="amount"><input type="hidden" name="currency"><input type="hidden" name="frequency"><input type="hidden" name="allocation"><input type="hidden" name="display_name">
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="field"><label for="d-email">Your email</label><input id="d-email" type="email" name="email" required></div>
<button class="btn btn-primary btn-lg" type="submit" style="width:100%">Pledge my support 💚</button><div class="form-msg"></div></form>
<p class="notice center" style="margin-top:10px">Contributions support an independent publication and are not tax-deductible charitable donations unless stated otherwise.</p>
</div></div></section>
<section class="alt"><div class="wrap"><div class="center"><span class="eyebrow">Where your money goes</span><h2>Transparent allocation</h2></div>
<div class="alloc" style="margin-top:24px"><div><b>35%</b>Operations, hosting & tools</div><div><b>25%</b>Writers, reviewers & talent</div><div><b>20%</b>Promotion & marketing</div><div><b>15%</b>Contests & prizes</div><div><b>5%</b>Accessibility & translation</div></div>
<p class="notice center" style="margin-top:16px">Target allocation. We publish a short supporter update every quarter.</p></div></section>
<section><div class="wrap grid g3">
<div class="card"><h3>🏢 Corporate sponsorship</h3><p>Sponsor a calculator, guide series or contest season with clear "Sponsored by" credit.</p><a class="more" href="advertise.html">Sponsorship packages →</a></div>
<div class="card"><h3>🏆 Fund a prize</h3><p>Donate a prize — cash, gift cards, courses or software — for our community money challenges.</p><a class="more" href="contests.html">See contests →</a></div>
<div class="card"><h3>🧑‍💻 Give your time</h3><p>Finance writer, reviewer, designer, video creator or translator? Join our talent network.</p><a class="more" href="careers.html">Join the team →</a></div>
</div></section>'''
    js = '''<script>
(function(){var C=window.EF_CONFIG||{},D=C.donate||{},amt=document.getElementById("d-amt"),freq="one-time";
document.querySelectorAll(".tier").forEach(function(t){t.addEventListener("click",function(){document.querySelectorAll(".tier").forEach(function(x){x.classList.remove("sel")});t.classList.add("sel");amt.value=t.dataset.amt})});
document.querySelectorAll("#freq button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll("#freq button").forEach(function(x){x.classList.remove("sel")});b.classList.add("sel");freq=b.dataset.f})});
var pb=document.getElementById("pay-buttons"),links=[["paypal","Donate with PayPal"],["stripe","Pay by card (Stripe)"],["buymeacoffee","Buy us a coffee"]],any=false;
links.forEach(function(l){if(D[l[0]]){any=true;var a=document.createElement("a");a.className="btn btn-primary";a.href=D[l[0]];a.target="_blank";a.rel="noopener";a.textContent=l[1];pb.appendChild(a)}});
if(D.upi){any=true;var u=document.createElement("div");u.className="notice";u.innerHTML="India: pay by UPI to <b>"+D.upi+"</b>";pb.appendChild(u)}
if(any){document.getElementById("pledge-note").textContent="Prefer an invoice or bank transfer? Pledge below and we'll email payment details."}
document.getElementById("pledge").addEventListener("submit",function(){var f=this;f.amount.value=amt.value;f.currency.value=document.getElementById("d-cur").value;f.frequency.value=freq;f.allocation.value=document.getElementById("d-use").value;f.display_name.value=document.getElementById("d-name").value||"Anonymous"},true);
})();</script>'''
    layout("support.html","Support Easy.Finance — Donate & Sponsor","Support free financial education. Donate one-time or monthly, sponsor a contest, or fund new calculators and guides.",body,active="support.html",extra_js=js)
    SEARCH.append({"t":"Support us / donate","d":"Help keep finance education free","k":"donate donation sponsor support","u":"support.html"})

# ---------------- ADVERTISE ----------------
def build_advertise():
    body = f'''<section class="hero"><div class="wrap center"><span class="eyebrow">Advertise · Sponsor · Partner</span><h1>Reach people making real money decisions</h1><p class="lede">Our readers arrive with intent: calculating a mortgage, planning debt payoff, choosing investments. Put your brand in front of them — transparently.</p>
<a class="btn btn-primary btn-lg" href="{INQ}" target="_blank" rel="noopener">Start a conversation →</a></div></section>
<section class="section-tight"><div class="wrap grid g3">
<div class="card"><div class="ico">🧮</div><h3>Calculator sponsorship</h3><p>Exclusive "Sponsored by" placement on a calculator page plus a contextual call-to-action under the result.</p></div>
<div class="card"><div class="ico">📚</div><h3>Guide series sponsorship</h3><p>Sponsor a topic hub (home buying, debt freedom, retirement). Editorial stays independent; your brand gets clear credit.</p></div>
<div class="card"><div class="ico">🏆</div><h3>Contest partner</h3><p>Fund prizes for a money challenge and receive co-branding across the contest page, emails and winner announcements.</p></div>
<div class="card"><div class="ico">📨</div><h3>Newsletter placement</h3><p>A clearly labelled sponsor slot in our weekly email.</p></div>
<div class="card"><div class="ico">🤝</div><h3>Lead partnerships</h3><p>Licensed lenders, advisers, insurers and tax professionals can join our referral network for qualified, consented requests.</p></div>
<div class="card"><div class="ico">🌐</div><h3>Domain & website</h3><p>Interested in acquiring or co-developing Easy.Finance itself? We're open to serious proposals.</p></div>
</div></section>
<section class="alt"><div class="wrap" style="max-width:760px"><h2 class="center">Partnership inquiry</h2><p class="center notice">Or use our main inquiry page: <a href="{INQ}" target="_blank" rel="noopener">web.works/contact</a></p>
<form class="card" data-ef-form="Advertising / partnership inquiry" data-ok="Thanks — we'll reply within 2 business days.">
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="grid g2" style="gap:0 16px"><div class="field"><label for="a-name">Name</label><input id="a-name" name="name" required></div><div class="field"><label for="a-co">Company</label><input id="a-co" name="company" required></div>
<div class="field"><label for="a-email">Work email</label><input id="a-email" type="email" name="email" required></div><div class="field"><label for="a-web">Website</label><input id="a-web" name="website" type="text"></div></div>
<div class="field"><label for="a-int">Interested in</label><select id="a-int" name="interest"><option>Calculator sponsorship</option><option>Guide series sponsorship</option><option>Contest partnership</option><option>Newsletter placement</option><option>Lead / referral partnership</option><option>Domain acquisition</option><option>Website partnership / JV</option><option>Other</option></select></div>
<div class="field"><label for="a-bud">Budget range (optional)</label><select id="a-bud" name="budget"><option>Prefer not to say</option><option>Under $1,000</option><option>$1,000 – $5,000</option><option>$5,000 – $25,000</option><option>$25,000+</option></select></div>
<div class="field"><label for="a-msg">Message</label><textarea id="a-msg" name="message" rows="5" required></textarea></div>
<button class="btn btn-primary btn-lg" type="submit">Send inquiry</button><div class="form-msg"></div></form>
<p class="notice" style="margin-top:16px">All sponsored content is clearly labelled. We don't accept advertising for products we consider predatory (for example payday loans with extreme APRs or unregistered investment schemes). See our <a href="editorial-guidelines.html">editorial guidelines</a>.</p>
</div></section>'''
    layout("advertise.html","Advertise, Sponsor or Partner with Easy.Finance","Sponsorships, calculator placements, contest partnerships, lead partnerships and domain inquiries for Easy.Finance.",body)
    SEARCH.append({"t":"Advertise & partner","d":"Sponsorship and partnership options","k":"advertise sponsor partner domain buy","u":"advertise.html"})

# ---------------- CONTESTS ----------------
def build_contests():
    body = f'''<section class="hero"><div class="wrap center"><span class="eyebrow">Community challenge</span><h1>The Easy.Finance Money Challenge</h1><p class="lede">Share a real money win, a smart budgeting hack or a savings story. The most helpful entries win prizes and get featured to our readers.</p>
<a class="btn btn-primary btn-lg" href="#enter">Enter the challenge →</a></div></section>
<section class="section-tight"><div class="wrap">
<div class="grid g3">
<div class="card"><div class="ico">💡</div><h3>Best money tip</h3><p>Your single most useful, practical money tip in 150 words or fewer.</p></div>
<div class="card"><div class="ico">📊</div><h3>Budget makeover</h3><p>Show your before-and-after budget (no personal account details) and what changed.</p></div>
<div class="card"><div class="ico">🎯</div><h3>Goal smashed</h3><p>Tell us how you paid off a debt or hit a savings goal — and what kept you going.</p></div>
</div>
<h2 style="margin-top:48px">Prizes</h2>
<div class="grid g3"><div class="card center"><div class="big-num">🥇</div><h3>1st place</h3><p>Top prize from the round's prize pool + featured story on Easy.Finance</p></div>
<div class="card center"><div class="big-num">🥈</div><h3>2nd place</h3><p>Runner-up prize + featured tip in our newsletter</p></div>
<div class="card center"><div class="big-num">🥉</div><h3>3rd place</h3><p>Third prize + "Community Pick" badge</p></div></div>
<p class="notice" style="margin-top:12px">Prize values for each round are funded by supporters and sponsors and are announced on this page before the round opens. Want to fund a prize? <a href="support.html">Support us</a> or <a href="advertise.html">become a contest partner</a>.</p>
</div></section>
<section class="alt" id="enter"><div class="wrap" style="max-width:760px"><h2 class="center">Submit your entry</h2>
<form class="card" data-ef-form="Contest entry" data-ok="Entry received — good luck! We'll email you if you're shortlisted.">
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="grid g2" style="gap:0 16px"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required></div><div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required></div>
<div class="field"><label for="c-country">Country</label><input id="c-country" name="country" required></div><div class="field"><label for="c-cat">Category</label><select id="c-cat" name="category"><option>Best money tip</option><option>Budget makeover</option><option>Goal smashed</option></select></div></div>
<div class="field"><label for="c-title">Entry title</label><input id="c-title" name="title" required maxlength="100"></div>
<div class="field"><label for="c-entry">Your entry</label><textarea id="c-entry" name="entry" rows="7" required maxlength="3000"></textarea><div class="hint">Do not include account numbers, ID numbers or anyone else's private information.</div></div>
<label class="consent"><input type="checkbox" name="age_confirm" required> <span>I confirm I am 18 or older (or the age of majority where I live).</span></label>
<label class="consent"><input type="checkbox" name="rules_accept" required> <span>I accept the official rules below and allow Easy.Finance to publish my entry with my first name and country.</span></label>
<button class="btn btn-primary btn-lg" type="submit">Submit entry</button><div class="form-msg"></div></form></div></section>
<section><div class="wrap" style="max-width:860px"><h2>Official rules (summary)</h2><div class="prose">
<ol><li><b>No purchase or donation necessary</b> to enter or win. A donation does not improve your chances.</li>
<li><b>Eligibility:</b> open to individuals aged 18+ (or the age of majority in their jurisdiction). Void where prohibited or restricted by law. Employees and immediate family of Easy.Finance are not eligible.</li>
<li><b>Entry period:</b> each round's start and end dates are posted on this page. One entry per person per category per round.</li>
<li><b>Judging:</b> winners are selected by an editorial panel based on usefulness (40%), originality (30%), clarity (20%) and real-world impact (10%). This is a contest of skill, not a lottery.</li>
<li><b>Prizes:</b> as announced for the round; non-transferable; may be substituted with a prize of equal or greater value. Winners are responsible for any taxes. Some jurisdictions (for example Quebec, Canada) may require a skill-testing question or additional registration.</li>
<li><b>Notification:</b> winners are contacted by email and must respond within 14 days.</li>
<li><b>Content:</b> entries must be original and your own. You keep copyright and grant Easy.Finance a non-exclusive licence to publish and edit your entry for length and clarity.</li>
<li><b>Privacy:</b> entry details are handled under our <a href="privacy.html">privacy policy</a>.</li></ol></div></div></section>'''
    layout("contests.html","Money Challenge Contests & Prizes","Enter the Easy.Finance Money Challenge: share your best money tip, budget makeover or savings win and compete for prizes.",body)
    SEARCH.append({"t":"Contests & prizes","d":"Enter the Money Challenge","k":"contest prize win challenge","u":"contests.html"})

# ---------------- CAREERS ----------------
def build_careers():
    roles = [("✍️","Freelance finance writer","Write clear, accurate guides. Strong research and plain-English skills required; finance qualifications a plus."),
             ("🎓","Credentialed reviewer (CFP, CFA, CPA, CA or equivalent)","Review guides and calculators for accuracy. Part-time, remote, paid per review."),
             ("🎬","Short-form video creator","Turn our guides into engaging 60-second explainers for YouTube Shorts, Reels and TikTok."),
             ("📈","SEO & growth marketer","Grow organic traffic with keyword research, technical SEO and partnerships."),
             ("🧑‍💻","Front-end developer","Build new calculators and interactive tools in vanilla JavaScript."),
             ("🌍","Translator (Hindi, French, Spanish, Sinhala)","Localise top guides and calculators for new audiences.")]
    rc = "".join(f'<div class="card"><div class="ico">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i,t,d in roles)
    opts = "".join(f"<option>{t}</option>" for _,t,_ in roles)
    body = f'''<section class="hero"><div class="wrap center"><span class="eyebrow">Careers & talent network</span><h1>Help millions make easier money decisions</h1><p class="lede">We're a remote-first team. Join our talent network for paid, flexible projects.</p></div></section>
<section class="section-tight"><div class="wrap"><div class="grid g3">{rc}</div></div></section>
<section class="alt"><div class="wrap" style="max-width:760px"><h2 class="center">Apply / join the network</h2>
<form class="card" data-ef-form="Talent application" data-ok="Thanks for applying! We review applications weekly and will be in touch if there's a fit.">
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="grid g2" style="gap:0 16px"><div class="field"><label for="t-name">Name</label><input id="t-name" name="name" required></div><div class="field"><label for="t-email">Email</label><input id="t-email" type="email" name="email" required></div>
<div class="field"><label for="t-role">Role</label><select id="t-role" name="role">{opts}<option>Other</option></select></div><div class="field"><label for="t-loc">Location / time zone</label><input id="t-loc" name="location" required></div></div>
<div class="field"><label for="t-link">Portfolio, LinkedIn or work samples (URL)</label><input id="t-link" name="portfolio" type="url" placeholder="https://"></div>
<div class="field"><label for="t-msg">Tell us about yourself</label><textarea id="t-msg" name="about" rows="5" required maxlength="2000"></textarea></div>
<button class="btn btn-primary btn-lg" type="submit">Send application</button><div class="form-msg"></div></form>
<p class="notice center">We're an equal-opportunity collaborator. We'll never ask you to pay to apply.</p></div></section>'''
    layout("careers.html","Careers & Talent Network","Join the Easy.Finance remote talent network: finance writers, credentialed reviewers, video creators, SEO, developers and translators.",body)
    SEARCH.append({"t":"Careers","d":"Join our talent network","k":"jobs hiring work writer careers","u":"careers.html"})

# ---------------- TOOLS / GLOSSARY / QUIZ ----------------
GLOSS = [("Amortisation","Paying off a loan through scheduled payments that cover interest and gradually reduce principal."),("APR","Annual percentage rate — the yearly cost of borrowing, including certain fees."),("APY","Annual percentage yield — the yearly return on savings including compounding."),("Asset allocation","How your investments are divided among stocks, bonds, cash and other assets."),("Balance transfer","Moving debt from one credit card to another, often for a lower promotional rate."),("Bond","A loan you make to a government or company in exchange for interest payments."),("Budget","A plan that assigns your income to spending, saving and debt repayment."),("Capital gain","Profit from selling an asset for more than you paid."),("CIBIL score","A widely used Indian credit score from 300 to 900."),("Compound interest","Interest earned on both the original amount and previously earned interest."),("Credit utilisation","The share of available revolving credit you're using."),("Debt-to-income ratio (DTI)","Monthly debt payments divided by gross monthly income."),("Diversification","Spreading money across many investments to reduce risk."),("Dividend","A share of company profits paid to shareholders."),("Down payment","The upfront portion of a purchase price you pay in cash."),("EMI","Equated monthly instalment — a fixed monthly loan payment."),("Emergency fund","Cash set aside for unexpected essential expenses."),("ETF","Exchange-traded fund — a basket of investments that trades like a stock."),("Expense ratio","The annual fee a fund charges, as a percentage of assets."),("FICO score","A widely used US credit score from 300 to 850."),("Fixed rate","An interest rate that doesn't change over the agreed term."),("Index fund","A fund that tracks a market index such as the S&P 500 or Nifty 50."),("Inflation","The general rise in prices that reduces purchasing power."),("Liquidity","How quickly an asset can be turned into cash without loss."),("LTV","Loan-to-value — loan amount divided by property value."),("Mutual fund","A pooled investment managed by a fund company."),("Net worth","Everything you own minus everything you owe."),("Principal","The original amount borrowed or invested."),("Rebalancing","Adjusting a portfolio back to its target allocation."),("Refinancing","Replacing an existing loan with a new one, usually for better terms."),("Roth IRA","A US retirement account funded with after-tax money that can grow tax-free."),("RRSP","Canada's Registered Retirement Savings Plan."),("Rule of 72","72 divided by the annual rate ≈ years for money to double."),("Sinking fund","Money saved in advance for a known future expense."),("SIP","Systematic investment plan — fixed regular investing into a fund."),("Snowball method","Paying off the smallest debt balance first."),("Avalanche method","Paying off the highest-interest debt first."),("TFSA","Canada's Tax-Free Savings Account."),("Variable rate","An interest rate that moves with a benchmark."),("401(k)","A US employer-sponsored retirement plan.")]

def build_tools():
    gl = sorted(GLOSS, key=lambda x: x[0].lower().lstrip("0123456789("))
    letters = sorted({g[0][0].upper() for g in gl if g[0][0].isalpha()})
    dl = ""
    cur=None
    for t,d in gl:
        L = t[0].upper() if t[0].isalpha() else "#"
        anchor = f' id="l-{L}"' if L!=cur else ""
        cur=L
        dl += f'<dt{anchor}>{t}</dt><dd>{d}</dd>'
    body = f'''<div class="wrap">{crumbs("",[(None,"Glossary")])}</div><section class="section-tight"><div class="wrap" style="max-width:860px"><span class="eyebrow">Reference</span><h1>Finance glossary</h1><p class="lede">{len(GLOSS)} essential money terms in one sentence each.</p>
<div class="az">{"".join(f'<a href="#l-{l}">{l}</a>' for l in letters)}</div><dl class="gloss">{dl}</dl></div></section>'''
    sch = [{"@context":"https://schema.org","@type":"DefinedTermSet","name":"Easy.Finance glossary","hasDefinedTerm":[{"@type":"DefinedTerm","name":t,"description":d} for t,d in GLOSS]}]
    layout("glossary.html","Finance Glossary — Money Terms Explained Simply","Plain-English definitions of APR, EMI, compound interest, index funds, credit utilisation, DTI, SIP and more.",body,active="tools.html",schema=sch)
    SEARCH.append({"t":"Finance glossary","d":"Money terms explained","k":" ".join(t for t,_ in GLOSS),"u":"glossary.html"})

    qs = [("Do you have an emergency fund covering at least 3 months of essential expenses?",["Yes, 3+ months","1–3 months","Less than 1 month"],"emergency-fund"),
          ("Do you pay your credit card balance in full each month?",["Always / no cards","Sometimes","Rarely — I carry a balance"],"credit-card-payoff"),
          ("What share of take-home pay do you save or invest?",["15% or more","5–15%","Under 5%"],"budget"),
          ("Do you have any debt above 10% interest?",["None","Some, with a plan","Yes, and no plan"],"debt-payoff"),
          ("Are you contributing to a retirement account?",["Yes, regularly","Occasionally","Not yet"],"retirement"),
          ("Do you use a budget or spending plan?",["Yes, and I review it","Loosely","No"],"budget"),
          ("Do you know your credit score?",["Yes, and it's good","Yes, it needs work","No idea"],"credit-card-payoff"),
          ("Do you have adequate insurance (health, and life if others depend on you)?",["Yes","Partly","No"],"savings-goal")]
    qh = "".join(f'<div class="q card" data-tool="{tool}"><p>{i+1}. {q}</p><div class="options">' + "".join(f'<button type="button" class="opt" data-s="{2-j}">{a}</button>' for j,a in enumerate(opts)) + '</div></div>' for i,(q,opts,tool) in enumerate(qs))
    body = f'''<div class="wrap">{crumbs("",[(None,"Money check-up")])}</div><section class="section-tight"><div class="wrap" style="max-width:820px"><span class="eyebrow">2-minute quiz</span><h1>Money check-up</h1><p class="lede">Eight questions. Instant score. Your top priorities and the tools to fix them. Your answers stay in your browser.</p>
<div id="quiz" style="margin-top:24px">{qh}</div><button class="btn btn-primary btn-lg" id="q-go" disabled>See my score</button>
<div id="q-res" class="card" style="display:none;margin-top:24px"></div></div></section>'''
    js = '''<script>(function(){var Q=document.querySelectorAll("#quiz .q"),go=document.getElementById("q-go"),R=document.getElementById("q-res");
var names={"emergency-fund":"Emergency Fund Calculator","credit-card-payoff":"Credit Card Payoff Calculator",budget:"50/30/20 Budget Calculator","debt-payoff":"Debt Payoff Calculator",retirement:"Retirement Calculator","savings-goal":"Savings Goal Calculator"};
document.getElementById("quiz").addEventListener("click",function(e){var o=e.target.closest(".opt");if(!o)return;var q=o.closest(".q");q.querySelectorAll(".opt").forEach(function(x){x.classList.remove("sel")});o.classList.add("sel");go.disabled=document.querySelectorAll("#quiz .opt.sel").length<Q.length});
go.addEventListener("click",function(){var s=0,weak=[];Q.forEach(function(q){var v=+q.querySelector(".sel").dataset.s;s+=v;if(v<2)weak.push([v,q.dataset.tool])});
var score=Math.round(s/(Q.length*2)*100),label=score>=80?"Strong foundation":score>=55?"Solid — with clear upgrades":"Time for a reset — you've got this";
weak.sort(function(a,b){return a[0]-b[0]});var seen={},top=weak.filter(function(w){if(seen[w[1]])return false;seen[w[1]]=1;return true}).slice(0,3);
R.style.display="block";R.innerHTML='<div class="score-ring">'+score+'<span style="font-size:1.2rem">/100</span></div><h2>'+label+'</h2><div class="bar"><i style="width:'+score+'%;background:var(--brand)"></i></div>'+(top.length?'<h3 style="margin-top:18px">Your top priorities</h3><ol>'+top.map(function(t){return '<li><a href="calculators/'+t[1]+'.html">'+names[t[1]]+'</a></li>'}).join("")+'</ol>':'<p>Excellent — keep automating and review once a year.</p>')+'<a class="btn btn-primary" href="get-help.html">Get a free expert review →</a>';R.scrollIntoView({behavior:"smooth"})});})();</script>'''
    layout("money-checkup.html","Money Check-Up: Free Financial Health Quiz","Take the free 2-minute financial health quiz. Get a score out of 100, your top three priorities, and tools to fix them.",body,active="tools.html",extra_js=js)
    SEARCH.append({"t":"Money check-up quiz","d":"Financial health score in 2 minutes","k":"quiz test score health","u":"money-checkup.html"})

    allc = "".join(f'<a class="card" href="calculators/{c[0]}.html"><div class="ico">{c[2]}</div><h3>{c[1]}</h3></a>' for c in CALCS)
    body = f'''<div class="wrap">{crumbs("",[(None,"Tools")])}</div><section class="section-tight"><div class="wrap"><span class="eyebrow">Toolbox</span><h1>Money tools</h1><p class="lede">Everything interactive on Easy.Finance in one place.</p>
<div class="grid g3" style="margin-top:24px"><a class="card" href="money-checkup.html"><div class="ico">🩺</div><h3>Money check-up quiz</h3><p>Score your finances in 2 minutes.</p></a><a class="card" href="glossary.html"><div class="ico">📖</div><h3>Finance glossary</h3><p>{len(GLOSS)} terms, one sentence each.</p></a><a class="card" href="get-help.html"><div class="ico">🤝</div><h3>Free expert match</h3><p>Get help from a relevant professional.</p></a></div>
<h2 style="margin-top:40px">All calculators</h2><div class="grid g4">{allc}</div></div></section>'''
    layout("tools.html","Money Tools Hub","All free Easy.Finance money tools: calculators, financial health quiz, glossary and expert matching.",body,active="tools.html")
    SEARCH.append({"t":"Tools hub","d":"All interactive tools","k":"tools","u":"tools.html"})

# ---------------- COMPANY & LEGAL ----------------
def simple(path, title, desc, inner, key=""):
    body = f'<div class="wrap">{crumbs("",[(None,title)])}</div><section class="section-tight"><div class="wrap prose" style="max-width:820px"><h1>{title}</h1><p class="notice">Last updated: {TODAY.strftime("%B %d, %Y")}</p>{inner}</div></section>'
    layout(path, title, desc, body)
    SEARCH.append({"t":title,"d":desc,"k":key,"u":path})

def build_legal():
    simple("about.html","About Easy.Finance","Easy.Finance is an independent personal finance publication offering free calculators, plain-English guides and free expert matching.",f'''
<p class="lede">Money shouldn't need a dictionary. Easy.Finance exists to make everyday financial decisions clear, fast and free.</p>
<h2>What we do</h2><ul><li><b>Free calculators</b> for mortgages, loans and EMIs, compound interest, SIPs, retirement, debt payoff, budgeting, inflation and emergency funds — in seven currencies.</li><li><b>Plain-English guides</b> that explain the "why" and the "how", each paired with a tool.</li><li><b>Free expert matching</b> for readers who want personalised help from a professional.</li><li><b>Community challenges</b> that reward practical money wisdom.</li></ul>
<h2>Our principles</h2><ol><li><b>Independent:</b> no lender, bank or fund owns us.</li><li><b>Transparent:</b> we explain exactly <a href="how-we-make-money.html">how we make money</a>.</li><li><b>Private by default:</b> calculators run in your browser; we don't store what you type.</li><li><b>Accurate:</b> we follow published <a href="editorial-guidelines.html">editorial guidelines</a> and correct errors quickly.</li><li><b>Global:</b> principles that work everywhere, with local notes where rules differ.</li></ol>
<h2>Who's behind it</h2><p>Easy.Finance is published by the Webworks Media Network, an independent digital publisher. Content is produced by the Easy.Finance Editorial Team.</p>
<h2>Get in touch</h2><p>Use our <a href="contact.html">contact form</a>. For sponsorship, advertising, partnership or domain inquiries, visit <a href="{INQ}" target="_blank" rel="noopener">web.works/contact</a>.</p>''',"about company team")
    simple("contact.html","Contact Us","Contact Easy.Finance with questions, corrections, partnership or advertising inquiries.",f'''
<p class="lede">We read every message. Typical reply time: 1–2 business days.</p>
<div class="callout"><b>Interested in this website, the domain name, sponsorship, advertising or partnership?</b> Please use <a href="{INQ}" target="_blank" rel="noopener">web.works/contact</a> for the fastest response.</div>
<form class="card" data-ef-form="Contact form" data-ok="Thanks — your message has been sent. We'll reply soon.">
<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required maxlength="80"></div>
<div class="field"><label for="ct-email">Email</label><input id="ct-email" type="email" name="email" required></div>
<div class="field"><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Report an error / correction</option><option>Suggest a calculator or guide</option><option>Privacy request</option><option>Advertising / sponsorship</option><option>Partnership</option><option>Domain / website acquisition</option><option>Press</option></select></div>
<div class="field"><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" rows="6" required maxlength="4000"></textarea></div>
<button class="btn btn-primary btn-lg" type="submit">Send message</button><div class="form-msg"></div></form>
<p class="notice">Please don't send account numbers, passwords or government ID numbers. We can't give personalised financial advice by message — for that, use <a href="get-help.html">Get free help</a>.</p>''',"contact email message")
    simple("how-we-make-money.html","How We Make Money","How Easy.Finance is funded: advertising, referral fees, reader support and sponsorships — and how we protect editorial independence.",'''
<p>Easy.Finance is free to use. Here's exactly how we keep it that way.</p>
<h2>1. Advertising</h2><p>We display ads served by Google AdSense and possibly other networks. Ad networks may use cookies to show relevant ads. Ads are visually separate from content and we don't control which specific ads appear. See our <a href="cookies.html">cookie policy</a>.</p>
<h2>2. Referral fees</h2><p>When you submit a <a href="get-help.html">free help request</a> and consent, we may share your details with relevant partners. Some partners pay us a fee for introductions or if you become their customer. You never pay more because of this.</p>
<h2>3. Reader support</h2><p>Readers can <a href="support.html">contribute</a> one-time or monthly to fund operations, promotion, hiring and contest prizes.</p>
<h2>4. Sponsorships & partnerships</h2><p>Brands may sponsor calculators, guide series, newsletters or contests. Sponsored placements are always labelled "Sponsored" or "Sponsored by".</p>
<h2>Editorial independence</h2><p>Advertisers, partners and supporters do not review or approve our editorial content, calculator logic or rankings. Compensation never determines what we say a product is good or bad at. Read our <a href="editorial-guidelines.html">editorial guidelines</a>.</p>''',"advertiser disclosure affiliate compensation")
    simple("editorial-guidelines.html","Editorial Guidelines","Easy.Finance's standards for accuracy, sourcing, independence, corrections and updates.",'''
<h2>Accuracy & sourcing</h2><p>We base guides on primary sources wherever possible — government and regulator websites, central banks, official tax authorities and peer-reviewed research. Figures, limits and rules are checked before publication and at each review.</p>
<h2>Calculator methodology</h2><p>Every calculator uses standard, documented financial formulas, explained on the calculator page. We test calculators against independent reference results before publishing.</p>
<h2>Independence</h2><p>Commercial relationships never influence our editorial content. Sponsored content is clearly labelled and written separately from editorial guides.</p>
<h2>Plain English</h2><p>We avoid jargon. When a technical term is needed, we define it or link to our <a href="glossary.html">glossary</a>.</p>
<h2>Reviews & updates</h2><p>Guides show a "last updated" date and are reviewed regularly, and immediately when rules change.</p>
<h2>Corrections</h2><p>Found an error? <a href="contact.html">Tell us</a>. We correct material errors promptly and note significant corrections on the page.</p>
<h2>Not advice</h2><p>Our content is educational. It isn't personalised financial, investment, tax or legal advice. See our <a href="disclaimer.html">disclaimer</a>.</p>''',"editorial standards corrections")
    simple("privacy.html","Privacy Policy","How Easy.Finance collects, uses and protects personal information, including cookies and Google AdSense advertising.",'''
<p>This policy explains what information Easy.Finance ("we", "us") collects, why, and your choices.</p>
<h2>Information you give us</h2><ul><li><b>Forms</b> (contact, help requests, newsletter, contest entries, applications, pledges): the details you enter, such as name, email, phone, location and your message.</li><li>We use this information only to respond, provide the service you asked for, and — for help requests where you consent — share it with up to three relevant partners.</li></ul>
<h2>Information we don't collect</h2><p>Numbers you enter into calculators and the money check-up quiz stay in your browser and are not sent to us.</p>
<h2>Automatically collected information</h2><p>Like most websites, our hosting provider and advertising partners may receive standard technical data such as IP address, browser type, device, pages visited and referring URL.</p>
<h2>Cookies and advertising</h2><ul><li>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites.</li><li>Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this and/or other sites on the Internet.</li><li>You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>.</li><li>Learn how Google uses information from sites that use its services at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">policies.google.com/technologies/partner-sites</a>.</li></ul>
<h2>Service providers</h2><p>We use trusted providers to operate the site: GitHub Pages (hosting), FormSubmit (form delivery), Google AdSense (advertising), Google Fonts (typography) and YouTube (embedded videos in privacy-enhanced mode, loaded only when you press play).</p>
<h2>Legal bases (EEA/UK)</h2><p>We process data based on your consent, to respond to your requests, and for our legitimate interest in operating and improving the site.</p>
<h2>Your rights</h2><p>Depending on where you live (including under GDPR, UK GDPR, CCPA/CPRA, PIPEDA, Quebec Law 25 and India's DPDP Act), you may have rights to access, correct, delete or port your data, to withdraw consent and to opt out of sale or sharing. To make a request, use our <a href="contact.html">contact form</a> and choose "Privacy request".</p>
<h2>Retention</h2><p>We keep form submissions only as long as needed for the purpose they were provided, typically no longer than 24 months.</p>
<h2>Children</h2><p>Easy.Finance is not directed to children under 13 (or the applicable minimum age), and we do not knowingly collect their data.</p>
<h2>Security</h2><p>The site is served over HTTPS. No method of transmission is perfectly secure, so please don't submit sensitive data such as account or ID numbers.</p>
<h2>Changes</h2><p>We'll post updates here with a new "last updated" date.</p>''',"privacy gdpr data cookies")
    simple("cookies.html","Cookie Policy","What cookies Easy.Finance and its partners use, and how to control them.",'''
<h2>What are cookies?</h2><p>Small text files stored by your browser that help websites remember information.</p>
<h2>Cookies we use</h2><ul><li><b>Essential / preference (local storage):</b> remember your theme, preferred currency and cookie choice. These never leave your device.</li><li><b>Advertising:</b> Google AdSense and its partners may set cookies to serve and measure ads, limit repetition and prevent fraud.</li><li><b>Embedded content:</b> YouTube videos load in privacy-enhanced mode only when you press play; YouTube may then set its own cookies.</li></ul>
<h2>Your choices</h2><ul><li>Use the cookie notice to accept all or essential only.</li><li>Manage personalised ads at <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>.</li><li>Block or delete cookies in your browser settings.</li><li>Visitors in the EEA, UK and Switzerland will be shown a Google-certified consent message where required.</li></ul>''',"cookies consent")
    simple("terms.html","Terms of Use","The terms governing your use of Easy.Finance.",'''
<h2>Acceptance</h2><p>By using Easy.Finance you agree to these terms. If you don't agree, please don't use the site.</p>
<h2>Educational purpose</h2><p>All content and calculators are for general information and education. Nothing on the site is financial, investment, tax, legal or credit advice, or an offer or solicitation to buy or sell any product. See our <a href="disclaimer.html">disclaimer</a>.</p>
<h2>No warranty</h2><p>We aim for accuracy but provide the site "as is", without warranties of any kind. Calculator results are estimates based on your inputs and simplified assumptions.</p>
<h2>Limitation of liability</h2><p>To the fullest extent permitted by law, Easy.Finance and its publisher are not liable for any loss arising from use of the site or reliance on its content.</p>
<h2>Third parties</h2><p>We may link to or refer you to third-party sites and partners. We're not responsible for their content, products, services or policies.</p>
<h2>Your submissions</h2><p>You're responsible for the accuracy of information you submit. Don't submit unlawful, infringing or sensitive information. Contest entries are governed by the <a href="contests.html">contest rules</a>.</p>
<h2>Intellectual property</h2><p>Site content, design, code and calculators are © Easy.Finance unless otherwise noted. You may share links and short quotes with attribution. See our <a href="trademark.html">trademark & copyright notice</a>.</p>
<h2>Acceptable use</h2><p>Don't scrape, overload, attempt to breach or misuse the site or its forms.</p>
<h2>Changes</h2><p>We may update these terms; continued use means acceptance of the updated terms.</p>''',"terms conditions legal")
    simple("disclaimer.html","Disclaimer","Easy.Finance content is educational, not financial advice.",'''
<p><b>Easy.Finance is not a bank, lender, broker, insurer, investment adviser, tax preparer or law firm.</b></p>
<p>Information on this website is general and educational. It does not consider your personal circumstances and is not a recommendation to buy, sell or hold any product. Interest rates, tax rules, contribution limits and regulations vary by country and change frequently.</p>
<p>Calculator results are estimates based on the information you enter and on simplifying assumptions (for example, constant rates of return and fixed interest rates). Actual results will differ.</p>
<p>Investing involves risk, including possible loss of principal. Past performance does not guarantee future results.</p>
<p>Before making financial decisions, consult a qualified, licensed professional in your jurisdiction. Partner professionals introduced through our free help service are independent and solely responsible for their own advice, products and licensing.</p>
<p>Embedded videos are created by independent third parties; their views are their own.</p>''',"disclaimer not advice")
    simple("trademark.html","Trademark & Copyright Disclosure","Easy.Finance trademark, copyright and non-affiliation disclosure.",f'''
<h2>Independence and non-affiliation</h2><p>Easy.Finance (easy.finance) is an independent personal-finance publication. It is <b>not affiliated with, endorsed by, sponsored by or connected to</b>:</p>
<ul><li>easyGroup Ltd, easyJet plc, or any other member or licensee of the "easy" family of brands;</li><li>any company, app or service trading as "EasyFinance", "Easy Finance", "Easy-Finance", "EZ Finance" or any similar name, in any country.</li></ul>
<p>The name "Easy.Finance" is used descriptively — to describe making finance easy — and as the name of this domain. We do not use, imitate or reference any third-party logo, colour scheme or trade dress.</p>
<h2>Third-party trademarks</h2><p>Product names, company names, index names (such as S&amp;P 500, Nifty 50, S&amp;P/TSX), credit scoring models (such as FICO, VantageScore, CIBIL) and account types mentioned on this site are trademarks or registered trademarks of their respective owners. Their mention is for identification and educational purposes only and does not imply endorsement.</p>
<h2>Embedded media</h2><p>Videos are embedded using YouTube's official embed player and remain the copyright of their creators. Easy.Finance does not host, copy or claim ownership of them. Creators can request removal via our <a href="contact.html">contact form</a>.</p>
<h2>Our copyright</h2><p>All original text, calculators, code, graphics and design on Easy.Finance are © {TODAY.year} Easy.Finance, all rights reserved, unless otherwise stated.</p>
<h2>Infringement notices (DMCA and equivalents)</h2><p>If you believe content on this site infringes your rights, please send a notice through our <a href="contact.html">contact form</a> (topic: "Report an error") including: identification of the work, the URL of the material, your contact details, a good-faith statement and a statement of accuracy. We respond promptly and remove infringing material.</p>''',"trademark copyright dmca affiliation")
    simple("accessibility.html","Accessibility Statement","Our commitment to making Easy.Finance usable by everyone.",'''
<p>We aim to meet WCAG 2.2 Level AA. The site supports keyboard navigation, visible focus states, a skip link, sufficient colour contrast, dark mode, reduced-motion-friendly design, responsive layouts from 320px wide, labelled form fields and live-updating calculator results announced to screen readers.</p>
<p>If you find a barrier, please <a href="contact.html">tell us</a> and we'll fix it.</p>''',"accessibility wcag")

def build_404_sitemap():
    body = '''<section class="hero"><div class="wrap center"><div style="font-size:4rem">🧭</div><h1>Page not found</h1><p class="lede">This page may have moved. Try a search, or start with our most popular tools.</p>
<form class="search-wrap" role="search" style="margin:20px auto"><div class="hero-search" style="margin:0 auto"><input data-search type="search" placeholder="Search tools & guides" aria-label="Search"><button class="btn btn-primary" type="submit">Search</button></div><div class="search-results"></div></form>
<div class="pill-list" style="justify-content:center"><a href="calculators/">Calculators</a><a href="guides/">Guides</a><a href="get-help.html">Get help</a></div></div></section>'''
    base = "<script>document.write('<base href=\"'+(/github\\.io$/.test(location.hostname)?'/easyfinance-com/':'/')+'\">')</script>"
    layout("404.html","Page Not Found","The page you were looking for could not be found.",body,head_extra=base,root="")
    PAGES.remove("404.html")
    links = "".join(f'<li><a href="{s["u"]}">{s["t"]}</a></li>' for s in SEARCH)
    simple("sitemap.html","Sitemap","Every page on Easy.Finance.",f"<ul>{links}</ul>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in PAGES:
        u = DOMAIN + "/" + (p[:-10] if p.endswith("index.html") else p)
        pr = "1.0" if p=="index.html" else "0.9" if p.startswith(("calculators","guides")) or p=="get-help.html" else "0.5"
        xml += f"  <url><loc>{u}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{pr}</priority></url>\n"
    xml += "</urlset>\n"
    open(os.path.join(OUT,"sitemap.xml"),"w").write(xml)
    with open(os.path.join(OUT,"assets/js/search-index.js"),"w",encoding="utf-8") as f:
        f.write("window.EF_SEARCH="+json.dumps(SEARCH,ensure_ascii=False)+";\n")

if __name__ == "__main__":
    build_home(); build_calcs(); build_guides(); build_videos(); build_lead(); build_support()
    build_advertise(); build_contests(); build_careers(); build_tools(); build_legal(); build_404_sitemap()
    print(f"Built {len(PAGES)+1} pages")
