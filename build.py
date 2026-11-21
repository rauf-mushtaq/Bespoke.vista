#!/usr/bin/env python3
"""Builds the static pages for the Bespoke Vista website.

All page content lives in this file so the header, footer, prices and
service names stay consistent everywhere. Edit here, then run:

    python3 build.py

The generated .html files are committed, so the site can be hosted as-is on
any static host (GitHub Pages, Netlify, Cloudflare Pages, a normal web server).
"""
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "Bespoke Vista"
TAGLINE = "Bridging Strategy and Execution"
CONTACT_EMAIL = "hello@bespokevista.co.uk"  # TODO: confirm the business email address

NAV = [
    ("services.html", "Services"),
    ("managed-teams.html", "Managed Teams"),
    ("pricing.html", "Pricing"),
    ("about.html", "About"),
    ("insights.html", "Insights"),
]
LOGO = ('<img src="assets/img/logo.png" srcset="assets/img/logo.png 1x, assets/img/logo@2x.png 2x" '
        'alt="" width="55" height="38">')
ARR = '<span class="arr" aria-hidden="true">→</span>'


def esc_attr(s):
    return s.replace('"', "&quot;")


# ============================================================== Shared chrome
def header(active):
    def cur(h):
        return ' aria-current="page"' if h == active else ""
    items = "\n".join(f'        <li><a href="{h}"{cur(h)}>{l}</a></li>' for h, l in NAV)
    return f"""  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <nav class="container nav" aria-label="Main">
      <a class="brand" href="index.html" aria-label="{SITE} home">
        {LOGO}
        <span><span class="brand-name">{SITE}</span><span class="brand-tag">{TAGLINE}</span></span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Menu
      </button>
      <ul class="nav-links" id="nav-links">
{items}
        <li class="nav-btns">
          <a class="btn btn-line btn-sm" href="scorecard.html"{cur("scorecard.html")}>Free AI Scorecard</a>
          <a class="btn btn-primary btn-sm" href="contact.html"{cur("contact.html")}>Book a call</a>
        </li>
      </ul>
    </nav>
  </header>"""


