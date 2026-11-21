#!/usr/bin/env python3
"""Builds the static pages for the Bespoke Vista website.

All page content lives in this file so the header, footer, prices and
service names stay consistent everywhere. Edit here, then run:

    python3 build.py

The generated .html files are committed, so the site can be hosted as-is on
GitHub Pages (or any static host) with no build step on the server.

The previous implementation is preserved in git history at commit d2388d9.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

# ============================================================== Site configuration
# Items marked TODO must be completed by the owner before publication.
SITE = "Bespoke Vista"
TAGLINE = "Bridging Strategy and Execution"
BASE_URL = "https://rauf-mushtaq.github.io/Bespoke.vista/"  # TODO: change if a custom domain is used
CONTACT_EMAIL = "hello@bespokevista.co.uk"  # TODO: confirm this mailbox exists and is monitored

# TODO: paste your Microsoft Bookings page URL. While empty, "Book a Managed Operations
# Assessment" buttons go to the contact form with the assessment topic pre-selected.
BOOKING_URL = ""
# TODO: form endpoint (e.g. a Power Automate "When an HTTP request is received" URL or Formspree).
# While empty, forms open the visitor's email app and say so on screen.
FORM_ENDPOINT = ""
# TODO: analytics IDs. Only add these once a cookie-consent mechanism and privacy notice are live.
GA4_ID = ""       # e.g. "G-XXXXXXXXXX"
CLARITY_ID = ""   # e.g. "abcd1234ef"

# Company details shown in the footer and on the homepage. TODO: complete.
COMPANY_NUMBER = ""      # e.g. "12345678"
REGISTERED_OFFICE = ""   # e.g. "1 Example Street, London, EC1A 1AA"
LAHORE_ADDRESS = ""      # e.g. "Office 4, Example Plaza, Gulberg III, Lahore"
LINKEDIN_URL = ""        # founder or company LinkedIn URL

# Shows dashed "Owner to provide" boxes where information is missing.
# Set to False before publication: missing items are then hidden instead.
SHOW_OWNER_PLACEHOLDERS = True

ASSESS_HREF = BOOKING_URL or "contact.html?topic=assessment"
ARR = '<span class="arr" aria-hidden="true">→</span>'

NAV = [
    ("services.html", "Services"),
    ("managed-teams.html", "Delivery Model"),
    ("pricing.html", "Pricing"),
    ("samples.html", "Samples"),
    ("about.html", "About"),
]
LOGO = ('<img src="assets/img/logo.png" srcset="assets/img/logo.png 1x, assets/img/logo@2x.png 2x" '
        'alt="" width="55" height="38">')
LOGO_LAZY = LOGO.replace('<img ', '<img loading="lazy" ')


def esc_attr(s):
    return s.replace('"', "&quot;")


def owner(text, inline=False):
    """Visible 'Owner to provide' note while SHOW_OWNER_PLACEHOLDERS is True; an HTML comment otherwise."""
    if not SHOW_OWNER_PLACEHOLDERS:
        return f"<!-- OWNER TO PROVIDE: {text} -->"
    tag = "span" if inline else "div"
    return f'<{tag} class="owner-ph" role="note"><strong>Owner to provide:</strong> {text}</{tag}>'


def track_for(href):
    if href == ASSESS_HREF:
        return "booking_start" if BOOKING_URL else "assessment_enquiry_start"
    if "topic=pilot" in href:
        return "pilot_cta"
    if href.startswith("samples.html"):
        return "sample_view"
    if href.startswith("scorecard.html") or href == "#scorecard":
        return "scorecard_cta"
    return ""


def btn(text, href, cls="btn-primary", arrow=True):
    t = track_for(href)
    ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    data = f' data-track="{t}"' if t else ""
    return f'<a class="btn {cls}" href="{href}"{data}{ext}>{text}{" " + ARR if arrow else ""}</a>'


def label(text):
    return f'<span class="label">{text}</span>'


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
        <span><span class="brand-name">{SITE}</span><span class="brand-tag">UK-managed · Lahore-delivered</span></span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Menu
      </button>
      <ul class="nav-links" id="nav-links">
{items}
        <li class="nav-btns">
          <a class="btn btn-line btn-sm" href="scorecard.html"{cur("scorecard.html")} data-track="scorecard_cta">Free Scorecard</a>
          <a class="btn btn-primary btn-sm" href="{ASSESS_HREF}" data-track="{track_for(ASSESS_HREF)}">Book an Assessment</a>
        </li>
      </ul>
    </nav>
  </header>"""


def company_line():
    bits = ["Bespoke Vista Ltd. Registered in England &amp; Wales"]
    if COMPANY_NUMBER:
        bits.append(f"Company no. {COMPANY_NUMBER}")
    if REGISTERED_OFFICE:
        bits.append(f"Registered office: {REGISTERED_OFFICE}")
    return ". ".join(bits) + "."


FOOTER = f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-word" aria-hidden="true">Bespoke <span>Vista</span></div>
      <div class="footer-grid">
        <div>
          <div class="footer-brand">{LOGO_LAZY}<span>{SITE}</span></div>
          <p>UK-led business analysis, PMO, process documentation and AI-enabled operational services, delivered by managed teams in Lahore.</p>
          <p class="clocks" style="margin-top:8px"><span><span class="dot"></span><span data-status="lahore">Lahore office</span></span><span><b>LDN</b><span data-clock="london">--:--</span></span><span><b>LHE</b><span data-clock="lahore">--:--</span></span></p>
        </div>
        <div>
          <h4>Managed services</h4>
          <ul>
            <li><a href="pricing.html#pmo">PMO-in-a-Box</a></li>
            <li><a href="pricing.html#ba">Managed Business Analysis</a></li>
            <li><a href="pricing.html#documentation">Documentation Factory</a></li>
            <li><a href="index.html#ai">AI workflow services</a></li>
            <li><a href="services.html">All services</a></li>
          </ul>
        </div>
        <div>
          <h4>Start here</h4>
          <ul>
            <li><a href="scorecard.html">Free Readiness Scorecard</a></li>
            <li><a href="index.html#assessment">Managed Operations Assessment</a></li>
            <li><a href="index.html#pilot">30-Day Pilot</a></li>
            <li><a href="samples.html">Sample deliverables</a></li>
            <li><a href="pricing.html">Pricing and terms</a></li>
          </ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="about.html">About</a></li>
            <li><a href="case-studies.html">Experience</a></li>
            <li><a href="insights.html">Insights</a></li>
            <li><a href="ai-scorecard.html">AI Readiness Scorecard</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
            <li>United Kingdom</li>
            <li>Delivery centre: Lahore, Pakistan</li>
            {f'<li><a href="{LINKEDIN_URL}" rel="noopener">LinkedIn</a></li>' if LINKEDIN_URL else ''}
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span id="year">2026</span> {company_line()}</span>
        <span>All prices exclude VAT.</span>
      </div>
    </div>
  </footer>"""


def analytics():
    out = ""
    if GA4_ID:
        out += f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>
"""
    if CLARITY_ID:
        out += f"""  <script>(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{CLARITY_ID}");</script>
"""
    return out


def page(filename, title, description, body, schema=None, full_title=None):
    full = full_title or (f"{SITE} | {TAGLINE}" if filename == "index.html" else f"{title} | {SITE}")
    url = BASE_URL + ("" if filename == "index.html" else filename)
    graphs = list(schema or [])
    if filename != "index.html":
        graphs.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": title, "item": url}]})
    ld = ""
    if graphs:
        ld = ('  <script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@graph": graphs}, ensure_ascii=False).replace("</", "<\\/")
              + "</script>\n")
    body = body.replace('data-endpoint=""', f'data-endpoint="{FORM_ENDPOINT}"')
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full}</title>
  <meta name="description" content="{esc_attr(description)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc_attr(full)}">
  <meta property="og:description" content="{esc_attr(description)}">
  <meta property="og:image" content="{BASE_URL}assets/img/logo@2x.png">
  <meta name="twitter:card" content="summary">
  <meta name="theme-color" content="#F7F3EE">
  <link rel="icon" href="assets/img/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/styles.css">
{ld}{analytics()}</head>
<body>
{header(filename)}
  <main id="main">
{body}
  </main>
{FOOTER}
  <script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


def cta(title="Start with a £495 Managed Operations Assessment.",
        text="A 60-minute discovery workshop, a written view of what could be handed over safely, and a recommended pilot. The fee is credited against a qualifying pilot commissioned within 30 days.",
        primary=("Book a Managed Operations Assessment", ASSESS_HREF),
        secondary=("Take the Free Readiness Scorecard", "scorecard.html")):
    return f"""    <section class="sec-tight">
      <div class="container">
        <div class="cta reveal">
          {label("Next step")}
          <h2>{title}</h2>
          <p>{text}</p>
          <div class="btns">
            {btn(primary[0], primary[1], "btn-ember")}
            {btn(secondary[0], secondary[1], "btn-line-light", arrow=False)}
          </div>
        </div>
      </div>
    </section>"""


CLOCKS = ('<p class="clocks"><span><span class="dot"></span><span data-status="lahore">Lahore office</span></span>'
          '<span><b>London</b><span data-clock="london">--:--</span></span>'
          '<span><b>Lahore</b><span data-clock="lahore">--:--</span></span></p>')


def horizon(labels, aria=None):
    a, b, c, d = labels
    role = f'role="img" aria-label="{aria}"' if aria else 'aria-hidden="true"'
    return f"""<svg class="horizon" viewBox="-70 20 540 352" {role}>
            <defs>
              <linearGradient id="sunG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7941D"/><stop offset="1" stop-color="#EE2A24"/></linearGradient>
              <clipPath id="above"><rect x="-70" y="-50" width="560" height="280"/></clipPath>
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
              <circle cx="31" cy="168" r="4" fill="#0B1120"/><text x="20" y="172" text-anchor="end">{a}</text>
              <circle cx="110" cy="74" r="4" fill="#0B1120"/><text x="100" y="64" text-anchor="end">{b}</text>
              <circle cx="290" cy="74" r="4" fill="#0B1120"/><text x="300" y="64">{c}</text>
              <circle cx="369" cy="168" r="4" fill="#0B1120"/><text x="380" y="172">{d}</text>
            </g>
          </svg>"""


TIMELINE = """<div class="sun-timeline reveal" aria-label="Working hours shown in UK time">
          <div class="tl-row"><div class="who">Lahore office<small>09:00–18:00 PKT</small></div><div class="tl-bar"><span class="lahore" style="left:16.7%;width:37.5%">Lahore 04:00–13:00</span><i class="tl-now"></i></div></div>
          <div class="tl-row"><div class="who">UK lead<small>09:00–17:30 UK</small></div><div class="tl-bar"><span class="uk" style="left:37.5%;width:35.4%">UK 09:00–17:30</span><i class="tl-now"></i></div></div>
          <div class="tl-row"><div class="who">Together<small>live overlap</small></div><div class="tl-bar"><span class="overlap" style="left:37.5%;width:16.7%">Live overlap 09:00–13:00</span><i class="tl-now"></i></div></div>
          <div class="tl-axis"><div></div><div><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div></div>
          <p class="small" style="color:var(--slate);margin:18px 0 0">Shown in UK time. Lahore is <span data-offset>5</span> hours ahead, so the live overlap is about four hours in winter and five in summer. The white line is now.</p>
        </div>"""

MOBILISATION = """<p>A standard delivery pod can normally be mobilised within <strong>two to four weeks</strong> following contract signature, role confirmation, security approval and access provisioning.</p>
            <p class="small">Mobilisation may take longer for specialist roles, dedicated recruitment, client security checks, complex systems, regulated data, or software and equipment provisioning. We confirm a mobilisation plan in writing before you commit.</p>"""

# ============================================================== Catalogue data
# Subscriptions (secondary offers, shown on the pricing page only)
SUBSCRIPTIONS = [
    ("intelligence", "Executive AI Intelligence", "For directors, owners and senior managers",
     "A monthly briefing on what has changed in AI, what matters for UK organisations and what to do next.",
     [("Briefing", "Stay informed in 15 minutes a month.", 49,
       ["Monthly executive briefing (PDF and audio)", "Curated tools and vendor watchlist", "Prompt and template library", "Member-only articles"]),
      ("Professional", "For leaders actively planning AI.", 99,
       ["Everything in Briefing", "Monthly live Q&amp;A session", "Sector playbooks: logistics, professional services, property", "Policy and template updates"]),
      ("Boardroom", "For the whole leadership team.", 199,
       ["Everything in Professional", "Up to 5 team seats", "Quarterly 30-minute 1:1 with Azeem", "Board-ready AI update slides each quarter"])], 1),
    ("advisory", "Bespoke Vista AI Advisory", "For SMEs and mid-market firms adopting AI",
     "A standing senior AI adviser who keeps your AI plans on track, safe and paying back.",
     [("Starter", "Light-touch guidance as you begin.", 495,
       ["2 hours of advisory a month", "Monthly AI opportunities and risks review", "Email support, 2-working-day response", "Policy and governance templates"]),
      ("Growth", "Structured adoption across teams.", 995,
       ["5 hours of advisory a month", "Quarterly AI roadmap refresh", "AI usage policy and governance set-up", "One team workshop each quarter", "Next-working-day response"]),
      ("Partner", "An AI lead without the hire.", 1995,
       ["10 hours of advisory a month", "Monthly AI steering meeting", "Use-case pipeline managed for you", "Vendor and licence reviews", "Same-day response"])], 1),
    ("fractional", "Fractional Business Architect", "For growing firms with change on the agenda",
     "Senior business architecture and transformation leadership a few days a month.",
     [("Navigator", "Keep change joined up.", 995,
       ["1 day a month", "Capability and process map kept current", "Monthly change roadmap review", "Ad-hoc advice by email"]),
      ("Architect", "Own the target operating model.", 1995,
       ["2.5 days a month", "Target operating model ownership", "Change portfolio prioritisation", "Supplier and solution design reviews", "Seat at your leadership meeting"]),
      ("Director", "Fractional transformation director.", 3995,
       ["5 days a month", "Leads your transformation portfolio", "Programme governance and assurance", "Board reporting", "Backed by the Lahore delivery centre"])], 1),
]

# The three primary managed services. Tier tuple: (name, short description, price, [inclusions], one-line summary)
PMO = ("pmo", "PMO-in-a-Box", "For organisations running 3 to 15 projects without a consistent PMO",
       "Governance, reporting and control across your project portfolio, run as a managed service. It supports your project managers; it does not take over their accountability for delivery.",
       [("Foundation", "Consistent control for a small portfolio.", "£1,950",
         ["Up to 5 active projects", "Up to 6 PMO delivery days a month", "Governance templates", "RAID and action management",
          "Reporting calendar", "Monthly portfolio dashboard", "Monthly service review"], "Up to 5 projects · 6 delivery days a month"),
        ("Managed", "A weekly PMO rhythm for a growing portfolio.", "£3,950",
         ["Up to 10 active projects", "Up to 12 PMO delivery days a month", "Weekly reporting cycle", "Portfolio dashboard",
          "Governance-meeting preparation", "Dependency and milestone tracking", "Benefits register", "Risk and issue escalation",
          "Monthly UK-led service review"], "Up to 10 projects · weekly reporting cycle"),
        ("Transformation Office", "Programme-level support across workstreams.", "From £7,500",
         ["Multiple workstreams", "Dedicated PMO analyst", "Programme-level reporting", "Financial and resource tracking",
          "Executive governance packs", "Dependency management", "Programme assurance", "Senior UK transformation oversight"],
         "Multiple workstreams · dedicated PMO analyst")], 1)

