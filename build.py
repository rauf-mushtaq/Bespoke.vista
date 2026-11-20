#!/usr/bin/env python3
"""Builds the static pages for bespokevista from the templates below.

Header and footer are shared, so edit them once here and run:
    python3 build.py
The generated .html files are committed so the site can be hosted as-is
(GitHub Pages, Netlify, any static host) with no build step on the server.
"""
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "Bespoke Vista"
TAGLINE = "Bridging Strategy and Execution"
CONTACT_EMAIL = "hello@bespokevista.co.uk"  # TODO: confirm the business email address

# Logo links to Home, so the menu stays short: four links plus a Contact button.
NAV = [
    ("services.html", "Services"),
    ("case-studies.html", "Case Studies"),
    ("about.html", "About"),
    ("insights.html", "Insights"),
]

LOGO = ('<img src="assets/img/logo.png" srcset="assets/img/logo.png 1x, assets/img/logo@2x.png 2x" '
        'alt="" width="58" height="40">')

# Simple stroke icons (24x24)
I = {
    "transform": '<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>',
    "architecture": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M17.5 14v7M14 17.5h7"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "ai": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9z"/>',
    "delivery": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "strategy": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "hands": '<path d="M4 20h16M6 20V10l6-6 6 6v10"/><path d="M10 20v-5h4v5"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
    "handshake": '<path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}


def icon(name):
    return (f'<div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg></div>')


def header(active):
    items = "\n".join(
        f'        <li><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f"""  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <nav class="container nav" aria-label="Main">
      <a class="brand" href="index.html" aria-label="{SITE} home">
        {LOGO}
        <span class="brand-text"><span class="brand-name">{SITE}</span><span class="brand-tag">{TAGLINE}</span></span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
      <ul class="nav-links" id="nav-links">
{items}
        <li><a class="btn btn-primary btn-sm nav-cta" href="contact.html"{" aria-current=\"page\"" if active == "contact.html" else ""}>Contact</a></li>
      </ul>
    </nav>
  </header>"""


FOOTER = f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a class="brand" href="index.html" aria-label="{SITE} home">
            {LOGO}
            <span class="brand-text"><span class="brand-name">{SITE}</span></span>
          </a>
          <p class="footer-tagline">{TAGLINE}.</p>
          <p>Independent UK consultancy for business architecture, digital transformation, cyber security and AI adoption.</p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="services.html#digital-transformation">Digital Transformation</a></li>
            <li><a href="services.html#business-analysis">Business Analysis &amp; Architecture</a></li>
            <li><a href="services.html#cyber-security">Cyber Security</a></li>
            <li><a href="services.html#ai-adoption">AI Adoption &amp; Automation</a></li>
            <li><a href="services.html#delivery">Programme Delivery</a></li>
          </ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="case-studies.html">Case Studies</a></li>
            <li><a href="insights.html">Insights</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul>
            <li><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
            <li>United Kingdom</li>
            <li><a href="contact.html">Book a consultation</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span id="year">2026</span> Bespoke Vista Ltd. All rights reserved.</span>
        <span>Registered in England &amp; Wales.</span>
      </div>
    </div>
  </footer>"""


def page(filename, title, description, body):
    full_title = f"{title} | {SITE}" if filename != "index.html" else f"{SITE} | {TAGLINE}"
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta name="theme-color" content="#0F172A">
  <link rel="icon" href="assets/img/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap" rel="stylesheet">
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


CTA = """    <section>
      <div class="container">
        <div class="cta-band reveal">
          <div>
            <h2>Let's discuss your next transformation initiative.</h2>
            <p>Whether you're starting a programme, recovering one, or exploring what AI could do for your teams, a short conversation is the best place to begin.</p>
          </div>
          <a class="btn" href="contact.html">Book a Consultation</a>
        </div>
      </div>
    </section>"""

# ---------------------------------------------------------------- Home
SERVICES = [
    ("digital-transformation", "transform", "Digital Transformation",
     "Modernising processes, systems and operating models to improve performance and customer outcomes."),
    ("business-analysis", "architecture", "Business Analysis &amp; Architecture",
     "Bringing clarity to complex business challenges, from capability maps to target operating models."),
    ("cyber-security", "shield", "Cyber Security Consulting",
     "Improving resilience and reducing risk through well-governed, well-delivered security programmes."),
    ("ai-adoption", "ai", "AI Adoption &amp; Automation",
     "Practical, governed use of AI and automation that frees people to do higher-value work."),
    ("delivery", "delivery", "Project &amp; Programme Delivery",
     "Leading large initiatives from concept to implementation, including recovery of programmes in trouble."),
]

service_cards = "\n".join(f"""          <a class="card reveal" href="services.html#{sid}" style="color:inherit;text-decoration:none">
            {icon(ic)}
            <h3>{name}</h3>
            <p>{desc}</p>
            <span class="card-link">Learn more &rarr;</span>
          </a>""" for sid, ic, name, desc in SERVICES)

WHY = [
    ("strategy", "Strategic thinking", "A business-first approach. Technology is chosen to serve the outcome, not the other way round."),
    ("hands", "Hands-on delivery", "Not just advice. Real implementation experience, from mobilisation to go-live and beyond."),
    ("layers", "Cross-disciplinary expertise", "Business, technology, cyber security and AI, joined up in one perspective."),
    ("globe", "Global experience", "Delivery across the UK, Pakistan and India, bridging multicultural and offshore teams."),
    ("handshake", "Trusted partner", "25+ years of transformation experience across public and private sectors."),
]
why_cards = "\n".join(f"""          <div class="card reveal">
            {icon(ic)}
            <h3>{t}</h3>
            <p>{d}</p>
          </div>""" for ic, t, d in WHY)

INDUSTRIES = ["Logistics", "Supply Chain", "Retail", "Financial Services", "Healthcare",
              "Education", "Government", "Professional Services", "Property"]
industry_chips = "\n".join(f"            <li>{x}</li>" for x in INDUSTRIES)

home = f"""    <section class="hero">
      <div class="container">
        <span class="eyebrow">Independent UK consultancy</span>
        <h1>Transforming Businesses Through Strategy, Technology and AI</h1>
        <p class="lead">Helping organisations design better operating models, modernise technology, strengthen cyber resilience and harness AI to improve productivity and business performance.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="contact.html?topic=consultation">Book a Consultation</a>
          <a class="btn btn-ghost" href="contact.html?topic=project">Discuss Your Project</a>
        </div>
        <div class="hero-stats">
          <div><strong>25+</strong><span>Years delivering business and technology change</span></div>
          <div><strong>5</strong><span>Core disciplines, one joined-up view</span></div>
          <div><strong>8+</strong><span>Sectors, from logistics to healthcare</span></div>
          <div><strong>3</strong><span>Countries of delivery: UK, Pakistan, India</span></div>
        </div>
      </div>
    </section>

    <section>
      <div class="container split">
        <div class="reveal">
          <span class="eyebrow">Our approach</span>
          <h2>From strategy to successful execution</h2>
          <p>Many organisations have a clear strategy and capable teams, yet change still stalls somewhere between the boardroom and the front line. Bespoke Vista works in that gap.</p>
          <p>We align business goals, technology, operations and people so that change programmes deliver measurable outcomes rather than slide decks.</p>
          <a class="btn btn-outline" href="about.html">About Bespoke Vista</a>
        </div>
        <blockquote class="quote reveal">Understand the business. Simplify complexity. Deliver measurable outcomes.</blockquote>
      </div>
    </section>

    <section class="section-alt">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Services</span>
          <h2>Where business, technology and AI meet</h2>
          <p>Five connected disciplines, delivered by someone who has done the work, not just advised on it.</p>
        </div>
        <div class="grid grid-3">
{service_cards}
          <a class="card reveal" href="services.html#packages" style="color:inherit;text-decoration:none;background:var(--navy);border-color:var(--navy)">
            <h3 style="color:#fff">Fixed-scope engagements</h3>
            <p style="color:var(--silver)">AI Readiness Assessments, Copilot adoption, Transformation Health Checks and fractional leadership, with clear scope and pricing.</p>
            <span class="card-link" style="color:var(--accent-light)">View packages &rarr;</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section-dark">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow" style="color:var(--accent-light)">How we work</span>
          <h2>A simple, practical method</h2>
        </div>
        <div class="approach">
          <div class="reveal">
            <div class="num">01</div>
            <h3>Understand the business</h3>
            <p>We start with goals, constraints and the people doing the work. Capability maps, process models and honest conversations come before any solution.</p>
          </div>
          <div class="reveal">
            <div class="num">02</div>
            <h3>Simplify complexity</h3>
            <p>We turn competing priorities into a clear target state, a realistic roadmap and decisions that stakeholders can stand behind.</p>
          </div>
          <div class="reveal">
            <div class="num">03</div>
            <h3>Deliver measurable outcomes</h3>
            <p>We stay through delivery: mobilising teams, managing risk, coordinating vendors and offshore partners, and tracking benefits.</p>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Why Bespoke Vista</span>
          <h2>Senior expertise, without the overhead</h2>
        </div>
        <div class="grid grid-3">
{why_cards}
          <div class="card reveal" style="background:var(--accent-soft);border-color:var(--accent-border);box-shadow:none">
            <h3>Industries we know</h3>
            <ul class="chips" style="margin-top:6px">
{industry_chips}
            </ul>
          </div>
        </div>
      </div>
    </section>

{CTA}"""

page("index.html", SITE,
     "Bespoke Vista is an independent UK consultancy helping organisations bridge strategy and execution across digital transformation, business architecture, cyber security and AI adoption.",
     home)

# ---------------------------------------------------------------- About
ROLES = ["Business Architect", "Senior Business Analyst", "Programme Consultant", "Project Manager",
         "Digital Transformation Consultant", "Cyber Security Consultant", "AI Adoption Advisor"]
FOCUS = ["AI adoption and workplace productivity", "Business process optimisation", "Cyber security programmes",
         "Operating model design", "Digital transformation", "Automation", "Change management",
         "Transformation delivery", "Data and technology strategy"]
role_chips = "\n".join(f"              <li>{r}</li>" for r in ROLES)
focus_list = "\n".join(f"              <li>{f}</li>" for f in FOCUS)
SECTORS = ["Logistics", "Supply chain", "Government", "Financial services", "Healthcare", "Education", "Commercial"]
sector_chips = "\n".join(f"            <li>{x}</li>" for x in SECTORS)

about = f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">About</span>
        <h1>Over 25 years helping organisations navigate complex change</h1>
        <p>An independent consultancy built on a simple belief: strategy only matters when it is delivered.</p>
      </div>
    </section>

    <section>
      <div class="container split" style="align-items:start">
        <div class="reveal">
          <h2>Who we are</h2>
          <p>For over 25 years, Bespoke Vista's founder has helped organisations navigate complex business and technology change.</p>
          <p>Founded by Azeem Mushtaq, the consultancy brings together expertise across business architecture, target operating model design, business analysis, programme delivery, cyber security and AI transformation.</p>
          <p>Whether supporting large transformation programmes, cyber security initiatives, operational redesign or AI adoption, Bespoke Vista helps organisations move from strategy to successful execution.</p>
          <blockquote class="quote" style="margin-top:36px">Understand the business. Simplify complexity. Deliver measurable outcomes.</blockquote>
        </div>
        <aside class="profile-card reveal" aria-label="Founder profile">
          <div class="monogram" aria-hidden="true">AM</div>
          <h3>Azeem Mushtaq</h3>
          <p class="role">Founder &amp; Principal Consultant</p>
          <p>Business Architecture, Digital Transformation and Cyber Security Consultant with over 25 years of experience delivering complex technology and business change.</p>
          <p style="color:#fff;font-weight:600;margin:24px 0 12px">Roles held</p>
          <ul class="chips">
{role_chips}
          </ul>
        </aside>
      </div>
    </section>

    <section class="section-alt">
      <div class="container split" style="align-items:start">
        <div class="reveal">
          <span class="eyebrow">Current focus</span>
          <h2>Where we spend our time today</h2>
          <p>The fundamentals of good change haven't moved. The tools have. Our recent work concentrates on the areas where organisations are seeing the most pressure and the most opportunity.</p>
        </div>
        <div class="reveal">
          <ul class="checks cols">
{focus_list}
          </ul>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="grid grid-2">
          <div class="reveal">
            <span class="eyebrow">Sector experience</span>
            <h2>Breadth across industries</h2>
            <p>Experience across the public and private sector means we recognise the patterns, regulatory pressures and stakeholder dynamics quickly, and we bring ideas that have worked elsewhere.</p>
            <ul class="chips">
{sector_chips}
            </ul>
          </div>
          <div class="reveal">
            <span class="eyebrow">International delivery</span>
            <h2>Bridging teams across geographies</h2>
            <p>Bespoke Vista has supported offshore delivery teams in Pakistan and India, bridging multicultural teams and helping UK organisations make the most of global talent.</p>
            <p>That means clear requirements, shared ways of working, realistic governance and the cultural understanding that keeps distributed teams moving in the same direction.</p>
          </div>
        </div>
      </div>
    </section>

{CTA}"""

page("about.html", "About",
     "Founded by Azeem Mushtaq, Bespoke Vista brings 25+ years of experience in business architecture, transformation, cyber security and AI adoption.",
     about)

# ---------------------------------------------------------------- Services
SERVICE_DETAIL = [
    ("digital-transformation", "transform", "Digital Transformation",
     "Helping organisations modernise processes, systems and operating models to improve performance and customer outcomes.",
     ["Transformation strategy", "Business architecture", "Process redesign", "Technology roadmap development",
      "Change management", "Programme mobilisation"]),
    ("business-analysis", "architecture", "Business Analysis &amp; Architecture",
     "Bringing clarity to complex business challenges.",
     ["Requirements management", "Process modelling", "Capability mapping", "Business architecture",
      "Operating model design", "Stakeholder engagement"]),
    ("cyber-security", "shield", "Cyber Security Consulting",
     "Supporting organisations to improve resilience and reduce risk.",
     ["Security programme delivery", "Security governance", "Risk assessment", "Security transformation",
      "Regulatory compliance support", "Cyber awareness initiatives"]),
    ("ai-adoption", "ai", "AI Adoption &amp; Automation",
     "Helping organisations take practical advantage of AI, safely and with clear business value.",
     ["AI opportunity assessments", "Productivity improvements", "Process automation", "AI governance",
      "Copilot adoption", "Prompt engineering", "AI use case development"]),
    ("delivery", "delivery", "Project &amp; Programme Delivery",
     "Leading large-scale initiatives from concept to implementation.",
     ["Programme management", "Project recovery", "Delivery assurance", "PMO leadership",
      "Vendor management", "Offshore coordination"]),
]
service_blocks = "\n".join(f"""          <article class="service reveal" id="{sid}">
            <div>
              {icon(ic)}
              <h2>{name}</h2>
            </div>
            <div>
              <p class="intro">{intro}</p>
              <h3>Services include</h3>
              <ul class="checks cols">
{chr(10).join(f"                <li>{i}</li>" for i in items)}
              </ul>
              <a class="btn btn-outline btn-sm" href="contact.html?topic=project">Discuss your requirements</a>
            </div>
          </article>""" for sid, ic, name, intro, items in SERVICE_DETAIL)

PACKAGES = [
    ("AI Readiness Assessment", "Fixed price: £1,500 to £3,000",
     "A focused review of your current business processes to identify where AI can genuinely help, with a prioritised set of opportunities and next steps.", "ai-readiness", True),
    ("Microsoft Copilot Adoption Programme", "£5,000 to £25,000",
     "Assessment, governance, training and implementation, so Copilot is used well, safely and widely rather than left as an unused licence.", "copilot", False),
    ("Transformation Health Check", "Fixed scope",
     "An executive-level, independent review of a struggling programme: what is really happening, what to stop, and how to get back on track.", "health-check", False),
    ("Process Automation Review", "Fixed scope",
     "Identify automation opportunities using AI and workflow tools, with effort, value and risk set out for each.", "automation", False),
    ("Target Operating Model Design", "Day rate",
     "Design the people, process, technology and governance needed to deliver your strategy, and a practical path to get there.", "tom", False),
    ("Cyber Security Business Analysis", "Contract or consultancy",
     "Experienced business analysis for security programmes, bridging security teams, the business and suppliers.", "cyber-ba", False),
    ("Fractional Transformation Director", "Part-time retainer",
     "Senior transformation leadership for SMEs, a few days a month, without the cost of a full-time hire.", "fractional", False),
]
package_cards = "\n".join(f"""          <div class="card offer reveal{' featured' if feat else ''}">
            {'<span class="badge">Popular starting point</span>' if feat else ''}
            <span class="price">{price}</span>
            <h3>{name}</h3>
            <p>{desc}</p>
            <a class="card-link" href="contact.html?topic={topic}">Enquire &rarr;</a>
          </div>""" for name, price, desc, topic, feat in PACKAGES)

SUBNAV = [("digital-transformation", "Digital Transformation"), ("business-analysis", "Business Analysis"),
          ("cyber-security", "Cyber Security"), ("ai-adoption", "AI &amp; Automation"),
          ("delivery", "Programme Delivery"), ("packages", "Packages &amp; Pricing")]
subnav_links = "\n".join(f'          <li><a href="#{a}">{l}</a></li>' for a, l in SUBNAV)

services = f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Services</span>
        <h1>Expertise across business, technology, security and AI</h1>
        <p>Engage us for a defined package, a consultancy assignment or hands-on delivery leadership. Every engagement is shaped around the outcome you need.</p>
      </div>
    </section>

    <nav class="subnav" aria-label="Jump to a service">
      <div class="container">
        <ul>
{subnav_links}
        </ul>
      </div>
    </nav>

    <section>
      <div class="container">
{service_blocks}
      </div>
    </section>

    <section class="section-alt" id="packages" style="scroll-margin-top:72px">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Packaged engagements</span>
          <h2>Clear scope. Clear value.</h2>
          <p>Well-defined engagements for common needs. Each can be tailored, and each is a natural starting point for longer-term support.</p>
        </div>
        <div class="grid grid-3">
{package_cards}
        </div>
        <p style="margin-top:28px;color:var(--muted);font-size:.92rem">Prices are indicative and exclude VAT. Final pricing depends on scope and is always agreed in advance.</p>
      </div>
    </section>

{CTA}"""

page("services.html", "Services",
     "Digital transformation, business analysis and architecture, cyber security consulting, AI adoption and programme delivery from Bespoke Vista.",
     services)

# ---------------------------------------------------------------- Case studies
CASES = [
    ("enterprise-transformation", "Transformation", "Enterprise Transformation",
     "People, process and technology",
     "Large organisations needing to change how they operate while keeping day-to-day services running, with many stakeholders, legacy systems and competing priorities.",
     "Business architecture and analysis to establish a shared view of the current state and target operating model, followed by roadmap planning, stakeholder engagement and hands-on support through delivery.",
     "Supported major organisations through complex transformation programmes involving people, process and technology, turning strategic intent into workable delivery plans."),
    ("cyber-security", "Cyber Security", "Cyber Security Programmes",
     "Business analysis, project management and consulting",
     "Security initiatives that cut across the whole organisation, needing technical controls to be translated into business requirements, governance and change that people actually adopt.",
     "Business analysis to define requirements and processes, project management to coordinate workstreams and suppliers, and consulting support on governance and risk.",
     "Delivered business analysis, project management and consulting services on significant cyber security initiatives, helping organisations strengthen resilience and reduce risk."),
    ("ai-productivity", "AI &amp; Automation", "AI Productivity Improvements",
     "Practical AI in everyday work",
     "Teams spending too much time on repetitive, manual work such as drafting, summarising, analysis and documentation, with inconsistent outputs as a result.",
     "Identifying the right use cases, introducing AI-driven ways of working with sensible guardrails, and helping teams build the skills and prompts to use the tools well.",
     "Implemented AI-driven approaches that helped teams reduce manual effort, improve consistency and accelerate delivery."),
    ("international-delivery", "Global Delivery", "International Delivery",
     "UK, Pakistan and India",
     "Organisations wanting to use global talent and offshore capability without losing quality, control or pace.",
     "Bridging UK stakeholders and offshore teams with clear requirements, shared ways of working, practical governance and cultural understanding.",
     "Worked across the UK, Pakistan and India, helping organisations make effective use of global talent and offshore capability."),
    ("property-recovery", "Business Recovery", "Property Business Recovery",
     "Rental property business, Lahore",
     "A rental property business in Lahore with declining performance and operations that needed restoring and modernising.",
     "A practical turnaround: reviewing the business end to end, improving operations and tenant management, and modernising how the business was run.",
     "Successfully restored and modernised the business, improving occupancy, operations and overall business performance."),
]
case_blocks = "\n".join(f"""        <article class="case reveal" id="{cid}">
          <div class="case-meta">
            <span class="tag">{tag}</span>
            <h2>{title}</h2>
            <p>{sub}</p>
          </div>
          <div class="case-body">
            <h3>The challenge</h3>
            <p>{ch}</p>
            <h3>Our approach</h3>
            <p>{ap}</p>
            <h3>The outcome</h3>
            <p>{out}</p>
          </div>
        </article>""" for cid, tag, title, sub, ch, ap, out in CASES)

cases = f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Case Studies</span>
        <h1>Experience across transformation, security, AI and delivery</h1>
        <p>A selection of the work behind Bespoke Vista. Client names are withheld; we're happy to talk through relevant experience in more detail.</p>
      </div>
    </section>

    <section class="section-alt">
      <div class="container">
{case_blocks}
      </div>
    </section>

    <section>
      <div class="container">
        <div class="section-head center">
          <span class="eyebrow">Industries</span>
          <h2>Sectors we've worked in</h2>
        </div>
        <ul class="chips reveal" style="justify-content:center">
{industry_chips}
        </ul>
      </div>
    </section>

{CTA}"""

page("case-studies.html", "Case Studies",
     "Case studies from Bespoke Vista: enterprise transformation, cyber security programmes, AI productivity, international delivery and business recovery.",
     cases)

# ---------------------------------------------------------------- Insights
ARTICLES = [
    ("ai-readiness", "AI Adoption", "6 min read",
     "Five questions to ask before you invest in AI",
     "Most AI initiatives stall not because the technology fails, but because the groundwork was skipped. Here is where to start.",
     """<p>Every leadership team is being asked what it is doing about AI. The pressure to act is real, but the organisations getting value are the ones that start with the business problem, not the tool.</p>
          <h3>1. Which work actually hurts?</h3>
          <p>Look for high-volume, repetitive tasks where people spend time drafting, searching, summarising or re-keying information. These are where AI most reliably saves time.</p>
          <h3>2. Is the process stable enough to improve?</h3>
          <p>Automating a broken process just produces broken outcomes faster. If a process varies wildly between teams, simplify and standardise it first.</p>
          <h3>3. Where does your data live, and who can see it?</h3>
          <p>Tools such as Microsoft Copilot surface whatever a user already has access to. Poor permissions become visible very quickly. Tidy access before rollout, not after.</p>
          <h3>4. What does "good" look like?</h3>
          <p>Agree a small number of measures up front: hours saved, turnaround time, error rates or customer response times. Without them, AI becomes a cost line with anecdotes attached.</p>
          <h3>5. Who owns adoption?</h3>
          <p>Licences don't change behaviour; people do. Plan for training, champions, guidance on safe use and a feedback loop. Adoption is a change programme, and it needs to be run like one.</p>
          <p>An <a href="services.html#packages">AI Readiness Assessment</a> works through these questions with you in a few weeks and leaves you with a prioritised, costed set of opportunities.</p>"""),
    ("failing-programmes", "Delivery", "5 min read",
     "Spotting a failing programme before it fails",
     "Programmes rarely collapse overnight. The warning signs are usually visible months earlier, if you know where to look.",
     """<p>When a transformation programme goes wrong, the post-mortem often reveals that people knew. The signals were there; they just weren't joined up or acted on.</p>
          <h3>The status report is always amber</h3>
          <p>A programme that has been "amber, recovering" for three reporting cycles is red. Persistent amber usually means the reporting is protecting someone rather than informing decisions.</p>
          <h3>Requirements keep growing, dates don't move</h3>
          <p>Scope creep without re-planning is borrowing from the future. Somewhere, quality or testing is being squeezed to make the numbers work.</p>
          <h3>The business has stopped turning up</h3>
          <p>When senior users stop attending design sessions and send delegates instead, the programme has lost its sponsor in all but name.</p>
          <h3>Nobody can explain the benefits</h3>
          <p>If the team cannot describe, in plain language, what will be better and for whom, the programme has drifted from its purpose.</p>
          <p>An independent <a href="services.html#packages">Transformation Health Check</a> gives executives an honest view and a practical recovery plan, while there is still time to use it.</p>"""),
    ("cyber-is-business", "Cyber Security", "4 min read",
     "Cyber security is a business change programme",
     "Security programmes that are run purely as technology projects struggle to land. The ones that succeed treat people and process as seriously as tools.",
     """<p>New controls, new tooling and new policies all change how people work. Yet security programmes are often scoped and resourced as if they were infrastructure upgrades.</p>
          <h3>Translate risk into business language</h3>
          <p>Boards fund what they understand. Framing security work in terms of service continuity, customer trust and regulatory exposure gets better decisions than framing it in terms of technical controls.</p>
          <h3>Map the processes you are changing</h3>
          <p>Access management, joiner-mover-leaver, incident response and supplier assurance are all business processes. Good business analysis makes sure the new way of working is clear, owned and workable.</p>
          <h3>Plan for adoption</h3>
          <p>Awareness campaigns, clear guidance and sensible exceptions processes stop people finding workarounds. A control nobody follows is not a control.</p>
          <p>Bespoke Vista provides <a href="services.html#cyber-security">business analysis and delivery support</a> for security programmes, bridging security specialists, the wider business and suppliers.</p>"""),
]
article_cards = "\n".join(f"""          <a class="card article-card reveal" href="#{aid}" style="color:inherit;text-decoration:none">
            <div class="meta">{cat} &middot; {mins}</div>
            <h3>{title}</h3>
            <p>{summary}</p>
            <span class="card-link">Read article &rarr;</span>
          </a>""" for aid, cat, mins, title, summary, _ in ARTICLES)
article_bodies = "\n".join(f"""        <article class="article" id="{aid}">
          <div class="meta">{cat} &middot; {mins}</div>
          <h2>{title}</h2>
          {body}
        </article>""" for aid, cat, mins, title, summary, body in ARTICLES)

insights = f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Insights</span>
        <h1>Practical thinking on transformation, security and AI</h1>
        <p>Short, practical articles drawn from real delivery experience. No jargon, no hype.</p>
      </div>
    </section>

    <section class="section-alt">
      <div class="container">
        <div class="grid grid-3">
{article_cards}
        </div>
      </div>
    </section>

    <section>
      <div class="container">
{article_bodies}
      </div>
    </section>

{CTA}"""

page("insights.html", "Insights",
     "Practical articles from Bespoke Vista on AI adoption, programme delivery and cyber security.",
     insights)

# ---------------------------------------------------------------- Contact
TOPICS = [
    ("consultation", "Book a consultation"),
    ("project", "Discuss a project"),
    ("ai-readiness", "AI Readiness Assessment"),
    ("copilot", "Microsoft Copilot Adoption Programme"),
    ("health-check", "Transformation Health Check"),
    ("automation", "Process Automation Review"),
    ("tom", "Target Operating Model Design"),
    ("cyber-ba", "Cyber Security Business Analysis"),
    ("fractional", "Fractional Transformation Director"),
    ("other", "Something else"),
]
topic_opts = "\n".join(f'                  <option value="{v}">{l}</option>' for v, l in TOPICS)

contact = f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Contact</span>
        <h1>Let's discuss your next transformation initiative</h1>
        <p>Whether you're launching a digital transformation programme, strengthening cyber resilience, exploring AI opportunities or redesigning your operating model, Bespoke Vista can help.</p>
      </div>
    </section>

    <section>
      <div class="container contact-grid">
        <div class="reveal">
          <h2>Start with a conversation</h2>
          <p>Tell us a little about your organisation and what you're trying to achieve. We'll come back to you to arrange an initial, no-obligation discussion.</p>
          <ul class="contact-list">
            <li>{icon("mail")}<div><strong>Email</strong><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></div></li>
            <li>{icon("pin")}<div><strong>Location</strong>United Kingdom, working with clients across the UK, Pakistan and India</div></li>
            <li>{icon("clock")}<div><strong>Response time</strong>Usually within one working day</div></li>
          </ul>
        </div>
        <form class="form reveal" id="contact-form" data-email="{CONTACT_EMAIL}" data-endpoint="" novalidate>
          <div class="form-row">
            <div class="field">
              <label for="name">Name *</label>
              <input id="name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="organisation">Organisation</label>
              <input id="organisation" name="organisation" type="text" autocomplete="organization">
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="email">Email *</label>
              <input id="email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field">
            <label for="topic">How can we help?</label>
            <select id="topic" name="topic">
{topic_opts}
            </select>
          </div>
          <div class="field">
            <label for="message">Your message *</label>
            <textarea id="message" name="message" required placeholder="A few lines about your organisation, the challenge and any timescales."></textarea>
          </div>
          <button class="btn btn-primary" type="submit">Send message</button>
          <p class="form-note">We only use your details to respond to your enquiry.</p>
          <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </section>"""

page("contact.html", "Contact",
     "Contact Bespoke Vista to discuss digital transformation, cyber security, AI adoption or operating model design.",
     contact)