FOOTER = f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-word" aria-hidden="true">Bespoke <span>Vista</span></div>
      <div class="footer-grid">
        <div>
          <div class="footer-brand">{LOGO}<span>{SITE}</span></div>
          <p>{TAGLINE}. Senior UK consulting, AI-enabled delivery and managed teams in Lahore.</p>
          <p class="clocks" style="margin-top:8px"><span><span class="dot"></span><span data-status="lahore">Lahore team</span></span><span><b>LDN</b><span data-clock="london">--:--</span></span><span><b>LHE</b><span data-clock="lahore">--:--</span></span></p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="services.html#advise">Consulting &amp; advisory</a></li>
            <li><a href="services.html#ai">AI services</a></li>
            <li><a href="managed-teams.html">Managed teams</a></li>
            <li><a href="services.html#learn">Training</a></li>
            <li><a href="pricing.html#dojoos">DojoOS</a></li>
          </ul>
        </div>
        <div>
          <h4>Start here</h4>
          <ul>
            <li><a href="scorecard.html">AI Readiness Scorecard</a></li>
            <li><a href="pricing.html#intelligence">Executive AI Intelligence</a></li>
            <li><a href="pricing.html">Plans &amp; pricing</a></li>
            <li><a href="contact.html">Book a call</a></li>
          </ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="case-studies.html">Case studies</a></li>
            <li><a href="insights.html">Insights</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
            <li>United Kingdom</li>
            <li>Delivery hub: Lahore, Pakistan</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span id="year">2026</span> Bespoke Vista Ltd. Registered in England &amp; Wales.</span>
        <span>All prices exclude VAT.</span>
      </div>
    </div>
  </footer>"""


def page(filename, title, description, body):
    full = f"{SITE} | {TAGLINE}" if filename == "index.html" else f"{title} | {SITE}"
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full}</title>
  <meta name="description" content="{esc_attr(description)}">
  <meta property="og:title" content="{esc_attr(full)}">
  <meta property="og:description" content="{esc_attr(description)}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="assets/img/logo@2x.png">
  <meta name="theme-color" content="#F7F3EE">
  <link rel="icon" href="assets/img/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
{header(filename)}
  <main id="main">
{body}
  </main>
{FOOTER}
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


def label(text):
    return f'<span class="label">{text}</span>'


def cta(title="Find out where AI will pay off in your business.",
        text="Take the free AI Readiness Scorecard: ten questions, three minutes, and a personalised result with clear next steps.",
        primary=("Get your free AI score", "scorecard.html"),
        secondary=("Book a 30-minute call", "contact.html?topic=consultation")):
    return f"""    <section class="sec-tight">
      <div class="container">
        <div class="cta reveal">
          {label("Next step")}
          <h2>{title}</h2>
          <p>{text}</p>
          <div class="btns">
            <a class="btn btn-ember" href="{primary[1]}">{primary[0]} {ARR}</a>
            <a class="btn btn-line-light" href="{secondary[1]}">{secondary[0]}</a>
          </div>
        </div>
      </div>
    </section>"""


CLOCKS = ('<p class="clocks"><span><span class="dot"></span><span data-status="lahore">Lahore team</span></span>'
          '<span><b>London</b><span data-clock="london">--:--</span></span>'
          '<span><b>Lahore</b><span data-clock="lahore">--:--</span></span></p>')

# ============================================================== Catalogue data
# Subscriptions: (id, name, for, description, [(tier, desc, monthly £, [features]), ...], featured index)
SUBSCRIPTIONS = [
    ("intelligence", "Executive AI Intelligence", "For directors, owners and senior managers",
     "A monthly briefing that tells busy leaders what has changed in AI, what matters for their business and what to do next. No hype, no jargon.",
     [("Briefing", "Stay informed in 15 minutes a month.", 49,
       ["Monthly executive briefing (PDF and audio)", "Curated tools and vendor watchlist", "Prompt and template library", "Member-only articles"]),
      ("Professional", "For leaders actively planning AI.", 99,
       ["Everything in Briefing", "Monthly live Q&amp;A session", "Sector playbooks: logistics, professional services, property", "Policy and template updates"]),
      ("Boardroom", "For the whole leadership team.", 199,
       ["Everything in Professional", "Up to 5 team seats", "Quarterly 30-minute 1:1 with Azeem", "Board-ready AI update slides each quarter"])], 1),
    ("advisory", "Bespoke Vista AI Advisory", "For UK SMEs and mid-market firms adopting AI",
     "A standing senior AI adviser who keeps your AI plans on track, safe and paying back, for less than a single consulting week a month.",
     [("Starter", "Light-touch guidance as you begin.", 495,
       ["2 hours of advisory a month", "Monthly AI opportunities and risks review", "Email support, 2-working-day response", "Policy and governance templates"]),
      ("Growth", "Structured adoption across teams.", 995,
       ["5 hours of advisory a month", "Quarterly AI roadmap refresh", "AI usage policy and governance set-up", "One team workshop each quarter", "Next-working-day response"]),
      ("Partner", "An AI lead without the hire.", 1995,
       ["10 hours of advisory a month", "Monthly AI steering meeting", "Use-case pipeline managed for you", "Vendor and licence reviews", "Same-day response"])], 1),
    ("fractional", "Fractional Business Architect", "For growing firms with change on the agenda",
     "Senior business architecture and transformation leadership a few days a month, at a fraction of the cost of a full-time hire.",
     [("Navigator", "Keep change joined up.", 995,
       ["1 day a month", "Capability and process map kept current", "Monthly change roadmap review", "Ad-hoc advice by email"]),
      ("Architect", "Own the target operating model.", 1995,
       ["2.5 days a month", "Target operating model ownership", "Change portfolio prioritisation", "Supplier and solution design reviews", "Seat at your leadership meeting"]),
      ("Director", "Fractional transformation director.", 3995,
       ["5 days a month", "Leads your transformation portfolio", "Programme governance and assurance", "Board reporting", "Backed by the Lahore support office"])], 1),
]

MANAGED_PLANS = [
    ("pmo", "Managed PMO Office", "For organisations running several projects without a PMO",
     "Reporting, risk, governance and control, run for you by a UK-led team at a predictable monthly cost.",
     [("Essentials", "Control for a handful of projects.", "£1,500",
       ["Up to 3 projects", "RAID log and action tracking", "Weekly status reports", "Monthly UK PMO lead review", "Essential SLA"]),
      ("Programme", "A full PMO for a growing portfolio.", "£2,950",
       ["Up to 10 projects", "Portfolio dashboard (Power BI or Excel)", "Resource and budget tracking", "Fortnightly governance pack", "Assured SLA"]),
      ("Portfolio", "Multi-programme governance.", "£5,000",
       ["Multiple programmes", "Benefits tracking", "Board reporting pack", "Dedicated UK PMO lead", "Critical SLA"])], 1),
    ("aiops", "AI Operations Team", "For firms with high volumes of admin, documents and data",
     "AI does the repetitive work; our people check the results and keep improving it. You pay for processed outcomes, not hours.",
     [("Pilot", "Prove the value on one workflow.", "£2,500",
       ["One workflow run end to end", "Human review of AI outputs", "Monthly performance report", "Essential SLA"]),
      ("Scale", "Automate across a department.", "£5,500",
       ["Up to 4 workflows", "Copilot, ChatGPT or Claude with Power Automate", "Prompt and knowledge-base upkeep", "Weekly reporting", "Assured SLA"]),
      ("Enterprise", "An AI operations function.", "£10,000",
       ["Up to 10 workflows", "Extended-hours cover", "Continuous improvement backlog", "Quarterly value review with UK lead", "Critical SLA"])], 1),
]

DOJOOS = ("dojoos", "DojoOS", "For martial arts schools and wellness studios",
          "Run your school, not your spreadsheets. Members, payments, attendance and gradings in one simple platform, with AI help for marketing. Built by a martial artist, for martial artists.",
          [("Starter", "For a single, growing school.", "£99",
            ["Up to 100 students", "Membership and payment tracking", "Attendance check-in", "Grading records"]),
           ("Club", "Automate the admin.", "£179",
            ["Up to 300 students", "Automatic renewals and reminders", "Parent and student portal", "Lead and trial-class tracking"]),
           ("Academy", "Multi-site and instructors.", "£299",
            ["Unlimited students, multiple sites", "AI marketing and content assistant", "Instructor scheduling", "Reporting dashboard"])], 1)

# Projects: (name, description, price, time)
PROJECTS = [
    ("AI Readiness Assessment", "Review your processes, data and skills, and leave with a prioritised, costed set of AI opportunities.", "£1,500–£3,000", "2–3 weeks"),
    ("AI Optimisation Review", "Already paying for Copilot or ChatGPT but not seeing the value? We find out why and fix it.", "£1,950", "2 weeks"),
    ("AI Governance Pack", "Usage policy, risk register, data rules, DPIA template and an approval process for new use cases.", "£2,500–£6,000", "3–4 weeks"),
    ("AI Implementation Sprint", "Build and launch one to three AI workflows using Power Automate, SharePoint and Copilot, ChatGPT or Claude.", "£4,000–£12,000", "4–6 weeks"),
    ("Microsoft Copilot Adoption Programme", "Readiness, permissions clean-up, governance, champions, training and rollout.", "£5,000–£25,000", "6–12 weeks"),
    ("Transformation Health Check", "Independent executive review of a struggling programme, with a practical recovery plan.", "£4,950", "2 weeks"),
    ("Documentation Factory", "Process maps, SOPs, user guides and knowledge bases, produced at pace by our Lahore team.", "£3,000–£15,000", "2–8 weeks"),
    ("Target Operating Model Design", "People, process, technology and governance designed together, with a roadmap to get there.", "From £12,000", "6–10 weeks"),
    ("Cyber Security Business Analysis", "Requirements, process design and change support for security programmes.", "Fixed scope or day rate", "By agreement"),
]

TRAINING = [
    ("AI for Leaders", "Half-day workshop for leadership teams: what is real, what is hype and where to start.", "£1,450", "Up to 12 people"),
    ("Copilot Skills Bootcamp", "Two days of hands-on, role-based Microsoft Copilot training using your own work.", "£2,950", "Up to 15 people"),
    ("Prompting for Teams", "Practical half day on getting reliable results from ChatGPT, Claude and Copilot.", "£995", "Up to 15 people"),
    ("Calm Under Pressure", "Leadership resilience workshop drawing on Tai Chi, martial arts and breathing practice.", "£1,250", "Half day, up to 20"),
]

# Managed team offerings: (id, name, outcome, [deliverables], price)
OFFERINGS = [
    ("Managed PMO", "Every project reported, every risk owned, every week.",
     ["RAID logs and action tracking", "Weekly status and portfolio dashboards", "Governance packs and minutes", "Resource and budget tracking"], "From £1,500/month"),
    ("Documentation Factory", "Your processes, written down properly, fast.",
     ["Process maps (BPMN or Visio)", "SOPs and work instructions", "User guides and training materials", "Policy and operating manuals"], "£3,000–£15,000 per project"),
    ("Business Analysis as a Service", "Requirements ready before your developers are.",
     ["Requirements and user stories", "Process and data modelling", "Backlog refinement", "UAT scripts and test support"], "From £2,000/month"),
    ("AI Operations Team", "AI does the repetitive work; people check the results.",
     ["Document and inbox processing", "Data extraction and entry", "Copilot, ChatGPT and Claude workflows", "Monthly performance reporting"], "From £2,500/month"),
    ("Managed Back Office", "Admin handled, so your UK team can focus on customers.",
     ["Invoicing and purchase-ledger support", "CRM and data upkeep", "Scheduling and customer admin", "Operational reporting"], "From £1,800/month"),
    ("Knowledge Management Service", "One trusted place to find the answer.",
     ["SharePoint knowledge base build", "Content curation and updates", "AI-ready knowledge for Copilot", "Search and usage reporting"], "From £1,200/month"),
    ("Transformation Support Office", "Change delivered, not just planned.",
     ["Change plans and communications", "Stakeholder and training logistics", "Benefits tracking", "Programme reporting"], "From £3,500/month"),
]

INDUSTRIES = ["Logistics", "Warehousing", "Manufacturing", "Supply Chain", "Professional Services", "Technology",
              "Property", "Financial Services", "Healthcare", "Education", "Public Sector", "Martial Arts Schools", "Wellness"]


def plan_cards(tiers, featured, annual=False, cta_topic="", unit="/month"):
    out = []
    for i, (name, desc, price, feats) in enumerate(tiers):
        f = i == featured
        if annual:
            amount = f'<div class="amount" data-monthly="{price}">£{price:,}</div><div class="per">per month, ex VAT</div>'
        else:
            amount = f'<div class="amount">{price}</div><div class="per">per month, ex VAT</div>'
        lis = "".join(f"<li>{x}</li>" for x in feats)
        out.append(f"""          <div class="plan{' featured' if f else ''} reveal">
            {'<span class="flag">Most popular</span>' if f else ''}
            <h3>{name}</h3>
            <p class="tier-desc">{desc}</p>
            {amount}
            <ul>{lis}</ul>
            <a class="btn {'btn-ember' if f else 'btn-line'}" href="contact.html?topic={cta_topic}">Choose {name} {ARR}</a>
          </div>""")
    return "\n".join(out)


def product_block(pid, name, who, desc, tiers, featured, annual=False, extra=""):
    return f"""        <div class="product" id="{pid}">
          <div class="product-head">
            <div><h2>{name}</h2><p>{desc}</p>{extra}</div>
            <div class="for">{who}</div>
          </div>
          <div class="grid g3">
{plan_cards(tiers, featured, annual, pid)}
          </div>
        </div>"""


def pricelist(rows, topic):
    return "\n".join(f"""          <div class="pl-row reveal">
            <h3>{n}</h3><p>{d}</p><span class="p">{p}</span><span class="t">{t}</span>
          </div>""" for n, d, p, t in rows)


# ============================================================== HOME
HORIZON = """<svg class="horizon" viewBox="-70 20 540 352" role="img" aria-label="A sun rising over a horizon: advise, build, run and learn">
            <defs>
              <linearGradient id="sunG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7941D"/><stop offset="1" stop-color="#EE2A24"/></linearGradient>
              <clipPath id="above"><rect x="-50" y="-50" width="500" height="280"/></clipPath>
              <mask id="stripes"><rect x="0" y="0" width="400" height="400" fill="#fff"/>
                <rect x="0" y="150" width="400" height="3" fill="#000"/><rect x="0" y="170" width="400" height="5" fill="#000"/>
                <rect x="0" y="189" width="400" height="7" fill="#000"/><rect x="0" y="207" width="400" height="9" fill="#000"/></mask>
            </defs>
            <g clip-path="url(#above)">
              <circle class="ring" cx="200" cy="230" r="182"/>
              <g class="sun" mask="url(#stripes)"><circle cx="200" cy="230" r="140" fill="url(#sunG)"/></g>
            </g>
            <line x1="-70" y1="230" x2="470" y2="230" stroke="#0B1120" stroke-width="1.5"/>
            <g class="gridlines">
              <line x1="200" y1="230" x2="-200" y2="370"/><line x1="200" y1="230" x2="-40" y2="370"/><line x1="200" y1="230" x2="90" y2="370"/>
              <line x1="200" y1="230" x2="200" y2="370"/><line x1="200" y1="230" x2="310" y2="370"/><line x1="200" y1="230" x2="440" y2="370"/>
              <line x1="200" y1="230" x2="600" y2="370"/>
              <line x1="-70" y1="244" x2="470" y2="244"/><line x1="-70" y1="262" x2="470" y2="262"/><line x1="-70" y1="288" x2="470" y2="288"/>
              <line x1="-70" y1="324" x2="470" y2="324"/><line x1="-70" y1="369" x2="470" y2="369"/>
            </g>
            <g font-family="JetBrains Mono, monospace" font-size="11" fill="#0B1120" letter-spacing="1.2">
              <circle cx="31" cy="168" r="4" fill="#0B1120"/><text x="20" y="172" text-anchor="end">ADVISE</text>
              <circle cx="110" cy="74" r="4" fill="#0B1120"/><text x="100" y="64" text-anchor="end">BUILD</text>
              <circle cx="290" cy="74" r="4" fill="#0B1120"/><text x="300" y="64">RUN</text>
              <circle cx="369" cy="168" r="4" fill="#0B1120"/><text x="380" y="172">LEARN</text>
            </g>
          </svg>"""

PILLARS = [
    ("01", "Advise", "Senior consulting and fractional leadership to set direction and fix what is stuck.",
     ["Transformation Health Check", "Target Operating Model", "Fractional Business Architect"], "From £995/month", "services.html#advise"),
    ("02", "Build", "AI and automation that solves measurable problems, using the tools you already pay for.",
     ["AI Readiness Assessment", "Copilot adoption", "AI Implementation Sprints"], "From £1,500", "services.html#ai"),
    ("03", "Run", "UK-led managed teams in Lahore that deliver outcomes to an agreed service level.",
     ["Managed PMO Office", "AI Operations Team", "Documentation Factory"], "From £1,200/month", "managed-teams.html"),
    ("04", "Learn", "Training and membership that build lasting capability in your leaders and teams.",
     ["Executive AI Intelligence", "AI for Leaders", "Copilot Skills Bootcamp"], "From £49/month", "services.html#learn"),
]
pillars_html = "\n".join(f"""          <a class="pillar" href="{href}">
            <span class="n">{n}</span>
            <h3>{t}</h3>
            <p>{d}</p>
            <ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>
            <span class="from">{frm} →</span>
          </a>""" for n, t, d, items, frm, href in PILLARS)

COMPARE = [
    ("Who does the work", "Partners sell, junior teams deliver", "One person, limited capacity", "Senior UK lead on every engagement, backed by a Lahore team"),
    ("Minimum spend", "Often six figures", "A day rate, open-ended", "From £49 a month; fixed-price projects from £1,500"),
    ("How you pay", "Time and materials", "Day rate", "Fixed monthly fees and outcome-based service levels"),
    ("Time to start", "Weeks to months", "Days, if available", "Days"),
    ("AI in delivery", "Varies by team", "Varies", "Built into how every service runs"),
    ("After the project", "Team rolls off", "Contract ends", "Optional managed service keeps it running"),
]
compare_rows = "\n".join(f"""              <tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td class="us">{d}</td></tr>""" for a, b, c, d in COMPARE)

LADDER = [
    ("Free", "Discover", "Take the AI Readiness Scorecard or read our insights.", "£0", "scorecard.html"),
    ("Subscribe", "Stay ahead", "Executive AI Intelligence, the monthly briefing for leaders.", "From £49/month", "pricing.html#intelligence"),
    ("Assess", "Get clarity", "A fixed-price assessment or health check with a clear plan.", "£1,500–£4,950", "pricing.html#projects"),
    ("Deliver", "Make it real", "Implementation sprints, Copilot rollouts and operating model design.", "£4,000–£25,000", "services.html#ai"),
    ("Partner", "Keep it running", "Advisory retainers and managed teams that keep improving.", "From £495/month", "managed-teams.html"),
]
ladder_html = "\n".join(f"""          <a class="step reveal" href="{h}">
            <span class="k">{i+1:02d} / {k}</span>
            <h3>{t}</h3>
            <p>{d}</p>
            <span class="price">{p}</span>
          </a>""" for i, (k, t, d, p, h) in enumerate(LADDER))

marquee_items = "".join(f"<li>{x}</li>" for x in INDUSTRIES)

home_plans = "\n".join(f"""          <a class="card reveal" href="pricing.html#{pid}">
            <span class="label">{who.replace('For ', 'For ')}</span>
            <h3 style="font-family:var(--display);font-size:1.6rem;font-weight:600">{name}</h3>
            <p>{desc}</p>
            <p style="font-family:var(--display);font-size:2rem;color:var(--ink);font-weight:600;margin:6px 0 18px">£{tiers[0][2]:,}<span style="font-size:1rem;color:var(--muted);font-family:var(--sans);font-weight:400"> to £{tiers[-1][2]:,} /month</span></p>
            <span class="more">Compare plans →</span>
          </a>""" for pid, name, who, desc, tiers, _ in SUBSCRIPTIONS)

home = f"""    <section class="hero">
      <div class="container hero-grid">
        <div>
          {label(TAGLINE)}
          <h1>Strategy that gets <em class="ember">done.</em></h1>
          <p class="lead">Bespoke Vista pairs senior UK consulting with AI-enabled delivery teams in Lahore. We design the change, build the automation and run the operations, on clear monthly pricing instead of open-ended day rates.</p>
          <div class="hero-actions">
            <a class="btn btn-ember" href="scorecard.html">Get your free AI score {ARR}</a>
            <a class="btn btn-line" href="contact.html?topic=consultation">Book a 30-minute call</a>
          </div>
          {CLOCKS}
        </div>
        <div class="hero-art">
          {HORIZON}
        </div>
      </div>
    </section>

    <div class="marquee" aria-label="Sectors we work with">
      <div class="marquee-track"><ul>{marquee_items}</ul><ul aria-hidden="true">{marquee_items}</ul></div>
    </div>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("What we do")}<h2>Advise. Build. Run. <em class="ember">Learn.</em></h2></div>
          <p>One partner from the first conversation to the day-to-day running. Start with whichever you need; the others are there when you are ready.</p>
        </div>
        <div class="pillars reveal">
{pillars_html}
        </div>
      </div>
    </section>

    <section class="sec sec-dark">
      <div class="container">
        <div class="head">
          <div>{label("Why Bespoke Vista")}<h2>Big-firm thinking. <em class="ember">Small-firm</em> speed.</h2></div>
          <p>Large consultancies are built for large budgets. Freelancers run out of hands. We sit in the gap, with senior expertise, a delivery team and prices UK SMEs and mid-market firms can plan around.</p>
        </div>
        <div class="table-wrap reveal">
          <table class="compare">
            <thead><tr><th scope="col"><span class="sr-only"></span></th><th scope="col">Large consultancy</th><th scope="col">Independent contractor</th><th scope="col" class="us">Bespoke Vista</th></tr></thead>
            <tbody>
{compare_rows}
            </tbody>
          </table>
        </div>
        <p class="note" style="color:var(--slate)">A general comparison of typical engagement models, not of any specific firm.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container split" style="align-items:center">
        <div class="reveal">
          {label("UK-led. Lahore-delivered.")}
          <h2>Your work keeps moving <em class="ember">while you sleep.</em></h2>
          <p>Our Lahore team starts its day before the UK wakes up. Brief us in the afternoon and the work is well under way by the time you're back at your desk, with a few hours of live overlap every morning for questions and reviews.</p>
          <p>Every service has a UK lead who is accountable for quality, and a clear service level. You buy outcomes, not people.</p>
          <a class="btn btn-primary" href="managed-teams.html">How managed teams work {ARR}</a>
        </div>
        <div class="dark sun-timeline reveal" aria-label="Working hours in UK time">
          <div class="tl-row"><div class="who">Lahore team<small>09:00–18:00 PKT</small></div><div class="tl-bar"><span class="lahore" style="left:16.7%;width:37.5%">Lahore 04:00–13:00</span><i class="tl-now"></i></div></div>
          <div class="tl-row"><div class="who">UK lead<small>09:00–17:30 UK</small></div><div class="tl-bar"><span class="uk" style="left:37.5%;width:35.4%">UK 09:00–17:30</span><i class="tl-now"></i></div></div>
          <div class="tl-row"><div class="who">Together<small>live collaboration</small></div><div class="tl-bar"><span class="overlap" style="left:37.5%;width:16.7%">Live overlap 09:00–13:00</span><i class="tl-now"></i></div></div>
          <div class="tl-axis"><div></div><div><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div></div>
          <p class="small" style="color:var(--slate);margin:18px 0 0">Shown in UK time. Lahore is <span data-offset>5</span> hours ahead. The white line is now.</p>
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container">
        <div class="head">
          <div>{label("Subscriptions")}<h2>Senior expertise, <em class="ember">on a monthly plan.</em></h2></div>
          <p>Predictable monthly pricing. No day-rate surprises, no long contracts to start, and you can step up or down as your needs change.</p>
        </div>
        <div class="grid g3">
{home_plans}
        </div>
        <p class="note"><a href="pricing.html">See all plans and prices →</a></p>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Start where you are")}<h2>Begin small. <em class="ember">Grow when ready.</em></h2></div>
          <p>Most clients start with something free or low-cost, see the value, then take the next step. Every rung is useful on its own.</p>
        </div>
        <div class="ladder">
{ladder_html}
        </div>
      </div>
    </section>

    <section class="sec sec-dark">
      <div class="container">
        <div class="head">
          <div>{label("Principles from the dojo")}<h2>How we work.</h2></div>
          <p>Our founder's background in martial arts, Tai Chi and Shiatsu shapes how we approach change: calm, deliberate and practised until it becomes habit.</p>
        </div>
        <div class="principles">
          <div class="principle reveal"><div class="word">Balance.</div><p>Between strategy and delivery, cost and quality, people and technology. Change that ignores one of these doesn't last.</p></div>
          <div class="principle reveal"><div class="word">Discipline.</div><p>Clear governance, honest reporting and service levels we keep. The basics done well, every week.</p></div>
          <div class="principle reveal"><div class="word">Flow.</div><p>Remove friction from how work moves. Automate the repetitive, simplify the complex, and let people focus on what matters.</p></div>
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="stats reveal">
          <div><strong>25+</strong><span>years delivering business and technology change</span></div>
          <div><strong>2</strong><span>delivery hubs: United Kingdom and Lahore</span></div>
          <div><strong>13</strong><span>sectors, from logistics to wellness</span></div>
          <div><strong>£49</strong><span>a month is all it takes to start</span></div>
        </div>
        <div class="grid g3" style="margin-top:56px">
          <a class="card reveal" href="case-studies.html#ai-productivity"><span class="label">AI &amp; Automation</span><h3>AI productivity improvements</h3><p>AI-driven ways of working that cut manual effort, improved consistency and sped up delivery.</p><span class="more">Read the case study →</span></a>
          <a class="card reveal" href="case-studies.html#cyber-security"><span class="label">Cyber security</span><h3>Cyber security programmes</h3><p>Business analysis, project management and consulting on significant security initiatives.</p><span class="more">Read the case study →</span></a>
          <a class="card reveal" href="case-studies.html#property-recovery"><span class="label">Business recovery</span><h3>Property business turnaround</h3><p>A Lahore rental business restored and modernised, with better occupancy and operations.</p><span class="more">Read the case study →</span></a>
        </div>
      </div>
    </section>