BA = ("ba", "Managed Business Analysis", "For transformation and change teams without enough business-analysis capacity",
      "Business analysis delivered to an agreed standard and capacity each month, with senior UK quality review. You buy outputs, not timesheets.",
      [("Essential", "Steady analysis capacity.", "£2,250",
        ["Up to 6 delivery days a month", "Process mapping", "Requirements capture", "Backlog maintenance",
         "One stakeholder workshop a month", "Monthly findings and recommendations report"], "Up to 6 delivery days a month"),
       ("Growth", "A named analyst in your change team.", "£4,250",
        ["Up to 12 delivery days a month", "Named analyst", "Current-state and future-state process design",
         "User stories and acceptance criteria", "Requirements traceability", "Fortnightly governance meeting",
         "Senior UK quality review"], "Up to 12 delivery days · named analyst"),
       ("Transformation", "Lead and supporting analysts.", "From £7,500",
        ["Lead business analyst and analyst support", "Multiple workstreams", "Business cases", "Options analysis",
         "Vendor evaluation", "Change-impact analysis", "Executive reporting", "Senior UK oversight"],
        "Lead analyst plus support · multiple workstreams")], 1)

DOCS = ("documentation", "Documentation Factory", "For organisations with undocumented or inconsistent processes",
        "Fixed-price process documentation: process maps, SOPs and a controlled library your teams, auditors and AI tools can rely on.",
        [("Process Starter", "Your most critical processes, documented.", "£2,950",
          ["Five documented processes", "Five SOPs or work instructions", "Standard document templates", "One review cycle",
           "Controlled final document library", "Typically 3 to 4 weeks"], "5 processes · 5 SOPs"),
         ("Operations Manual", "A working operations manual.", "£5,950",
          ["Twelve documented processes", "Twelve SOPs", "Roles and responsibilities", "Control points", "Operational KPIs",
           "Two review cycles", "SharePoint-ready structure", "Typically 6 to 8 weeks"], "12 processes · 12 SOPs"),
         ("Enterprise Knowledge Sprint", "A structured knowledge base.", "From £9,500",
          ["Approximately 25 to 30 processes", "Stakeholder interviews and workshops", "Process maps",
           "SOPs and work instructions", "Controls and ownership", "Knowledge-base structure", "Implementation support",
           "Typically 10 to 12 weeks"], "Around 25 to 30 processes")], 1)

PRIMARY = [PMO, BA, DOCS]

SOP_DEFINITION = ["One defined process", "Up to five pages", "Up to two stakeholder interviews", "One agreed process map",
                  "Review cycles as stated in the package (a maximum of two per SOP)", "One final approved document"]

ASSESSMENT = ("Managed Operations Assessment", "£495", "fixed price · ex VAT",
              ["60-minute discovery workshop", "Operational suitability assessment", "Managed-service and offshore-delivery readiness review",
               "Process prioritisation", "Initial capacity model", "Indicative cost model", "Recommended pilot", "Written findings"],
              "The £495 assessment fee will be credited against a qualifying pilot commissioned within 30 days.")
PILOT = ("30-Day Managed Delivery Pilot", "£1,500–£2,500", "fixed fee · ex VAT",
         ["One clearly defined process or workstream", "Named delivery lead", "Agreed inputs and outputs", "Baseline measurements",
          "Weekly progress review", "End-of-pilot results report", "Business case for ongoing delivery"],
         "The final price depends on scope, system access, complexity and data sensitivity, and is confirmed in writing after the assessment.")
AI_DISCOVERY = ("AI Operations Discovery", "£2,500", "fixed price · ex VAT",
                ["AI readiness assessment", "Process and data review", "Five prioritised use cases", "Risk and governance review",
                 "90-day implementation roadmap", "Indicative business case"], "Typically three to four weeks.")
AI_WORKFLOW = ("AI Workflow Implementation", "£5,000–£15,000", "fixed price per scope · ex VAT",
               ["One to three defined workflows", "Microsoft Copilot, SharePoint, Power Automate, Claude or ChatGPT integration where appropriate",
                "Testing", "User guidance", "Governance documentation", "Handover"],
               "We only propose an integration once we have confirmed a viable technical route in your environment. Software licences and AI consumption are charged separately.")

# Shared commercial terms
TERMS = [
    ("Prices", "All prices exclude VAT."),
    ("Initial term", "Monthly managed services have a three-month initial term."),
    ("Payment", "Monthly in advance for managed services. Fixed-price work is invoiced as set out in the proposal."),
    ("Notice", "30 days' notice after the initial term."),
    ("Change control", "Changes to scope, capacity or service levels go through a formal change request and are only made once you approve the impact in writing."),
    ("Out-of-scope work", "Quoted separately. No package provides unlimited work."),
    ("Licences", "Third-party software, AI tools and AI consumption charges are not included and are charged separately or licensed by you."),
]

# Package boundaries for the pricing page: rows that differ by tier, then rows common to all tiers.
BOUNDARIES = {
    "pmo": {
        "rows": [
            ("Included capacity", ["Up to 6 PMO delivery days a month", "Up to 12 PMO delivery days a month", "Dedicated PMO analyst plus UK oversight, as agreed in the proposal"]),
            ("Projects", ["Up to 5 active projects", "Up to 10 active projects", "Multiple workstreams, as agreed"]),
            ("Meetings", ["Monthly service review", "Governance-meeting preparation; monthly UK-led service review", "Executive governance cycle, as agreed"]),
            ("Reporting", ["Monthly portfolio dashboard", "Weekly reporting cycle and dashboard", "Weekly programme reporting; monthly executive pack"]),
            ("Review cycles", ["One per report", "One per report", "As agreed in the proposal"]),
            ("Response target (UK business hours)", ["Next working day", "Within 4 working hours", "Within 2 working hours"]),
        ],
        "common": [
            ("Supported platforms", "Your Microsoft 365 environment (SharePoint, Teams, Excel, Planner; Power BI where you hold licences). Smartsheet, Jira or similar by agreement."),
            ("Your responsibilities", "A named sponsor and day-to-day contact; project managers who provide updates on time; access to the systems and information needed; your own software licences."),
            ("Exclusions", "Accountability for delivering your projects; decisions on your behalf; legal, financial or regulatory advice; software development; on-site attendance unless agreed."),
            ("Additional work", "Extra projects or delivery days are quoted separately through change control."),
        ],
    },
    "ba": {
        "rows": [
            ("Included capacity", ["Up to 6 delivery days a month", "Up to 12 delivery days a month", "Lead analyst plus analyst support, as agreed in the proposal"]),
            ("Workstreams", ["One workstream", "Up to two workstreams", "Multiple workstreams, as agreed"]),
            ("Meetings", ["One stakeholder workshop a month", "Fortnightly governance meeting", "Executive and workstream governance, as agreed"]),
            ("Reporting", ["Monthly findings and recommendations report", "Fortnightly progress; monthly report", "Executive reporting, as agreed"]),
            ("Review cycles", ["Up to two per deliverable", "Up to two per deliverable", "Up to two per deliverable"]),
            ("Response target (UK business hours)", ["Next working day", "Within 4 working hours", "Within 2 working hours"]),
        ],
        "common": [
            ("Supported platforms", "Microsoft 365, Visio or similar for process maps; Jira, Azure DevOps or your existing backlog tool by agreement."),
            ("Your responsibilities", "A named product owner or sponsor; stakeholder availability for interviews and workshops; timely review and approval of outputs; access and licences."),
            ("Exclusions", "Product ownership and decisions on your behalf; solution build or testing execution; legal or regulatory advice; on-site attendance unless agreed."),
            ("Additional work", "Additional delivery days or workstreams are quoted separately through change control."),
        ],
    },
    "documentation": {
        "rows": [
            ("Processes and SOPs", ["5 processes, 5 SOPs", "12 processes, 12 SOPs", "Approximately 25 to 30 processes"]),
            ("Interviews and workshops", ["Up to two interviews per SOP", "Up to two interviews per SOP", "Interviews and workshops, as agreed"]),
            ("Review cycles", ["One", "Two", "Two"]),
            ("Reporting", ["Weekly progress note", "Weekly progress note", "Weekly progress note; steering as agreed"]),
            ("Typical duration", ["3 to 4 weeks", "6 to 8 weeks", "10 to 12 weeks"]),
            ("Response target (UK business hours)", ["Next working day", "Next working day", "Next working day"]),
        ],
        "common": [
            ("Supported platforms", "Word and SharePoint by default; Visio or similar for process maps; your document templates if you have them."),
            ("Your responsibilities", "A named owner for each process; subject-matter experts available for interviews; source material; review and approval within agreed timescales."),
            ("Exclusions", "Process redesign beyond documenting the agreed way of working; legal or regulatory sign-off; translation; system configuration."),
            ("Additional work", "Additional processes or review cycles are quoted separately through change control."),
        ],
    },
}

TRAINING = [
    ("AI for Leaders", "Half-day workshop for leadership teams: what is real, what is hype and where to start.", "£1,450", "Up to 12 people"),
    ("Copilot Skills Bootcamp", "Two days of hands-on, role-based Microsoft Copilot training using your own work.", "£2,950", "Up to 15 people"),
    ("Prompting for Teams", "Practical half day on getting reliable results from ChatGPT, Claude and Copilot.", "£995", "Up to 15 people"),
    ("Calm Under Pressure", "Leadership resilience workshop drawing on Tai Chi, martial arts and breathing practice.", "£1,250", "Half day, up to 20"),
]

PROJECTS = [
    (ASSESSMENT[0], "Discovery workshop, readiness review, process prioritisation, capacity and cost model, recommended pilot and written findings. Credited against a qualifying pilot commissioned within 30 days.", "£495", "1 to 2 weeks"),
    (PILOT[0], "One defined process or workstream, named delivery lead, baseline, weekly reviews, results report and business case.", "£1,500–£2,500", "30 days"),
    (AI_DISCOVERY[0], "AI readiness, process and data review, five prioritised use cases, risk review, 90-day roadmap and indicative business case.", "£2,500", "3 to 4 weeks"),
    (AI_WORKFLOW[0], "One to three defined workflows with testing, user guidance, governance documentation and handover.", "£5,000–£15,000", "4 to 8 weeks"),
    ("Microsoft Copilot Adoption Programme", "Readiness, permissions clean-up, governance, champions, training and rollout.", "£5,000–£25,000", "6 to 12 weeks"),
    ("AI Governance Pack", "Usage policy, risk register, data rules, DPIA template and an approval process for new use cases.", "£2,500–£6,000", "3 to 4 weeks"),
    ("AI Optimisation Review", "Already paying for Copilot or ChatGPT but not seeing the value? We find out why and fix it.", "£1,950", "2 weeks"),
    ("Transformation Health Check", "Independent executive review of a struggling programme, with a practical recovery plan.", "£4,950", "2 weeks"),
    ("Target Operating Model Design", "People, process, technology and governance designed together, with a roadmap.", "From £12,000", "6 to 10 weeks"),
    ("Cyber Security Business Analysis", "Requirements, process design and change support for security programmes.", "Fixed scope or day rate", "By agreement"),
]

DOJOOS = ("dojoos", "DojoOS", "For martial arts schools and wellness studios",
          "Members, payments, attendance and gradings in one simple platform. In development: founding schools wanted.",
          [("Starter", "For a single, growing school.", "£99", ["Up to 100 students", "Membership and payment tracking", "Attendance check-in", "Grading records"]),
           ("Club", "Automate the admin.", "£179", ["Up to 300 students", "Automatic renewals and reminders", "Parent and student portal", "Lead and trial-class tracking"]),
           ("Academy", "Multi-site and instructors.", "£299", ["Unlimited students, multiple sites", "AI marketing and content assistant", "Instructor scheduling", "Reporting dashboard"])], 1)

# Secondary managed services: offered after an assessment, not priced publicly.
SECONDARY = [
    ("AI Operations Team", "Managed AI-assisted workflows with human review and monthly improvement.", "Scoped after an AI Operations Discovery"),
    ("Managed Back Office", "Admin, data upkeep and operational reporting to an agreed service level.", "Scoped after a Managed Operations Assessment"),
    ("Knowledge Management Service", "A SharePoint knowledge base kept current and ready for Copilot.", "Usually follows a Documentation Factory project"),
    ("Transformation Support Office", "Change plans, communications, training logistics and benefits tracking.", "Scoped after a Managed Operations Assessment"),
]

INDUSTRIES = ["Logistics", "Warehousing", "Supply chain", "Professional services", "Technology", "Property",
              "Financial services", "Healthcare", "Education", "Public sector"]


def tier_cards(product, featured_flag="Recommended", per="per month, ex VAT", annual=False):
    pid, name, who, desc, tiers, featured = product[:6]
    out = []
    for i, t in enumerate(tiers):
        tname, tdesc, price, feats = t[0], t[1], t[2], t[3]
        f = i == featured
        if annual:
            amount = f'<div class="amount" data-monthly="{price}">£{price:,}</div><div class="per">per month, ex VAT</div>'
        else:
            amount = f'<div class="amount">{price}</div><div class="per">{per}</div>'
        lis = "".join(f"<li>{x}</li>" for x in feats)
        out.append(f"""          <div class="plan{' featured' if f else ''} reveal">
            {f'<span class="flag">{featured_flag}</span>' if f else ''}
            <h3>{tname}</h3>
            <p class="tier-desc">{tdesc}</p>
            {amount}
            <ul>{lis}</ul>
            <a class="btn {'btn-ember' if f else 'btn-line'}" href="contact.html?topic={pid}">Discuss {tname} {ARR}</a>
          </div>""")
    return "\n".join(out)


def product_block(product, per="per month, ex VAT", annual=False, extra=""):
    pid, name, who, desc = product[:4]
    return f"""        <div class="product" id="{pid}">
          <div class="product-head">
            <div><h2>{name}</h2><p>{desc}</p>{extra}</div>
            <div class="for">{who}</div>
          </div>
          <div class="grid g3">
{tier_cards(product, per=per, annual=annual)}
          </div>
        </div>"""