{cta()}"""

page("index.html", SITE,
     "Bespoke Vista combines senior UK consulting with AI-enabled delivery teams in Lahore: advisory subscriptions, AI adoption, managed PMO and AI operations on clear monthly pricing.",
     home)

# ============================================================== SERVICES
def svc(name, one, tag, who, gets, topic):
    return f"""            <details class="svc">
              <summary><h3>{name}</h3><span class="tag">{tag}</span><p class="one">{one}</p><span class="plus">Details</span></summary>
              <div class="body">
                <dl><dt>Ideal for</dt><dd>{who}</dd><dt>You get</dt><dd>{gets}</dd></dl>
                <a class="btn btn-line btn-sm" href="contact.html?topic={topic}">Discuss this {ARR}</a>
              </div>
            </details>"""


ADVISE = [
    ("Transformation Health Check", "An honest, independent view of a programme that's late, over budget or losing confidence.", "£4,950 · 2 weeks",
     "Boards and sponsors of programmes in trouble.", "Independent review, evidence-based RAG assessment, a prioritised recovery plan and an executive briefing.", "health-check"),
    ("Target Operating Model Design", "Redesign how the business works after growth, a merger or a change in strategy.", "From £12,000",
     "Growing SMEs and mid-market firms, especially logistics, warehousing and manufacturing.", "Capability map, process and organisation design, technology and governance model, and a phased roadmap.", "tom"),
    ("Fractional Business Architect", "Senior architecture and transformation leadership, a few days a month.", "£995–£3,995/month",
     "Firms with change on the agenda but no architect or transformation director.", "Operating model ownership, roadmap and portfolio prioritisation, supplier design reviews and board reporting.", "fractional"),
    ("Programme Delivery &amp; Recovery", "Interim programme leadership to mobilise, deliver or rescue major initiatives.", "Monthly or fixed scope",
     "Organisations without the senior delivery capacity for a critical programme.", "Programme management, PMO set-up, vendor management, delivery assurance and offshore coordination.", "project"),
    ("Cyber Security Business Analysis", "Turn security requirements into processes and change that people actually follow.", "Fixed scope or day rate",
     "Organisations running security, compliance or resilience programmes.", "Requirements, process design (access, joiners-movers-leavers, incident response), governance and adoption support.", "cyber-ba"),
]
AI = [
    ("AI Readiness Assessment", "Find out where AI will genuinely pay off, and what needs fixing first.", "£1,500–£3,000 · 2–3 weeks",
     "SMEs and mid-market firms at the start of their AI journey.", "Process, data and skills review; prioritised, costed opportunities; risks; and a 90-day plan.", "ai-readiness"),
    ("AI Governance Pack", "Use AI confidently without putting data, customers or reputation at risk.", "£2,500–£6,000 · 3–4 weeks",
     "Any organisation where staff already use AI tools, approved or not.", "AI usage policy, risk register, data classification rules, DPIA template and a use-case approval process.", "governance"),
    ("Microsoft Copilot Adoption Programme", "Turn Copilot licences into everyday productivity.", "£5,000–£25,000 · 6–12 weeks",
     "Microsoft 365 organisations rolling out, or struggling with, Copilot.", "Readiness and permissions review, governance, champions network, role-based training and adoption tracking.", "copilot"),
    ("AI Implementation Sprint", "Build and launch working AI workflows in weeks, not quarters.", "£4,000–£12,000 · 4–6 weeks",
     "Teams with a clear, repetitive process to automate.", "One to three live workflows using Power Automate, SharePoint and Copilot, ChatGPT or Claude, with documentation and handover.", "ai-sprint"),
    ("AI Optimisation Review", "Already paying for AI tools? Find out why the value is low and fix it.", "£1,950 · 2 weeks",
     "Organisations 6+ months into Copilot, ChatGPT or Claude with patchy usage.", "Usage analysis, staff interviews, quick-win fixes and a prioritised improvement plan.", "ai-optimisation"),
    ("Bespoke Vista AI Advisory", "A standing senior AI adviser on a monthly subscription.", "£495–£1,995/month",
     "Leadership teams who want expert guidance without hiring.", "Monthly advisory hours, roadmap reviews, governance, workshops and use-case pipeline management.", "advisory"),
]
RUN = [
    ("Managed PMO Office", "Project reporting, risk and governance, run for you.", "£1,500–£5,000/month",
     "Organisations running several projects without a PMO.", "RAID management, weekly reporting, dashboards, governance packs and benefits tracking.", "pmo"),
    ("AI Operations Team", "AI handles the repetitive work; our team checks and improves it.", "£2,500–£10,000/month",
     "Firms with high volumes of documents, admin and data entry.", "Managed AI workflows with human review, performance reporting and continuous improvement.", "aiops"),
    ("Documentation Factory", "Processes, SOPs and guides written properly, at pace.", "£3,000–£15,000/project",
     "Firms preparing for growth, audit, certification, outsourcing or AI.", "Process maps, SOPs, user guides, training materials and knowledge bases.", "documentation"),
    ("Business Analysis as a Service", "Requirements and analysis capacity on a monthly plan.", "From £2,000/month",
     "Tech companies and change teams with more demand than analysts.", "User stories, process and data models, backlog refinement and UAT support.", "baas"),
    ("Managed Back Office", "Admin, data and reporting handled to an agreed standard.", "From £1,800/month",
     "SMEs whose UK staff are buried in admin.", "Ledger support, CRM upkeep, scheduling, customer admin and reporting.", "back-office"),
    ("Knowledge Management Service", "One trusted place for answers, ready for Copilot.", "From £1,200/month",
     "Organisations where knowledge lives in inboxes and people's heads.", "SharePoint knowledge base, content upkeep and AI-ready structure.", "knowledge"),
]
LEARN = [
    ("Executive AI Intelligence", "The monthly AI briefing for busy leaders.", "£49–£199/month",
     "Directors, owners and senior managers.", "Monthly briefing, tool watchlist, prompt library, live Q&amp;A and sector playbooks.", "intelligence"),
    ("AI for Leaders", "What is real, what is hype and where to start.", "£1,450 · half day",
     "Leadership teams up to 12 people.", "Interactive workshop, opportunity mapping and a one-page action plan.", "training"),
    ("Copilot Skills Bootcamp", "Hands-on, role-based Copilot training using your own work.", "£2,950 · 2 days",
     "Teams of up to 15 with Copilot licences.", "Practical exercises, prompt packs per role and follow-up resources.", "training"),
    ("Calm Under Pressure", "Leadership resilience through Tai Chi, martial arts and breath.", "£1,250 · half day",
     "Leadership and high-pressure teams, up to 20 people.", "A grounded, practical session on focus, composure and recovery, with techniques to use daily.", "wellbeing"),
]


def svc_block(bid, n, title, intro, rows, extra=""):
    items = "\n".join(svc(*r) for r in rows)
    return f"""        <div class="pillar-block" id="{bid}">
          <div class="side reveal">
            <span class="big-n">{n}</span>
            <h2>{title}</h2>
            <p>{intro}</p>
            {extra}
          </div>
          <div class="stack">
{items}
          </div>
        </div>"""


SUBNAV_SERVICES = [("advise", "Advise"), ("ai", "Build with AI"), ("run", "Run"), ("learn", "Learn"), ("products", "DojoOS"), ("industries", "Industries")]


def subnav(items):
    return """    <nav class="subnav" aria-label="Jump to section">
      <div class="container"><ul>