def boundaries_table(product):
    pid = product[0]
    tiers = [t[0] for t in product[4]]
    b = BOUNDARIES[pid]
    head = "".join(f'<th scope="col">{t}</th>' for t in tiers)
    rows = "".join(f'<tr><th scope="row">{r}</th>' + "".join(f"<td>{v}</td>" for v in vals) + "</tr>" for r, vals in b["rows"])
    common = "".join(f'<tr><th scope="row">{r}</th><td colspan="3">{v}</td></tr>' for r, v in b["common"])
    term = ("Fixed price, invoiced as set out in the proposal." if pid == "documentation"
            else "Three-month initial term, monthly in advance, then 30 days' notice.")
    return f"""          <details class="bounds" id="{pid}-terms">
            <summary>Package boundaries and terms</summary>
            <div class="table-wrap table-light">
              <table class="sla bounds-table">
                <thead><tr><th scope="col"><span class="sr-only">Item</span></th>{head}</tr></thead>
                <tbody>{rows}{common}<tr><th scope="row">Term</th><td colspan="3">{term}</td></tr><tr><th scope="row">Licences</th><td colspan="3">Not included. Third-party software and AI consumption are charged separately.</td></tr></tbody>
              </table>
            </div>
          </details>"""


def pricelist(rows):
    return "\n".join(f"""          <div class="pl-row reveal">
            <h3>{n}</h3><p>{d}</p><span class="p">{p}</span><span class="t">{t}</span>
          </div>""" for n, d, p, t in rows)


def offer_card(o, cta_text, cta_href, flag=None, cls=""):
    name, price, per, items, note = o
    lis = "".join(f"<li>{x}</li>" for x in items)
    return f"""          <div class="plan {cls} reveal">
            {f'<span class="flag">{flag}</span>' if flag else ''}
            <h3>{name}</h3>
            <div class="amount">{price}</div><div class="per">{per}</div>
            <ul>{lis}</ul>
            <p class="small" style="margin:0 0 20px">{note}</p>
            {btn(cta_text, cta_href, 'btn-ember' if 'featured' in cls else 'btn-primary')}
          </div>"""


# ============================================================== HOME
FAQ = [
    ("Where is the work delivered?", "Delivery takes place in our office in Lahore, Pakistan. Commercial ownership, service management and senior oversight remain in the UK with Bespoke Vista Ltd. Workshops and governance meetings can be led by our UK lead."),
    ("Who is accountable for delivery?", "Bespoke Vista Ltd is contractually accountable for every service. Azeem Mushtaq, our founder, is the senior UK lead and your escalation point."),
    ("Will we communicate directly with the Lahore team?", "Yes. Day-to-day work runs through a named delivery lead using channels you agree, typically Microsoft Teams and email. Scope, priorities, quality and escalation stay with your UK lead."),
    ("What UK working-hours overlap is available?", "Our Lahore office normally works 09:00 to 18:00 Pakistan time. That gives a live overlap with UK mornings of about four hours in winter and five hours in summer. Later cover can be agreed for higher service levels."),
    ("How quickly can a delivery team be established?", "A standard delivery pod can normally be mobilised within two to four weeks following contract signature, role confirmation, security approval and access provisioning. Specialist roles, dedicated recruitment, client security checks, complex systems or regulated data can extend this. We confirm a mobilisation plan before you commit."),
    ("Do you supply individual contractors?", "No. We don't supply CVs, contractors or staff for you to manage. We deliver a defined service with agreed outputs, and we manage the people who deliver it."),
    ("How is confidential information protected?", "Through a Data Processing Agreement, confidentiality agreements, role-based access, multi-factor authentication and managed devices, with international data-transfer safeguards where personal data is involved. The security section on this page shows the status of each control."),
    ("Can the team work in our Microsoft 365 environment?", "Yes, and it is our preferred approach. Working in your tenant keeps information under your access controls, audit logs and retention policies."),
    ("Can our data remain within our systems?", "In most cases, yes. We aim to work inside your systems so data is not copied to ours. Where that is not possible, we agree in writing what is transferred, how it is protected and when it is deleted."),
    ("What happens if a team member is absent?", "Every recurring task has an SOP, so another trained team member can step in. Short absences are covered within the service. For single-analyst packages, how longer absences are covered is set out in your service definition."),
    ("Can capacity be increased or reduced?", "Yes, through change control. Reductions take effect from the next billing month after notice. Increases depend on recruitment and onboarding lead times, which we confirm before you approve."),
    ("Are software and AI licences included?", "No. Third-party software, AI tools and consumption charges are excluded. We tell you up front what each service needs, and you can license tools directly or have them recharged."),
    ("What is the minimum contract term?", "Assessments, pilots and documentation projects are one-off, fixed-price engagements. Monthly managed services have a three-month initial term, paid monthly in advance, then continue on 30 days' notice."),
    ("What is included in the 30-day pilot?", "One clearly defined process or workstream, a named delivery lead, agreed inputs and outputs, baseline measurements, weekly progress reviews, an end-of-pilot results report and a business case for ongoing delivery."),
    ("How is quality measured?", "Against measures agreed in your service definition, typically accuracy, turnaround time, rework and service-level performance. Work is checked by a second person before release, sampled weekly and reported in the monthly service report."),
    ("What happens to access and data at contract end?", "We remove all access, return or securely delete your data as set out in the Data Processing Agreement, and hand over all documentation and deliverables, which belong to you."),
    ("Which activities are out of scope?", "Anything not in your service definition, including decisions on your behalf, accountability for delivering your projects, legal or financial advice, software development, third-party licences and on-site attendance unless agreed."),
    ("How are changes to scope handled?", "Through change control. You raise a change request, we confirm the effect on capacity, timescale and price in writing, and nothing changes until you approve it."),
]
faq_html = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)

WHO = [
    ("Logistics and supply chain", "Warehousing, transport and 3PL businesses where operations, customer reporting and change projects compete for the same people."),
    ("3 to 15 projects, no consistent PMO", "Status lives in spreadsheets and inboxes, and slippage surfaces late."),
    ("Change teams short of analysts", "Transformation work held up because nobody has time to define requirements properly."),
    ("Undocumented processes", "Operations that depend on what experienced people remember."),
    ("Professional services", "Firms that need repeatable, auditable operating procedures as they grow."),
    ("Practical AI automation", "Organisations that want working AI-assisted workflows, not another AI strategy deck."),
]
who_html = "\n".join(f"""          <div class="fit reveal"><span class="fit-n">{i+1:02d}</span><div><h3>{t}</h3><p>{d}</p></div></div>""" for i, (t, d) in enumerate(WHO))

PROBLEMS = [
    ("“Nobody has a single, current view of our projects.”", "PMO-in-a-Box", "#pmo-card"),
    ("“We hear about slippage at the monthly meeting, not when it happens.”", "PMO-in-a-Box", "#pmo-card"),
    ("“Requirements depend on whoever has time.”", "Managed Business Analysis", "#ba-card"),
    ("“We keep reworking things we thought were agreed.”", "Managed Business Analysis", "#ba-card"),
    ("“Our processes live in people’s heads.”", "Documentation Factory", "#documentation-card"),
    ("“We want AI to help, but our processes aren’t ready for it.”", "Documentation Factory, then AI Operations Discovery", "#ai"),
]
problems_html = "\n".join(f"""          <div class="problem reveal"><p class="pq">{q}</p><a href="{h}" class="fix"><span>Addressed by</span>{s} →</a></div>""" for q, s, h in PROBLEMS)

SERVICE_CTA = {
    "pmo": ("Discuss Your Project Portfolio", "contact.html?topic=pmo"),
    "ba": ("Book a Managed Operations Assessment", ASSESS_HREF),
    "documentation": ("View a Sample Deliverable", "samples.html#sop"),
}


def service_card(product):
    pid, name, who, desc, tiers, featured = product
    unit = "" if pid == "documentation" else "/month"
    rows = "".join(f"""<li><span class="tn">{t[0]}</span><span class="tp">{t[2]}{unit}</span><span class="ts">{t[4]}</span></li>""" for t in tiers)
    key = tiers[1][3][:5]
    extra = ""
    if pid == "documentation":
        extra = ('<div class="sop-def"><strong>One standard SOP</strong> = one defined process, up to five pages, up to two stakeholder interviews, '
                 'one agreed process map, up to two review cycles and one final approved document.</div>')
    c_text, c_href = SERVICE_CTA[pid]
    return f"""          <article class="svc-card reveal" id="{pid}-card">
            <span class="label">{'Fixed price' if pid == 'documentation' else 'Monthly managed service'}</span>
            <h3>{name}</h3>
            <p class="who">{who}.</p>
            <p>{desc}</p>
            <ul class="tier-rows">{rows}</ul>
            <p class="small muted" style="margin:0 0 8px">{tiers[1][0]} includes:</p>
            <ul class="ticks compact">{''.join(f'<li>{x}</li>' for x in key)}</ul>
            {extra}
            <div class="svc-actions">
              {btn(c_text, c_href, 'btn-primary btn-sm')}
              <a class="text-link" href="pricing.html#{pid}-terms">Package boundaries and terms</a>
            </div>
          </article>"""


services_cards = "\n".join(service_card(p) for p in PRIMARY)

LADDER = [
    ("Free", "Readiness Scorecard", "13 questions. Your score, risks and recommended next step, instantly.", "£0", "scorecard.html"),
    ("Assess", "Managed Operations Assessment", "Workshop, readiness review, capacity and cost model, recommended pilot.", "£495", "#assessment"),
    ("Pilot", "30-day delivery pilot", "One defined workflow, baseline measures and a results report.", "£1,500–£2,500", "#pilot"),
    ("Run", "Managed service", "Defined monthly capacity, outputs and service levels.", "From £1,950/month", "#services"),
    ("Expand", "Further workstreams", "Add services once the first one is stable and measured.", "Priced per service", "pricing.html"),
]
ladder_html = "\n".join(f"""          <a class="step reveal" href="{h}">
            <span class="k">{i+1:02d} / {k}</span>
            <h3>{t}</h3>
            <p>{d}</p>
            <span class="price">{p}</span>
          </a>""" for i, (k, t, d, p, h) in enumerate(LADDER))

MODEL_POINTS = [
    ("UK commercial ownership", "Your contract, invoicing and liability sit with Bespoke Vista Ltd, a UK company."),
    ("Senior UK oversight", "Azeem Mushtaq scopes every service, reviews quality and chairs service reviews."),
    ("Office-based delivery in Lahore", "Work is carried out by our managed team in a controlled office environment, not by remote freelancers."),
    ("One point of accountability", "A named UK lead for the service, and a named delivery lead for day-to-day coordination."),
    ("Documented tasks and service levels", "Scope, outputs, service levels and SOPs are written down and agreed before work starts."),
    ("Regular performance reporting", "Weekly or monthly reporting against agreed measures, and a formal service review."),
    ("Scalable delivery capacity", "Capacity can be increased or reduced by agreement, subject to recruitment and onboarding."),
    ("Controlled AI-enabled processes", "AI is used where it improves speed or consistency, within approved tools and governance."),
]
model_html = "\n".join(f"""          <div class="point reveal"><span class="pn">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></div>""" for i, (t, d) in enumerate(MODEL_POINTS))

SAMPLES = [
    ("pmo-dashboard", "PMO dashboard", "Portfolio status, milestones, decisions needed and RAG trend on one page."),
    ("raid", "RAID register", "Risks, assumptions, issues and dependencies with owners and dates."),
    ("service-report", "Monthly service report", "Outputs delivered, service-level performance, issues and next month's plan."),
    ("process-map", "Process map", "A swim-lane map showing who does what, with control points."),
    ("sop", "SOP", "A standard operating procedure in our controlled template."),
    ("rtm", "Requirements traceability matrix", "Requirements traced to user stories, tests and status."),
    ("ai-report", "AI readiness report", "Prioritised use cases scored for value, effort and risk."),
    ("pilot-plan", "30-day pilot plan", "Week-by-week activities, measures and decision points."),
]
samples_cards = "\n".join(f"""          <a class="card sample-link reveal" href="samples.html#{sid}" data-track="sample_view">
            <span class="ill">Illustrative example</span>
            <h3>{t}</h3>
            <p>{d}</p>
            <span class="more">View sample →</span>
          </a>""" for sid, t, d in SAMPLES)

AI_USES = ["Drafting and structuring process documentation", "First-draft SOPs from approved source material",
           "Meeting transcription and action extraction", "Classifying and de-duplicating requirements",
           "Searching your knowledge base", "Preparing management reports", "Workflow automation with Power Automate",
           "Quality and consistency checks before human review"]
AI_RULES = ["People remain accountable for every final output.",
            "Client information is never put into unapproved public AI tools.",
            "Tools are selected for each engagement and agreed with you.",
            "AI use needs suitable governance and access controls in your environment.",
            "Software licences and AI consumption may be charged separately."]

SEC_CONTRACT = ["Data Processing Agreement setting out UK GDPR responsibilities",
                "International data-transfer safeguards: the UK International Data Transfer Agreement or UK Addendum where required, supported by a Transfer Risk Assessment",
                "Confidentiality agreements for everyone working on your account",
                "Intellectual-property assignment: deliverables belong to you",
                "Data minimisation: we access only what the service needs",
                "Incident-reporting obligations and timescales",
                "Access removal and data return or deletion at the end of an engagement"]
SEC_OPS = ["Role-based access, granted in your own systems where possible", "Multi-factor authentication on all accounts",
           "Managed devices with endpoint protection", "Activity logging", "Joiner, mover and leaver procedures",
           "Business-continuity arrangements for the Lahore office"]

EXPERIENCE = ["Business architecture", "Business analysis", "Digital and enterprise transformation", "Programme delivery",
              "PMO and governance", "Process improvement", "Logistics and supply chain", "Cyber security", "AI adoption",
              "Microsoft 365, Copilot, SharePoint and Power Automate"]

METHOD = [
    ("Discover", "Scorecard and assessment: the work, volumes, systems, constraints and data sensitivity."),
    ("Define", "Scope, outputs, capacity, service levels and success measures, agreed in writing."),
    ("Mobilise", "Access, onboarding, SOPs and baseline measures, following a written mobilisation plan."),
    ("Deliver", "The team works to SOPs, with second-person checks and weekly progress reporting."),
    ("Review and improve", "Monthly service review, KPI reporting, automation backlog and change control."),
]
method_html = "\n".join(f"""          <div class="reveal"><h3>{t}</h3><p>{d}</p></div>""" for t, d in METHOD)

SCENARIO = [
    ("Client situation", "A UK logistics business with around 200 employees, running nine concurrent projects, including a warehouse-system upgrade and two customer onboardings, with no PMO."),
    ("Operational problem", "Project managers spend most of a day each week compiling status reports, RAG ratings are inconsistent, and leadership hears about slippage late."),
    ("Baseline position", "Measured during the assessment: projects with a current RAID log, hours spent on reporting each week, and days between a milestone slipping and leadership being told."),
    ("Bespoke Vista intervention", "£495 Managed Operations Assessment, then a 30-day pilot covering RAID and weekly reporting for three projects, then PMO-in-a-Box Managed."),
    ("Deliverables", "Governance templates, RAID registers, a weekly portfolio dashboard, governance-meeting packs and a monthly service report."),
    ("Measured result", "In a real engagement we would report the change against each baseline measure. No results are shown because this is not a real engagement."),
    ("Delivery period", "Assessment in one to two weeks, a 30-day pilot, then a three-month initial term."),
    ("Client quotation", "None. Verified quotations will only be published with the client's written permission."),
    ("Next phase", "Extend to dependency and benefits tracking, and add a Documentation Factory project for warehouse SOPs."),
]
scenario_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in SCENARIO)

SAMPLE_BARS = [("Process maturity", 50), ("Documentation", 33), ("Project governance", 42), ("Technology readiness", 67), ("Leadership commitment", 67)]
sample_bars = "\n".join(f"""              <div class="bar-row"><span>{n}</span><div class="track"><div class="fill" style="width:{v}%"></div></div><span class="v">{v}%</span></div>""" for n, v in SAMPLE_BARS)

home = f"""    <section class="hero home-hero">
      <div class="container hero-grid">
        <div>
          {label("Managed PMO · Business analysis · Process documentation")}
          <h1>Build the capability you need, <em class="ember">without building another department.</em></h1>
          <p class="lead">Bespoke Vista provides UK-led business analysis, PMO, process documentation and AI-enabled operational services, delivered by managed teams in our Lahore office.</p>
          <p class="support">Senior UK oversight. Office-based delivery. Defined outputs, transparent pricing and accountable service management.</p>
          <div class="hero-actions">
            {btn("Take the Free Readiness Scorecard", "scorecard.html", "btn-ember")}
            {btn("Book a Managed Operations Assessment", ASSESS_HREF, "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">UK-managed. Lahore-delivered. AI-enabled.</p>
        </div>
        <div class="hero-art">
          {horizon(["ASSESS", "PILOT", "RUN", "SCALE"], "A sun rising over a horizon, marking the route: assess, pilot, run and scale")}
        </div>
      </div>
      <div class="container">
        <dl class="facts">
          <div><dt>Start with</dt><dd>£495 assessment</dd></div>
          <div><dt>Prove it with</dt><dd>30-day pilot from £1,500</dd></div>
          <div><dt>Run it as</dt><dd>Managed service from £1,950/month</dd></div>
          <div><dt>Led by</dt><dd>Azeem Mushtaq, 25+ years in transformation</dd></div>
        </dl>
      </div>
    </section>

    <section class="sec sec-white" id="who">
      <div class="container">
        <div class="head">
          <div>{label("Who we work with")}<h2>For UK organisations of 50 to 500 people where the work has <em class="ember">outgrown the team.</em></h2></div>
          <p>We focus on a small number of situations where managed capacity makes the biggest difference. If yours isn't listed, the scorecard will tell you quickly whether we're a good fit.</p>
        </div>
        <div class="fit-grid">
{who_html}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Common problems")}<h2>Six problems our services are <em class="ember">designed to fix.</em></h2></div>
          <p>Each one costs senior time every week and gets worse as the organisation grows. Each one has a defined, priced service behind it.</p>
        </div>
        <div class="grid g3">
{problems_html}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="services">
      <div class="container">
        <div class="head">
          <div>{label("Managed services")}<h2>Three services. <em class="ember">Clear scope, clear prices.</em></h2></div>
          <p>Each runs to defined capacity, outputs and service levels. Monthly services have a three-month initial term, then 30 days' notice. All prices exclude VAT. No package provides unlimited work.</p>
        </div>
        <div class="grid g3 svc-grid">
{services_cards}
        </div>
      </div>
    </section>

    <section class="sec sec-sand">
      <div class="container split" style="align-items:center">
        <div class="reveal">
          {label("Free readiness scorecard")}
          <h2>Is your organisation ready for <em class="ember">managed delivery?</em></h2>
          <p>Thirteen questions covering process maturity, documentation, internal capacity, project governance, management reporting, technology, AI, data sensitivity, outsourcing readiness and leadership commitment.</p>
          <ul class="ticks">
            <li>Your score straight away, with no email required</li>
            <li>Plain-English interpretation and principal risks</li>
            <li>Three recommended actions and the most suitable service</li>
            <li>Download or email your result</li>
          </ul>
          <div class="hero-actions" style="margin-bottom:0">{btn("Take the Free Readiness Scorecard", "scorecard.html", "btn-ember")}</div>
        </div>
        <div class="sample-card reveal" aria-label="Example of a scorecard result">
          <div class="sample-top"><span class="label" style="margin:0">Example result</span><span class="sample-score"><strong>48</strong>/100</span></div>
          <p class="band" style="margin:10px 0 0">Suitable for a controlled pilot</p>
          <div class="bars" style="margin:18px 0">
{sample_bars}
          </div>
          <div class="sample-foot"><span class="small muted">Recommended next step</span><strong>30-Day Managed Delivery Pilot</strong><span class="small muted">after a £495 assessment</span></div>
        </div>
      </div>
    </section>

    <section class="sec" id="pathway">
      <div class="container">
        <div class="head">
          <div>{label("Low-risk route")}<h2>Start small. Prove it. <em class="ember">Then scale.</em></h2></div>
          <p>You don't need to commit to a managed service to find out whether it will work. Each step is paid for on its own, and you decide whether to continue.</p>
        </div>
        <div class="ladder">
{ladder_html}
        </div>
        <div class="grid g2" style="margin-top:48px">
          <div id="assessment" class="anchor-offset">
{offer_card(ASSESSMENT, "Book a Managed Operations Assessment", ASSESS_HREF, "Start here", "featured")}
          </div>
          <div id="pilot" class="anchor-offset">
{offer_card(PILOT, "Start a 30-Day Pilot", "contact.html?topic=pilot")}
          </div>
        </div>
      </div>
    </section>

    <section class="sec sec-dark" id="delivery-model">
      <div class="container">
        <div class="head">
          <div>{label("Delivery model")}<h2>UK-managed. Lahore-delivered. <em class="ember">AI-enabled.</em></h2></div>
          <p>You contract with a UK company and deal with a UK lead. The work is carried out by office-based professionals in our Lahore delivery centre, using controlled AI-enabled processes where they help.</p>
        </div>
        <div class="points">
{model_html}
        </div>
        <div class="split" style="margin-top:64px;align-items:center">
          {TIMELINE}
          <div class="reveal">
            <h3 style="font-family:var(--display);font-size:1.6rem;font-weight:600">Mobilisation</h3>
            {MOBILISATION}
            {CLOCKS}
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="samples">
      <div class="container">
        <div class="head">
          <div>{label("Example outputs")}<h2>See what you <em class="ember">will receive.</em></h2></div>
          <p>Every service produces defined documents and reports. These examples show the format and level of detail. They are illustrative examples, not actual client deliverables.</p>
        </div>
        <div class="grid g4">
{samples_cards}
        </div>
        <div class="hero-actions" style="margin:32px 0 0">{btn("View a Sample Deliverable", "samples.html", "btn-primary")}</div>
      </div>
    </section>

    <section class="sec sec-white" id="ai">
      <div class="container">
        <div class="head">
          <div>{label("AI-enabled delivery")}<h2>AI speeds up the work. <em class="ember">People stay accountable</em> for it.</h2></div>
          <p>We use AI inside delivery where it saves time or improves consistency, and never as a substitute for checking the work.</p>
        </div>
        <div class="split">
          <div class="reveal">
            <h3>Where AI helps in practice</h3>
            <ul class="ticks">{''.join(f'<li>{x}</li>' for x in AI_USES)}</ul>
          </div>
          <div class="reveal">
            <h3>Our rules for using AI</h3>
            <ul class="ticks">{''.join(f'<li>{x}</li>' for x in AI_RULES)}</ul>
          </div>
        </div>
        <div class="grid g2" style="margin-top:48px">
{offer_card(AI_DISCOVERY, "Enquire about AI Operations Discovery", "contact.html?topic=ai-discovery")}
{offer_card(AI_WORKFLOW, "Enquire about AI Workflow Implementation", "contact.html?topic=ai-workflow")}
        </div>
      </div>
    </section>

    <section class="sec" id="security">
      <div class="container">
        <div class="head">
          <div>{label("Security and data protection")}<h2>How we protect your <em class="ember">operations and data.</em></h2></div>
          <p>Where we process personal data for you, you are normally the controller and Bespoke Vista acts as your processor under UK GDPR. This is what we put in place, and where each control stands today.</p>
        </div>
        <div class="sec-cols">
          <div class="sec-col reveal">
            <span class="status s-contract">Contractual commitments</span>
            <h3>In our client contracts</h3>
            <ul class="ticks">{''.join(f'<li>{x}</li>' for x in SEC_CONTRACT)}</ul>
            {owner("confirm the DPA, IDTA/Addendum, TRA, confidentiality and IP-assignment templates are drafted with legal advice before publishing this column as a commitment.")}
          </div>
          <div class="sec-col reveal">
            <span class="status s-progress">Being implemented</span>
            <h3>Operational controls</h3>
            <ul class="ticks">{''.join(f'<li>{x}</li>' for x in SEC_OPS)}</ul>
            {owner("mark each control as in place or in progress, with a target date.")}
          </div>
          <div class="sec-col reveal">
            <span class="status s-future">Certification objectives</span>
            <h3>Independent assurance</h3>
            <p>Security controls are being developed with reference to Cyber Essentials and ISO/IEC 27001 requirements.</p>
            <p>Bespoke Vista does not currently hold either certification, and we will say so plainly until we do.</p>
            {owner("target dates for Cyber Essentials (and Cyber Essentials Plus, if planned).")}
          </div>
        </div>
      </div>
    </section>

    <section class="sec sec-sand" id="founder">
      <div class="container split">
        <div class="reveal">
          {label("Founder")}
          <h2>Senior UK oversight from first conversation <em class="ember">to final delivery.</em></h2>
          <p>Azeem Mushtaq brings more than 25 years of experience across business architecture, business analysis, transformation, programme delivery, cyber security and operational improvement. He provides UK-based commercial accountability and senior quality assurance across Bespoke Vista engagements.</p>
          <h3>In every engagement, Azeem:</h3>
          <ul class="ticks">
            <li>Leads the Managed Operations Assessment personally</li>
            <li>Agrees scope, service levels and success measures with you</li>
            <li>Reviews quality before outputs reach you</li>
            <li>Chairs service reviews and is your escalation point</li>
          </ul>
          {btn("Book a Managed Operations Assessment", ASSESS_HREF, "btn-primary")}
        </div>
        <aside class="profile reveal" aria-label="Founder profile">
          {owner("professional photograph of Azeem (replaces the initials below).") if SHOW_OWNER_PLACEHOLDERS else ''}
          <div class="avatar" aria-hidden="true">AM</div>
          <h3>Azeem Mushtaq</h3>
          <p class="role">Founder and senior UK lead</p>
          <p style="color:var(--paper);font-weight:600;margin:18px 0 10px">Experience</p>
          <ul class="chips">{''.join(f'<li>{x}</li>' for x in EXPERIENCE)}</ul>
          {f'<p style="margin-top:18px"><a href="{LINKEDIN_URL}" rel="noopener">View LinkedIn profile →</a></p>' if LINKEDIN_URL else owner("LinkedIn profile URL (set LINKEDIN_URL in build.py).")}
          {owner("verified qualifications, certifications, professional memberships, sector experience, major programme examples (no client names without permission) and client recommendations.")}
        </aside>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Delivery methodology")}<h2>How every engagement runs.</h2></div>
          <p>The same five stages apply whether you start with an assessment, a documentation project or a managed service.</p>
        </div>
        <div class="steps steps5">
{method_html}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="proof">
      <div class="container">
        <div class="head">
          <div>{label("Evidence")}<h2>How a managed service works <em class="ember">in practice.</em></h2></div>
          <p>Published case studies will include the client's situation, baseline, intervention, measured result and quotation, with permission. Until then, this scenario shows how an engagement runs.</p>
        </div>
        <article class="scenario reveal">
          <div class="scenario-head">
            <span class="status s-future">Illustrative delivery scenario</span>
            <h3>PMO-in-a-Box for a UK logistics business</h3>
            <p class="small"><strong>This example demonstrates how the service operates and is not presented as an actual client engagement.</strong></p>
          </div>
          <dl>{scenario_html}</dl>
        </article>
        <div class="split" style="margin-top:40px">
          <div class="reveal">
            <h3>Founder experience</h3>
            <p>Azeem's background includes enterprise transformation, cyber security programmes, AI productivity work, delivery across the UK, Pakistan and India, and the turnaround of a property business in Lahore.</p>
            <a class="text-link" href="case-studies.html">Read the experience summaries →</a>
          </div>
          <div class="reveal">
            <h3>Client testimonials</h3>
            {owner("verified testimonials with name, role, organisation and written permission to publish. Until then this block is hidden when placeholders are switched off.")}
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="container split">
        <div>
          {label("FAQs")}
          <h2>Straight answers.</h2>
          <p class="muted">Something else? <a href="contact.html?topic=consultation">Ask us directly.</a></p>
        </div>
        <div class="faq">
{faq_html}
        </div>
      </div>
    </section>

{cta()}

    <section class="sec-tight" id="company">
      <div class="container">
        <div class="company reveal">
          <div>
            <h3>Bespoke Vista Ltd</h3>
            <p>Registered in England and Wales.{f' Company number {COMPANY_NUMBER}.' if COMPANY_NUMBER else ''}</p>
            {f'<p>Registered office: {REGISTERED_OFFICE}</p>' if REGISTERED_OFFICE else owner("company number and registered office address (set in build.py).")}
          </div>
          <div>
            <h3>Contact</h3>
            <p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
            <p><a href="contact.html">Contact form</a> · <a href="{ASSESS_HREF}" data-track="{track_for(ASSESS_HREF)}">Book an assessment</a></p>
          </div>
          <div>
            <h3>Lahore delivery centre</h3>
            <p>{LAHORE_ADDRESS or 'Lahore, Pakistan'}</p>
            {'' if LAHORE_ADDRESS else owner("office address, and photographs of the office once verified.")}
          </div>
        </div>
      </div>
    </section>"""

ORG = {"@type": "Organization", "@id": BASE_URL + "#org", "name": "Bespoke Vista Ltd", "alternateName": "Bespoke Vista",
       "url": BASE_URL, "logo": BASE_URL + "assets/img/logo@2x.png", "email": CONTACT_EMAIL,
       "founder": {"@type": "Person", "name": "Azeem Mushtaq"}, "areaServed": "GB"}
if LINKEDIN_URL:
    ORG["sameAs"] = [LINKEDIN_URL]


def svc_schema(name, desc, price):
    s = {"@type": "Service", "name": name, "description": desc, "provider": {"@id": BASE_URL + "#org"}, "areaServed": "GB"}
    if price:
        s["offers"] = {"@type": "Offer", "priceCurrency": "GBP", "price": price, "description": "Price excludes VAT"}
    return s