""" + "\n".join(f'        <li><a href="#{a}">{l}</a></li>' for a, l in items) + """
      </ul></div>
    </nav>"""


services = f"""    <section class="page-hero">
      <div class="container">
        {label("Services")}
        <h1>Everything you need to <em class="ember">change well.</em></h1>
        <p class="lead">Consulting to set direction, AI to build capability, managed teams to run it, and training so it sticks. Tap any service for details and pricing.</p>
      </div>
    </section>
{subnav(SUBNAV_SERVICES)}
    <section class="sec">
      <div class="container">
{svc_block("advise", "01", "Advise", "Senior consulting and fractional leadership. Fixed scope wherever possible, so you know the cost before we start.", ADVISE)}
{svc_block("ai", "02", "Build with AI", "Practical AI using Microsoft Copilot, ChatGPT, Claude, Power Automate and SharePoint. Every engagement starts with a measurable business problem, not a tool.", AI, '<a class="btn btn-ember btn-sm" href="scorecard.html">Take the free AI Scorecard ' + ARR + '</a>')}
{svc_block("run", "03", "Run", "Managed services delivered by our Lahore team under a UK lead, priced on outcomes and backed by service levels.", RUN, '<a class="btn btn-primary btn-sm" href="managed-teams.html">How managed teams work ' + ARR + '</a>')}
{svc_block("learn", "04", "Learn", "Training and membership that build lasting capability, from the boardroom to the front line.", LEARN)}
        <div class="pillar-block" id="products">
          <div class="side reveal">
            <span class="big-n">05</span>
            <h2>DojoOS</h2>
            <p>Our first sector product: a simple platform for martial arts schools and wellness studios, built by someone who has trained and taught.</p>
          </div>
          <div class="card reveal" style="background:var(--ink);border-color:var(--ink);color:var(--slate-light)">
            {label("Coming soon · Founding schools wanted")}
            <h3 style="color:var(--paper);font-family:var(--display);font-size:1.8rem;font-weight:600">Run your school, not your spreadsheets.</h3>
            <p style="color:var(--slate)">Members, payments, attendance and gradings in one place, with AI help for marketing and renewals. £99 to £299 a month.</p>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px"><a class="btn btn-ember btn-sm" href="contact.html?topic=dojoos">Join the founding list {ARR}</a><a class="btn btn-line-light btn-sm" href="pricing.html#dojoos">See plans</a></div>
          </div>
        </div>
        <div class="pillar-block" id="industries">
          <div class="side reveal">
            <span class="big-n">✦</span>
            <h2>Industries</h2>
            <p>Deep experience in logistics and supply chain, and practical knowledge across the sectors below.</p>
          </div>
          <ul class="chips reveal" style="align-self:start">{''.join(f'<li>{x}</li>' for x in INDUSTRIES)}</ul>
        </div>
      </div>
    </section>