HOME_SCHEMA = [
    ORG,
    {"@type": "ProfessionalService", "name": "Bespoke Vista", "url": BASE_URL, "parentOrganization": {"@id": BASE_URL + "#org"},
     "description": "UK-led managed PMO, business analysis, process documentation and AI-enabled operational services, delivered by office-based teams in Lahore.",
     "areaServed": "GB", "priceRange": "£495–£15,000"},
    svc_schema("PMO-in-a-Box", PMO[3], "1950"),
    svc_schema("Managed Business Analysis", BA[3], "2250"),
    svc_schema("Documentation Factory", DOCS[3], "2950"),
    svc_schema("Managed Operations Assessment", "Discovery workshop, readiness review, capacity and cost model, recommended pilot and written findings.", "495"),
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]

page("index.html", SITE,
     "UK-led managed PMO, business analysis and process documentation for SMEs and mid-market organisations, delivered by office-based teams in Lahore. Assessments from £495.",
     home, schema=HOME_SCHEMA,
     full_title="Managed PMO, Business Analysis &amp; Process Documentation | Bespoke Vista")

# ============================================================== SERVICES
def svc(name, one, tag, who, gets, topic):
    return f"""            <details class="svc">
              <summary><h3>{name}</h3><span class="tag">{tag}</span><p class="one">{one}</p><span class="plus">Details</span></summary>
              <div class="body">
                <dl><dt>Ideal for</dt><dd>{who}</dd><dt>You get</dt><dd>{gets}</dd></dl>
                <a class="btn btn-line btn-sm" href="contact.html?topic={topic}">Discuss {name} {ARR}</a>
              </div>
            </details>"""


RUN = [
    ("PMO-in-a-Box", "Governance, reporting and control across your project portfolio.", "£1,950–£7,500+/month",
     "Organisations running 3 to 15 projects without a consistent PMO.", "RAID and action management, dashboards, governance packs, dependency and benefits tracking, monthly service review.", "pmo"),
    ("Managed Business Analysis", "Business-analysis capacity to an agreed standard each month.", "£2,250–£7,500+/month",
     "Transformation and change teams short of analysts.", "Process mapping, requirements, user stories, traceability, options analysis and business cases, with senior UK quality review.", "ba"),
    ("Documentation Factory", "Processes, maps and SOPs documented properly, at a fixed price.", "£2,950–£9,500+",
     "Organisations with undocumented or inconsistent processes.", "Process maps, SOPs, roles and responsibilities, controls, KPIs and a controlled document library.", "documentation"),
] + [(n, d, "Priced after assessment", "Clients with an established first service.", note, "managed") for n, d, note in SECONDARY]

ADVISE = [
    ("Managed Operations Assessment", "Find out what could be handed over safely, and how.", "£495 · 1 to 2 weeks",
     "Any organisation considering managed delivery.", "Discovery workshop, readiness review, process prioritisation, capacity and cost model, recommended pilot and written findings.", "assessment"),
    ("Transformation Health Check", "An honest, independent view of a programme that's late, over budget or losing confidence.", "£4,950 · 2 weeks",
     "Boards and sponsors of programmes in trouble.", "Independent review, evidence-based RAG assessment, recovery plan and executive briefing.", "health-check"),
    ("Target Operating Model Design", "Redesign how the business works after growth, a merger or a change in strategy.", "From £12,000",
     "Growing SMEs and mid-market firms, especially logistics and warehousing.", "Capability map, process and organisation design, technology and governance model, and a phased roadmap.", "tom"),
    ("Fractional Business Architect", "Senior architecture and transformation leadership, a few days a month.", "£995–£3,995/month",
     "Firms with change on the agenda but no architect.", "Operating model ownership, roadmap and portfolio prioritisation, design reviews and board reporting.", "fractional"),
    ("Cyber Security Business Analysis", "Security requirements turned into processes people follow.", "Fixed scope or day rate",
     "Organisations running security, compliance or resilience programmes.", "Requirements, process design, governance and adoption support.", "cyber-ba"),
]
AI = [
    ("AI Operations Discovery", "Find the five AI use cases worth doing, and the risks.", "£2,500 · 3 to 4 weeks",
     "Organisations ready to move from AI interest to AI delivery.", "AI readiness assessment, process and data review, five prioritised use cases, risk and governance review, 90-day roadmap and indicative business case.", "ai-discovery"),
    ("AI Workflow Implementation", "One to three working AI-assisted workflows.", "£5,000–£15,000",
     "Teams with defined, repetitive processes.", "Workflows using Copilot, SharePoint, Power Automate, Claude or ChatGPT where technically viable, with testing, user guidance, governance documentation and handover.", "ai-workflow"),
    ("AI Governance Pack", "Use AI confidently without putting data or reputation at risk.", "£2,500–£6,000",
     "Any organisation where staff already use AI tools.", "Usage policy, risk register, data rules, DPIA template and a use-case approval process.", "governance"),
    ("Microsoft Copilot Adoption Programme", "Turn Copilot licences into everyday productivity.", "£5,000–£25,000",
     "Microsoft 365 organisations rolling out Copilot.", "Readiness and permissions review, governance, champions, role-based training and adoption tracking.", "copilot"),
    ("AI Optimisation Review", "Already paying for AI tools? Find out why value is low.", "£1,950 · 2 weeks",
     "Organisations six months or more into Copilot, ChatGPT or Claude.", "Usage analysis, staff interviews, quick fixes and an improvement plan.", "ai-optimisation"),
]
LEARN = [
    ("Executive AI Intelligence", "The monthly AI briefing for busy leaders.", "£49–£199/month",
     "Directors, owners and senior managers.", "Monthly briefing, tool watchlist, prompt library, live Q&amp;A and sector playbooks.", "intelligence"),
    ("AI for Leaders", "What is real, what is hype and where to start.", "£1,450 · half day",
     "Leadership teams of up to 12.", "Interactive workshop, opportunity mapping and a one-page action plan.", "training"),
    ("Copilot Skills Bootcamp", "Hands-on, role-based Copilot training.", "£2,950 · 2 days",
     "Teams of up to 15 with Copilot licences.", "Practical exercises, prompt packs per role and follow-up resources.", "training"),
    ("Calm Under Pressure", "Leadership resilience through Tai Chi, martial arts and breath.", "£1,250 · half day",
     "Leadership and high-pressure teams.", "Practical techniques for focus, composure and recovery.", "wellbeing"),
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


def subnav(items):
    return """    <nav class="subnav" aria-label="Jump to section">
      <div class="container"><ul>
""" + "\n".join(f'        <li><a href="#{a}">{l}</a></li>' for a, l in items) + """
      </ul></div>
    </nav>"""


services = f"""    <section class="page-hero">
      <div class="container">
        {label("Services")}
        <h1>Managed services first. <em class="ember">Specialist support when you need it.</em></h1>
        <p class="lead">Our three core managed services are PMO-in-a-Box, Managed Business Analysis and the Documentation Factory. Assessment, AI and advisory services support them. Tap any service for details.</p>
      </div>
    </section>
{subnav([("run", "Managed services"), ("advise", "Assess and advise"), ("ai", "AI services"), ("learn", "Training"), ("industries", "Sectors")])}
    <section class="sec">
      <div class="container">
{svc_block("run", "01", "Managed services", "Delivered by our Lahore team under a UK lead, to defined capacity, outputs and service levels.", RUN, btn("Book a Managed Operations Assessment", ASSESS_HREF, "btn-ember btn-sm"))}
{svc_block("advise", "02", "Assess and advise", "Fixed-scope consulting wherever possible, so you know the cost before we start.", ADVISE)}
{svc_block("ai", "03", "AI services", "Practical AI using Microsoft Copilot, SharePoint, Power Automate, ChatGPT and Claude, starting from a measurable business problem.", AI, '<a class="btn btn-line btn-sm" href="ai-scorecard.html">Take the AI Readiness Scorecard ' + ARR + '</a>')}
{svc_block("learn", "04", "Training and briefings", "Capability building for leaders and teams.", LEARN)}
        <div class="pillar-block" id="industries">
          <div class="side reveal">
            <span class="big-n">✦</span>
            <h2>Sectors</h2>
            <p>Our focus is logistics, supply chain and professional services. We also work with the sectors below.</p>
          </div>
          <ul class="chips reveal" style="align-self:start">{''.join(f'<li>{x}</li>' for x in INDUSTRIES)}</ul>
        </div>
      </div>
    </section>

{cta()}"""

page("services.html", "Services",
     "Managed PMO, Business Analysis as a Service and process documentation from Bespoke Vista, plus assessment, AI workflow and advisory services with clear prices.",
     services, schema=[svc_schema(r[0], r[1], None) for r in RUN[:3] + AI[:2]])

# ============================================================== DELIVERY MODEL (managed-teams.html)
primary_offers = "\n".join(f"""          <div class="offer reveal">
            <h3>{p[1]}</h3>
            <p class="outcome">{p[3]}</p>
            <ul>{''.join(f'<li>{x}</li>' for x in p[4][1][3][:4])}</ul>
            <div class="meta"><span class="p">From {p[4][0][2]}{'' if p[0] == 'documentation' else '/month'}</span><a href="pricing.html#{p[0]}">Packages and terms →</a></div>
          </div>""" for p in PRIMARY)
secondary_offers = "\n".join(f"""          <div class="pl-row reveal"><h3>{n}</h3><p>{d}</p><span class="t">{note}</span><span></span></div>""" for n, d, note in SECONDARY)

SLA = [
    ("Typical package", "Foundation, Essential, Process Starter", "Managed, Growth, Operations Manual", "Transformation Office, Transformation"),
    ("Cover", "Lahore office hours, with UK-morning overlap", "Lahore office hours, with UK-morning overlap", "Extended cover by agreement"),
    ("Response to requests", "Next working day", "Within 4 working hours", "Within 2 working hours"),
    ("Reporting", "Monthly", "Weekly, plus monthly review", "Weekly, plus monthly executive pack"),
    ("Service review", "Monthly", "Monthly, UK-led", "Monthly, with senior UK oversight"),
    ("Improvement", "Quarterly review", "Monthly improvement backlog", "Monthly backlog and quarterly value review"),
]
sla_rows = "\n".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in SLA)

managed = f"""    <section class="page-hero">
      <div class="container">
        {label("Delivery model")}
        <h1>UK-managed. Lahore-delivered. <em class="ember">AI-enabled.</em></h1>
        <p class="lead">You contract with a UK company. A senior UK lead owns the outcome. Office-based professionals in our Lahore delivery centre do the work to documented processes and service levels.</p>
        <div style="margin-top:28px">{CLOCKS}</div>
      </div>
    </section>

    <section class="sec">
      <div class="container split">
        <div class="reveal">
          {label("Our model")}
          <h2>We don't sell people. <em class="ember">We sell defined outcomes.</em></h2>
        </div>
        <div class="reveal">
          <p>We don't supply CVs, contractors or staff for you to manage. Each service has defined deliverables, capacity and quality standards. A UK lead owns the result. AI-enabled processes take on repetitive steps, under human review.</p>
          <ul class="ticks">
            <li>Fixed monthly price for an agreed scope and capacity</li>
            <li>Written service levels and regular reporting</li>
            <li>One accountable UK contact</li>
            <li>Documented SOPs, so the knowledge stays with you</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="sec sec-dark">
      <div class="container">
        <div class="points">
{model_html}
        </div>
        <div class="split" style="margin-top:64px;align-items:center">
          {TIMELINE}
          <div class="reveal">
            <h3 style="font-family:var(--display);font-size:1.6rem;font-weight:600">Mobilisation</h3>
            {MOBILISATION}
          </div>
        </div>
        <div class="steps steps5" style="margin-top:72px">
{method_html}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="offerings">
      <div class="container">
        <div class="head">
          <div>{label("Core managed services")}<h2>Three services, <em class="ember">ready to run.</em></h2></div>
          <p>Most clients start with an assessment and a 30-day pilot. <a href="index.html#pathway">See the low-risk route →</a></p>
        </div>
        <div class="grid g3">
{primary_offers}
        </div>
        <h3 style="margin-top:56px">Further managed services</h3>
        <p class="muted">Available once a first service is running, or where an assessment shows a clear fit. Priced after assessment.</p>
        <div class="pricelist">
{secondary_offers}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Service levels")}<h2>Three levels of <em class="ember">service.</em></h2></div>
          <p>Each package runs to one of these service levels. Response targets apply during UK business hours. Service credits, if offered, are set out in your contract.</p>
        </div>
        <div class="table-wrap table-light reveal">
          <table class="sla">
            <thead><tr><th scope="col"><span class="sr-only">Item</span></th><th scope="col">Essential</th><th scope="col">Assured</th><th scope="col">Critical</th></tr></thead>
            <tbody>{sla_rows}</tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container split">
        <div class="reveal">
          {label("Security")}
          <h2>Your data, <em class="ember">your controls.</em></h2>
          <p>We prefer to work inside your systems and Microsoft 365 tenant, under your access controls. Contractual protections, operational controls and certification objectives are set out, with their current status, on the homepage.</p>
          <a class="text-link" href="index.html#security">How we protect your operations and data →</a>
        </div>
        <ul class="ticks reveal">{''.join(f'<li>{x}</li>' for x in SEC_CONTRACT[:4])}</ul>
      </div>
    </section>

{cta()}"""

page("managed-teams.html", "Delivery Model",
     "How Bespoke Vista's UK-managed, Lahore-delivered, AI-enabled model works: UK accountability, office-based delivery, service levels and mobilisation.",
     managed)

# ============================================================== PRICING
SUBNAV_PRICING = [("start", "Assessment and pilot"), ("pmo", "PMO-in-a-Box"), ("ba", "Managed BA"), ("documentation", "Documentation Factory"),
                  ("terms", "Commercial terms"), ("projects", "AI and fixed-price projects"), ("intelligence", "Subscriptions"),
                  ("training", "Training"), ("dojoos", "DojoOS"), ("faq", "FAQs")]

subs_html = "\n".join(product_block(s, annual=True) for s in SUBSCRIPTIONS)
terms_html = "\n".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in TERMS)
pricing_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in [FAQ[12], FAQ[11], FAQ[16], FAQ[17], FAQ[13], FAQ[10]])

pricing = f"""    <section class="page-hero">
      <div class="container">
        {label("Pricing and terms")}
        <h1>Real prices. <em class="ember">Clear boundaries.</em></h1>
        <p class="lead">Every package states what's included, how much capacity you get, and what isn't covered. No package provides unlimited work. All prices exclude VAT.</p>
      </div>
    </section>
{subnav(SUBNAV_PRICING)}
    <section class="sec" id="start" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Start here")}<h2>Assess first. <em class="ember">Pilot before you commit.</em></h2></div>
          <p>The assessment fee is credited against a qualifying pilot commissioned within 30 days.</p>
        </div>
        <div class="grid g2">
{offer_card(ASSESSMENT, "Book a Managed Operations Assessment", ASSESS_HREF, "Start here", "featured")}
{offer_card(PILOT, "Start a 30-Day Pilot", "contact.html?topic=pilot")}
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container">
{product_block(PMO)}
{boundaries_table(PMO)}
        <div style="height:72px"></div>
{product_block(BA)}
{boundaries_table(BA)}
      </div>
    </section>

    <section class="sec">
      <div class="container">
{product_block(DOCS, per="fixed price, ex VAT")}
        <div class="sop-def" style="margin-top:-40px;margin-bottom:24px"><strong>What counts as one standard SOP:</strong> <ul>{''.join(f'<li>{x}</li>' for x in SOP_DEFINITION)}</ul></div>
{boundaries_table(DOCS)}
      </div>
    </section>

    <section class="sec sec-sand" id="terms" style="scroll-margin-top:140px">
      <div class="container split">
        <div>{label("Commercial terms")}<h2>The terms behind <em class="ember">every price.</em></h2><p class="muted">Full terms are set out in your proposal and contract.</p></div>
        <div class="table-wrap table-light"><table class="sla"><tbody>{terms_html}</tbody></table></div>
      </div>
    </section>

    <section class="sec" id="projects" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("AI and fixed-price projects")}<h2>Defined scope. <em class="ember">Defined price.</em></h2></div>
          <p>One-off engagements with a clear deliverable. AI integrations are only proposed once a viable technical route is confirmed.</p>
        </div>
        <div class="pricelist">
{pricelist(PROJECTS)}
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:56px">
          <div>{label("Subscriptions")}<h2 style="margin:0">Advisory and briefings</h2></div>
          <div class="billing" role="group" aria-label="Billing period">
            <button type="button" data-billing="monthly" aria-pressed="true">Monthly</button>
            <button type="button" data-billing="annual" aria-pressed="false">Annual<span class="save">2 months free</span></button>
          </div>
        </div>
{subs_html}
      </div>
    </section>

    <section class="sec sec-sand" id="training" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Training")}<h2>Build capability <em class="ember">that lasts.</em></h2></div>
          <p>On-site in the UK or live online. Prices are per session for your group.</p>
        </div>
        <div class="pricelist">
{pricelist(TRAINING)}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
{product_block(DOJOOS, extra='<p style="margin-top:10px">' + label("In development · founding schools wanted") + '</p>')}
      </div>
    </section>

    <section class="sec sec-white" id="faq" style="scroll-margin-top:140px">
      <div class="container split">
        <div>{label("FAQs")}<h2>Pricing questions.</h2><p class="muted">More answers on the <a href="index.html#faq">homepage</a>.</p></div>
        <div class="faq">
{pricing_faq}
        </div>
      </div>
    </section>

{cta()}"""

page("pricing.html", "Pricing",
     "Bespoke Vista prices and package boundaries: £495 assessment, 30-day pilots from £1,500, PMO-in-a-Box from £1,950/month, Managed Business Analysis from £2,250/month, Documentation Factory from £2,950.",
     pricing, schema=[svc_schema("PMO-in-a-Box", PMO[3], "1950"), svc_schema("Managed Business Analysis", BA[3], "2250"),
                      svc_schema("Documentation Factory", DOCS[3], "2950")])


# ============================================================== SCORECARDS
# Both scorecards share one engine (assets/js/main.js). Each is defined by a data block:
# dimensions, scored questions (options score 0-3, most ready last), unscored context
# questions, and result bands with interpretation, risks, actions, service and next step.

CONTEXT_QS = [
    {"id": "size", "text": "How many people does your organisation employ?",
     "options": ["Fewer than 50", "50 to 249", "250 to 500", "More than 500"]},
    {"id": "sector", "text": "Which best describes your organisation?",
     "options": ["Logistics, warehousing or supply chain", "Professional services", "Technology",
                 "Property", "Other: membership, training, wellbeing or similar"]},
]
CONTEXT_NOTES = {
    "sector": {"0": "Logistics and supply chain is where our founder has spent much of his career, so we already understand warehouse and transport processes, peak planning, customer reporting and the systems behind them."},
    "size": {"0": "For organisations under 50 people we usually start with a single workflow or a Process Starter documentation project, so the commitment stays proportionate."},
}

S_PMO = {"name": "PMO-in-a-Box", "price": "From £1,950/month", "href": "pricing.html#pmo",
         "what": "Governance, RAID management and portfolio reporting across your projects, with a monthly UK-led service review."}
S_BA = {"name": "Managed Business Analysis", "price": "From £2,250/month", "href": "pricing.html#ba",
        "what": "Process mapping, requirements and backlog management to a defined monthly capacity, with senior UK quality review."}
S_DOCS = {"name": "Documentation Factory: Process Starter", "price": "£2,950 fixed", "href": "pricing.html#documentation",
          "what": "Five documented processes and SOPs in a controlled library: the foundation for handing any work over safely."}
S_PILOT = {"name": "30-Day Managed Delivery Pilot", "price": "£1,500–£2,500", "href": "index.html#pilot",
           "what": "One defined process or workstream, a named delivery lead, baseline measures, weekly reviews and a results report."}
S_AI = {"name": "AI Operations Discovery", "price": "£2,500 fixed", "href": "index.html#ai",
        "what": "AI readiness, process and data review, five prioritised use cases, risk review and a 90-day roadmap."}
S_SCALE = {"name": "PMO-in-a-Box Managed or Transformation Office", "price": "£3,950 to £7,500+/month", "href": "pricing.html#pmo",
           "what": "A weekly PMO rhythm or programme-level support across several workstreams, with senior UK oversight."}

NEXT_ASSESS = {"label": "Book a Managed Operations Assessment", "href": ASSESS_HREF, "track": track_for(ASSESS_HREF),
               "text": "Book a £495 Managed Operations Assessment. The fee is credited against a qualifying pilot commissioned within 30 days."}

OPS_QUIZ = {
    "id": "operations",
    "topic": "scorecard",
    "title": "Managed Delivery Readiness Scorecard",
    "dims": [
        {"id": "process", "name": "Process maturity", "service": S_DOCS},
        {"id": "docs", "name": "Documentation quality", "service": S_DOCS},
        {"id": "capacity", "name": "Internal capacity", "service": S_PILOT},
        {"id": "governance", "name": "Project governance", "service": S_PMO},
        {"id": "reporting", "name": "Management reporting", "service": S_PMO},
        {"id": "tech", "name": "Technology readiness", "service": None},
        {"id": "ai", "name": "AI readiness", "service": S_AI},
        {"id": "data", "name": "Data sensitivity", "service": None},
        {"id": "outsourcing", "name": "Outsourcing readiness", "service": S_PILOT},
        {"id": "leadership", "name": "Leadership commitment", "service": None},
    ],
    "questions": [
        {"dim": "process", "text": "How consistent are your core operational processes?",
         "options": ["Different every time, depending on who does it", "Consistent within teams, but not across them",
                     "Mostly standardised", "Standardised, owned and measured"]},
        {"dim": "docs", "text": "If a key person left tomorrow, how much of their process knowledge is written down?",
         "options": ["Very little, it's in their head", "Some notes, mostly out of date",
                     "Most of it, scattered across different places", "Documented SOPs, owned and kept current"]},
        {"dim": "docs", "text": "How long does it take a new starter to work independently?",
         "options": ["Months, learnt by shadowing", "Several weeks, mostly shadowing", "A few weeks, with some guides",
                     "Days, with SOPs and training material"]},
        {"dim": "capacity", "text": "Who could own a managed service day to day, briefing the team and approving outputs?",
         "options": ["Nobody has the time", "Someone, but only occasionally", "A named manager with a few hours a week",
                     "A named owner with time set aside"]},
        {"dim": "governance", "text": "How are your current change projects governed?",
         "options": ["Informally, through emails and meetings", "Each project manager does it their own way",
                     "Common templates, applied inconsistently", "Consistent governance, with RAID logs and decisions recorded"]},
        {"dim": "reporting", "text": "How is management reporting produced?",
         "options": ["Ad hoc, when someone asks", "Manually each month, and it takes days",
                     "Regular templates, partly automated", "Scheduled, consistent and largely automated"]},
        {"dim": "tech", "text": "Where does most operational work happen?",
         "options": ["Paper, email and personal spreadsheets", "Shared drives and a mix of tools",
                     "Mainly Microsoft 365 or other cloud systems", "Cloud systems with role-based access we manage centrally"]},
        {"dim": "tech", "text": "Could you give an external team secure, controlled access to the systems they would need?",
         "options": ["No, not without major change", "Possibly, with significant IT effort", "Yes, through standard onboarding",
                     "Yes, we already do this for partners"]},
        {"dim": "ai", "text": "How are AI tools used in your organisation?",
         "options": ["Not at all, or we don't know", "Individuals using free tools", "Approved business tools in some teams",
                     "Governed tools with a usage policy"]},
        {"dim": "data", "text": "How sensitive is the information the work would involve?",
         "options": ["Highly regulated or special-category data", "Significant personal or commercially sensitive data",
                     "Some personal data, manageable with controls", "Mostly operational, low-sensitivity information"]},
        {"dim": "outsourcing", "text": "What is your experience of outsourced or managed services?",
         "options": ["None, and we have real reservations", "We tried it and it didn't go well", "Some positive experience",
                     "Established, well-managed suppliers"]},
        {"dim": "outsourcing", "text": "Could the work you'd hand over be described in terms of inputs, outputs and quality standards?",
         "options": ["Not really", "Partly", "Mostly", "Yes, clearly"]},
        {"dim": "leadership", "text": "How committed is leadership to changing how this work is done?",
         "options": ["It isn't a priority", "Interested, but no sponsor", "A sponsor, but no budget yet", "Sponsor and budget agreed"]},
    ],
    "context": CONTEXT_QS,
    "notes": CONTEXT_NOTES,
    "bands": [
        {"max": 30, "name": "Not yet ready for managed delivery",
         "title": "Get the foundations in place first",
         "text": "Handing work over now would transfer confusion rather than capacity. That's common, and fixable: the priority is to document the work that matters most, name an internal owner and agree what an external team could safely access.",
         "risks": ["Undocumented work can't be transferred reliably", "Without a named owner, outputs won't be reviewed or used", "Access and data questions could stall any pilot"],
         "actions": ["Document the three to five processes that matter most", "Nominate an internal owner with a few hours a week", "Agree which systems and data an external team could access"],
         "service": S_DOCS, "next": NEXT_ASSESS},
        {"max": 55, "name": "Suitable for a controlled pilot",
         "title": "Prove it on one workflow",
         "text": "You have enough in place to test managed delivery safely on one bounded process or workstream. A short, measured pilot will show what works before you commit to anything ongoing.",
         "risks": ["Scope creep if the pilot workflow isn't tightly defined", "Inconsistent processes may need documenting during the pilot", "Results are hard to judge without a baseline"],
         "actions": ["Choose one bounded process or workstream", "Capture today's baseline: volumes, turnaround and rework", "Agree success criteria before the pilot starts"],
         "service": S_PILOT,
         "next": {"label": "Start a 30-Day Pilot", "href": "contact.html?topic=pilot", "track": "pilot_cta",
                  "text": "Most pilots start with a £495 assessment to fix the scope and price. The fee is credited against the pilot if commissioned within 30 days."}},
        {"max": 75, "name": "Ready for a managed service",
         "title": "Put the work on a managed footing",
         "text": "Your processes, governance and access are mature enough for a monthly managed service with defined capacity, outputs and service levels.",
         "risks": ["Capacity agreed too loosely leads to friction later", "Governance cadence slips once the service is running", "Benefits aren't tracked, so value is hard to show"],
         "actions": ["Define monthly capacity, outputs and service levels", "Set the reporting and service-review cadence", "Start with one service and expand once it's stable"],
         "service": S_PMO,
         "next": {"label": "Discuss Your Project Portfolio", "href": "contact.html?topic=pmo", "track": "portfolio_cta",
                  "text": "A short conversation about your portfolio, then a £495 assessment to confirm capacity and price."}},
        {"max": 100, "name": "Ready for scaled operational delivery",
         "title": "Scale with control",
         "text": "You're well placed to run several workstreams through a managed service. The risk now is growing too quickly rather than not being ready.",
         "risks": ["Scaling before the first service is stable", "Single points of failure in your own team", "AI and licence costs rising without governance"],
         "actions": ["Stabilise one service, then add workstreams", "Agree a quarterly capacity plan", "Build an automation backlog with measurable targets"],
         "service": S_SCALE,
         "next": {"label": "Discuss Your Project Portfolio", "href": "contact.html?topic=pmo", "track": "portfolio_cta",
                  "text": "Talk to us about the workstreams you'd run first and how capacity would grow."}},
    ],
}