{cta("Not sure where to start?", "Book a free 30-minute call. We'll listen, ask good questions and suggest the smallest sensible next step, even if that isn't us.", ("Book a 30-minute call", "contact.html?topic=consultation"), ("Take the AI Scorecard", "scorecard.html"))}"""

page("services.html", "Services",
     "Consulting, AI adoption, managed teams, training and DojoOS from Bespoke Vista, with clear pricing for every service.",
     services)

# ============================================================== MANAGED TEAMS
offer_cards = "\n".join(f"""          <div class="offer reveal">
            <h3>{n}</h3>
            <p class="outcome">“{o}”</p>
            <ul>{''.join(f'<li>{x}</li>' for x in d)}</ul>
            <div class="meta"><span class="p">{p}</span><a href="contact.html?topic=managed">Enquire →</a></div>
          </div>""" for n, o, d, p in OFFERINGS)

SLA = [
    ("Cover", "UK business hours", "Lahore and UK hours combined", "Extended hours, plus agreed weekend cover"),
    ("Response to requests", "Next working day", "Within 4 working hours", "Within 1 working hour"),
    ("Reporting", "Monthly service report", "Weekly report and monthly review", "Weekly report and monthly steering"),
    ("UK service lead", "Named contact", "Named lead, monthly review", "Dedicated lead, fortnightly review"),
    ("Improvement", "Quarterly review", "Monthly improvement backlog", "Monthly backlog and quarterly value review"),
    ("Service credits", "—", "Included", "Included"),
]
sla_rows = "\n".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in SLA)

managed = f"""    <section class="page-hero">
      <div class="container">
        {label("Managed Teams")}
        <h1>UK-led. Lahore-delivered. <em class="ember">Priced on outcomes.</em></h1>
        <p class="lead">Productised services run by our team in Lahore and assured by a UK lead. You agree the outcome and the service level; we manage the people, tools and AI that deliver it.</p>
        <div style="margin-top:28px">{CLOCKS}</div>
      </div>
    </section>

    <section class="sec">
      <div class="container split">
        <div class="reveal">
          {label("Our model")}
          <h2>We don't sell people. <em class="ember">We sell outcomes.</em></h2>
        </div>
        <div class="reveal">
          <p>Traditional offshoring rents you people by the hour and leaves the managing to you. That's where quality slips and savings disappear.</p>
          <p>Our managed teams work the other way round. Each service has defined deliverables, volumes and quality standards. A UK lead owns the result. AI and automation do the repetitive work, so costs fall over time rather than rise.</p>
          <ul class="ticks">
            <li>Fixed monthly price for an agreed scope</li>
            <li>Service levels with real consequences</li>
            <li>One accountable UK contact</li>
            <li>Documented playbooks, so the knowledge stays with you</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="offerings">
      <div class="container">
        <div class="head">
          <div>{label("Offerings")}<h2>Seven services, <em class="ember">ready to run.</em></h2></div>
          <p>Each one starts with a short mobilisation period, typically two to four weeks, while we map your process and build the playbook.</p>
        </div>
        <div class="grid g3">
{offer_cards}
          <div class="offer reveal" style="background:var(--ink);border-color:var(--ink)">
            <h3 style="color:var(--paper)">Something else?</h3>
            <p style="color:var(--slate)">If the work is repeatable and can be described, we can usually package it as a managed service.</p>
            <div class="meta" style="border-color:var(--line-dark)"><a class="btn btn-ember btn-sm" href="contact.html?topic=managed">Talk to us {ARR}</a></div>
          </div>
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Service levels")}<h2>Three levels of <em class="ember">assurance.</em></h2></div>
          <p>Every managed service runs to one of these service levels. Pick the one that matches how critical the work is.</p>
        </div>
        <div class="table-wrap table-light reveal">
          <table class="sla">
            <thead><tr><th scope="col"></th><th scope="col">Essential<small>Standard work</small></th><th scope="col">Assured<small>Business important</small></th><th scope="col">Critical<small>Time sensitive</small></th></tr></thead>
            <tbody>{sla_rows}</tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="sec sec-dark">
      <div class="container">
        <div class="head">
          <div>{label("Follow the sun")}<h2>More hours in <em class="ember">your day.</em></h2></div>
          <p>Lahore is <span data-offset>5</span> hours ahead of the UK. Work starts before you wake, and the morning overlap gives you live time for reviews and questions.</p>
        </div>
        <div class="sun-timeline reveal" aria-label="Working hours in UK time">
          <div class="tl-row"><div class="who">Lahore team<small>09:00–18:00 PKT</small></div><div class="tl-bar"><span class="lahore" style="left:16.7%;width:37.5%">Lahore 04:00–13:00</span><i class="tl-now"></i></div></div>
          <div class="tl-row"><div class="who">UK lead<small>09:00–17:30 UK</small></div><div class="tl-bar"><span class="uk" style="left:37.5%;width:35.4%">UK 09:00–17:30</span><i class="tl-now"></i></div></div>
          <div class="tl-row"><div class="who">Together<small>live collaboration</small></div><div class="tl-bar"><span class="overlap" style="left:37.5%;width:16.7%">Live overlap 09:00–13:00</span><i class="tl-now"></i></div></div>
          <div class="tl-axis"><div></div><div><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div></div>
          <p class="small" style="color:var(--slate);margin:18px 0 0">Shown in UK time. The white line is now.</p>
        </div>
        <div class="steps" style="margin-top:72px">
          <div class="reveal"><h3>Define the outcome</h3><p>We agree deliverables, volumes, quality standards and the service level.</p></div>
          <div class="reveal"><h3>Build the playbook</h3><p>Your UK lead maps the process, writes the SOPs and sets up the tools and AI.</p></div>
          <div class="reveal"><h3>Run to the SLA</h3><p>The Lahore team delivers. The UK lead checks quality and is your single point of contact.</p></div>
          <div class="reveal"><h3>Report and improve</h3><p>Regular reporting, and steady automation that takes cost out over time.</p></div>
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container split">
        <div class="reveal">
          {label("Trust &amp; security")}
          <h2>Your data, <em class="ember">your controls.</em></h2>
          <p>Working with an offshore team should feel as safe as working with your own. These are the foundations of every managed service.</p>
        </div>
        <ul class="ticks reveal">
          <li>The team works inside your systems and Microsoft 365 tenant, under your access controls</li>
          <li>Data processing agreement and UK GDPR safeguards for international transfers</li>
          <li>Confidentiality agreements for every team member</li>
          <li>A UK-based lead accountable for every service</li>
          <li>Quality checks on every deliverable before it reaches you</li>
          <li>Documented playbooks, so you are never dependent on one person</li>
        </ul>
      </div>
    </section>

{cta("Hand over the work. Keep the control.", "Tell us about the process that's slowing your team down. We'll come back with a scoped service, a service level and a fixed monthly price.", ("Discuss a managed service", "contact.html?topic=managed"), ("See pricing", "pricing.html#managed"))}"""

page("managed-teams.html", "Managed Teams",
     "UK-led, Lahore-delivered managed services priced on outcomes: Managed PMO, Documentation Factory, AI Operations Team, Business Analysis as a Service and more.",
     managed)

# ============================================================== PRICING
SUBNAV_PRICING = [("intelligence", "Executive AI Intelligence"), ("advisory", "AI Advisory"), ("fractional", "Fractional Architect"),
                  ("managed", "Managed services"), ("projects", "Fixed-price projects"), ("training", "Training"), ("dojoos", "DojoOS"), ("faq", "FAQs")]

subs_html = "\n".join(product_block(*s, annual=True) for s in SUBSCRIPTIONS)
managed_html = "\n".join(product_block(*m) for m in MANAGED_PLANS)

FAQ = [
    ("Do prices include VAT?", "No. All prices are shown excluding VAT."),
    ("Is there a minimum term?", "Subscriptions run month to month and can be cancelled with 30 days' notice. Managed services have a three-month minimum, then continue month to month."),
    ("How does annual billing work?", "Pay annually for any subscription and get two months free: you pay for ten months and receive twelve."),
    ("Is this resource augmentation?", "No. We agree outcomes, volumes and a service level, and we manage the team, tools and quality. You never have to manage individual staff."),
    ("How do you protect our data?", "Our team works inside your systems and Microsoft 365 tenant under your access controls, covered by a data processing agreement and UK GDPR safeguards for international transfers. A UK lead is accountable for every service."),
    ("Can we start small?", "Yes, and most clients do. Take the free AI Scorecard, subscribe to Executive AI Intelligence, or start with a fixed-price assessment before committing to anything larger."),
]
faq_html = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)

pricing = f"""    <section class="page-hero">
      <div class="container">
        {label("Plans &amp; pricing")}
        <h1>Clear prices. <em class="ember">No day-rate surprises.</em></h1>
        <p class="lead">Monthly subscriptions, managed services and fixed-price projects. Choose what fits, change plans as you grow, and always know the cost before we start.</p>
      </div>
    </section>
{subnav(SUBNAV_PRICING)}
    <section class="sec">
      <div class="container">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:56px">
          <div>{label("Subscriptions")}<h2 style="margin:0">Expertise on a monthly plan</h2></div>
          <div class="billing" role="group" aria-label="Billing period">
            <button type="button" data-billing="monthly" aria-pressed="true">Monthly</button>
            <button type="button" data-billing="annual" aria-pressed="false">Annual<span class="save">2 months free</span></button>
          </div>
        </div>
{subs_html}
      </div>
    </section>

    <section class="sec sec-white" id="managed" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Managed services")}<h2>Outcomes, <em class="ember">run for you.</em></h2></div>
          <p>Delivered by our Lahore team under a UK lead, to an agreed service level. <a href="managed-teams.html">More managed services →</a></p>
        </div>
{managed_html}
      </div>
    </section>

    <section class="sec" id="projects" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Fixed-price projects")}<h2>Defined scope. <em class="ember">Defined price.</em></h2></div>
          <p>Each project ends with a clear deliverable and a recommendation, and many lead naturally into a subscription or managed service.</p>
        </div>
        <div class="pricelist">
{pricelist(PROJECTS, "project")}
        </div>
      </div>
    </section>

    <section class="sec sec-sand" id="training" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Training")}<h2>Build capability <em class="ember">that lasts.</em></h2></div>
          <p>Delivered on-site in the UK or live online. Prices are per session for your group.</p>
        </div>
        <div class="pricelist">
{pricelist(TRAINING, "training")}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
{product_block(*DOJOOS, extra='<p style="margin-top:10px">' + label("Coming soon · Founding schools wanted") + '</p>')}
      </div>
    </section>

    <section class="sec sec-white" id="faq" style="scroll-margin-top:140px">
      <div class="container split">
        <div>{label("FAQs")}<h2>Good questions.</h2><p class="muted">Anything else? <a href="contact.html">Just ask.</a></p></div>
        <div class="faq">
{faq_html}
        </div>
      </div>
    </section>