AI_QUIZ = {
    "id": "ai",
    "topic": "ai-scorecard",
    "title": "AI Readiness Scorecard",
    "dims": [
        {"id": "strategy", "name": "Strategy", "service": S_AI},
        {"id": "people", "name": "People", "service": {"name": "AI for Leaders or Copilot Skills Bootcamp", "price": "£1,450–£2,950", "href": "pricing.html#training", "what": "Practical, role-based training, starting with your leadership team."}},
        {"id": "process", "name": "Process", "service": S_DOCS},
        {"id": "data", "name": "Data and tools", "service": {"name": "AI Workflow Implementation", "price": "£5,000–£15,000", "href": "index.html#ai", "what": "One to three workflows with testing, user guidance, governance documentation and handover."}},
        {"id": "governance", "name": "Governance", "service": {"name": "AI Governance Pack", "price": "£2,500–£6,000", "href": "pricing.html#projects", "what": "Usage policy, risk register, data rules, DPIA template and an approval process."}},
    ],
    "questions": [
        {"dim": "strategy", "text": "Does your leadership team agree on what AI should achieve for the business?", "options": ["Not discussed yet", "Talked about, nothing agreed", "Some goals agreed for specific areas", "Clear goals, with owners and measures"]},
        {"dim": "strategy", "text": "Have you identified specific processes where AI could save time or money?", "options": ["No", "A few ideas", "A shortlist with rough value", "A prioritised, costed pipeline"]},
        {"dim": "people", "text": "How are your people using AI tools today?", "options": ["Not at all, or we don't know", "A few enthusiasts, on their own", "Several teams use approved tools", "Widely used, part of how we work"]},
        {"dim": "people", "text": "Have staff been trained to use AI well and safely?", "options": ["No training", "Informal tips and videos", "Some formal training", "Role-based training with ongoing support"]},
        {"dim": "process", "text": "How well documented are your core processes?", "options": ["Mostly in people's heads", "Some documents, often out of date", "Key processes documented", "Documented, owned and kept current"]},
        {"dim": "process", "text": "How much repetitive manual work do teams do?", "options": ["A lot, it's a daily burden", "Quite a bit", "Some, we've automated the worst", "Very little, most is automated"]},
        {"dim": "data", "text": "Where does your business information live?", "options": ["Scattered across email, desktops and paper", "Shared drives, hard to find things", "Mostly in Microsoft 365 or SharePoint", "Well structured, searchable, clear permissions"]},
        {"dim": "data", "text": "Which AI tools do you have access to?", "options": ["None", "Free consumer tools only", "Business licences for some (Copilot, ChatGPT, Claude)", "Business tools connected to our systems"]},
        {"dim": "governance", "text": "Do you have an AI usage policy?", "options": ["No", "Being drafted", "Yes, but few people know it", "Yes, communicated and reviewed regularly"]},
        {"dim": "governance", "text": "Do you know what company data is going into AI tools?", "options": ["No idea", "We suspect it happens", "Partly, with some controls", "Yes, with controls and monitoring"]},
    ],
    "context": CONTEXT_QS,
    "notes": CONTEXT_NOTES,
    "bands": [
        {"max": 34, "name": "Explorer", "title": "Start with clarity",
         "text": "AI is on the radar but not yet in the business. Agree where it will genuinely pay off, and put a few safe rules in place.",
         "risks": ["Staff using unapproved tools with company data", "Investment in licences before the use cases are clear", "Processes too undocumented to automate"],
         "actions": ["Agree two or three business problems AI should address", "Publish a short AI usage policy", "Document the processes you'd most like to improve"],
         "service": S_AI, "next": {"label": "Enquire about AI Operations Discovery", "href": "contact.html?topic=ai-discovery", "track": "ai_cta", "text": "A fixed-price discovery that ends with five prioritised use cases and a 90-day roadmap."}},
        {"max": 59, "name": "Experimenter", "title": "Turn pockets of use into a plan",
         "text": "People are using AI, but without much structure. Agree priorities, put governance in place and pick use cases worth scaling.",
         "risks": ["Inconsistent results across teams", "Data leakage through unapproved tools", "No measurable benefit to show leadership"],
         "actions": ["Prioritise use cases by value and risk", "Put governance and approved tools in place", "Measure a baseline before implementing"],
         "service": S_AI, "next": {"label": "Enquire about AI Operations Discovery", "href": "contact.html?topic=ai-discovery", "track": "ai_cta", "text": "Turn scattered experiments into a prioritised, governed plan."}},
        {"max": 79, "name": "Adopter", "title": "Scale what works",
         "text": "The foundations are in place. The value now comes from implementing end-to-end workflows and measuring the benefit.",
         "risks": ["Pilots that never become production workflows", "Rising consumption costs", "Workflows nobody maintains"],
         "actions": ["Pick one to three workflows to implement properly", "Agree ownership and maintenance", "Track time saved and quality"],
         "service": {"name": "AI Workflow Implementation", "price": "£5,000–£15,000", "href": "index.html#ai", "what": "One to three workflows with testing, user guidance, governance documentation and handover."},
         "next": {"label": "Enquire about AI Workflow Implementation", "href": "contact.html?topic=ai-workflow", "track": "ai_cta", "text": "We confirm a viable technical route before proposing any integration."}},
        {"max": 100, "name": "Leader", "title": "Optimise and run",
         "text": "You're ahead of most UK organisations. Get more from the tools you already pay for, and keep workflows improving.",
         "risks": ["Value plateauing after early wins", "Governance falling behind new tools", "Key-person dependency on internal champions"],
         "actions": ["Review usage and value quarterly", "Extend governance to new tools", "Build an improvement backlog"],
         "service": {"name": "AI Optimisation Review", "price": "£1,950", "href": "pricing.html#projects", "what": "Usage analysis, interviews, quick fixes and an improvement plan."},
         "next": {"label": "Enquire about an AI Optimisation Review", "href": "contact.html?topic=ai-optimisation", "track": "ai_cta", "text": "A two-week review of where your AI investment is and isn't paying back."}},
    ],
}


def quiz_data(d):
    return json.dumps(d, ensure_ascii=False).replace("</", "<\\/")


def quiz_block(d):
    return f"""        <div class="quiz" id="scorecard" data-quiz="{d['id']}">
          <script type="application/json" class="quiz-data">{quiz_data(d)}</script>
          <div class="progress" aria-hidden="true"><span></span></div>
          <div class="q-meta"><span class="q-count">Question 1</span><span class="q-dim"></span></div>
          <div class="questions"></div>
          <div class="quiz-nav">
            <button type="button" class="btn btn-line q-prev">← Back</button>
            <button type="button" class="btn btn-primary q-next" disabled>Next {ARR}</button>
          </div>
          <div class="result" tabindex="-1" aria-live="polite">
            <div class="score-wrap">
              <div class="gauge">
                <svg viewBox="0 0 200 200" width="200" height="200" aria-hidden="true">
                  <defs><linearGradient id="gG-{d['id']}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7941D"/><stop offset="1" stop-color="#EE2A24"/></linearGradient></defs>
                  <circle cx="100" cy="100" r="88" fill="none" stroke="#EDE5DA" stroke-width="14"/>
                  <circle class="r-arc" cx="100" cy="100" r="88" fill="none" stroke="url(#gG-{d['id']})" stroke-width="14" stroke-linecap="round" style="transition:stroke-dashoffset 1.2s cubic-bezier(.2,.7,.2,1)"/>
                </svg>
                <div class="num"><div><strong class="r-score">0</strong><small>out of 100</small></div></div>
              </div>
              <div>
                <span class="band r-band"></span>
                <h2 class="r-title" style="margin:6px 0 10px;font-size:clamp(1.8rem,3.4vw,2.6rem)"></h2>
                <p class="r-text muted"></p>
              </div>
            </div>
            <div class="bars r-bars"></div>
            <div class="grid g2 r-cols">
              <div class="r-box"><h3>Principal risks</h3><ul class="r-risks ticks warn"></ul></div>
              <div class="r-box"><h3>Three recommended actions</h3><ol class="r-actions"></ol></div>
            </div>
            <h3 class="r-recs-title">Most suitable service</h3>
            <div class="grid g2 r-recs"></div>
            <p class="r-context small"></p>
            <div class="rec">
              <span class="label">Your next step</span>
              <h3 class="r-next-title"></h3>
              <p class="r-next-text"></p>
              <div class="btns">
                <a class="btn btn-ember r-next" href="#">Next step</a>
                <button type="button" class="btn btn-line-light r-download">Download my result</button>
                <a class="btn btn-line-light r-email" href="#">Email my result to me</a>
                <button type="button" class="btn btn-line-light r-retake">Retake</button>
              </div>
              <div class="lead-box">
                <h4>Get the full assessment report</h4>
                <p>Leave your details and we'll send your full report, recommended service pathway and an outline pilot, with an invitation to a 30-minute consultation.</p>
                <form class="lead-form" data-email="{CONTACT_EMAIL}" data-subject="{d['title']}: full report request" data-endpoint="" data-event="scorecard_lead_submit" novalidate>
                  <input type="hidden" name="results" class="r-summary">
                  <div class="lead-fields">
                    <label class="sr-only" for="lf-name-{d['id']}">Name</label><input id="lf-name-{d['id']}" name="name" placeholder="Your name" autocomplete="name" required>
                    <label class="sr-only" for="lf-email-{d['id']}">Work email</label><input id="lf-email-{d['id']}" name="email" type="email" placeholder="Work email" autocomplete="email" required>
                    <label class="sr-only" for="lf-org-{d['id']}">Organisation</label><input id="lf-org-{d['id']}" name="organisation" placeholder="Organisation" autocomplete="organization">
                  </div>
                  <div class="btns"><button class="btn btn-ember" type="submit">Request my full report {ARR}</button></div>
                  <p class="form-mode small"></p>
                  <div class="form-status" role="status" aria-live="polite"></div>
                </form>
              </div>
            </div>
          </div>
        </div>
        <p class="note center">Your answers stay in your browser. Nothing is sent unless you request the full report.</p>"""


# ---------------------------------------------------------------- Readiness scorecard page
BUILT_FOR = [
    ("Logistics and supply chain", "Operations, customer reporting and change projects competing for the same few people."),
    ("50 to 500 employees", "Too big for informal ways of working, too lean for a full support function in every area."),
    ("3 to 15 projects, no consistent PMO", "Status lives in spreadsheets and inboxes, so slippage surfaces late."),
    ("Not enough business analysis", "Requirements depend on whoever has time, so rework is common."),
    ("Undocumented processes", "Operations that rely on what experienced people remember."),
    ("Practical AI automation", "You want working AI-assisted workflows, not another strategy deck."),
]
built_for = "\n".join(f"""          <div class="card reveal"><h3>{t}</h3><p style="margin:0">{d}</p></div>""" for t, d in BUILT_FOR)

VS = [
    ("Time to productive capacity", "Months, once notice periods and onboarding are included", "Days to weeks, then time learning your processes", "A standard pod normally mobilised in 2 to 4 weeks after contract, role confirmation, security approval and access"),
    ("Who manages the work", "You", "You", "We do, under a named UK lead"),
    ("Quality control", "Your own processes", "Depends on the individual", "SOPs, second-person checks and weekly sampling, reported to you"),
    ("If someone leaves", "Recruit again", "Start again", "Cover and continuity are our responsibility, set out in your service definition"),
    ("Flexing capacity", "Slow, and adds permanent cost", "Possible, but quality varies", "By agreement through change control"),
    ("What you pay for", "Salaries and overheads", "Hours", "Defined outputs, capacity and service levels"),
]
vs_rows = "\n".join(f"""              <tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td class="us">{d}</td></tr>""" for a, b, c, d in VS)

SC_FAQ = [FAQ[0], FAQ[1], FAQ[5], FAQ[4], FAQ[6], FAQ[13]]
sc_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in SC_FAQ)

SC_SAMPLE = [("Process maturity", 33), ("Documentation quality", 33), ("Project governance", 33), ("Technology readiness", 67), ("Leadership commitment", 67)]
sc_sample = "\n".join(f"""              <div class="bar-row"><span>{n}</span><div class="track"><div class="fill" style="width:{v}%"></div></div><span class="v">{v}%</span></div>""" for n, v in SC_SAMPLE)

scorecard = f"""    <section class="page-hero sc-hero">
      <div class="container hero-grid">
        <div>
          {label("Free readiness scorecard · 5 minutes · instant result")}
          <h1>Find out what you could hand over, <em class="ember">and how safely.</em></h1>
          <p class="lead">Thirteen questions for UK organisations considering managed delivery. See your score straight away, with a plain-English interpretation, principal risks, three recommended actions and the most suitable next step.</p>
          <div class="hero-actions">
            {btn("Start the scorecard", "#scorecard", "btn-ember")}
            {btn("Book a Managed Operations Assessment", ASSESS_HREF, "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">UK-managed. Lahore-delivered. AI-enabled.</p>
        </div>
        <div class="sc-art">
          {horizon(["UK-LED", "MANAGED", "LAHORE", "AI-ENABLED"])}
        <div class="sample-card reveal" aria-label="Example of a scorecard result">
          <div class="sample-top"><span class="label" style="margin:0">Example result</span><span class="sample-score"><strong>48</strong>/100</span></div>
          <p class="band" style="margin:8px 0 0">Suitable for a controlled pilot</p>
          <div class="bars" style="margin:16px 0">
{sc_sample}
          </div>
          <div class="sample-foot"><span class="small muted">Recommended next step</span><strong>30-Day Managed Delivery Pilot</strong><span class="small muted">£1,500–£2,500, after a £495 assessment</span></div>
        </div>
        </div>
      </div>
    </section>

    <div class="trust">
      <div class="container trust-grid">
        <div><strong>UK company</strong><span>Contract and accountability with Bespoke Vista Ltd</span></div>
        <div><strong>Senior UK lead</strong><span>On every service, from scoping to service reviews</span></div>
        <div><strong>Lahore delivery centre</strong><span>Office-based, managed delivery team</span></div>
        <div><strong>AI-enabled</strong><span>Controlled use of Microsoft 365, Copilot and Power Automate</span></div>
      </div>
    </div>

    <section class="sec sec-sand" id="take-the-scorecard">
      <div class="container">
        <div class="head solo center" style="margin-left:auto;margin-right:auto">
          {label("The scorecard")}
          <h2>Thirteen questions. <em class="ember">An honest answer.</em></h2>
          <p class="muted">Covers process maturity, documentation, internal capacity, project governance, management reporting, technology, AI, data sensitivity, outsourcing readiness and leadership commitment. No email needed to see your result.</p>
        </div>
{quiz_block(OPS_QUIZ)}
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Who it's for")}<h2>Built for organisations where the work has <em class="ember">outgrown the team.</em></h2></div>
          <p>Most useful for UK SMEs and mid-market organisations with 50 to 500 people.</p>
        </div>
        <div class="grid g3">
{built_for}
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container">
        <div class="head">
          <div>{label("Why a managed service")}<h2>Faster than recruiting. <em class="ember">More control</em> than contractors.</h2></div>
          <p>The comparison that matters isn't price per hour. It's how quickly you get reliable capacity, who is responsible for quality, and what happens when things change.</p>
        </div>
        <div class="table-wrap table-light reveal">
          <table class="compare compare-light">
            <thead><tr><th scope="col"><span class="sr-only">Factor</span></th><th scope="col">Recruiting in the UK</th><th scope="col">Freelancers or agency staff</th><th scope="col" class="us">Bespoke Vista managed service</th></tr></thead>
            <tbody>
{vs_rows}
            </tbody>
          </table>
        </div>
        <p class="note">A general comparison of typical options, not of any specific provider.</p>
      </div>
    </section>

    <section class="sec" id="route">
      <div class="container">
        <div class="head">
          <div>{label("How to start")}<h2>Assess. Pilot. <em class="ember">Then decide.</em></h2></div>
          <p>A low-risk route from first conversation to managed service. You see the work running on your own processes before committing to a monthly service.</p>
        </div>
        <div class="grid g2">
{offer_card(ASSESSMENT, "Book a Managed Operations Assessment", ASSESS_HREF, "Start here", "featured")}
{offer_card(PILOT, "Start a 30-Day Pilot", "contact.html?topic=pilot")}
        </div>
        <p class="note">Managed services then start from £1,950 a month with a three-month initial term. <a href="pricing.html">See all prices and package boundaries →</a></p>
      </div>
    </section>

    <section class="sec sec-white" id="faq">
      <div class="container split">
        <div>{label("Straight answers")}<h2>Questions UK buyers ask.</h2><p class="muted"><a href="index.html#faq">All 18 FAQs →</a></p></div>
        <div class="faq">
{sc_faq}
        </div>
      </div>
    </section>

{cta()}"""

page("scorecard.html", "Free Readiness Scorecard",
     "Free 5-minute readiness scorecard for UK SMEs and mid-market organisations. Find out what you could hand over to a UK-managed, Lahore-delivered service, the risks, and your next step.",
     scorecard, full_title="Free Managed Delivery Readiness Scorecard | Bespoke Vista",
     schema=[{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in SC_FAQ]}])

ai_scorecard = f"""    <section class="page-hero">
      <div class="container">
        {label("Free · 3 minutes · no sign-up")}
        <h1>How ready is your business <em class="ember">for AI?</em></h1>
        <p class="lead">Ten questions across strategy, people, process, data and governance. See your score, risks, recommended actions and the most suitable next step.</p>
      </div>
    </section>

    <section class="sec sec-sand">
      <div class="container">
{quiz_block(AI_QUIZ)}
      </div>
    </section>

{cta("Considering managed delivery as well?", "The Free Readiness Scorecard shows whether your processes, governance and data are ready for a managed service.", ("Take the Free Readiness Scorecard", "scorecard.html"), ("Book a Managed Operations Assessment", ASSESS_HREF))}"""