{cta()}"""

page("pricing.html", "Pricing",
     "Bespoke Vista pricing: Executive AI Intelligence from £49/month, AI Advisory from £495/month, Fractional Business Architect, Managed PMO, AI Operations Team, fixed-price AI projects and DojoOS.",
     pricing)

# ============================================================== SCORECARD
scorecard = f"""    <section class="page-hero">
      <div class="container">
        {label("Free · 3 minutes · No sign-up")}
        <h1>How ready is your business <em class="ember">for AI?</em></h1>
        <p class="lead">Ten quick questions across strategy, people, process, data and governance. Get your score, see where you're strong and where to focus, and find out what to do next.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <form class="quiz" id="scorecard" onsubmit="return false" aria-live="polite">
          <div class="progress" aria-hidden="true"><span></span></div>
          <div class="q-meta"><span id="q-count">Question 1 of 10</span><span id="q-dim">Strategy</span></div>
          <div id="questions"></div>
          <div class="quiz-nav">
            <button type="button" class="btn btn-line" id="q-prev">← Back</button>
            <button type="button" class="btn btn-primary" id="q-next" disabled>Next {ARR}</button>
          </div>
          <div class="result" id="result">
            <div class="score-wrap">
              <div class="gauge">
                <svg viewBox="0 0 200 200" width="200" height="200" aria-hidden="true">
                  <defs><linearGradient id="gG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7941D"/><stop offset="1" stop-color="#EE2A24"/></linearGradient></defs>
                  <circle cx="100" cy="100" r="88" fill="none" stroke="#EDE5DA" stroke-width="14"/>
                  <circle id="r-arc" cx="100" cy="100" r="88" fill="none" stroke="url(#gG)" stroke-width="14" stroke-linecap="round" style="transition:stroke-dashoffset 1.2s cubic-bezier(.2,.7,.2,1)"/>
                </svg>
                <div class="num"><div><strong id="r-score">0</strong><small>out of 100</small></div></div>
              </div>
              <div>
                <span class="band" id="r-band"></span>
                <h2 id="r-title" style="margin:6px 0 10px;font-size:clamp(1.8rem,3.4vw,2.6rem)"></h2>
                <p id="r-text" class="muted"></p>
                <p class="small">Your biggest opportunity: <strong id="r-weak"></strong></p>
              </div>
            </div>
            <div class="bars" id="r-bars"></div>
            <div class="rec">
              <h3>Recommended next steps</h3>
              <p>Based on your answers, these are the services most likely to help. A short call is the quickest way to turn your score into a plan.</p>
              <div class="btns" id="r-recs"></div>
              <div class="btns"><a class="btn btn-ember" id="r-discuss" href="contact.html?topic=scorecard">Discuss my results {ARR}</a><button type="button" class="btn btn-line-light" id="r-retake">Retake the scorecard</button></div>
            </div>
          </div>
        </form>
        <p class="note center">Your answers stay in your browser. Nothing is sent unless you choose to contact us.</p>
      </div>
    </section>"""

page("scorecard.html", "AI Readiness Scorecard",
     "Free AI Readiness Scorecard: ten questions, three minutes. See how ready your business is for AI and what to do next.",
     scorecard)

# ============================================================== ABOUT
ROLES = ["Business Architect", "Senior Business Analyst", "Programme Consultant", "Project Manager",
         "Digital Transformation Consultant", "Cyber Security Consultant", "AI Adoption Advisor"]
FOCUS = ["AI adoption and workplace productivity", "Microsoft 365, Copilot and automation", "Business process optimisation",
         "Cyber security programmes", "Operating model design", "Change management", "Transformation delivery", "Data and technology strategy"]

about = f"""    <section class="page-hero">
      <div class="container">
        {label("About")}
        <h1>Twenty-five years of change, <em class="ember">delivered.</em></h1>
        <p class="lead">Bespoke Vista is an independent UK consultancy that combines senior expertise with a delivery team in Lahore, so good strategy actually reaches the front line.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container split">
        <div class="reveal">
          {label("Our story")}
          <h2>Built in the gap between <em class="ember">strategy and execution.</em></h2>
          <p>Founded by Azeem Mushtaq, Bespoke Vista brings together business architecture, operating model design, business analysis, programme delivery, cyber security and AI transformation.</p>
          <p>Over 25 years, Azeem has worked across logistics, supply chain, government, financial services, healthcare, education and commercial sectors, and seen the same pattern again and again: the strategy is sound, the people are capable, and the change still stalls somewhere in the middle.</p>
          <p>Bespoke Vista exists to close that gap. Senior expertise to design the change, AI to make it efficient, and a managed delivery team in Lahore to make it happen and keep it running.</p>
          <p class="pullquote" style="margin-top:36px">Understand the business. Simplify complexity. Deliver <em class="ember">measurable outcomes.</em></p>
        </div>
        <aside class="profile reveal" aria-label="Founder profile">
          <div class="avatar" aria-hidden="true">AM</div>
          <h3>Azeem Mushtaq</h3>
          <p class="role">Founder &amp; Principal Consultant</p>
          <p>Business Architecture, Digital Transformation and Cyber Security Consultant with over 25 years delivering complex technology and business change. Practitioner of martial arts, Tai Chi and Shiatsu.</p>
          <p style="color:var(--paper);font-weight:600;margin:24px 0 12px">Roles held</p>
          <ul class="chips">{''.join(f'<li>{r}</li>' for r in ROLES)}</ul>
        </aside>
      </div>
    </section>

    <section class="sec sec-dark">
      <div class="container">
        <div class="head">
          <div>{label("Principles from the dojo")}<h2>Calm, deliberate, <em class="ember">practised.</em></h2></div>
          <p>Martial arts, Tai Chi and Shiatsu teach that real skill comes from balance, discipline and flow. The same is true of organisations going through change.</p>
        </div>
        <div class="principles">
          <div class="principle reveal"><div class="word">Balance.</div><p>Strategy and delivery, cost and quality, people and technology, held together rather than traded off.</p></div>
          <div class="principle reveal"><div class="word">Discipline.</div><p>Clear governance, honest reporting and service levels we keep, week in, week out.</p></div>
          <div class="principle reveal"><div class="word">Flow.</div><p>Work that moves without friction: simpler processes, sensible automation, less waiting.</p></div>
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container grid g2" style="gap:64px">
        <div class="reveal">
          {label("Current focus")}
          <h2>Where we spend our time today</h2>
          <ul class="ticks">{''.join(f'<li>{f}</li>' for f in FOCUS)}</ul>
        </div>
        <div class="reveal">
          {label("Lahore delivery hub")}
          <h2>A team that extends yours</h2>
          <p>Bespoke Vista has office facilities and teams in Lahore, Pakistan, and can rapidly mobilise analysts, PMO staff, administrators, AI operators, customer support and shared-service teams.</p>
          <p>We have long experience bridging UK organisations and offshore teams in Pakistan and India: clear requirements, shared ways of working, practical governance and the cultural understanding that keeps distributed teams moving together.</p>
          <a class="btn btn-primary" href="managed-teams.html">Explore managed teams {ARR}</a>
        </div>
      </div>
    </section>

{cta("Let's talk about what you're trying to change.", "A 30-minute conversation, no obligation. You'll leave with at least one useful idea, whether or not we work together.", ("Book a 30-minute call", "contact.html?topic=consultation"), ("Read our case studies", "case-studies.html"))}"""

page("about.html", "About",
     "Founded by Azeem Mushtaq, Bespoke Vista combines 25+ years of business architecture, transformation, cyber security and AI expertise with a delivery hub in Lahore.",
     about)

# ============================================================== CASE STUDIES
CASES = [
    ("enterprise-transformation", "Transformation", "Enterprise transformation", "People, process and technology",
     "Large organisations needing to change how they operate while keeping day-to-day services running, with many stakeholders, legacy systems and competing priorities.",
     "Business architecture and analysis to build a shared view of the current state and target operating model, followed by roadmap planning, stakeholder engagement and hands-on support through delivery.",
     "Supported major organisations through complex transformation programmes, turning strategic intent into workable delivery plans."),
    ("cyber-security", "Cyber security", "Cyber security programmes", "Business analysis, project management and consulting",
     "Security initiatives that cut across the whole organisation, needing technical controls translated into business requirements, governance and change that people actually adopt.",
     "Business analysis to define requirements and processes, project management to coordinate workstreams and suppliers, and consulting support on governance and risk.",
     "Delivered business analysis, project management and consulting on significant cyber security initiatives, helping organisations strengthen resilience and reduce risk."),
    ("ai-productivity", "AI &amp; automation", "AI productivity improvements", "Practical AI in everyday work",
     "Teams spending too much time on repetitive manual work such as drafting, summarising, analysis and documentation, with inconsistent results.",
     "Identifying the right use cases, introducing AI-driven ways of working with sensible guardrails, and helping teams build the skills and prompts to use the tools well.",
     "AI-driven approaches that helped teams reduce manual effort, improve consistency and accelerate delivery."),
    ("international-delivery", "Global delivery", "International delivery", "UK, Pakistan and India",
     "Organisations wanting to use global talent and offshore capability without losing quality, control or pace.",
     "Bridging UK stakeholders and offshore teams with clear requirements, shared ways of working, practical governance and cultural understanding.",
     "Effective delivery across the UK, Pakistan and India, helping organisations make the most of global talent."),
    ("property-recovery", "Business recovery", "Property business recovery", "Rental property business, Lahore",
     "A rental property business in Lahore with declining performance and operations that needed restoring and modernising.",
     "A practical turnaround: reviewing the business end to end, improving operations and tenant management, and modernising how it was run.",
     "The business was restored and modernised, with improved occupancy, operations and overall performance."),
]
case_html = "\n".join(f"""        <article class="case reveal" id="{cid}">
          <div class="idx">{i+1:02d}</div>
          <div><span class="tag">{tag}</span><h2>{t}</h2><p class="sub">{sub}</p></div>
          <div class="case-body"><h3>The challenge</h3><p>{c}</p><h3>Our approach</h3><p>{a}</p><h3>The outcome</h3><p>{o}</p></div>
        </article>""" for i, (cid, tag, t, sub, c, a, o) in enumerate(CASES))

cases = f"""    <section class="page-hero">
      <div class="container">
        {label("Case studies")}
        <h1>Work that <em class="ember">speaks for itself.</em></h1>
        <p class="lead">A selection of the experience behind Bespoke Vista. Client names are withheld; we're happy to talk through relevant work in more detail.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container">
{case_html}
      </div>
    </section>

{cta("Have a challenge like these?", "Tell us about it. We'll suggest a practical first step and a fixed price to get started.", ("Book a 30-minute call", "contact.html?topic=consultation"), ("See services", "services.html"))}"""

page("case-studies.html", "Case Studies",
     "Case studies from Bespoke Vista: enterprise transformation, cyber security, AI productivity, international delivery and business recovery.",
     cases)

# ============================================================== INSIGHTS
ARTICLES = [
    ("ai-readiness", "AI adoption", "6 min read", "Five questions to ask before you invest in AI",
     "Most AI initiatives stall not because the technology fails, but because the groundwork was skipped.",
     """<p>Every leadership team is being asked what it is doing about AI. The pressure to act is real, but the organisations getting value are the ones that start with the business problem, not the tool.</p>
          <h3>1. Which work actually hurts?</h3>
          <p>Look for high-volume, repetitive tasks where people spend time drafting, searching, summarising or re-keying information. These are where AI most reliably saves time.</p>
          <h3>2. Is the process stable enough to improve?</h3>
          <p>Automating a broken process just produces broken outcomes faster. If a process varies wildly between teams, simplify and standardise it first.</p>
          <h3>3. Where does your data live, and who can see it?</h3>
          <p>Tools such as Microsoft Copilot surface whatever a user already has access to. Poor permissions become visible very quickly. Tidy access before rollout, not after.</p>
          <h3>4. What does good look like?</h3>
          <p>Agree a small number of measures up front: hours saved, turnaround time, error rates or customer response times. Without them, AI becomes a cost line with anecdotes attached.</p>
          <h3>5. Who owns adoption?</h3>
          <p>Licences don't change behaviour; people do. Plan for training, champions, guidance on safe use and a feedback loop. Adoption is a change programme and needs to be run like one.</p>
          <p>Want a quick read on where you stand? <a href="scorecard.html">Take the free AI Readiness Scorecard.</a></p>"""),
    ("failing-programmes", "Delivery", "5 min read", "Spotting a failing programme before it fails",
     "Programmes rarely collapse overnight. The warning signs are visible months earlier, if you know where to look.",
     """<p>When a transformation programme goes wrong, the post-mortem often reveals that people knew. The signals were there; they just weren't joined up or acted on.</p>
          <h3>The status report is always amber</h3>
          <p>A programme that has been "amber, recovering" for three reporting cycles is red. Persistent amber usually means the reporting is protecting someone rather than informing decisions.</p>
          <h3>Requirements keep growing, dates don't move</h3>
          <p>Scope creep without re-planning is borrowing from the future. Somewhere, quality or testing is being squeezed to make the numbers work.</p>
          <h3>The business has stopped turning up</h3>
          <p>When senior users stop attending design sessions and send delegates instead, the programme has lost its sponsor in all but name.</p>
          <h3>Nobody can explain the benefits</h3>
          <p>If the team cannot describe, in plain language, what will be better and for whom, the programme has drifted from its purpose.</p>
          <p>An independent <a href="pricing.html#projects">Transformation Health Check</a> gives executives an honest view and a recovery plan while there is still time to use it.</p>"""),
    ("offshore-outcomes", "Managed services", "5 min read", "Why offshoring fails, and how to make it work",
     "Most offshoring disappoints because it sells hours, not results. Change what you buy and the results change too.",
     """<p>Many UK businesses have tried offshoring and been burned: missed deadlines, quality issues and a UK manager spending half their week chasing. The talent was rarely the problem. The model was.</p>
          <h3>Buying hours shifts the risk to you</h3>
          <p>When you rent people by the hour, every inefficiency is your cost and every quality issue is your problem to manage. The supplier is paid either way.</p>
          <h3>Define the outcome, not the headcount</h3>
          <p>Describe what "done" looks like: the reports, the documents processed, the turnaround time and the quality standard. Then let the supplier decide how to staff it.</p>
          <h3>Write the playbook first</h3>
          <p>Documented processes are what make a remote team effective, and they mean the knowledge belongs to you, not to whoever happens to be doing the work.</p>
          <h3>Put AI in the loop</h3>
          <p>AI handles the repetitive first pass; people review, correct and improve it. Costs fall over time instead of creeping up.</p>
          <p>That's the model behind our <a href="managed-teams.html">managed teams</a>: UK-led, Lahore-delivered and priced on outcomes.</p>"""),
    ("cyber-is-business", "Cyber security", "4 min read", "Cyber security is a business change programme",
     "Security programmes run purely as technology projects struggle to land. The ones that succeed treat people and process as seriously as tools.",
     """<p>New controls, new tooling and new policies all change how people work. Yet security programmes are often scoped and resourced as if they were infrastructure upgrades.</p>
          <h3>Translate risk into business language</h3>
          <p>Boards fund what they understand. Framing security work in terms of service continuity, customer trust and regulatory exposure gets better decisions than framing it in terms of technical controls.</p>
          <h3>Map the processes you are changing</h3>
          <p>Access management, joiners-movers-leavers, incident response and supplier assurance are all business processes. Good business analysis makes sure the new way of working is clear, owned and workable.</p>
          <h3>Plan for adoption</h3>
          <p>Awareness, clear guidance and a sensible exceptions process stop people finding workarounds. A control nobody follows is not a control.</p>
          <p>We provide <a href="services.html#advise">business analysis and delivery support</a> for security programmes, bridging specialists, the wider business and suppliers.</p>"""),
]
art_cards = "\n".join(f"""          <a class="card article-card reveal" href="#{aid}">
            <div class="meta">{cat} · {m}</div>
            <h3>{t}</h3>
            <p>{s}</p>
            <span class="more">Read →</span>
          </a>""" for aid, cat, m, t, s, _ in ARTICLES)
art_bodies = "\n".join(f"""        <article class="article" id="{aid}">
          <div class="meta">{cat} · {m}</div>
          <h2>{t}</h2>
          {b}
        </article>""" for aid, cat, m, t, s, b in ARTICLES)

SUBSCRIBE = f"""        <div class="subscribe reveal">
          <div>
            {label("Executive AI Intelligence")}
            <h2>The AI briefing for <em class="ember">busy leaders.</em></h2>
            <p>What's changed, what matters for UK businesses and what to do next, in one short monthly briefing. Plans from £49 a month.</p>
          </div>
          <form data-email="{CONTACT_EMAIL}" data-subject="Executive AI Intelligence: subscription request" data-endpoint="" novalidate>
            <div class="inline-form">
              <label class="sr-only" for="sub-email">Work email</label>
              <input id="sub-email" name="email" type="email" placeholder="Your work email" autocomplete="email" required>
              <button class="btn btn-ember" type="submit">Request a sample</button>
            </div>
            <small>We'll send a sample briefing and plan details. No spam, unsubscribe any time.</small>
            <div class="form-status" role="status" aria-live="polite"></div>
          </form>
        </div>"""

insights = f"""    <section class="page-hero">
      <div class="container">
        {label("Insights")}
        <h1>Practical thinking, <em class="ember">no hype.</em></h1>
        <p class="lead">Short articles on AI adoption, delivery, managed services and cyber security, drawn from real experience.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="grid g2">
{art_cards}
        </div>
      </div>
    </section>

    <section class="sec-tight">
      <div class="container">
{SUBSCRIBE}
      </div>
    </section>

    <section class="sec">
      <div class="container">
{art_bodies}
      </div>
    </section>

{cta()}"""

page("insights.html", "Insights",
     "Practical articles from Bespoke Vista on AI adoption, programme delivery, offshore managed services and cyber security.",
     insights)

# ============================================================== CONTACT
TOPICS = [
    ("consultation", "Book a 30-minute call"),
    ("project", "Discuss a project"),
    ("scorecard", "My AI Scorecard results"),
    ("intelligence", "Executive AI Intelligence"),
    ("advisory", "Bespoke Vista AI Advisory"),
    ("fractional", "Fractional Business Architect"),
    ("managed", "Managed teams (general)"),
    ("pmo", "Managed PMO Office"),
    ("aiops", "AI Operations Team"),
    ("documentation", "Documentation Factory"),
    ("baas", "Business Analysis as a Service"),
    ("back-office", "Managed Back Office"),
    ("knowledge", "Knowledge Management Service"),
    ("ai-readiness", "AI Readiness Assessment"),
    ("ai-optimisation", "AI Optimisation Review"),
    ("governance", "AI Governance Pack"),
    ("ai-sprint", "AI Implementation Sprint"),
    ("copilot", "Microsoft Copilot Adoption Programme"),
    ("health-check", "Transformation Health Check"),
    ("tom", "Target Operating Model Design"),
    ("cyber-ba", "Cyber Security Business Analysis"),
    ("training", "Training and workshops"),
    ("wellbeing", "Calm Under Pressure workshop"),
    ("dojoos", "DojoOS founding list"),
    ("other", "Something else"),
]
topic_opts = "\n".join(f'                <option value="{v}">{l}</option>' for v, l in TOPICS)

contact = f"""    <section class="page-hero">
      <div class="container">
        {label("Contact")}
        <h1>Let's talk about <em class="ember">what's next.</em></h1>
        <p class="lead">Whether you're launching a transformation, strengthening cyber resilience, exploring AI or looking to hand over operational work, start with a conversation.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container contact-grid">
        <div class="reveal">
          <h2>A 30-minute call, no obligation.</h2>
          <p>Tell us a little about your organisation and what you're trying to achieve. We'll come back within one working day to arrange a time.</p>
          <ul class="contact-ways">
            <li><strong>Email</strong><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
            <li><strong>Where we are</strong>United Kingdom, with a delivery hub in Lahore, Pakistan</li>
            <li><strong>Right now</strong>{CLOCKS}</li>
            <li><strong>Prefer to start on your own?</strong><a href="scorecard.html">Take the free AI Readiness Scorecard →</a></li>
          </ul>
        </div>
        <form class="form reveal" id="contact-form" data-email="{CONTACT_EMAIL}" data-endpoint="" novalidate>
          <div class="form-row">
            <div class="field"><label for="name">Name *</label><input id="name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="organisation">Organisation</label><input id="organisation" name="organisation" type="text" autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="email">Email *</label><input id="email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>
          <div class="field">
            <label for="topic">What can we help with?</label>
            <select id="topic" name="topic">
{topic_opts}
            </select>
          </div>
          <div class="field"><label for="message">Your message *</label><textarea id="message" name="message" required placeholder="A few lines about your organisation, the challenge and any timescales."></textarea></div>
          <button class="btn btn-primary" type="submit">Send message {ARR}</button>
          <p class="form-note">We only use your details to respond to your enquiry.</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </section>"""

page("contact.html", "Contact",
     "Contact Bespoke Vista to discuss AI adoption, managed teams, transformation or a subscription plan.",
     contact)