page("ai-scorecard.html", "AI Readiness Scorecard",
     "Free AI Readiness Scorecard: ten questions, three minutes. See how ready your business is for AI and what to do next.",
     ai_scorecard)


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
          <p>Bespoke Vista has office facilities and teams in Lahore, Pakistan, and where office-based delivery teams for analysis, PMO, administration, AI operations, customer support and shared services can be established. A standard delivery pod can normally be mobilised within two to four weeks of contract, subject to role confirmation, security approval and access provisioning.</p>
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

{cta("Have a challenge like these?", "Tell us about it. We'll suggest a practical first step with a fixed price.", ("Book a 30-minute call", "contact.html?topic=consultation"), ("See services", "services.html"))}"""

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
          <p>Want a quick read on where you stand? <a href="ai-scorecard.html">Take the free AI Readiness Scorecard.</a></p>"""),
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
    ("assessment", "Book a Managed Operations Assessment (£495)"),
    ("pilot", "Start a 30-Day Pilot"),
    ("pmo", "PMO-in-a-Box / discuss our project portfolio"),
    ("ba", "Managed Business Analysis"),
    ("documentation", "Documentation Factory"),
    ("ai-discovery", "AI Operations Discovery"),
    ("ai-workflow", "AI Workflow Implementation"),
    ("scorecard", "Readiness Scorecard results"),
    ("ai-scorecard", "AI Scorecard results"),
    ("consultation", "General consultation"),
    ("managed", "Other managed services"),
    ("intelligence", "Executive AI Intelligence"),
    ("advisory", "Bespoke Vista AI Advisory"),
    ("fractional", "Fractional Business Architect"),
    ("health-check", "Transformation Health Check"),
    ("tom", "Target Operating Model Design"),
    ("governance", "AI Governance Pack"),
    ("copilot", "Microsoft Copilot Adoption Programme"),
    ("ai-optimisation", "AI Optimisation Review"),
    ("cyber-ba", "Cyber Security Business Analysis"),
    ("training", "Training and workshops"),
    ("wellbeing", "Calm Under Pressure workshop"),
    ("dojoos", "DojoOS founding list"),
    ("other", "Something else"),
]
topic_opts = "\n".join(f'                <option value="{v}">{l}</option>' for v, l in TOPICS)

booking_block = (f'<li><strong>Book directly</strong><a href="{BOOKING_URL}" target="_blank" rel="noopener" data-track="booking_start">Choose a time in our booking calendar →</a></li>'
                 if BOOKING_URL else "<!-- CONFIGURE: set BOOKING_URL in build.py to show a Microsoft Bookings link here. -->")

contact = f"""    <section class="page-hero">
      <div class="container">
        {label("Contact")}
        <h1>Book a Managed Operations Assessment, <em class="ember">or ask us anything.</em></h1>
        <p class="lead">Tell us about your organisation and the work you'd like help with. We'll reply within one working day to arrange the next step.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container contact-grid">
        <div class="reveal">
          <h2>What happens next</h2>
          <ol class="next-steps">
            <li>We reply within one working day to confirm a time.</li>
            <li>For an assessment, we send a short pre-workshop questionnaire and a £495 invoice (ex VAT).</li>
            <li>We run the 60-minute workshop and send written findings with a recommended pilot.</li>
          </ol>
          <ul class="contact-ways">
            {booking_block}
            <li><strong>Email</strong><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
            <li><strong>Where we are</strong>United Kingdom, with a delivery centre in Lahore, Pakistan</li>
            <li><strong>Right now</strong>{CLOCKS}</li>
            <li><strong>Not ready to talk yet?</strong><a href="scorecard.html" data-track="scorecard_cta">Take the Free Readiness Scorecard →</a></li>
          </ul>
        </div>
        <form class="form reveal" id="contact-form" data-email="{CONTACT_EMAIL}" data-endpoint="" data-event="contact_submit" novalidate>
          <div class="form-row">
            <div class="field"><label for="name">Name *</label><input id="name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="organisation">Organisation</label><input id="organisation" name="organisation" type="text" autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="email">Work email *</label><input id="email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="topic">What can we help with?</label>
              <select id="topic" name="topic">
{topic_opts}
              </select>
            </div>
            <div class="field">
              <label for="size">Organisation size</label>
              <select id="size" name="size"><option value="">Select</option><option>Fewer than 50</option><option>50 to 249</option><option>250 to 500</option><option>More than 500</option></select>
            </div>
          </div>
          <div class="field"><label for="message">Your message *</label><textarea id="message" name="message" required placeholder="The work you'd like help with, roughly how many projects or processes are involved, and any timescales."></textarea></div>
          <button class="btn btn-primary" type="submit">Send enquiry {ARR}</button>
          <p class="form-mode small"></p>
          <p class="form-note">We use your details only to respond to your enquiry. {owner("link to your privacy notice here once published.", inline=True)}</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </section>"""

page("contact.html", "Contact",
     "Book a £495 Managed Operations Assessment or contact Bespoke Vista about managed PMO, business analysis, process documentation or AI workflows.",
     contact)

# ============================================================== SAMPLES
ILL = '<p class="ill-banner" role="note"><strong>Illustrative example, not an actual client deliverable.</strong> Names, dates and figures are fictitious.</p>'


def sample(sid, title, intro, body, files):
    return f"""        <article class="sample-doc reveal" id="{sid}">
          <div class="sample-doc-head">
            <span class="label">Sample deliverable</span>
            <h2>{title}</h2>
            <p class="muted">{intro}</p>
            {ILL}
          </div>
          <div class="sample-body">{body}</div>
          {owner(f"downloadable version of this sample ({files}), clearly marked as illustrative.")}
        </article>"""


def table(head, rows, cls="tbl"):
    h = "".join(f"<th scope=\"col\">{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap table-light"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'


def rag(c):
    return f'<span class="rag rag-{c[0].lower()}">{c}</span>'


S1 = ('<div class="kpis"><div><strong>9</strong><span>Active projects</span></div><div><strong>6</strong><span>On track</span></div><div><strong>2</strong><span>At risk</span></div><div><strong>1</strong><span>Off track</span></div></div>'
      + table(["Project", "Status", "Next milestone", "Due", "Decision needed"], [
          ["Warehouse system upgrade", rag("Amber"), "User acceptance testing complete", "14 Mar", "Approve extra test cycle"],
          ["Customer A onboarding", rag("Green"), "Go-live", "28 Mar", "None"],
          ["Transport planning tool", rag("Red"), "Supplier contract signed", "07 Mar", "Choose supplier option B or C"],
          ["Returns process redesign", rag("Green"), "Future-state process approved", "21 Mar", "None"],
          ["Customer B onboarding", rag("Amber"), "Data migration test", "18 Mar", "Confirm data owner"]]))
S2 = table(["ID", "Type", "Description", "Owner", "Rating", "Action", "Due"], [
    ["R-014", "Risk", "Key warehouse SME unavailable during testing", "Ops Manager", rag("Amber"), "Agree back-fill for two weeks", "10 Mar"],
    ["A-006", "Assumption", "Supplier test environment ready by 1 March", "IT Lead", rag("Green"), "Confirm in weekly call", "01 Mar"],
    ["I-009", "Issue", "Label printer integration failing in test", "Supplier PM", rag("Red"), "Fix and retest", "05 Mar"],
    ["D-003", "Dependency", "Customer A data extract required for onboarding", "Account Manager", rag("Amber"), "Chase customer contact", "08 Mar"]])
S3 = ('<div class="doc-cols"><div><h3>Summary</h3><p>All scheduled outputs were delivered. One response-time target was missed during month-end; root cause and fix below.</p>'
      '<h3>Outputs delivered</h3><ul><li>Weekly portfolio dashboard: 4 of 4</li><li>RAID reviews: 9 projects, weekly</li><li>Governance packs: 2 of 2</li></ul></div>'
      '<div>' + table(["Service level", "Target", "Actual"], [["Reports on time", "100%", "100%"], ["Response within 4 working hours", "95%", "92%"], ["Rework after review", "Under 5%", "3%"]]) +
      '<h3>Next month</h3><ul><li>Add benefits register for two projects</li><li>Automate RAID reminders in Power Automate</li></ul></div></div>')
S4 = """<svg class="swim" viewBox="0 0 760 270" role="img" aria-label="Illustrative swim-lane process map for goods receipt">
  <g font-family="Inter, sans-serif" font-size="12" fill="#0B1120">
    <rect x="0" y="0" width="760" height="90" fill="#FFFDF9" stroke="#E2D9CC"/><rect x="0" y="90" width="760" height="90" fill="#F7F3EE" stroke="#E2D9CC"/><rect x="0" y="180" width="760" height="90" fill="#FFFDF9" stroke="#E2D9CC"/>
    <text x="12" y="50" font-weight="600">Supplier</text><text x="12" y="140" font-weight="600">Goods-in</text><text x="12" y="230" font-weight="600">Inventory</text>
    <rect x="110" y="28" width="120" height="36" rx="8" fill="#fff" stroke="#0B1120"/><text x="170" y="51" text-anchor="middle">Send ASN</text>
    <rect x="260" y="118" width="120" height="36" rx="8" fill="#fff" stroke="#0B1120"/><text x="320" y="141" text-anchor="middle">Receive and check</text>
    <polygon points="470,116 520,136 470,156 420,136" fill="#FFF1E6" stroke="#C2410C"/><text x="470" y="140" text-anchor="middle" font-size="11">Matches?</text>
    <rect x="560" y="208" width="140" height="36" rx="8" fill="#fff" stroke="#0B1120"/><text x="630" y="231" text-anchor="middle">Put away and update</text>
    <rect x="560" y="28" width="140" height="36" rx="8" fill="#fff" stroke="#0B1120"/><text x="630" y="51" text-anchor="middle">Resolve discrepancy</text>
    <g stroke="#0B1120" fill="none"><path d="M230 46 H245 V136 H260"/><path d="M380 136 H420"/><path d="M520 136 H540 V226 H560"/><path d="M470 116 V46 H560"/></g>
    <text x="545" y="190" font-size="11" fill="#C2410C">Yes</text><text x="478" y="80" font-size="11" fill="#C2410C">No</text>
    <circle cx="320" cy="108" r="9" fill="#C2410C"/><text x="320" y="112" text-anchor="middle" fill="#fff" font-size="10">C1</text>
  </g>
</svg><p class="small muted">C1 = control point: quantity and condition check recorded before stock is accepted.</p>"""
S5 = ('<div class="sop">' + table(["SOP ID", "Title", "Owner", "Version", "Review date"], [["SOP-GI-002", "Goods receipt and discrepancy handling", "Warehouse Manager", "1.0 (approved)", "Annually"]]) +
      '<h3>1. Purpose</h3><p>To receive inbound goods accurately and resolve discrepancies within one working day.</p>'
      '<h3>2. Scope</h3><p>All inbound deliveries at the main site. Excludes returns (see SOP-RT-001).</p>'
      '<h3>3. Procedure</h3><ol><li>Check the advance shipping notice (ASN) against the purchase order.</li><li>Count and inspect goods; record results in the warehouse system (control point C1).</li><li>If quantities match, put away and confirm the location.</li><li>If not, raise a discrepancy and notify the buyer within two hours.</li></ol>'
      '<h3>4. Controls and KPIs</h3><ul><li>C1: receipt check recorded before put-away</li><li>KPI: dock-to-stock time; discrepancy resolution within one working day</li></ul></div>')
S6 = table(["Req ID", "Requirement", "Source", "User story", "Test case", "Status"], [
    ["BR-01", "Record carrier and seal number at receipt", "Workshop 2", "US-114", "TC-201", rag("Green") + " Passed"],
    ["BR-02", "Alert buyer when discrepancy exceeds 2%", "Ops interview", "US-118", "TC-205", rag("Amber") + " In test"],
    ["BR-03", "Daily discrepancy report by supplier", "Finance", "US-121", "TC-210", "Not started"]])
S7 = table(["Use case", "Value", "Effort", "Risk", "Recommendation"], [
    ["Draft SOPs from recorded walkthroughs", "High", "Low", "Low", "Pilot in month 1"],
    ["Summarise weekly project updates into the dashboard", "High", "Medium", "Low", "Pilot in month 2"],
    ["Classify inbound customer emails", "Medium", "Medium", "Medium", "Design governance first"],
    ["Extract data from supplier invoices", "Medium", "High", "Medium", "Assess after data review"],
    ["Search the operations knowledge base with Copilot", "High", "Medium", "Medium", "Fix permissions, then pilot"]])
S8 = table(["Week", "Activities", "Measures", "Decision point"], [
    ["1", "Access, onboarding, process walkthrough, SOP drafted", "Baseline captured", "SOP approved by client"],
    ["2", "Team delivers with daily UK review", "Accuracy, turnaround", "Weekly progress review"],
    ["3", "Normal operation with second-person checks", "Accuracy, turnaround, rework", "Weekly progress review"],
    ["4", "Steady state; results report and business case", "Against baseline", "Go / no-go for managed service"]])

samples_body = "\n".join([
    sample("pmo-dashboard", "PMO dashboard", "The one-page portfolio view produced each week (Managed) or month (Foundation) in PMO-in-a-Box.", S1, "Excel or Power BI file"),
    sample("raid", "RAID register", "Risks, assumptions, issues and dependencies, with owners, ratings and actions.", S2, "Excel template"),
    sample("service-report", "Monthly service report", "How we report outputs and service-level performance at each monthly service review.", S3, "PDF"),
    sample("process-map", "Process map", "A swim-lane process map from the Documentation Factory, with control points marked.", S4, "Visio or PDF"),
    sample("sop", "Standard operating procedure", "An extract from an SOP in our controlled template. A standard SOP covers one process, up to five pages.", S5, "Word or PDF"),
    sample("rtm", "Requirements traceability matrix", "From Managed Business Analysis: each requirement traced to its source, user story, test and status.", S6, "Excel template"),
    sample("ai-report", "AI readiness report", "The prioritised use-case table from an AI Operations Discovery.", S7, "PDF"),
    sample("pilot-plan", "30-day pilot plan", "How a 30-Day Managed Delivery Pilot is structured, measured and decided.", S8, "PDF"),
])

samples = f"""    <section class="page-hero">
      <div class="container">
        {label("Sample deliverables")}
        <h1>See what you <em class="ember">will receive.</em></h1>
        <p class="lead">Examples of the documents and reports our services produce. All examples on this page are illustrative: they are not actual client deliverables, and names, dates and figures are fictitious.</p>
      </div>
    </section>
{subnav([(s[0], s[1]) for s in SAMPLES])}
    <section class="sec">
      <div class="container">
{samples_body}
      </div>
    </section>

{cta()}"""

page("samples.html", "Sample Deliverables",
     "Illustrative examples of Bespoke Vista deliverables: PMO dashboard, RAID register, service report, process map, SOP, traceability matrix, AI readiness report and 30-day pilot plan.",
     samples)
