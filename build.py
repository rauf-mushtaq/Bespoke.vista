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
import re
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
SHOW_OWNER_PLACEHOLDERS = False  # switch to True to see every missing item marked on the pages

# TODO: confirm VAT registration. If False, "ex VAT" wording becomes "no VAT charged".
VAT_REGISTERED = True
# Founding-client programme: reduced terms for the first managed-service clients in return for
# a published case study and reference. Set to 0 to remove it from the site.
FOUNDING_PLACES = 3
PRIVACY_UPDATED = "21 November 2026"

ASSESS_HREF = BOOKING_URL or "contact.html?topic=blueprint"
# TODO: optional separate Microsoft Bookings page for transformation discovery calls (logistics page).
DISCOVERY_BOOKING_URL = ""
DISCOVERY_HREF = DISCOVERY_BOOKING_URL or "contact.html?topic=discovery-call"

# Virtual Consultancy. Leave blank to use the request form on virtual-consultancy.html.
# Set to a Microsoft Bookings page or a Stripe Payment Link once scope checks and terms are in place.
TRIAL_BOOKING_URL = ""
SUBSCRIBE_URLS = {"Essentials": "", "Professional": "", "Partner": ""}
TRIAL_HREF = TRIAL_BOOKING_URL or "virtual-consultancy.html?plan=trial#book"

# Instant checkout. Paste a Stripe Payment Link (or similar) against any plan to turn its button into
# "Subscribe" / "Buy now". Plans left blank keep the request form, so nothing appears payable until it is.
PAY_LINKS = {
    "Executive AI Intelligence: Briefing": "", "Executive AI Intelligence: Professional": "", "Executive AI Intelligence: Boardroom": "",
    "Member Portal: Portal": "", "Member Portal: Portal + Website": "", "Member Portal: Portal + Website + Content": "",
    "Content Creation: Starter": "", "Content Creation: Growth": "", "Content Creation: Leader": "",
    "Website Care": "",
}
EMPTYHANDS_URL = "https://emptyhands.co.uk/"
EMPTYHANDS_APP_URL = "https://emptyhands.co.uk/our-app.html"

# Older offers outside the six core services are hidden from public pages.
# Switch to True to show the Executive AI Intelligence briefing on Insights, its contact topics,
# and the "further managed services" list on the Delivery Model page.
SHOW_EXTRA_OFFERS = False

# The core proposition, used across the site.
USP = "We lead the change. Our team keeps it running."
ARR = '<span class="arr" aria-hidden="true">→</span>'

NAV = [
    ("services.html", "Services"),
    ("pricing.html", "Pricing"),
    ("websites-apps.html", "Websites &amp; Apps"),
    ("about.html", "About"),
]
LOGO = ('<img src="assets/img/logo.png" srcset="assets/img/logo.png 1x, assets/img/logo@2x.png 2x" '
        'alt="Bespoke Vista" width="55" height="38">')
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
    if href == DISCOVERY_HREF:
        return "discovery_call_start" if DISCOVERY_BOOKING_URL else "discovery_enquiry_start"
    if href == ASSESS_HREF:
        return "booking_start" if BOOKING_URL else "assessment_enquiry_start"
    if href == TRIAL_HREF or "plan=trial" in href:
        return "virtual_trial_start"
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
        <span><span class="brand-name">{SITE}</span></span>
      </a>
      <ul class="nav-links" id="nav-links">
{items}
        <li class="drawer-only"><a href="scorecard.html"{cur("scorecard.html")} data-track="scorecard_cta">Free Readiness Scorecard</a></li>
        <li class="drawer-only drawer-cta"><a class="btn btn-ember" href="{DISCOVERY_HREF}" data-track="{track_for(DISCOVERY_HREF)}">Book a Discovery Call</a></li>
      </ul>
      <div class="nav-actions">
        <a class="nav-quiet" href="scorecard.html"{cur("scorecard.html")} data-track="scorecard_cta">Free Scorecard</a>
        <a class="btn btn-primary btn-sm" href="{DISCOVERY_HREF}" data-track="{track_for(DISCOVERY_HREF)}">Book a Discovery Call</a>
      </div>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Menu
      </button>
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
          <p><strong style="color:var(--paper)">{USP}</strong> Senior UK transformation leadership, with a managed delivery team, under one UK contract.</p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="services.html#pods">Managed Delivery Pods</a></li>
            <li><a href="services.html#sprints">Specialist Sprints</a></li>
            <li><a href="services.html#fractional">Fractional Operations Lead</a></li>
            <li><a href="pmo-in-a-box.html">PMO-in-a-Box</a></li>
            <li><a href="logistics.html">For logistics businesses</a></li>
            <li><a href="virtual-consultancy.html">Virtual Consultancy</a></li>
            <li><a href="websites-apps.html">Websites, apps and content</a></li>
          </ul>
        </div>
        <div>
          <h4>Start here</h4>
          <ul>
            <li><a href="scorecard.html">Free Readiness Scorecard</a></li>
            <li><a href="services.html#audit">Cost-Leakage Audit</a></li>
            <li><a href="services.html#blueprint">Offshoring Readiness Blueprint</a></li>
            <li><a href="virtual-consultancy.html#trial">Two-Week Work Package Trial</a></li>
            <li><a href="samples.html">Sample deliverables</a></li>
            <li><a href="pricing.html">Pricing and terms</a></li>
          </ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="about.html">About</a></li>
            <li><a href="managed-teams.html">Delivery model</a></li>
            <li><a href="case-studies.html">Experience</a></li>
            <li><a href="insights.html">Insights</a></li>
            <li><a href="ai-scorecard.html">AI Readiness Scorecard</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="privacy.html">Privacy notice</a></li>
            {'<li><button type="button" class="linklike" data-consent-open>Cookie settings</button></li>' if (GA4_ID or CLARITY_ID) else ''}
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
    """Analytics load only after the visitor accepts cookies (see the consent banner in main.js)."""
    if not (GA4_ID or CLARITY_ID):
        return ""
    return f"  <script>window.BV_ANALYTICS={json.dumps({'ga4': GA4_ID, 'clarity': CLARITY_ID})};</script>\n"


CONSENT_BANNER = """  <div class="consent" role="dialog" aria-live="polite" aria-label="Cookie preferences" hidden>
    <p>We'd like to use analytics cookies (Google Analytics and Microsoft Clarity) to understand how the site is used. They are only set if you accept. <a href="privacy.html#cookies">Privacy notice</a></p>
    <div class="consent-btns"><button type="button" class="btn btn-primary btn-sm" data-consent="accept">Accept analytics</button><button type="button" class="btn btn-line btn-sm" data-consent="reject">Reject</button></div>
  </div>"""

HONEYPOT = ('<div class="hp" aria-hidden="true"><label>Leave this field empty'
            '<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>')


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
    body = body.replace(" novalidate>", " novalidate>" + HONEYPOT)
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
{'' if filename == 'contact.html' else f'  <a class="sticky-cta" href="{DISCOVERY_HREF}" data-track="{track_for(DISCOVERY_HREF)}">Book a Discovery Call {ARR}</a>'}
{CONSENT_BANNER if (GA4_ID or CLARITY_ID) else ''}
  <script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    if not VAT_REGISTERED:
        for a, b in [("All prices exclude VAT.", "Bespoke Vista is not VAT-registered, so no VAT is charged."),
                     ("All prices are shown excluding VAT.", "No VAT is charged."),
                     ("exclude VAT", "carry no VAT"), ("excluding VAT", "with no VAT"),
                     (", ex VAT", ", no VAT charged"), (" · ex VAT", " · no VAT charged"), ("ex VAT", "no VAT charged"),
                     ("Price excludes VAT", "No VAT charged")]:
            html = html.replace(a, b)
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


def cta(title="Tell us what needs to change.",
        text="A free 20-minute discovery call with a senior consultant. We'll talk through your priorities and suggest the right first step: a Cost-Leakage Audit, an Offshoring Readiness Blueprint, a sprint, or a referral elsewhere if we're not the right fit.",
        primary=("Book a Discovery Call", DISCOVERY_HREF),
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
       ["Everything in Professional", "Up to 5 team seats", "Quarterly 30-minute 1:1 with a senior consultant", "Board-ready AI update slides each quarter"])], 1),
    ("advisory", "Bespoke Vista AI Advisory", "For SMEs and mid-market firms adopting AI",
     "A standing senior AI adviser who keeps your AI plans on track, safe and paying back.",
     [("Starter", "Light-touch guidance as you begin.", 495,
       ["2 hours of advisory a month", "Monthly AI opportunities and risks review", "Email support, 2-working-day response", "Policy and governance templates"]),
      ("Growth", "Structured adoption across teams.", 995,
       ["5 hours of advisory a month", "Quarterly AI roadmap refresh", "AI usage policy and governance set-up", "One team workshop each quarter", "Next-working-day response"]),
      ("Partner", "An AI lead without the hire.", 1995,
       ["10 hours of advisory a month", "Monthly AI steering meeting", "Use-case pipeline managed for you", "Vendor and licence reviews", "Same-day response"])], 1),
]

# The three primary managed services. Tier tuple: (name, short description, price, [inclusions], one-line summary)
PMO = ("pmo", "PMO-in-a-Box", "For organisations running 3 to 15 projects without a consistent PMO",
       "Governance, RAID and reporting across your portfolio, run as a managed service: the audit trail ISO 27001, Cyber Essentials Plus and client vendor audits ask for, and the clean reporting investors and acquirers expect. It supports your project managers; it doesn't take over their accountability.",
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
      "Requirements, process design and defect analysis to an agreed standard and capacity each month, so system rollouts and stabilisation don't wait for analysts you can't hire. Senior UK quality review. You buy outputs, not timesheets.",
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
        "Fixed-price, auditable processes: maps, SOPs, owners and controls in a controlled library. The evidence auditors, enterprise clients and due-diligence teams ask for, and the knowledge that stops living in a few people's heads.",
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

PRIMARY = [PMO, DOCS, BA]  # lead with PMO and documentation (easiest to buy, lowest data risk)

SOP_DEFINITION = ["One defined process", "Up to five pages", "Up to two stakeholder interviews", "One agreed process map",
                  "Review cycles as stated in the package (a maximum of two per SOP)", "One final approved document"]

ASSESSMENT = ("Offshoring Readiness Blueprint", "£2,950", "fixed price · 3 weeks · ex VAT",
              ["Role-by-role feasibility, comparing in-house and managed-pod costs", "SOPs for the work to be handed over",
               "KPI scorecards and quality-assurance checklists", "Data security, compliance and hand-off governance playbook",
               "Recommended pod size, service levels and onboarding plan"],
              "The fee is credited in full against your first pod month if you proceed within 30 days.")
PILOT = ("60-Day Pod Onboarding", "From £1,950/month", "monthly pod fee · ex VAT",
         ["One clearly defined process or workstream to start", "Named delivery lead and senior UK lead", "Agreed inputs, outputs and service levels",
          "Baseline measurements", "Weekly progress review", "Day-60 review and results report"],
         "After 60 days the pod continues month to month on 30 days' notice, or stops.")
AI_WORKFLOW = ("AI Workflow Implementation", "£5,000–£15,000", "fixed price per scope · ex VAT",
               ["One to three defined workflows", "Microsoft Copilot, SharePoint, Power Automate, Claude or ChatGPT integration where appropriate",
                "Testing", "User guidance", "Governance documentation", "Handover"],
               "We only propose an integration once we have confirmed a viable technical route in your environment. Software licences and AI consumption are charged separately.")

# Virtual Consultancy: a two-week trial on one work package, then a monthly subscription.
VC_TRIAL = ("Two-Week Work Package Trial", "£950", "fixed price · ex VAT",
            ["60-minute virtual kick-off with your senior consultant", "Work-package plan: scope, milestones, owners and dates",
             "RAID and action log set up in your Microsoft 365", "Actions followed up with your team for two weeks",
             "Two 30-minute weekly check-ins", "Two weekly status reports", "End-of-trial review: continue, change or stop"],
            "The £950 is credited in full against your first month if you subscribe within 30 days of the trial ending.")
VIRTUAL = ("virtual", "Virtual Consultancy", "For leaders with more work packages than people to run them",
           "A senior UK consultant and a named delivery coordinator, working with you online each month to plan, track and report on defined work packages.",
           [("Essentials", "One work package, kept moving.", "£1,450",
             ["1 active work package", "Up to 4 hours a month of senior consultant time", "Up to 3 coordinator days a month",
              "Fortnightly 30-minute check-in", "RAID and action log maintained", "Fortnightly status report",
              "Shared Teams channel, next-working-day response"], "1 work package · 4 senior hours"),
            ("Professional", "Several work packages, one rhythm.", "£2,950",
             ["Up to 3 active work packages", "Up to 8 hours a month of senior consultant time", "Up to 6 coordinator days a month",
              "Weekly 30-minute check-in", "Weekly status report and a monthly leadership summary",
              "One governance meeting attended each month", "Plans, briefs and process notes drafted for you",
              "Same-working-day response (UK hours)"], "3 work packages · 8 senior hours"),
            ("Partner", "A virtual change office.", "£5,450",
             ["Up to 6 active work packages", "Up to 16 hours a month of senior consultant time", "Up to 12 coordinator days a month",
              "Weekly check-in and fortnightly steering", "Monthly leadership reporting pack", "Dependency and benefits tracking",
              "Quarterly priorities review", "Same-working-day response (UK hours)"], "6 work packages · 16 senior hours")], 1)



def vc_cta(tier):
    """CTA for a Virtual Consultancy plan: a payment/subscription link if configured, else the request form."""
    url = SUBSCRIBE_URLS.get(tier)
    return ((f"Subscribe to {tier}", url, "virtual_subscribe_start") if url
            else (f"Request {tier}", f"virtual-consultancy.html?plan={tier.lower()}#book", "virtual_subscribe_start"))


# Shared commercial terms
TERMS = [
    ("Prices", "All prices exclude VAT."),
    ("Initial term", "Delivery pods: a 60-day onboarding period, then month to month. Fractional support and Virtual Consultancy: one-month minimum. Specialist sprints and diagnostics are fixed-scope."),
    ("Payment", "Monthly in advance for pods and fractional support. Fixed-price work is invoiced as set out in the proposal."),
    ("Notice", "30 days' notice after the onboarding period or minimum term. No long lock-ins."),
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


# Build: websites, apps and content. The Member Portal lists only features running today in the
# EmptyHands Portal (emptyhands.co.uk/our-app.html). Add features here only once they are live.
PORTAL = ("portal", "Member Portal", "For martial arts schools, studios, clubs, tutors and coaches",
          "The member app we built for EmptyHands, set up with your name, classes and fees. Members install it on their phone; you run notices, homework and fees from one place.",
          [("Portal", "The app on its own.", "£99",
            ["Up to 100 members", "Class calendar with a countdown to the next class", "Notices, group chat and private messages",
             "Homework and training journal", "Fees by card or PayPal, with payment history", "Installs on Android and iPhone home screens",
             "New members join with your approval"]),
           ("Portal + Website", "Your app and website, looked after.", "£179",
            ["Everything in Portal", "Up to 300 members", "A website like emptyhands.co.uk, hosted and maintained",
             "Timetable, fees and contact pages kept up to date", "Up to 2 hours of changes a month"]),
           ("Portal + Website + Content", "Your online presence, run for you.", "£299",
            ["Everything in Portal + Website", "4 social posts a month, written and designed", "1 news article or newsletter a month",
             "Monthly content plan agreed with you", "Nothing published without your approval"])], 1)
PORTAL_SETUP = "One-off set-up from £495: your branding, classes, fees and calendar, member invitations and a launch guide. Card and PayPal charges are set by those providers and paid by you."

WEBSITE = ("Business Website", "From £1,495", "fixed price · ex VAT",
           ["Up to 8 pages, designed for phones first", "Copy written with you, in plain English", "Search basics: titles, descriptions, structured data",
            "Contact, booking and WhatsApp links", "Privacy notice and cookie consent where needed", "Hosting and domain set-up", "Two review rounds"],
           "Typically 3 to 4 weeks. Online shops and custom apps are quoted separately.")
WEBSITE_CARE = ("Website Care", "£49", "per month · ex VAT",
                ["Hosting and security updates", "Up to 1 hour of changes a month", "Monthly check of links, forms and speed", "Next-working-day response"],
                "Cancel with 30 days' notice. Included in the Portal + Website plans.")

CONTENT = ("content", "Content Creation", "For businesses and founders who need to show up consistently online",
           "Social posts, articles and newsletters planned, written and designed for you each month. AI-assisted drafting, always edited by a person and approved by you.",
           [("Starter", "Show up every week.", "£295",
             ["8 social posts a month, written and designed", "1 article or newsletter a month", "Monthly content calendar",
              "One round of edits", "Nothing published without your approval"]),
            ("Growth", "A steady, recognisable voice.", "£595",
             ["16 social posts a month", "2 articles a month", "Monthly email newsletter", "Scheduled to your channels",
              "Monthly performance summary"]),
            ("Leader", "Founder-led thought leadership.", "£995",
             ["Everything in Growth", "8 LinkedIn posts a month in the founder's voice", "2 thought-leadership articles a month",
              "Quarterly content strategy session", "Campaign landing-page copy each quarter"])], 1)
CONTENT_NOTE = "Photography and video are not included: we use your photos or properly licensed images. One-month minimum, then 30 days' notice."


def pay_cta(product_name, tier, fallback_href, fallback_text=None):
    """Use a payment link when one is configured; otherwise the request form."""
    url = PAY_LINKS.get(f"{product_name}: {tier}") if tier else PAY_LINKS.get(product_name)
    if url:
        return (f"Subscribe to {tier or product_name}", url, "checkout_start")
    return (fallback_text or f"Request {tier}", fallback_href, "")


# Secondary managed services: offered after an assessment, not priced publicly.
SECONDARY = [
    ("AI Operations Team", "Managed AI-assisted workflows with human review and monthly improvement.", "Scoped after an Automation and AI Opportunity Assessment"),
    ("Managed Back Office", "Admin, data upkeep and operational reporting to an agreed service level.", "Scoped after an Offshoring Readiness Blueprint"),
    ("Knowledge Management Service", "A SharePoint knowledge base kept current and ready for Copilot.", "Usually follows a Documentation Factory project"),
    ("Transformation Support Office", "Change plans, communications, training logistics and benefits tracking.", "Scoped after an Offshoring Readiness Blueprint"),
]

INDUSTRIES = ["Logistics", "Warehousing", "Supply chain", "Professional services", "Technology", "Property",
              "Financial services", "Healthcare", "Education", "Public sector"]


def tier_cards(product, featured_flag="Recommended", per="per month, ex VAT", annual=False, cta=None):
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
            {(lambda c: f'<a class="btn {"btn-ember" if f else "btn-line"}" href="{c[1]}" data-track="{c[2]}">{c[0]} {ARR}</a>')(cta(tname)) if cta else f'<a class="btn {"btn-ember" if f else "btn-line"}" href="contact.html?topic={pid}">Discuss {tname} {ARR}</a>'}
          </div>""")
    return "\n".join(out)


def product_block(product, per="per month, ex VAT", annual=False, extra="", cta=None):
    pid, name, who, desc = product[:4]
    return f"""        <div class="product" id="{pid}">
          <div class="product-head">
            <div><h2>{name}</h2><p>{desc}</p>{extra}</div>
            <div class="for">{who}</div>
          </div>
          <div class="grid g3">
{tier_cards(product, per=per, annual=annual, cta=cta)}
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
            else "60-day onboarding, monthly in advance, then 30 days' notice.")
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


def price_card(o, cta_text, cta_href, flag=None, cls=""):
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


# ============================================================== THE SIX OFFERINGS, IN THREE TIERS
# Single source for the homepage, Services and Pricing. Prices are proposals for the owner to confirm.
VALUE_PROP = "Cut operating overhead without slowing delivery."
VALUE_SUB = ("Senior-led diagnostics, managed delivery pods and on-demand specialist sprints, under one UK contract. "
             "Built for cost-conscious leaders who want measurable returns, not open-ended retainers.")
TIERS = [
    ("tier1", "Tier 1", "Entry diagnostics", "Fixed scope, fixed fee, credited if you go ahead."),
    ("tier2", "Tier 2", "Core execution", "Managed pods for ongoing work; specialist sprints for urgent change."),
    ("tier3", "Tier 3", "Self-serve and fractional", "Frameworks for lean teams, or senior leadership part-time."),
]
OFFERS = [
    {"id": "audit", "tier": "tier1", "name": "Operational and SaaS Cost-Leakage Audit",
     "tag": "Find hidden software spend, manual bottlenecks and hand-over opportunities in 14 days.",
     "format": "Fixed-scope 2-week diagnostic", "price": "£2,500", "per": "fixed · ex VAT",
     "ideal": "COOs, CFOs and founders preparing budgets or protecting margins now",
     "includes": ["Audit of your recurring software stack, licence tiers and overlapping tools",
                  "Workflow mapping to find repetitive, non-core work suited to automation or a managed pod",
                  "Prioritised 90-day cost-reduction roadmap, with projected savings for each action"],
     "hook": "Fee credited in full against implementation if you proceed within 30 days. We guarantee to identify annualised savings of at least three times the fee.",
     "cta": ("Book a 14-Day Audit", "contact.html?topic=cost-audit")},
    {"id": "blueprint", "tier": "tier1", "name": "Offshoring Readiness Blueprint",
     "tag": "Hand work to an offshore team safely, without losing quality or management time.",
     "format": "Fixed-scope 3-week blueprint", "price": "£2,950", "per": "fixed · ex VAT",
     "ideal": "Teams considering offshore delivery who want to avoid communication breakdowns, turnover and security gaps",
     "includes": ["Role-by-role feasibility and cost comparison: in-house versus a managed pod",
                  "SOPs, KPI scorecards and quality-assurance checklists for the work",
                  "Data security, compliance and hand-off governance playbook"],
     "hook": "Fee credited in full against your first pod month if you proceed within 30 days.",
     "cta": ("Get Your Offshore Blueprint", ASSESS_HREF)},
    {"id": "pods", "tier": "tier2", "name": "Managed Delivery Pods",
     "tag": "Offshore delivery costs, with UK senior oversight and accountability.",
     "format": "60-day onboarding, then monthly on 30 days' notice", "price": "From £1,950", "per": "per pod, per month · ex VAT",
     "ideal": "Organisations facing headcount freezes, or scaling PMO, analysis, documentation, back office or finance administration",
     "includes": ["A managed team in our Lahore office, trained on your workflows and SOPs",
                  "A senior UK lead responsible for quality, escalation and continuous improvement",
                  "Continuity cover: if a team member leaves, we replace and retrain at our cost",
                  "No recruitment, payroll, National Insurance or benefits overhead"],
     "hook": "Pods include PMO-in-a-Box, Managed Business Analysis and the Documentation Factory.",
     "cta": ("Build Your Delivery Pod", "contact.html?topic=pod")},
    {"id": "sprints", "tier": "tier2", "name": "Specialist Sprints",
     "tag": "Senior hands-on delivery for urgent operational, technology or restructuring problems, without a full-time senior hire.",
     "format": "30- to 90-day fixed-outcome sprint", "price": "From £4,950", "per": "per sprint · ex VAT",
     "ideal": "Stalled ERP or WMS rollouts, migrations, post-merger integration, automation rollouts, ISO 27001 or Cyber Essentials Plus preparation",
     "includes": ["Hands-on delivery by a senior practitioner, with no hand-off to juniors",
                  "Weekly milestones tied to agreed business outcomes",
                  "Knowledge transfer and handover to your team at the end"],
     "hook": "Need the change kept running afterwards? A delivery pod can take it on.",
     "cta": ("Scope a Specialist Sprint", "contact.html?topic=sprint")},
    {"id": "toolkit", "tier": "tier3", "name": "Lean Operations and Automation Toolkit",
     "tag": "Ready-to-use SOPs, supplier negotiation scripts and AI workflow templates for your own team.",
     "format": "One-time licence, with an optional half-day set-up workshop", "price": "Early access", "per": "workshop £1,450 · ex VAT",
     "ideal": "Lean teams with internal capacity who want proven frameworks without consulting day rates",
     "includes": ["Software renewal and supplier negotiation scripts", "Offshore onboarding and QA scorecard templates",
                  "AI prompt libraries and admin automation blueprints"],
     "hook": "In development. Join the early-access list for launch pricing.",
     "cta": ("Join the Toolkit Early-Access List", "contact.html?topic=toolkit")},
    {"id": "fractional", "tier": "tier3", "name": "Fractional Operations and Transformation Lead",
     "tag": "Senior operational leadership, part-time.",
     "format": "Monthly retainer, 1 or 2 days a week", "price": "From £4,500", "per": "per month · ex VAT",
     "ideal": "Growing businesses that need senior operational oversight without a full-time executive salary",
     "includes": ["Supplier consolidation and contract renegotiation",
                  "Oversight of delivery pods, automation projects and margin-improvement work",
                  "Monthly board-ready KPI and cost-efficiency reporting"],
     "hook": "1 day a week from £4,500 a month; 2 days a week from £8,500. One-month minimum.",
     "cta": ("Enquire About Fractional Support", "contact.html?topic=fractional")},
]
OFFER = {o["id"]: o for o in OFFERS}
TRUST_STRIP = [
    ("Senior-led delivery", "You work directly with experienced practitioners, never handed off to junior generalists."),
    ("No long lock-ins", "Fixed-scope sprints, and rolling monthly terms after onboarding, that fit departmental budgets."),
    ("Self-funding focus", "Every engagement is scoped around measurable savings, speed or margin protection."),
]


def offer_card(o, cta_text=None, cta_href=None, flag=None, cls="", **_):
    """Overloaded: a dict from OFFERS renders an offering card; a tuple falls through to the price card below."""
    if not isinstance(o, dict):
        return price_card(o, cta_text, cta_href, flag, cls)
    track = track_for(o["cta"][1]) or f'{o["id"]}_cta'
    return f"""          <article class="ocard reveal" id="{o['id']}">
            <p class="ocard-format">{o['format']}</p>
            <h3>{o['name']}</h3>
            <p class="ocard-tag">{o['tag']}</p>
            <p class="ideal"><span>Ideal for</span>{o['ideal']}</p>
            <ul class="ticks compact">{''.join(f'<li>{x}</li>' for x in o['includes'])}</ul>
            <p class="ocard-hook">{o['hook']}</p>
            <div class="ocard-foot">
              <div class="ocard-price"><b>{o['price']}</b><small>{o['per']}</small></div>
              <a class="btn btn-ember" href="{o['cta'][1]}" data-track="{track}">{o['cta'][0]} {ARR}</a>
            </div>
          </article>"""


def tiers_html(heading=True):
    out = []
    for tid, n, title, sub in TIERS:
        cards = "\n".join(offer_card(o) for o in OFFERS if o["tier"] == tid)
        out.append(f"""        <div class="tier" id="{tid}">
          <div class="tier-head reveal"><span class="tier-n">{n}</span><h3>{title}</h3><p>{sub}</p></div>
          <div class="tier-cards">
{cards}
          </div>
        </div>""")
    return "\n".join(out)


def trust_strip():
    return '        <ul class="trust-strip reveal">' + "".join(f'<li><strong>{t}</strong><span>{d}</span></li>' for t, d in TRUST_STRIP) + "</ul>"


# ============================================================== TRANSFORMATION CATALOGUE
# (id, label, heading, intro, [scope], extra paragraph, tools, (cta text, cta href))
LT_SERVICES = [
    ("automation", "Process automation", "Absorb growth without adding back-office headcount",
     "With employer National Insurance and wage costs rising, every new back-office hire costs more. We measure the hours spent in finance, dispatch, onboarding and reporting, simplify the process, then automate what's worth automating, with human approval where it matters.",
     ["Identify manual and repetitive processes", "Map current workflows", "Find delays, duplication and control weaknesses",
      "Prioritise automation opportunities", "Redesign processes before automating them", "Implement workflow automation",
      "Improve management information", "Introduce appropriate human approval points", "Measure time, cost and quality improvements"],
     "We recommend a platform only when it suits your systems, licences and skills.",
     "Microsoft Power Automate, Microsoft 365, SharePoint, Microsoft Teams, Power Apps, approved AI platforms, and your existing systems and APIs.",
     ("Book an Automation Discovery Session", "contact.html?topic=automation")),
    ("ai", "AI adoption and implementation", "Turn AI interest into controlled, practical implementation",
     "Implementation-led AI adoption using established tools such as Microsoft Copilot and approved AI platforms, with the governance, data and training that make it safe and useful.",
     ["AI readiness assessments", "Identification of viable business use cases", "Process and data suitability", "AI risk assessment",
      "Governance and acceptable-use controls", "Proofs of concept", "Microsoft Copilot adoption", "AI-enabled knowledge management",
      "Document and information workflows", "User training", "Implementation roadmaps", "Adoption and benefits measurement"],
     "We help you adopt and implement existing AI platforms. We don't build proprietary machine-learning models.",
     "", ("Assess Your AI Readiness", "ai-scorecard.html")),
    ("cyber", "Cybersecurity implementation", "Get ready for ISO 27001, Cyber Essentials Plus and client audits",
     "When an enterprise client, insurer or certification body asks for evidence, we lead the business and delivery side: turning requirements and audit findings into controls, policies, processes and behaviours that are actually in place, with the evidence to show it.",
     ["Cybersecurity transformation programmes", "Control implementation", "Identity and access-management change",
      "Security-process design", "Governance and accountability", "Supplier coordination", "Risk remediation programmes",
      "Security requirements", "Business engagement", "Migration and implementation planning", "User adoption",
      "Programme reporting", "Operational handover"],
     "We provide strategy support, implementation leadership and programme delivery. We are not a penetration-testing company, security operations centre or managed detection provider: specialist technical testing is carried out by your internal teams or specialist partners.",
     "", ("Discuss a Cybersecurity Change Programme", "contact.html?topic=cyber-change")),
    ("migration", "Technology and data migration", "Rescue and stabilise ERP, WMS and system rollouts",
     "Whether a NetSuite, Dynamics 365, SAP or WMS rollout is still being planned, running late or unstable after go-live, we lead the business change, governance and delivery, coordinating your teams and implementation partners so operations keep running.",
     ["Business and technical requirements", "Current-state analysis", "Migration strategy", "Impact assessment",
      "Stakeholder coordination", "Data and system dependencies", "Cutover planning", "Business readiness", "Testing governance",
      "Communications", "Training", "Hypercare", "Benefits tracking", "Decommissioning planning"],
     "Specialist technical migration work, such as data transformation scripts or platform configuration, is carried out by your teams or technology partners under our coordination.",
     "Microsoft 365 migration, SharePoint migration, collaboration-platform migration, application replacement, cloud adoption, data migration and workplace technology change.",
     ("Plan Your Migration", "contact.html?topic=migration")),
    ("tom", "Target operating-model design", "Design how the future organisation will actually operate",
     "A target operating model describes how your organisation will work in future: who does what, through which processes, with what information and technology. We design it so it can be implemented, not just presented.",
     ["Current-state assessment", "Target operating-model blueprint", "Business capability map", "Process architecture",
      "Organisation and responsibility design", "Governance model", "Technology implications", "Transition roadmap",
      "Implementation work packages", "Benefits and KPI framework"],
     "The model connects customer needs, capabilities, structure, roles, processes, governance, decision rights, data, technology, controls, performance measures, and sourcing and delivery locations, with a practical route from today's operation to the future one.",
     "", ("Design Your Future Operating Model", "contact.html?topic=tom")),
    ("simplify", "Process simplification and cost reduction", "Reduce operating cost by fixing complexity at its source",
     "Much avoidable cost comes from complexity: repeated entry, unclear handoffs, rework and technology that isn't used. We find it, remove it and measure the difference.",
     ["Repeated manual entry", "Duplicate systems", "Unclear handoffs", "Unnecessary approvals", "Process delays", "Rework",
      "Poor information quality", "Weak ownership", "Unused technology", "Fragmented reporting", "Activities that don't add enough value"],
     "Our method: map the current process; establish the baseline; identify delay, duplication and failure demand; simplify; assess automation; define the future process; build the business case; implement and measure. We measure cycle time, cost per transaction, manual touches, error and rework rates, service response time, system usage and staff capacity released. We don't promise a percentage saving before an assessment.",
     "", ("Request a Process Review", "contact.html?topic=process-review")),
    ("change", "Complex change and programme delivery", "Bring structure, governance and momentum to complex change",
     "The value is in connecting strategy, business operations and technical delivery, so decisions are made on time and change lands in the operation.",
     ["Programme mobilisation", "Recovery of struggling programmes", "Delivery governance", "Workstream coordination",
      "Business architecture", "Business analysis", "RAID management", "Dependency management", "Stakeholder engagement",
      "Supplier coordination", "Executive reporting", "Decision management", "Business readiness", "Transition planning",
      "Benefits realisation", "Operational handover"],
     "", "", ("Discuss Your Change Programme", "contact.html?topic=change-programme")),
    ("workplace", "Remote and hybrid working enablement", "Enable secure and effective work across locations",
     "Distributed work is not just installing Microsoft Teams. It changes ways of working, processes, controls, management practices, information access, security and user behaviour, and each needs designing.",
     ["Microsoft 365, Teams and SharePoint", "Collaboration practices", "Document management", "Remote access", "Identity and access",
      "Information security", "Employee onboarding", "Digital approval processes", "Knowledge sharing", "Governance", "Adoption and training"],
     "", "", ("Review Your Digital Workplace", "contact.html?topic=digital-workplace")),
]


def lt_service(sid, lbl, heading, intro, scope, note, tools, cta_):
    visible, more = scope[:5], scope[5:]
    more_html = ""
    if more or note or tools:
        more_html = f"""<details class="more-scope"><summary>Full scope</summary>
              {'<ul class="ticks compact">' + ''.join(f'<li>{x}</li>' for x in more) + '</ul>' if more else ''}
              {f'<p class="small"><strong>Typical technologies:</strong> {tools}</p>' if tools else ''}
              {f'<p class="small">{note}</p>' if note else ''}
            </details>"""
    return f"""          <article class="svc-card reveal" id="svc-{sid}">
            <span class="label">{lbl}</span>
            <h3>{heading}</h3>
            <p>{intro}</p>
            <ul class="ticks compact">{''.join(f'<li>{x}</li>' for x in visible)}</ul>
            {more_html}
            <div class="svc-actions">{btn(cta_[0], cta_[1], 'btn-line btn-sm')}</div>
          </article>"""


lt_services = "\n".join(lt_service(*s) for s in LT_SERVICES)


# (name, price, period, [inclusions], note, cta)



# ============================================================== HOME
FAQ = [
    ("Where is the work delivered?", "Delivery takes place in our office in Lahore, Pakistan. Commercial ownership, service management and senior oversight remain in the UK with Bespoke Vista Ltd. Workshops and governance meetings can be led by our UK lead."),
    ("Who is accountable for delivery?", "Bespoke Vista Ltd is contractually accountable for every service. A named senior UK lead owns your engagement and is your escalation point."),
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
    ("What is the minimum contract term?", "Diagnostics, sprints and documentation projects are one-off, fixed-price engagements. Delivery pods start with a 60-day onboarding period, paid monthly in advance, then continue on 30 days' notice. Fractional support has a one-month minimum."),
    ("What happens during the 60-day pod onboarding?", "We start on one clearly defined process or workstream, with a named delivery lead, agreed inputs and outputs, baseline measurements and weekly progress reviews. At day 60 you receive a results report and decide whether the pod continues."),
    ("How is quality measured?", "Against measures agreed in your service definition, typically accuracy, turnaround time, rework and service-level performance. Work is checked by a second person before release, sampled weekly and reported in the monthly service report."),
    ("What happens to access and data at contract end?", "We remove all access, return or securely delete your data as set out in the Data Processing Agreement, and hand over all documentation and deliverables, which belong to you."),
    ("Which activities are out of scope?", "Anything not in your service definition, including decisions on your behalf, accountability for delivering your projects, legal or financial advice, software development, third-party licences and on-site attendance unless agreed."),
    ("How are changes to scope handled?", "Through change control. You raise a change request, we confirm the effect on capacity, timescale and price in writing, and nothing changes until you approve it."),
]
faq_html = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)

MODEL_POINTS = [
    ("UK commercial ownership", "Your contract, invoicing and liability sit with Bespoke Vista Ltd, a UK company."),
    ("Senior UK oversight", "A senior UK lead scopes every service, reviews quality and chairs service reviews."),
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
    ("pilot-plan", "Pod onboarding plan", "The first four weeks of a pod: activities, measures and decision points."),
]
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
    ("Bespoke Vista intervention", "Offshoring Readiness Blueprint, then a PMO pod with a 60-day onboarding covering RAID and weekly reporting for three projects, then PMO-in-a-Box Managed."),
    ("Deliverables", "Governance templates, RAID registers, a weekly portfolio dashboard, governance-meeting packs and a monthly service report."),
    ("Measured result", "In a real engagement we would report the change against each baseline measure. No results are shown because this is not a real engagement."),
    ("Delivery period", "Blueprint in three weeks, a 60-day onboarding, then month to month."),
    ("Client quotation", "None. Verified quotations will only be published with the client's written permission."),
    ("Next phase", "Extend to dependency and benefits tracking, and add a Documentation Factory project for warehouse SOPs."),
]
scenario_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in SCENARIO)

FOUNDING_BOX = f"""<div class="founding reveal">
            <span class="status s-contract">Founding clients</span>
            <h3>Be one of our first {FOUNDING_PLACES} managed-service clients</h3>
            <p>We're offering founding-client terms, a reduced rate for the 60-day onboarding and first month, agreed individually, to our first {FOUNDING_PLACES} managed-service clients. In return, we ask you to act as a reference and to let us publish a case study once results are measured. You approve the wording before anything is published.</p>
            {btn("Ask about founding-client terms", "contact.html?topic=founding", "btn-primary btn-sm")}
          </div>"""

# ---- Homepage content (v9: two paths, urgent triggers, trust block, illustrative scenarios)
TRIGGERS = [
    ("Audit and cyber readiness", "ISO 27001, Cyber Essentials Plus or an enterprise client's vendor audit is on the calendar, and the policies, processes and evidence aren't ready.",
     "A compliance Specialist Sprint to close the gaps, with a documentation and PMO pod to keep evidence and remediation actions current.", ("Prepare for an Audit", "contact.html?topic=audit-readiness")),
    ("Stalled ERP, WMS or system rollout", "A NetSuite, Dynamics 365, SAP or WMS rollout is late, over budget or unstable after go-live, and operations are running on workarounds.",
     "A rescue Specialist Sprint, starting with a two-week review, then an analysis and PMO pod through stabilisation.", ("Rescue a Stalled Rollout", "contact.html?topic=system-rescue")),
    ("Margin and headcount pressure", "Order and admin volumes are growing, but employer National Insurance and wage costs make every new back-office hire harder to justify.",
     "A Cost-Leakage Audit to find the hours and software spend, then automation and a back-office pod instead of new hires.", ("Find Hours to Automate", "contact.html?topic=headcount")),
    ("M&amp;A integration or exit readiness", "An acquisition, merger, investment or sale is coming, and too much of how the business runs lives in a few people's heads.",
     "A documentation pod turns tribal knowledge into auditable processes; a PMO pod gives buyers, investors and integration teams clean, current reporting.", ("Get Due-Diligence Ready", "contact.html?topic=m-and-a")),
]
triggers_html = "\n".join(f"""          <li class="trow reveal">
            <span class="trow-n">{i+1:02d}</span>
            <div class="trow-main"><h3>{t}</h3><p>{d}</p></div>
            <div class="trow-fix"><span>How we help</span><p>{h}</p><a class="text-link" href="{c[1]}">{c[0]} →</a></div>
          </li>""" for i, (t, d, h, c) in enumerate(TRIGGERS))


TRUST = [
    ("One UK contract", "You contract with Bespoke Vista Ltd, a UK company. Liability, invoicing and escalation sit here, not offshore."),
    ("Senior UK oversight", "A senior UK lead scopes every engagement, reviews quality before work reaches you and chairs every service review."),
    ("UK GDPR and data security", "A Data Processing Agreement, confidentiality agreements, MFA and role-based access. We prefer to work inside your Microsoft 365 tenant, so data stays under your controls."),
    ("Time-zone overlap", "Our Lahore office works 09:00–18:00 Pakistan time: about four to five hours of live overlap with UK mornings, and work finished before your day starts."),
    ("Quality assurance", "Work is done to documented SOPs, checked by a second person before release, sampled weekly and reported against agreed measures."),
    ("Office-based, managed team", "Professionals in a controlled office, managed by us. No freelancers, no CVs, and no staff for you to manage."),
]
trust_html = "\n".join(f'          <div class="point reveal"><span class="pn">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(TRUST))

COMPARE_SHORT = [
    ("Who leads the change", "Senior partners, mostly at the start", "One senior individual", "Usually nobody: technical leads only", "A senior UK lead, throughout"),
    ("Who does the follow-through", "Junior consultants", "Nobody: capacity runs out", "Staff you manage yourself", "Our managed team, run by us"),
    ("Accountability", "Firm-level", "Individual", "Split with you", "One UK contract, one lead"),
    ("After go-live", "The team rolls off", "The contract ends", "Continues if you manage it", "We keep it running"),
    ("First commitment", "A large programme", "An open-ended day rate", "A headcount contract", "A fixed-fee diagnostic from £2,500"),
]
COMPARE_COLS = ["Large consultancy", "Day-rate contractor", "Offshore supplier", "Bespoke Vista"]
compare_short_rows = "\n".join('              <tr><th scope="row">' + r[0] + '</th>'
                               + "".join(f'<td data-label="{COMPARE_COLS[k]}"{" class=\"us\"" if k == 3 else ""}>{r[k+1]}</td>' for k in range(4))
                               + '</tr>' for r in COMPARE_SHORT)

SCENARIOS = [
    ("WMS rollout rescue", "UK logistics and distribution business, around 300 employees",
     "A new warehouse management system went live months late. The warehouse was relying on spreadsheets and manual workarounds, and confidence in the programme was falling.",
     "A rescue Specialist Sprint: a two-week root-cause review, then senior delivery alongside the implementation partner; an analysis and PMO pod on defects, requirements and hypercare.",
     "One agreed recovery plan, a prioritised defect and decision log, weekly decisions instead of monthly surprises, and a stable hypercare rhythm handed over to the managed PMO."),
    ("ISO and Cyber audit readiness", "UK 3PL, around 180 employees",
     "A major retail client required ISO 27001-aligned controls and Cyber Essentials Plus within six months as a condition of renewal. Policies were out of date and key processes were undocumented.",
     "A compliance Specialist Sprint to scope and close the gaps; a documentation pod for policies and SOPs; a PMO pod tracking every remediation action with owners and dates.",
     "A controlled policy and SOP library, a remediation tracker the board could follow, and an evidence pack ready for the client audit and the certification body, kept current by the managed team."),
    ("Finance and operations automation", "UK professional services firm, around 120 employees",
     "Billing, client onboarding and management reporting volumes were rising, and leadership wanted to absorb the growth without adding back-office roles.",
     "A Cost-Leakage Audit with baseline hours and software spend measured; an automation Specialist Sprint in Microsoft 365 and Power Automate; a back-office pod for upkeep.",
     "Prioritised workflows automated, and a monthly report of hours saved against the baseline, so the business case is measured rather than assumed."),
]
scenarios_html = "\n".join(f"""          <article class="scn reveal">
            <span class="scn-tag">{t}</span>
            <p class="scn-org">{o}</p>
            <h3>Challenge</h3><p>{c}</p>
            <h3>Approach</h3><p>{a}</p>
            <h3>Outcome</h3><p>{r}</p>
          </article>""" for t, o, c, a, r in SCENARIOS)

home = f"""    <section class="hero home-hero">
      <div class="container hero-grid">
        <div>
          {label("For UK organisations of 50 to 500 people")}
          <h1>Cut operating overhead <em class="ember">without slowing delivery.</em></h1>
          <p class="lead">{VALUE_SUB}</p>
          <div class="hero-actions">
            {btn("Book a Discovery Call", DISCOVERY_HREF, "btn-ember")}
            {btn("See the Six Services", "#services", "btn-line", arrow=False)}
          </div>
          <p class="hero-note small muted">Free 20-minute call. Fixed-fee diagnostics from £2,500, credited if you go ahead. <strong>{USP}</strong></p>
        </div>
        <div class="hero-art">
          {horizon(["DESIGN", "LEAD", "DELIVER", "RUN"], "A sun rising over a horizon, marking design, lead, deliver and run")}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="services">
      <div class="container">
        <div class="head">
          <div>{label("What we offer")}<h2>Six services. <em class="ember">Three ways in.</em></h2></div>
          <p>Start with a fixed-fee diagnostic, move to managed delivery or a specialist sprint, or use our frameworks and part-time leadership. All prices exclude VAT.</p>
        </div>
{tiers_html()}
{trust_strip()}
        <a class="unsure reveal" href="scorecard.html" data-track="scorecard_cta">
          <span><strong>Not sure where to start?</strong> Thirteen questions, an instant score and a recommended next step. No email needed.</span>
          <span class="unsure-cta">Take the 5-minute Free Readiness Scorecard →</span>
        </a>
        <p class="small muted" style="margin-top:14px">Also from Bespoke Vista: <a href="virtual-consultancy.html">Virtual Consultancy</a> for single work packages, and <a href="websites-apps.html">websites, apps and content</a> for smaller organisations.</p>
      </div>
    </section>

    <section class="sec sec-sand" id="triggers">
      <div class="container">
        <div class="head">
          <div>{label("What's forcing the decision")}<h2>Four reasons UK firms <em class="ember">act now.</em></h2></div>
          <p>Each has a deadline someone else has set: an auditor, a client, a board or a buyer.</p>
        </div>
        <ol class="trows">
{triggers_html}
        </ol>
      </div>
    </section>

    <section class="sec sec-dark" id="trust">
      <div class="container">
        <div class="head">
          <div>{label("How the model works")}<h2>One accountable lead. <em class="ember">One managed team.</em> One contract.</h2></div>
          <p>Senior judgement where it matters, managed capacity where volume matters, and no hand-offs between suppliers.</p>
        </div>
        <figure class="model-flow reveal" aria-labelledby="model-cap">
          <div class="mf-node">
            <span class="mf-where">United Kingdom</span>
            <h3>Senior UK lead</h3>
            <p class="mf-who">Your accountable lead</p>
            <ul><li>Designs the change</li><li>Governs delivery and quality</li><li>Owns accountability to you</li></ul>
          </div>
          <div class="mf-link" aria-hidden="true"><span></span></div>
          <div class="mf-seal">
            <span class="mf-seal-k">One</span>
            <strong>UK contract</strong>
            <span class="mf-seal-s">Bespoke Vista Ltd</span>
          </div>
          <div class="mf-link" aria-hidden="true"><span></span></div>
          <div class="mf-node mf-node-run">
            <span class="mf-where">Lahore office</span>
            <h3>Managed delivery team</h3>
            <p class="mf-who">Run by us, not by you</p>
            <ul><li>PMO and reporting</li><li>Business analysis</li><li>Documentation</li><li>Ongoing upkeep</li></ul>
          </div>
          <figcaption id="model-cap" class="mf-cap"><span>Stage 1 · We lead the change</span><span>Stage 2 · Our team keeps it running</span></figcaption>
        </figure>
        <p class="founder-line reveal">Bespoke Vista was founded by Azeem Mushtaq, who has spent more than 25 years bridging business, technology and complex change. <a href="about.html">About us →</a></p>
        <div class="points points3" style="margin-top:56px">
{trust_html}
        </div>
        <div class="trust-foot reveal">
          {CLOCKS}
          <p>Bespoke Vista doesn't yet hold ISO 27001 or Cyber Essentials certification; our controls are being built against both. <a href="managed-teams.html#security">Security, service levels and FAQs →</a></p>
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="compare">
      <div class="container">
        <div class="head">
          <div>{label("The alternatives")}<h2>Where Bespoke Vista <em class="ember">fits.</em></h2></div>
          <p>A general comparison of typical options, not of any specific firm.</p>
        </div>
        <div class="table-wrap table-light reveal">
          <table class="compare compare-light compare4 compare-stack">
            <thead><tr><th scope="col">Factor</th><th scope="col">Large consultancy</th><th scope="col">Day-rate contractor</th><th scope="col">Offshore supplier</th><th scope="col" class="us">Bespoke Vista</th></tr></thead>
            <tbody>
{compare_short_rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="sec" id="scenarios">
      <div class="container">
        <div class="head">
          <div><span class="ill-flag">Illustrative mid-market scenarios</span><h2>What this looks like <em class="ember">in practice.</em></h2></div>
          <p>Composite examples showing how our services combine. They are not client case studies, and no client results are claimed.</p>
        </div>
        <div class="grid g3 scns">
{scenarios_html}
        </div>
        <div class="hero-actions" style="margin:36px 0 0">
          {btn("Book a Discovery Call", DISCOVERY_HREF, "btn-ember")}
          {btn("Take the Free Readiness Scorecard", "scorecard.html", "btn-line", arrow=False)}
        </div>
      </div>
    </section>

{cta("Tell us what's stalled, or what's costing too much.", "A free 20-minute discovery call with a senior consultant. You'll leave with a clear first step, whether that's a fixed-fee diagnostic, a pod, a sprint, or a referral elsewhere if we're not the right fit.")}"""

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
     "description": VALUE_PROP + " " + VALUE_SUB, "areaServed": "GB", "priceRange": "£1,950–£15,000"},
] + [svc_schema(o["name"], o["tag"], o["price"].replace("From ", "").replace("£", "").replace(",", "") if o["price"][0] in "£F" else None) for o in OFFERS]

page("index.html", SITE,
     "Cut operating overhead without slowing delivery: cost-leakage audits, offshoring blueprints, managed delivery pods, specialist sprints and fractional operations leadership for UK organisations of 50 to 500 people.",
     home, schema=HOME_SCHEMA,
     full_title="Cut Operating Overhead Without Slowing Delivery | Bespoke Vista")

# ============================================================== SERVICES
def subnav(items):
    return """    <nav class="subnav" aria-label="Jump to section">
      <div class="container"><ul>
""" + "\n".join(f'        <li><a href="#{a}">{l}</a></li>' for a, l in items) + """
      </ul></div>
    </nav>"""


SPRINT_EXAMPLES = [
    ("Stalled system rescue", "A two-week root-cause review of a late or unstable ERP, WMS or CRM rollout, then senior delivery to stabilise it.", "Review £4,950", "2 weeks, then 30–60 days"),
    ("Compliance and audit readiness", "ISO 27001, Cyber Essentials Plus or a client's vendor audit: gaps closed, policies and evidence in place.", "From £7,500", "30–90 days"),
    ("Workflow automation rollout", "Finance, onboarding, dispatch or reporting workflows automated in Microsoft 365 and Power Automate, with human approval points.", "£5,000–£15,000", "30–60 days"),
    ("Migration or post-merger integration", "Systems, data and teams brought together without losing operational control.", "From £7,500 per 30 days", "30–90 days"),
    ("Operating-model redesign", "How the organisation should work after the change: roles, processes, governance and a transition plan.", "£7,500–£15,000", "30–45 days"),
]
POD_TYPES = [
    ("PMO pod (PMO-in-a-Box)", "Governance, RAID and portfolio reporting.", "From £1,950/month", "pricing.html#pmo"),
    ("Business analysis pod", "Requirements, process design and defect analysis.", "From £2,250/month", "pricing.html#ba"),
    ("Documentation pod (Documentation Factory)", "Process maps, SOPs and a controlled library.", "From £2,950 fixed", "pricing.html#documentation"),
    ("Back-office and finance administration pod", "Admin, data upkeep, finance administration and operational reporting.", "Priced after a Blueprint", "#tier1"),
]
services = f"""    <section class="page-hero">
      <div class="container">
        {label("Services")}
        <h1>Six services. <em class="ember">Three ways in.</em></h1>
        <p class="lead">{VALUE_SUB}</p>
      </div>
    </section>
{subnav([("tier1", "Tier 1 · Entry diagnostics"), ("tier2", "Tier 2 · Core execution"), ("tier3", "Tier 3 · Self-serve and fractional"), ("detail", "Pods and sprints in detail"), ("also", "Also from Bespoke Vista")])}
    <section class="sec">
      <div class="container">
{tiers_html()}
{trust_strip()}
      </div>
    </section>

    <section class="sec sec-white" id="detail" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("In detail")}<h2>What pods and sprints <em class="ember">usually cover.</em></h2></div>
          <p>Each sprint is scoped to a fixed outcome before it starts. Each pod runs to written SOPs and service levels.</p>
        </div>
        <div class="split" style="align-items:start">
          <div class="reveal">
            <h3>Delivery pods</h3>
            <div class="pricelist">
{chr(10).join(f"""              <a class="pl-row" href="{h}"><h3>{n}</h3><p>{d}</p><span class="p">{pr}</span><span class="t"></span></a>""" for n, d, pr, h in POD_TYPES)}
            </div>
          </div>
          <div class="reveal">
            <h3>Specialist sprints</h3>
            <div class="pricelist">
{chr(10).join(f"""              <div class="pl-row"><h3>{n}</h3><p>{d}</p><span class="p">{pr}</span><span class="t">{t}</span></div>""" for n, d, pr, t in SPRINT_EXAMPLES)}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="also" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Also from Bespoke Vista")}<h2>For single work packages <em class="ember">and smaller organisations.</em></h2></div>
          <p>Separate services with their own pages and prices.</p>
        </div>
        <div class="grid g2">
          <article class="mini reveal">
            <span class="lr-tag">Virtual Consultancy</span>
            <h3>One work package, managed online</h3>
            <p>A senior consultant and a delivery coordinator plan, follow up and report on a defined piece of work.</p>
            <p class="mini-price"><span>Two-week trial</span><b>£950</b></p>
            <p class="mini-price"><span>Monthly plans</span><b>from £1,450/month</b></p>
            <a class="text-link" href="virtual-consultancy.html">See Virtual Consultancy →</a>
          </article>
          <article class="mini reveal">
            <span class="lr-tag">Websites, apps and content</span>
            <h3>Your website, members' app and content</h3>
            <p>Practical digital tools for clubs, schools, studios and small businesses, proven at EmptyHands.</p>
            <p class="mini-price"><span>Business Website</span><b>from £1,495</b></p>
            <p class="mini-price"><span>Member Portal</span><b>from £99/month</b></p>
            <a class="text-link" href="websites-apps.html">See Websites, Apps and Content →</a>
          </article>
        </div>
      </div>
    </section>

{cta()}"""

page("services.html", "Services",
     "Bespoke Vista services in three tiers: Cost-Leakage Audit and Offshoring Readiness Blueprint, managed delivery pods and specialist sprints, and a toolkit and fractional operations lead.",
     services, schema=[svc_schema(o["name"], o["tag"], o["price"].replace("From ", "").replace("£", "").replace(",", "") if o["price"][0] in "£F" else None) for o in OFFERS])

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
        <h1>UK-managed. Office-based delivery. <em class="ember">One contract.</em></h1>
        <p class="lead">This is the "keeps it running" half of what we do. You contract with a UK company, a senior UK lead owns the outcome, and office-based professionals in our Lahore delivery centre do the work to documented processes and service levels.</p>
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
          <p>Most clients start with an Offshoring Readiness Blueprint, then a 60-day pod onboarding. <a href="pricing.html#pods">See pod prices →</a></p>
        </div>
        <div class="grid g3">
{primary_offers}
        </div>
{f"""        <h3 style="margin-top:56px">Further managed services</h3>
        <p class="muted">Available once a first service is running, or where an assessment shows a clear fit. Priced after assessment.</p>
        <div class="pricelist">
{secondary_offers}
        </div>""" if SHOW_EXTRA_OFFERS else ""}
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

    <section class="sec sec-white" id="security" style="scroll-margin-top:100px">
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

    <section class="sec" id="faq" style="scroll-margin-top:100px">
      <div class="container split">
        <div>
          {label("FAQs")}
          <h2>Straight answers.</h2>
          <p class="muted">Something else? <a href="{DISCOVERY_HREF}">Book a 20-minute discovery call.</a></p>
        </div>
        <div class="faq">
{faq_html}
        </div>
      </div>
    </section>

{cta()}"""

page("managed-teams.html", "Delivery Model",
     "How Bespoke Vista's UK-managed, Lahore-delivered, AI-enabled model works: UK accountability, office-based delivery, service levels, security, mobilisation and FAQs.",
     managed, schema=[{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}])

# ============================================================== PRICING

terms_html = "\n".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in TERMS)
pricing_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in [FAQ[12], FAQ[11], FAQ[16], FAQ[17], FAQ[13], FAQ[10]])

FRACTIONAL_TIERS = [
    ("Fractional Lead: 1 day a week", "From £4,500", "per month · ex VAT",
     ["Around four days a month of senior time", "Supplier and contract review", "Oversight of pods and improvement work", "Monthly KPI and cost-efficiency report"],
     "One-month minimum, then 30 days' notice."),
    ("Fractional Lead: 2 days a week", "From £8,500", "per month · ex VAT",
     ["Around eight days a month of senior time", "Everything in 1 day a week", "Leadership-team and board attendance", "Programme and margin-improvement ownership"],
     "One-month minimum, then 30 days' notice."),
]
glance_rows = "\n".join(f'''              <tr><td data-label="Tier">{dict((t[0], t[1]) for t in TIERS)[o["tier"]]}</td><th scope="row"><a href="services.html#{o["id"]}">{o["name"]}</a></th><td data-label="Format">{o["format"]}</td><td data-label="Price" class="glance-price"><b>{o["price"]}</b><small>{o["per"]}</small></td><td data-label=""><a class="text-link" href="{o["cta"][1]}">{o["cta"][0]} →</a></td></tr>''' for o in OFFERS)
pricing = f"""    <section class="page-hero">
      <div class="container">
        {label("Pricing and terms")}
        <h1>Six services. <em class="ember">Clear prices.</em></h1>
        <p class="lead">Fixed fees for diagnostics and sprints, monthly fees for pods and fractional support. Every package states what's included and what isn't. All prices exclude VAT.</p>
      </div>
    </section>
{subnav([("glance", "At a glance"), ("pods", "Delivery pods"), ("sprints", "Specialist sprints"), ("fractional-prices", "Fractional lead"), ("also-prices", "Also available"), ("terms", "Terms"), ("faq", "FAQs")])}
    <section class="sec-tight" id="glance" style="scroll-margin-top:140px">
      <div class="container">
        <div class="table-wrap table-light reveal">
          <table class="compare compare-light glance compare-stack">
            <thead><tr><th scope="col">Tier</th><th scope="col">Service</th><th scope="col">Format</th><th scope="col">Price</th><th scope="col"><span class="sr-only">Next step</span></th></tr></thead>
            <tbody>
{glance_rows}
            </tbody>
          </table>
        </div>
        <p class="small muted" style="margin-top:14px">Cost-Leakage Audit and Offshoring Readiness Blueprint fees are credited in full if you go ahead within 30 days. The toolkit is in development.</p>
      </div>
    </section>

    <section class="sec sec-white" id="pods" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Tier 2 · Managed Delivery Pods")}<h2>Start with 60 days. <em class="ember">Then month to month.</em></h2></div>
          <p>Every pod starts with a 60-day onboarding on one defined workstream, then continues on 30 days' notice. Most clients begin with an Offshoring Readiness Blueprint, credited against the first month.</p>
        </div>
        <div class="grid g2">
          <div id="assessment" class="anchor-offset">
{price_card(ASSESSMENT, "Get Your Offshore Blueprint", ASSESS_HREF, "Recommended first step", "featured")}
          </div>
          <div id="pilot" class="anchor-offset">
{price_card(PILOT, "Build Your Delivery Pod", "contact.html?topic=pod")}
          </div>
        </div>
        <div style="height:72px"></div>
{product_block(PMO)}
{boundaries_table(PMO)}
        <div style="height:72px"></div>
{product_block(BA)}
{boundaries_table(BA)}
        <div style="height:72px"></div>
{product_block(DOCS, per="fixed price, ex VAT")}
        <div class="sop-def" style="margin-top:-40px;margin-bottom:24px"><strong>What counts as one standard SOP:</strong> <ul>{''.join(f'<li>{x}</li>' for x in SOP_DEFINITION)}</ul></div>
{boundaries_table(DOCS)}
        <p class="small muted" style="margin-top:24px">Back-office and finance administration pods are priced after a Blueprint, because the cost depends on volumes and systems.</p>
      </div>
    </section>

    <section class="sec" id="sprints" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Tier 2 · Specialist Sprints")}<h2>Fixed outcome. <em class="ember">Fixed price.</em></h2></div>
          <p>30 to 90 days of hands-on senior delivery. The outcome, milestones and price are agreed in writing before the sprint starts.</p>
        </div>
        <div class="pricelist">
{chr(10).join(f"""          <div class="pl-row reveal"><h3>{n}</h3><p>{d}</p><span class="p">{pr}</span><span class="t">{t}</span></div>""" for n, d, pr, t in SPRINT_EXAMPLES)}
        </div>
        <div class="hero-actions" style="margin:28px 0 0">{btn("Scope a Specialist Sprint", "contact.html?topic=sprint", "btn-ember")}</div>
      </div>
    </section>

    <section class="sec sec-white" id="fractional-prices" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Tier 3 · Fractional and self-serve")}<h2>Senior leadership, <em class="ember">part-time.</em></h2></div>
          <p>For growing businesses that need operational oversight without a full-time executive. The Lean Operations and Automation Toolkit is in development; <a href="contact.html?topic=toolkit">join the early-access list</a>.</p>
        </div>
        <div class="grid g2">
{price_card(FRACTIONAL_TIERS[0], "Enquire About Fractional Support", "contact.html?topic=fractional")}
{price_card(FRACTIONAL_TIERS[1], "Enquire About Fractional Support", "contact.html?topic=fractional", "Most hands-on", "featured")}
        </div>
      </div>
    </section>

    <section class="sec" id="also-prices" style="scroll-margin-top:140px">
      <div class="container">
        <div class="head">
          <div>{label("Also from Bespoke Vista")}<h2>Smaller pieces of work, <em class="ember">smaller organisations.</em></h2></div>
          <p>Full plans and prices are on each service's own page.</p>
        </div>
        <div class="pricelist">
          <a class="pl-row reveal" href="virtual-consultancy.html"><h3>Virtual Consultancy</h3><p>A senior consultant and a coordinator manage a work package online. Two-week trial, then monthly plans.</p><span class="p">£950 trial · from £1,450/month</span><span class="t">See plans →</span></a>
          <a class="pl-row reveal" href="websites-apps.html#portal"><h3>Member Portal</h3><p>The member app built for EmptyHands, for clubs, schools and studios.</p><span class="p">£99–£299/month</span><span class="t">See plans →</span></a>
          <a class="pl-row reveal" href="websites-apps.html#website"><h3>Business Website and Website Care</h3><p>A clear, fast website, then hosting and updates.</p><span class="p">From £1,495 · £49/month</span><span class="t">See details →</span></a>
          <a class="pl-row reveal" href="websites-apps.html#content"><h3>Content Creation</h3><p>Social posts, articles and newsletters every month.</p><span class="p">£295–£995/month</span><span class="t">See plans →</span></a>
        </div>
      </div>
    </section>

    <section class="sec sec-sand" id="terms" style="scroll-margin-top:140px">
      <div class="container split">
        <div>{label("Commercial terms")}<h2>The terms behind <em class="ember">every price.</em></h2><p class="muted">Full terms are set out in your proposal and contract.</p></div>
        <div class="table-wrap table-light"><table class="sla"><tbody>{terms_html}</tbody></table></div>
      </div>
    </section>

    <section class="sec sec-white" id="faq" style="scroll-margin-top:140px">
      <div class="container split">
        <div>{label("FAQs")}<h2>Pricing questions.</h2><p class="muted">More answers on the <a href="managed-teams.html#faq">Delivery Model page</a>.</p></div>
        <div class="faq">
{pricing_faq}
        </div>
      </div>
    </section>

{cta()}"""

page("pricing.html", "Pricing",
     "Bespoke Vista prices: Cost-Leakage Audit £2,500, Offshoring Readiness Blueprint £2,950, managed delivery pods from £1,950 a month, specialist sprints from £4,950 and fractional operations leadership from £4,500 a month.",
     pricing, schema=[svc_schema(o["name"], o["tag"], o["price"].replace("From ", "").replace("£", "").replace(",", "") if o["price"][0] in "£F" else None) for o in OFFERS])


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
    "sector": {"0": "Our founder has worked in logistics and supply-chain environments, so we understand how operational, customer and technology changes affect each other. Our role is the business and technology change, not logistics operations advice. <a href=\"logistics.html\">How we work with logistics businesses</a>."},
    "size": {"0": "For organisations under 50 people we usually start with a single workflow or a Process Starter documentation project, so the commitment stays proportionate."},
}

S_PMO = {"name": "PMO-in-a-Box", "price": "From £1,950/month", "href": "pricing.html#pmo",
         "what": "Governance, RAID management and portfolio reporting across your projects, with a monthly UK-led service review."}
S_BA = {"name": "Managed Business Analysis", "price": "From £2,250/month", "href": "pricing.html#ba",
        "what": "Process mapping, requirements and backlog management to a defined monthly capacity, with senior UK quality review."}
S_DOCS = {"name": "Documentation Factory: Process Starter", "price": "£2,950 fixed", "href": "pricing.html#documentation",
          "what": "Five documented processes and SOPs in a controlled library: the foundation for handing any work over safely."}
S_PILOT = {"name": "Managed Delivery Pod: 60-day onboarding", "price": "From £1,950/month", "href": "pricing.html#pods",
           "what": "One defined process or workstream, a named delivery lead, baseline measures, weekly reviews and a results report."}
S_AI = {"name": "Automation and AI Opportunity Assessment", "price": "£2,500–£5,000 fixed", "href": "services.html#sprints",
        "what": "AI readiness, process and data review, five prioritised use cases, risk review and a 90-day roadmap."}
S_SCALE = {"name": "PMO-in-a-Box Managed or Transformation Office", "price": "£3,950 to £7,500+/month", "href": "pricing.html#pmo",
           "what": "A weekly PMO rhythm or programme-level support across several workstreams, with senior UK oversight."}

NEXT_ASSESS = {"label": "Get Your Offshore Blueprint", "href": ASSESS_HREF, "track": track_for(ASSESS_HREF),
               "text": "Start with an Offshoring Readiness Blueprint (£2,950, three weeks). The fee is credited against your first pod month if you proceed within 30 days."}

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
        {"max": 55, "name": "Ready to start with one pod",
         "title": "Prove it on one workflow",
         "text": "You have enough in place to test managed delivery safely on one bounded process or workstream. A short, measured pilot will show what works before you commit to anything ongoing.",
         "risks": ["Scope creep if the pilot workflow isn't tightly defined", "Inconsistent processes may need documenting during the pilot", "Results are hard to judge without a baseline"],
         "actions": ["Choose one bounded process or workstream", "Capture today's baseline: volumes, turnaround and rework", "Agree success criteria before the pilot starts"],
         "service": S_PILOT,
         "next": {"label": "Build Your Delivery Pod", "href": "contact.html?topic=pod", "track": "pod_cta",
                  "text": "Start with one pod on one bounded workstream. Most clients fix the scope first with an Offshoring Readiness Blueprint, credited against the first month."}},
        {"max": 75, "name": "Ready for a managed service",
         "title": "Put the work on a managed footing",
         "text": "Your processes, governance and access are mature enough for a monthly managed service with defined capacity, outputs and service levels.",
         "risks": ["Capacity agreed too loosely leads to friction later", "Governance cadence slips once the service is running", "Benefits aren't tracked, so value is hard to show"],
         "actions": ["Define monthly capacity, outputs and service levels", "Set the reporting and service-review cadence", "Start with one service and expand once it's stable"],
         "service": S_PMO,
         "next": {"label": "Discuss Your Project Portfolio", "href": "contact.html?topic=pmo", "track": "portfolio_cta",
                  "text": "A short conversation about your portfolio, then an Offshoring Readiness Blueprint to confirm capacity and price."}},
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
        {"id": "data", "name": "Data and tools", "service": {"name": "AI Workflow Implementation", "price": "£5,000–£15,000", "href": "services.html#sprints", "what": "One to three workflows with testing, user guidance, governance documentation and handover."}},
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
         "service": S_AI, "next": {"label": "Request an Automation Assessment", "href": "contact.html?topic=automation", "track": "ai_cta", "text": "A fixed-price discovery that ends with five prioritised use cases and a 90-day roadmap."}},
        {"max": 59, "name": "Experimenter", "title": "Turn pockets of use into a plan",
         "text": "People are using AI, but without much structure. Agree priorities, put governance in place and pick use cases worth scaling.",
         "risks": ["Inconsistent results across teams", "Data leakage through unapproved tools", "No measurable benefit to show leadership"],
         "actions": ["Prioritise use cases by value and risk", "Put governance and approved tools in place", "Measure a baseline before implementing"],
         "service": S_AI, "next": {"label": "Request an Automation Assessment", "href": "contact.html?topic=automation", "track": "ai_cta", "text": "Turn scattered experiments into a prioritised, governed plan."}},
        {"max": 79, "name": "Adopter", "title": "Scale what works",
         "text": "The foundations are in place. The value now comes from implementing end-to-end workflows and measuring the benefit.",
         "risks": ["Pilots that never become production workflows", "Rising consumption costs", "Workflows nobody maintains"],
         "actions": ["Pick one to three workflows to implement properly", "Agree ownership and maintenance", "Track time saved and quality"],
         "service": {"name": "AI Workflow Implementation", "price": "£5,000–£15,000", "href": "services.html#sprints", "what": "One to three workflows with testing, user guidance, governance documentation and handover."},
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
                  <p class="small" style="color:var(--slate);margin:4px 0 0">We use your details only to send your report and arrange a consultation. <a href="privacy.html">Privacy notice</a></p>
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
            {btn("Get Your Offshore Blueprint", ASSESS_HREF, "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">UK-managed. One contract. Clear service levels.</p>
        </div>
        <div class="sc-art">
          {horizon(["UK-LED", "MANAGED", "LAHORE", "AI-ENABLED"])}
        <div class="sample-card reveal" aria-label="Example of a scorecard result">
          <div class="sample-top"><span class="label" style="margin:0">Example result</span><span class="sample-score"><strong>48</strong>/100</span></div>
          <p class="band" style="margin:8px 0 0">Ready to start with one pod</p>
          <div class="bars" style="margin:16px 0">
{sc_sample}
          </div>
          <div class="sample-foot"><span class="small muted">Recommended next step</span><strong>Managed Delivery Pod</strong><span class="small muted">60-day onboarding, after an Offshoring Readiness Blueprint</span></div>
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
          <div>{label("How to start")}<h2>Blueprint. Onboard. <em class="ember">Then decide.</em></h2></div>
          <p>A low-risk route from first conversation to a managed pod. You see the work running on your own processes before committing month to month.</p>
        </div>
        <div class="grid g2">
{price_card(ASSESSMENT, "Get Your Offshore Blueprint", ASSESS_HREF, "Start here", "featured")}
{price_card(PILOT, "Build Your Delivery Pod", "contact.html?topic=pod")}
        </div>
        <p class="note">After the 60-day onboarding, pods continue month to month on 30 days' notice. <a href="pricing.html#pods">See pod prices and package boundaries →</a></p>
      </div>
    </section>

    <section class="sec sec-white" id="faq">
      <div class="container split">
        <div>{label("Straight answers")}<h2>Questions UK buyers ask.</h2><p class="muted"><a href="managed-teams.html#faq">All 18 FAQs →</a></p></div>
        <div class="faq">
{sc_faq}
        </div>
      </div>
    </section>

{cta()}"""

page("scorecard.html", "Free Readiness Scorecard",
     "Free 5-minute readiness scorecard for UK SMEs and mid-market organisations. Find out what you could hand over to a UK-managed delivery service, the risks, and your next step.",
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

{cta("Considering managed delivery as well?", "The Free Readiness Scorecard shows whether your processes, governance and data are ready for a managed service.", ("Take the Free Readiness Scorecard", "scorecard.html"), ("Get Your Offshore Blueprint", ASSESS_HREF))}"""

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
        <p class="lead">Bespoke Vista is an independent UK consultancy that combines senior expertise with a managed delivery team, so good strategy actually reaches the front line.</p>
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
    ("emptyhands", "Website &amp; app", "EmptyHands: website and member portal", "Karate and wellbeing school, Ilford",
     "A traditional karate, Tai Chi, yoga and Shiatsu school, run since 2006 by our founder, with notices, homework, timetables and fee collection spread across messages, paper and cash.",
     "A new website (<a href=\"https://emptyhands.co.uk/\" rel=\"noopener\">emptyhands.co.uk</a>) and the EmptyHands Portal: an app students install on their phone for the dojo calendar, notices and messages from Sensei, homework, and fees by card or PayPal.",
     "Students and parents have the calendar, notices, homework and fees in one place, and the school takes payments online. This is our founder's own school, so it is where we test every feature first."),
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
          <p>An independent <a href="services.html#sprints">rescue Specialist Sprint</a> gives executives an honest view and a recovery plan while there is still time to use it.</p>"""),
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
          <p>That's the model behind our <a href="managed-teams.html">managed teams</a>: UK-led, delivered by our managed team and priced on outcomes.</p>"""),
    ("cyber-is-business", "Cyber security", "4 min read", "Cyber security is a business change programme",
     "Security programmes run purely as technology projects struggle to land. The ones that succeed treat people and process as seriously as tools.",
     """<p>New controls, new tooling and new policies all change how people work. Yet security programmes are often scoped and resourced as if they were infrastructure upgrades.</p>
          <h3>Translate risk into business language</h3>
          <p>Boards fund what they understand. Framing security work in terms of service continuity, customer trust and regulatory exposure gets better decisions than framing it in terms of technical controls.</p>
          <h3>Map the processes you are changing</h3>
          <p>Access management, joiners-movers-leavers, incident response and supplier assurance are all business processes. Good business analysis makes sure the new way of working is clear, owned and workable.</p>
          <h3>Plan for adoption</h3>
          <p>Awareness, clear guidance and a sensible exceptions process stop people finding workarounds. A control nobody follows is not a control.</p>
          <p>We provide <a href="services.html#tier1">business analysis and delivery support</a> for security programmes, bridging specialists, the wider business and suppliers.</p>"""),
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
            <small>We'll send a sample briefing and plan details. No spam, unsubscribe any time. <a href="privacy.html">Privacy notice</a></small>
            <div class="form-status" role="status" aria-live="polite"></div>
          </form>
        </div>"""

if not SHOW_EXTRA_OFFERS:
    SUBSCRIBE = f"""        <div class="subscribe reveal">
          <div>
            {label("Next step")}
            <h2>Something here sound <em class="ember">familiar?</em></h2>
            <p>Take the free 5-minute Readiness Scorecard for a score and a recommended next step, or talk it through on a free 20-minute discovery call.</p>
          </div>
          <div class="hero-actions" style="margin:0">
            {btn("Take the Free Readiness Scorecard", "scorecard.html", "btn-ember")}
            {btn("Book a Discovery Call", DISCOVERY_HREF, "btn-line-light", arrow=False)}
          </div>
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
    ("discovery-call", "Free 20-minute discovery call"),
    ("cost-audit", "Operational and SaaS Cost-Leakage Audit"),
    ("blueprint", "Offshoring Readiness Blueprint"),
    ("pod", "Managed Delivery Pod"),
    ("sprint", "Specialist Sprint"),
    ("toolkit", "Lean Operations and Automation Toolkit (early access)"),
    ("fractional", "Fractional Operations and Transformation Lead"),
    ("automation", "Automation discovery or assessment"),
    ("ai-readiness", "AI readiness and adoption"),
    ("cyber-change", "Cybersecurity change programme"),
    ("migration", "Technology or data migration"),
    ("process-review", "Process review and cost reduction"),
    ("change-programme", "Complex change programme"),
    ("digital-workplace", "Remote and hybrid working / digital workplace"),
    ("fractional-adviser", "Fractional Transformation Adviser"),
    ("virtual-trial", "Two-Week Work Package Trial (£950)"),
    ("virtual", "Virtual Consultancy subscription"),
    ("audit-readiness", "ISO 27001, Cyber Essentials Plus or client audit readiness"),
    ("headcount", "Absorb growth without adding back-office headcount"),
    ("m-and-a", "M&amp;A integration or exit readiness"),
    ("founding", "Founding-client terms"),
    ("pmo", "PMO-in-a-Box / discuss our project portfolio"),
    ("ba", "Managed Business Analysis"),
    ("documentation", "Documentation Factory"),
    ("ai-discovery", "Automation and AI Opportunity Assessment"),
    ("ai-workflow", "AI Workflow Implementation"),
    ("scorecard", "Readiness Scorecard results"),
    ("ai-scorecard", "AI Scorecard results"),
    ("consultation", "General consultation"),
    ("managed", "Other managed services"),
    ("intelligence", "Executive AI Intelligence"),
    ("advisory", "Bespoke Vista AI Advisory"),
    ("system-rescue", "Stalled ERP / WMS / system rescue"),
    ("tom", "Target Operating Model Design"),
    ("governance", "AI Governance Pack"),
    ("copilot", "Microsoft Copilot Adoption Programme"),
    ("ai-optimisation", "AI Optimisation Review"),
    ("cyber-ba", "Cyber Security Business Analysis"),
    ("training", "Training and workshops"),
    ("wellbeing", "Calm Under Pressure workshop"),
    ("portal", "Member Portal for a club or school"),
    ("website", "Business website"),
    ("content", "Content creation"),
    ("other", "Something else"),
]
if not SHOW_EXTRA_OFFERS:
    TOPICS = [t for t in TOPICS if t[0] not in ("intelligence", "advisory", "fractional-adviser")]
topic_opts = "\n".join(f'                <option value="{v}">{l}</option>' for v, l in TOPICS)

booking_block = (f'<li><strong>Book directly</strong><a href="{BOOKING_URL}" target="_blank" rel="noopener" data-track="booking_start">Choose a time in our booking calendar →</a></li>'
                 if BOOKING_URL else "<!-- CONFIGURE: set BOOKING_URL in build.py to show a Microsoft Bookings link here. -->")

contact = f"""    <section class="page-hero">
      <div class="container">
        {label("Contact")}
        <h1>Tell us what you need, <em class="ember">or ask us anything.</em></h1>
        <p class="lead">Tell us about your organisation and the work you'd like help with. We'll reply within one working day to arrange the next step.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container contact-grid">
        <div class="reveal">
          <h2>What happens next</h2>
          <ol class="next-steps">
            <li>We reply within one working day to confirm a time.</li>
            <li>For an audit, blueprint or sprint, we confirm the scope and fixed price in writing before anything starts.</li>
            <li>We run the 60-minute workshop and send written findings with a recommended pilot.</li>
          </ol>
          <ul class="contact-ways">
            {booking_block}
            <li><strong>Email</strong><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
            <li><strong>Where we are</strong>United Kingdom, with a delivery centre in Lahore, Pakistan</li>
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
          <p class="form-note">We use your details only to respond to your enquiry. See our <a href="privacy.html">privacy notice</a>.</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </section>"""

page("contact.html", "Contact",
     "Contact Bespoke Vista about a Cost-Leakage Audit, Offshoring Readiness Blueprint, managed delivery pod, specialist sprint or fractional operations lead.",
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
    ["4", "Steady state; interim results", "Against baseline", "Day-60 review confirmed"]])

samples_body = "\n".join([
    sample("pmo-dashboard", "PMO dashboard", "The one-page portfolio view produced each week (Managed) or month (Foundation) in PMO-in-a-Box.", S1, "Excel or Power BI file"),
    sample("raid", "RAID register", "Risks, assumptions, issues and dependencies, with owners, ratings and actions.", S2, "Excel template"),
    sample("service-report", "Monthly service report", "How we report outputs and service-level performance at each monthly service review.", S3, "PDF"),
    sample("process-map", "Process map", "A swim-lane process map from the Documentation Factory, with control points marked.", S4, "Visio or PDF"),
    sample("sop", "Standard operating procedure", "An extract from an SOP in our controlled template. A standard SOP covers one process, up to five pages.", S5, "Word or PDF"),
    sample("rtm", "Requirements traceability matrix", "From Managed Business Analysis: each requirement traced to its source, user story, test and status.", S6, "Excel template"),
    sample("ai-report", "AI readiness report", "The prioritised use-case table from an Automation and AI Opportunity Assessment.", S7, "PDF"),
    sample("pilot-plan", "Pod onboarding plan", "How the first four weeks of a pod's 60-day onboarding are structured and measured.", S8, "PDF"),
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
     "Illustrative examples of Bespoke Vista deliverables: PMO dashboard, RAID register, service report, process map, SOP, traceability matrix, AI readiness report and pod onboarding plan.",
     samples)

# ============================================================== LOGISTICS LANDING PAGE
# Positioning: business and technology transformation applied in logistics and operational
# environments. Logistics is the client context, not the specialist discipline.

LT_ORGS = ["Logistics companies", "Warehousing businesses", "Distribution organisations", "Freight and transport operators",
           "Supply-chain service providers", "Third-party logistics (3PL) businesses", "Other operationally complex organisations"]
LT_BUYERS = ["Chief Operating Officers", "Chief Information Officers", "Chief Technology Officers", "Transformation Directors",
             "IT Directors", "Programme Directors", "Heads of Change", "Heads of Automation", "Heads of Cybersecurity",
             "Business Architecture leaders", "Operational Excellence leaders"]

LT_CHALLENGES = [
    "“Our core operational system is ageing, and replacing it touches almost every team.”",
    "“People re-key the same information between operational, finance and customer systems.”",
    "“AI tools are appearing in teams before we've agreed how they should be used.”",
    "“Customers and insurers are asking for security improvements we need to actually deliver.”",
    "“We have a migration coming and too many dependencies to see clearly.”",
    "“Several programmes are competing for the same people, and nobody has the full picture.”",
    "“Management reporting is assembled by hand from spreadsheets every week.”",
    "“Sites and teams work in different ways, and there's no agreed operating model.”",
]
lt_challenges = "\n".join(f'          <div class="problem reveal"><p class="pq">{c}</p></div>' for c in LT_CHALLENGES)

LT_SITUATIONS = ["Replacing legacy operational systems", "Automating order and exception workflows", "Improving management reporting",
                 "Integrating customer and supplier information", "Migrating collaboration and document platforms",
                 "Strengthening identity and access controls", "Improving governance across programmes",
                 "Supporting organisational restructuring", "Enabling distributed operational teams",
                 "Introducing AI-assisted knowledge processes"]
LT_NOT = "route optimisation, warehouse layout engineering, fleet maintenance, customs brokerage, freight forwarding, demand forecasting, inventory planning, transport procurement or network design"


LT_METHOD = [
    ("Understand", "Establish the problem, objectives, stakeholders and current constraints."),
    ("Simplify", "Remove unnecessary complexity before selecting or automating technology."),
    ("Design", "Define the future process, target operating model, controls and technology requirements."),
    ("Deliver", "Mobilise the programme, coordinate teams and implement the change."),
    ("Embed", "Support adoption, operational handover, measurement and continuous improvement."),
]
lt_method = "\n".join(f'          <div class="reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in LT_METHOD)

LT_OUTCOMES = ["Less manual administration", "Simpler and more consistent processes", "Lower avoidable operating cost",
               "Better use of existing technology", "Clearer accountability", "Stronger programme governance", "Safer AI adoption",
               "Improved cybersecurity controls", "More effective remote collaboration", "Reduced migration risk",
               "Better management information", "Faster implementation of approved change"]
LT_MEASURES = ["Cycle time", "Cost per transaction", "Manual touches", "Error rate", "Rework rate", "Service response time",
               "System usage", "Staff capacity released"]

LT_EXPERTISE = ["Business and technology transformation", "Automation", "Practical AI adoption", "Cybersecurity implementation",
                "Technology and application migration", "Target operating-model design", "Business architecture", "Business analysis",
                "Process simplification", "Microsoft 365 implementation and adoption", "Remote and hybrid working", "Programme governance",
                "Stakeholder alignment"]

LT_SCENARIO = [
    ("Client context", "A UK distribution business with several sites, an ageing operational system and customer reporting compiled by hand."),
    ("Business problem", "Support for the operational system ends within two years. Delivery exceptions are handled through email and spreadsheets, and there is no agreed future process."),
    ("Bespoke Vista's role", "Transformation lead: discovery, operating-model design for exception management, migration governance, automation design and supplier coordination."),
    ("Complexity", "Dependencies across customer service, operations, finance, IT and two technology suppliers, with cutover windows constrained by trading peaks."),
    ("Approach", "A Cost-Leakage Audit, then a rescue and migration Specialist Sprint covering process simplification, automation design and a migration plan with business-readiness activities, followed by a PMO and documentation pod."),
    ("Deliverables", "Current- and future-state process maps, an exception-management operating model, a workflow automation design with human approval points, a migration and cutover plan, RAID and governance packs, and a benefits framework."),
    ("Measured result", "In a real engagement we would report cycle time, manual touches and error rate against the baseline. No results are shown because this is not a real engagement."),
    ("Lessons", "Simplify the exception process before automating it; plan cutover around trading peaks; agree benefit measures before go-live."),
]
lt_scenario = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in LT_SCENARIO)

LT_FAQ = [
    ("Are you a logistics operations consultancy?", "No. We are a business and technology transformation consultancy that works with logistics and other operationally complex organisations. We don't advise on " + LT_NOT + "."),
    ("What types of logistics transformation do you support?", "Process automation, AI adoption, cybersecurity implementation, technology and data migration, target operating-model design, process simplification, complex programme delivery and remote or hybrid working. Typical situations include replacing legacy operational systems, automating exception workflows and improving management reporting."),
    ("Can you deliver the technical implementation?", "We lead the business change, design, governance and delivery. Workflow automation in Microsoft 365 and Power Automate can be delivered directly where suitable. Specialist engineering, platform configuration and penetration testing are delivered by your internal teams or verified technical partners, depending on the engagement."),
    ("Do you work with internal IT teams and external suppliers?", "Yes. Coordinating internal teams and suppliers, and translating between business and technical teams, is a core part of the role."),
    ("Can you lead a migration programme?", "Yes: strategy, impact assessment, dependencies, cutover planning, business readiness, testing governance, communications, training, hypercare and decommissioning planning, working alongside your technical teams and partners."),
    ("How do you identify automation opportunities?", "We map candidate processes, measure volumes, delays and manual touches, simplify the process first, then assess automation suitability, data and control risks, and indicative benefits."),
    ("Can you help us adopt Microsoft Copilot?", "Yes: readiness and permissions review, governance and acceptable-use controls, use cases, user training and adoption measurement."),
    ("What is included in target operating-model design?", "A current-state assessment, blueprint, capability map, process architecture, roles and responsibilities, governance model, technology implications, transition roadmap, implementation work packages and a benefits and KPI framework."),
    ("Can you recover a delayed or struggling programme?", "Yes. We start with an independent review of scope, plan, governance, risks and stakeholder alignment, then agree a recovery plan and, if required, lead its delivery."),
    ("Do you provide cybersecurity testing?", "No. We lead cybersecurity change programmes and control implementation. Penetration testing, security monitoring and managed detection are provided by specialist partners or your internal teams."),
    ("Can you support remote and hybrid working?", "Yes, covering technology, ways of working, processes, information access, security, onboarding and adoption, not just collaboration tools."),
    ("How do you measure cost reduction?", "We establish a baseline at the start, covering cycle time, cost per transaction, manual touches, error and rework rates and staff capacity, agree how progress will be evaluated, and report against it. We don't promise a percentage saving before an assessment."),
    ("Can you work on a fractional basis?", "Yes. Change Delivery Leadership provides senior leadership for a defined number of days each month, and Virtual Consultancy offers monthly plans from £1,450 for smaller pieces of work."),
    ("How quickly can you start?", "A Cost-Leakage Audit or Specialist Sprint can usually begin within one to two weeks of agreement, subject to stakeholder availability and access."),
    ("What information is required to produce a proposal?", "Your objectives, the scope and scale of the change (functions, sites, systems and users), key stakeholders, known constraints and timescales, and any existing plans or supplier arrangements. A discovery call is usually enough to produce an outline proposal."),
]
lt_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in LT_FAQ)

logistics = f"""    <section class="hero home-hero">
      <div class="container hero-grid">
        <div>
          <h1><span class="h1-kicker">Technology-enabled transformation for logistics</span>Modernise operations. Simplify processes. <em class="ember">Deliver change with confidence.</em></h1>
          <p class="lead">Bespoke Vista helps logistics and operational organisations automate work, adopt AI, strengthen cybersecurity, migrate technology and design more efficient operating models.</p>
          <p class="support">From early-stage strategy through implementation and adoption, we connect business needs, operational processes and technology to produce change that works in practice.</p>
          <div class="hero-actions">
            {btn("Book a Discovery Call", DISCOVERY_HREF, "btn-ember")}
            {btn("Explore Our Transformation Services", "#services", "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">25+ years bridging business, technology and complex change.</p>
        </div>
        <div class="hero-art">
          {horizon(["PEOPLE", "PROCESS", "DATA", "TECHNOLOGY"], "A sun rising over a horizon, marked people, process, data and technology")}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="who">
      <div class="container">
        <div class="head">
          <div>{label("Who we work with")}<h2>Organisations where operations, partners and technology are <em class="ember">tightly connected.</em></h2></div>
          <p>We help logistics and operational organisations simplify processes, implement technology and deliver complex change.</p>
        </div>
        <div class="grid g2">
          <div class="reveal"><h3>Organisations</h3><ul class="chips">{''.join(f'<li>{x}</li>' for x in LT_ORGS)}</ul></div>
          <div class="reveal"><h3>Leaders we typically work with</h3><ul class="chips">{''.join(f'<li>{x}</li>' for x in LT_BUYERS)}</ul></div>
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Common challenges")}<h2>Where change tends to <em class="ember">get stuck.</em></h2></div>
          <p>These are the situations that usually prompt a first conversation. Most involve people, process, data and technology at the same time.</p>
        </div>
        <div class="grid g4">
{lt_challenges}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="services">
      <div class="container">
        <div class="head">
          <div>{label("Transformation services")}<h2>Eight ways we help <em class="ember">deliver change.</em></h2></div>
          <p>Each service can be engaged on its own or as part of a wider programme. Open "Full scope" for detail, typical technologies and what is delivered by partners.</p>
        </div>
        <div class="grid g2 svc-grid">
{lt_services}
        </div>
      </div>
    </section>

    <section class="sec sec-sand" id="keep-running">
      <div class="container split" style="align-items:center">
        <div class="reveal">
          {label("After go-live")}
          <h2>We lead the change. <em class="ember">Our team keeps it running.</em></h2>
          <p>Most transformation support ends at go-live. Ours doesn't have to. Our managed team can take on the PMO reporting, business analysis, process documentation and automation upkeep that keep the new way of working going, under the same UK contract and the same accountable lead.</p>
          <a class="text-link" href="services.html#sprints">See Design &amp; Run, Migrate &amp; Run and Automate &amp; Run →</a>
        </div>
        <ul class="ticks reveal"><li>PMO-in-a-Box from £1,950/month</li><li>Managed Business Analysis from £2,250/month</li><li>Documentation Factory from £2,950</li><li>Automation and AI workflow upkeep, scoped after implementation</li></ul>
      </div>
    </section>

    <section class="sec sec-dark" id="context">
      <div class="container">
        <div class="head">
          <div>{label("Why operational complexity matters")}<h2>Transformation designed for operationally <em class="ember">complex environments.</em></h2></div>
          <p>Logistics businesses operate through interconnected people, partners, processes, systems and data. Even a relatively small technology change can affect customer service, warehouse operations, transport planning, billing, reporting and compliance.</p>
        </div>
        <div class="split">
          <div class="reveal">
            <p>Bespoke Vista brings a business-and-technology perspective to these programmes. We help organisations understand dependencies, simplify processes, define the future operating model and coordinate delivery across operational and technical teams.</p>
            <h3>Typical situations</h3>
            <ul class="ticks">{''.join(f'<li>{x}</li>' for x in LT_SITUATIONS)}</ul>
          </div>
          <div class="not-box reveal">
            <h3>What we don't do</h3>
            <p>We are not a logistics operations consultancy. We don't provide {LT_NOT}.</p>
            <p>Where a programme needs that expertise, it comes from your operational teams or specialist partners. We make sure their decisions are reflected in the processes, systems and operating model we help you change.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="packages">
      <div class="container">
        <div class="head">
          <div>{label("Ways to work with us")}<h2>Clear ways to start, <em class="ember">with clear prices.</em></h2></div>
          <p>The same services we offer every client. Final scope and price are confirmed in writing before work starts.</p>
        </div>
        <div class="tier-cards tier-cards-2">
{chr(10).join(offer_card(OFFER[k]).replace(f' id="{k}"', '') for k in ("audit", "sprints", "pods", "fractional"))}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="approach">
      <div class="container">
        <div class="head">
          <div>{label("Delivery approach")}<h2>Understand. Simplify. Design. <em class="ember">Deliver. Embed.</em></h2></div>
          <p>Transformation isn't complete when the technology goes live. It's complete when the new way of working operates reliably and produces the intended business outcome.</p>
        </div>
        <div class="steps steps5">
{lt_method}
        </div>
      </div>
    </section>

    <section class="sec" id="outcomes">
      <div class="container split">
        <div class="reveal">
          {label("Outcomes and measurement")}
          <h2>Outcomes we help <em class="ember">clients pursue.</em></h2>
          <p>We establish baseline measures at the start of an engagement and agree how progress will be evaluated. We don't guarantee outcomes or quote savings before an assessment.</p>
          <h3>Typical measures</h3>
          <ul class="chips">{''.join(f'<li>{x}</li>' for x in LT_MEASURES)}</ul>
        </div>
        <ul class="ticks reveal">{''.join(f'<li>{x}</li>' for x in LT_OUTCOMES)}</ul>
      </div>
    </section>

    <section class="sec sec-sand" id="founder">
      <div class="container split">
        <div class="reveal">
          {label("Founder")}
          <h2>Experience at the intersection of business, technology <em class="ember">and change.</em></h2>
          <p>Azeem Mushtaq has more than 25 years of experience working between business and technology teams. His expertise centres on automation, AI adoption, cybersecurity implementation, migration, target operating-model design, process simplification and the delivery of complex change.</p>
          <p>His role is to turn strategic objectives into practical delivery: understanding the current operation, defining the future state, aligning stakeholders, managing dependencies and ensuring that technology change produces a usable business outcome.</p>
          {btn("Book a Discovery Call", DISCOVERY_HREF, "btn-primary")}
        </div>
        <aside class="profile reveal" aria-label="Founder profile">
          {owner("professional photograph of Azeem.")}
          <div class="avatar" aria-hidden="true">AM</div>
          <h3>Azeem Mushtaq</h3>
          <p class="role">Founder · Business and technology transformation</p>
          <ul class="chips">{''.join(f'<li>{x}</li>' for x in LT_EXPERTISE)}</ul>
          {f'<p style="margin-top:18px"><a href="{LINKEDIN_URL}" rel="noopener">View LinkedIn profile →</a></p>' if LINKEDIN_URL else owner("LinkedIn profile URL.")}
          {owner("verified project examples, industry experience, qualifications, certifications and client recommendations.")}
        </aside>
      </div>
    </section>

    <section class="sec" id="proof">
      <div class="container">
        <div class="head">
          <div>{label("Evidence")}<h2>Illustrative transformation <em class="ember">scenario.</em></h2></div>
          <p>Verified, anonymised case studies will be published here with client permission.</p>
        </div>
        <article class="scenario reveal">
          <div class="scenario-head">
            <span class="status s-future">Illustrative transformation scenario</span>
            <h3>Replacing a legacy operational system and automating exception handling</h3>
            <p class="small"><strong>This scenario illustrates how the service may be applied and is not presented as an actual client engagement.</strong></p>
          </div>
          <dl>{lt_scenario}</dl>
        </article>
        {owner("verified case studies: client context, business problem, Azeem's role, complexity, approach, deliverables, measured result and lessons learned. Use descriptions such as 'national logistics organisation' only where factually true.")}
      </div>
    </section>

    <section class="sec sec-white" id="faq">
      <div class="container split">
        <div>{label("FAQs")}<h2>Straight answers.</h2><p class="muted">Something else? <a href="{DISCOVERY_HREF}">Book a discovery call.</a></p></div>
        <div class="faq">
{lt_faq}
        </div>
      </div>
    </section>

{cta("Talk through your transformation priorities.", "A free 20-minute discovery call to understand your objectives, constraints and options. If it's a good fit, we'll propose a fixed-fee audit or Specialist Sprint with clear outputs.", ("Book a Discovery Call", DISCOVERY_HREF), ("Explore Our Transformation Services", "#services"))}

    <section class="sec-tight" id="company">
      <div class="container">
        <div class="company reveal">
          <div>
            <h3>Bespoke Vista Ltd</h3>
            <p>Registered in England and Wales.{f' Company number {COMPANY_NUMBER}.' if COMPANY_NUMBER else ''}</p>
            {f'<p>Registered office: {REGISTERED_OFFICE}</p>' if REGISTERED_OFFICE else owner("company number and registered office address.")}
          </div>
          <div>
            <h3>Contact</h3>
            <p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
            <p><a href="contact.html">Contact form</a> · <a href="privacy.html">Privacy notice</a></p>
          </div>
          <div>
            <h3>Other services</h3>
            <p><a href="services.html#pods">Managed PMO, business analysis and documentation</a></p>
            <p><a href="pricing.html">All prices and terms</a></p>
          </div>
        </div>
      </div>
    </section>"""

page("logistics.html", "Technology and Transformation for Logistics",
     "Bespoke Vista helps logistics and operational organisations automate processes, adopt AI, strengthen cybersecurity, migrate technology and deliver complex change.",
     logistics, full_title="Technology Transformation for Logistics | Bespoke Vista",
     schema=[svc_schema("Technology-enabled transformation for logistics", "Process automation, AI adoption, cybersecurity implementation, technology migration, target operating-model design, process simplification and complex change delivery for logistics and operational organisations.", "1500"),
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in LT_FAQ]}])

# ============================================================== PMO-IN-A-BOX LANDING PAGE
PMO_CYCLE = [
    ("Monday", "Project updates collected from your project managers against a standard template"),
    ("Tuesday", "RAID logs and action trackers updated; overdue actions chased"),
    ("Wednesday", "Portfolio dashboard refreshed; exceptions flagged to your UK lead"),
    ("Thursday", "Governance-meeting pack prepared and quality-checked"),
    ("Monthly", "Service review with your UK lead: outputs, service levels, risks and improvements"),
]
pmo_cycle = "".join(f"<tr><th scope=\"row\">{d}</th><td>{a}</td></tr>" for d, a in PMO_CYCLE)

PMO_NOT = ["It doesn't replace your project managers or their accountability for delivery",
           "It isn't unlimited: each package has a project limit and monthly capacity",
           "It isn't software: we use your Microsoft 365 tools, or others by agreement",
           "It doesn't make decisions for you: it makes sure the right decisions are visible on time"]

PMO_FAQ = [
    ("What do our project managers need to do?", "Provide updates by an agreed day each week or month, using a short template we set up. We do the chasing, consolidation, RAID upkeep and reporting."),
    ("Which tools do you use?", "Your Microsoft 365 environment by default: SharePoint, Teams, Excel and Planner, with Power BI where you hold licences. Smartsheet, Jira or similar by agreement."),
    ("Can you attend our governance meetings?", "Your UK lead can attend governance meetings where agreed. The delivery team prepares packs, logs and dashboards behind them."),
    ("What if we have more than ten projects?", "The Transformation Office package covers multiple workstreams with a dedicated PMO analyst, from £7,500 a month, scoped in a proposal."),
    ("How do we start?", "With an Offshoring Readiness Blueprint, then a 60-day pod onboarding covering a few projects, then a Foundation or Managed package month to month."),
]
pmo_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in PMO_FAQ)

pmo_page = f"""    <section class="hero home-hero">
      <div class="container hero-grid">
        <div>
          {label("PMO-in-a-Box · from £1,950 a month")}
          <h1>A working PMO for 3 to 15 projects, <em class="ember">without hiring one.</em></h1>
          <p class="lead">Governance, RAID management and portfolio reporting, run for you as a managed service by a UK-led, office-based team.</p>
          <p class="support">Defined monthly capacity. Weekly or monthly reporting. A UK-led service review every month.</p>
          <div class="hero-actions">
            {btn("Discuss Your Project Portfolio", "contact.html?topic=pmo", "btn-ember")}
            {btn("Get Your Offshore Blueprint", ASSESS_HREF, "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">UK-managed. One contract. Clear service levels.</p>
        </div>
        <div class="hero-art">
          {horizon(["RAID", "REPORT", "GOVERN", "REVIEW"])}
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container split">
        <div class="reveal">
          {label("How it runs")}
          <h2>Your weekly <em class="ember">PMO rhythm.</em></h2>
          <p>An example cycle for the Managed package. Foundation runs the same activities on a monthly cycle. Days are agreed with you.</p>
          <p class="small muted">Illustrative example; your schedule is set out in your service definition.</p>
        </div>
        <div class="table-wrap table-light reveal"><table class="sla"><tbody>{pmo_cycle}</tbody></table></div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
{product_block(PMO)}
{boundaries_table(PMO)}
      </div>
    </section>

    <section class="sec sec-sand">
      <div class="container split">
        <div class="reveal">
          {label("Clear boundaries")}
          <h2>What PMO-in-a-Box <em class="ember">isn't.</em></h2>
          <p>Being clear about limits is what keeps a managed PMO working well.</p>
        </div>
        <ul class="ticks warn reveal">{''.join(f'<li>{x}</li>' for x in PMO_NOT)}</ul>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Example outputs")}<h2>See what you <em class="ember">will receive.</em></h2></div>
          <p>Illustrative examples, not actual client deliverables.</p>
        </div>
        <div class="grid g3">
{chr(10).join(f'''          <a class="card sample-link reveal" href="samples.html#{sid}" data-track="sample_view"><span class="ill">Illustrative example</span><h3>{t}</h3><p>{d}</p><span class="more">View sample →</span></a>''' for sid, t, d in SAMPLES if sid in ("pmo-dashboard", "raid", "service-report"))}
        </div>
      </div>
    </section>

    <section class="sec sec-white">
      <div class="container">
        <article class="scenario reveal">
          <div class="scenario-head">
            <span class="status s-future">Illustrative delivery scenario</span>
            <h3>PMO-in-a-Box for a UK logistics business</h3>
            <p class="small"><strong>This example demonstrates how the service operates and is not presented as an actual client engagement.</strong></p>
          </div>
          <dl>{scenario_html}</dl>
        </article>
        {('<div style="margin-top:32px">' + FOUNDING_BOX + '</div>') if FOUNDING_PLACES else ''}
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="container split">
        <div>{label("FAQs")}<h2>PMO-in-a-Box questions.</h2><p class="muted"><a href="managed-teams.html#faq">All FAQs →</a></p></div>
        <div class="faq">
{pmo_faq}
        </div>
      </div>
    </section>

{cta("Start with a blueprint for your project portfolio.", "We review your projects, reporting and governance, recommend the right package and plan the 60-day onboarding. The fee is credited against your first month if you proceed within 30 days.", ("Get Your Offshore Blueprint", ASSESS_HREF), ("Discuss Your Project Portfolio", "contact.html?topic=pmo"))}"""

page("pmo-in-a-box.html", "PMO-in-a-Box",
     "PMO-in-a-Box: a managed PMO for UK organisations running 3 to 15 projects. RAID, reporting and governance from £1,950 a month, as a UK-led managed service.",
     pmo_page, full_title="PMO-in-a-Box: Managed and Outsourced PMO Service UK | Bespoke Vista",
     schema=[svc_schema("PMO-in-a-Box", PMO[3], "1950"),
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PMO_FAQ]}])

# ============================================================== VIRTUAL CONSULTANCY
VC_EXAMPLES = [
    ("A system or supplier change", "One phase of a roll-out: plan, readiness actions, supplier follow-up and go-live checklist."),
    ("A process or policy roll-out", "A new way of working introduced across teams, with owners, dates and evidence of completion."),
    ("A migration or cut-over plan", "Tasks, dependencies and decisions tracked so nothing is missed on the day."),
    ("An audit or improvement action plan", "Findings turned into owned actions, followed up and reported to leadership."),
    ("A Copilot or automation pilot", "Use cases, users, guidance, feedback and a recommendation at the end."),
    ("A project without a project manager", "A small, important piece of work that keeps slipping behind the day job."),
]
VC_TRIAL_STEPS = [
    ("Day 1", "Kick-off", "A 60-minute Teams call with your senior consultant: the outcome you need, the people involved, deadlines and constraints."),
    ("Days 2–3", "Plan agreed", "A one-page work-package plan with milestones, owners and dates, plus a RAID and action log in your Microsoft 365."),
    ("Days 4–9", "Run", "Your coordinator follows up actions with your team, keeps the log current and flags anything at risk to your senior consultant."),
    ("Day 10", "Review", "Status report, lessons and a recommendation: continue on a plan, change the approach, or stop. No obligation."),
]
VC_NOT = ["It isn't a virtual-assistant or admin service: every plan is led by a senior consultant",
          "It isn't staff supply: you don't manage our people, we deliver the agreed outputs",
          "It doesn't take over your accountability: you own decisions, we make sure they're visible and acted on",
          "It isn't unlimited: each plan has a work-package limit and monthly hours",
          "It doesn't include specialist technical build, penetration testing or legal and financial advice"]
VC_FAQ = [
    ("What counts as a work package?", "A defined piece of work with an outcome, an owner on your side and an end date, such as one phase of a system roll-out, a process change across teams or an audit action plan. If it's bigger than that, we'll suggest splitting it, or a Specialist Sprint."),
    ("Who will we work with?", "A senior UK consultant who leads the plan, attends key meetings and reviews every report, and a named delivery coordinator from our office-based team in Lahore who keeps the logs, follows up actions and prepares reports."),
    ("Is it all online?", "Yes. We work through Microsoft Teams, with documents in your SharePoint or a workspace we set up for you. Your senior consultant works UK hours. Your coordinator's day starts before the UK's, so updates are ready when your day starts."),
    ("What happens at the end of the trial?", "You receive a status report and a recommendation. If you subscribe within 30 days, the £950 is credited in full against your first month. If not, there's nothing further to pay."),
    ("Can we change plan or cancel?", "Yes. You can move up or down a plan from the next month. After the one-month minimum term, give 30 days' notice to cancel."),
    ("Do unused hours roll over?", "No. Each plan includes a set amount of senior and coordinator time each month. Extra time can be agreed in advance at a quoted price."),
    ("How is this different from PMO-in-a-Box?", "PMO-in-a-Box runs governance and reporting across a portfolio of projects your own project managers lead. Virtual Consultancy manages specific work packages for you, with senior consultant time included."),
    ("How do we pay?", "The trial is invoiced in advance. Subscriptions are invoiced monthly in advance. No payment is taken on this website: we confirm scope with you first."),
    ("How do you protect our information?", "Confidentiality agreements, access only to what the work needs, multi-factor authentication and no client data in public AI tools. See <a href=\"managed-teams.html#security\">security and data protection</a>."),
]
vc_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in VC_FAQ)
vc_examples = "\n".join(f'          <div class="card reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in VC_EXAMPLES)
vc_steps = "\n".join(f'          <div class="reveal"><span class="small muted">{d}</span><h3>{t}</h3><p>{x}</p></div>' for d, t, x in VC_TRIAL_STEPS)
vc_plan_opts = "".join(f'<option value="{v}">{l}</option>' for v, l in
                       [("trial", "Two-Week Work Package Trial (£950)"), ("essentials", "Essentials (£1,450/month)"),
                        ("professional", "Professional (£2,950/month)"), ("partner", "Partner (£5,450/month)"),
                        ("not-sure", "Not sure yet: please advise")])

virtual = f"""    <section class="hero home-hero">
      <div class="container hero-grid">
        <div>
          {label("Virtual Consultancy · trial £950 · plans from £1,450/month")}
          <h1>Your work package, managed. <em class="ember">Senior-led and fully online.</em></h1>
          <p class="lead">Give us a defined piece of work: a system roll-out phase, a process change, an audit action plan. We plan it, follow up the actions and report on it through your Microsoft Teams, led by a senior UK consultant with a named delivery coordinator.</p>
          <p class="support">Try it on one work package for two weeks at a fixed price. Or subscribe for a standing virtual consultancy, by the month.</p>
          <div class="hero-actions">
            {btn("Book a Two-Week Trial", TRIAL_HREF, "btn-ember")}
            {btn("Compare Monthly Plans", "#plans", "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">{USP}</p>
        </div>
        <div class="hero-art">
          {horizon(["SCOPE", "PLAN", "TRACK", "REPORT"], "A sun rising over a horizon, marking scope, plan, track and report")}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="work-packages">
      <div class="container">
        <div class="head">
          <div>{label("What we manage")}<h2>Work that matters, <em class="ember">but nobody has time to run.</em></h2></div>
          <p>A work package is a defined piece of work with an outcome, an owner on your side and an end date. Typical examples:</p>
        </div>
        <div class="grid g3">
{vc_examples}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="head">
          <div>{label("Who does what")}<h2>A senior lead and a coordinator, <em class="ember">for the price of neither.</em></h2></div>
          <p>The same model as the rest of Bespoke Vista: we lead the change, our team keeps it running.</p>
        </div>
        <div class="leadrun">
          <div class="lr-panel reveal">
            <span class="lr-tag">UK · Senior consultant</span>
            <h3>Your senior consultant</h3>
            <ul class="ticks compact"><li>Shapes the plan and agrees it with you</li><li>Makes the judgement calls and raises the hard questions</li><li>Joins check-ins and key meetings</li><li>Reviews every report before you see it</li></ul>
          </div>
          <div class="lr-join" aria-hidden="true"><span>One plan<br>One channel<br>One monthly fee</span></div>
          <div class="lr-panel lr-run reveal">
            <span class="lr-tag">Coordinator · Managed team</span>
            <h3>Your named coordinator</h3>
            <ul class="ticks compact"><li>Keeps the RAID and action log current</li><li>Follows up actions with your team, by agreement</li><li>Prepares status reports and meeting packs</li><li>Keeps documents organised in your SharePoint</li></ul>
          </div>
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="trial" style="scroll-margin-top:100px">
      <div class="container">
        <div class="head">
          <div>{label("Option 1 · Try it")}<h2>Two weeks. One work package. <em class="ember">Fixed price.</em></h2></div>
          <p>See how we work on something real before you commit to anything.</p>
        </div>
        <div class="grid g2" style="align-items:start">
{offer_card(VC_TRIAL, "Book a Two-Week Trial", TRIAL_HREF, "Try it first", "featured")}
          <div class="reveal">
            <h3>How the two weeks run</h3>
            <div class="steps" style="grid-template-columns:1fr 1fr;margin-top:20px">
{vc_steps}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="plans" style="scroll-margin-top:100px">
      <div class="container">
        <div class="head">
          <div>{label("Option 2 · Subscribe")}<h2>A standing virtual consultancy, <em class="ember">by the month.</em></h2></div>
          <p>One-month minimum, then monthly with 30 days' notice. Move up or down a plan from the next month. All prices exclude VAT.</p>
        </div>
{product_block(VIRTUAL, cta=vc_cta)}
        <p class="small muted" style="margin-top:16px">Hours and coordinator days are monthly maximums and don't roll over. Extra time can be agreed in advance at a quoted price. Software licences are not included.</p>
      </div>
    </section>

    <section class="sec sec-sand">
      <div class="container split">
        <div class="reveal">
          {label("Clear boundaries")}
          <h2>What Virtual Consultancy <em class="ember">isn't.</em></h2>
          <p>Bigger or more technical work? Start with a <a href="{DISCOVERY_HREF}">discovery call</a> and we'll suggest the right route, or the right partner.</p>
        </div>
        <ul class="ticks warn reveal">{''.join(f'<li>{x}</li>' for x in VC_NOT)}</ul>
      </div>
    </section>

    <section class="sec sec-white" id="book" style="scroll-margin-top:100px">
      <div class="container contact-grid">
        <div class="reveal">
          {label("Book or subscribe")}
          <h2>Tell us about <em class="ember">the work package.</em></h2>
          <ol class="next-steps">
            <li>We reply within one working day to confirm scope, or to ask a few questions on a short call.</li>
            <li>We send a one-page scope and the terms for your trial or plan.</li>
            <li>Once you approve, we invoice and book your kick-off, usually within five working days.</li>
          </ol>
          <p class="small muted">No payment is taken on this website. Nothing starts until you've approved the scope in writing.</p>
        </div>
        <form class="form reveal" id="virtual-form" data-email="{CONTACT_EMAIL}" data-endpoint="" data-event="virtual_request_submit" data-subject-from="plan" novalidate>
          <input type="hidden" name="topic" value="virtual-consultancy">
          <div class="form-row">
            <div class="field"><label for="vc-name">Name *</label><input id="vc-name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="vc-org">Organisation</label><input id="vc-org" name="organisation" type="text" autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="vc-email">Work email *</label><input id="vc-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="vc-phone">Phone</label><input id="vc-phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="vc-plan">Trial or plan *</label><select id="vc-plan" name="plan" data-param="plan" required>{vc_plan_opts}</select></div>
            <div class="field"><label for="vc-start">Preferred start</label><select id="vc-start" name="start"><option>As soon as possible</option><option>In 2 to 4 weeks</option><option>Next month or later</option></select></div>
          </div>
          <div class="field"><label for="vc-message">The work package *</label><textarea id="vc-message" name="message" required placeholder="What needs to happen, by when, who is involved on your side, and what's getting in the way."></textarea></div>
          <button class="btn btn-primary" type="submit">Send Trial or Plan Request {ARR}</button>
          <p class="form-mode small"></p>
          <p class="form-note">We use your details only to respond to your request. See our <a href="privacy.html">privacy notice</a>.</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="container split">
        <div>{label("FAQs")}<h2>Virtual Consultancy questions.</h2><p class="muted"><a href="managed-teams.html#faq">All FAQs →</a></p></div>
        <div class="faq">
{vc_faq}
        </div>
      </div>
    </section>

{cta("Hand us one work package for two weeks.", "A fixed £950 trial, credited in full if you subscribe within 30 days. Or talk it through first on a free 20-minute discovery call.", ("Book a Two-Week Trial", TRIAL_HREF), ("Book a Discovery Call", DISCOVERY_HREF))}"""

page("virtual-consultancy.html", "Virtual Consultancy",
     "Virtual consultancy from Bespoke Vista: a senior UK consultant and a coordinator manage your work packages online. Two-week trial £950, plans from £1,450 a month.",
     virtual, full_title="Virtual Consultancy and Work Package Management | Bespoke Vista",
     schema=[{"@type": "Service", "name": "Virtual Consultancy", "serviceType": "Virtual consultancy and work-package management",
              "provider": {"@id": BASE_URL + "#org"}, "areaServed": "GB",
              "description": "A senior UK consultant and a named coordinator manage defined work packages online: plans, RAID and action logs, follow-up and status reporting.",
              "offers": [{"@type": "Offer", "name": VC_TRIAL[0], "price": "950", "priceCurrency": "GBP"}]
                        + [{"@type": "Offer", "name": f"Virtual Consultancy {t[0]}", "price": t[2].replace("£", "").replace(",", ""), "priceCurrency": "GBP",
                            "priceSpecification": {"@type": "UnitPriceSpecification", "price": t[2].replace("£", "").replace(",", ""), "priceCurrency": "GBP", "unitText": "MONTH"}} for t in VIRTUAL[4]]},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in VC_FAQ]}])

# ============================================================== WEBSITES, APPS AND CONTENT
WA_FAQ = [
    ("Is the Member Portal a finished product?", "The features listed are running today at EmptyHands. We set the portal up for each club with its own name, classes and fees. Features we haven't built yet aren't listed."),
    ("Why is EmptyHands your example?", "EmptyHands is the karate and wellbeing school our founder has run in Ilford since 2006. It's our own school, which is why we can show it openly and test every change there first."),
    ("Who pays the card and PayPal fees?", "You do, at the rates set by those providers. Payments go to your own account, not through us."),
    ("Can we move our existing website?", "Usually, yes. We review it first and quote the move as part of the Business Website price."),
    ("Do you use AI to write content?", "We use AI to help with drafting and ideas. A person edits every piece, and nothing is published without your approval."),
    ("What's the minimum term?", "Member Portal and Content Creation: one month, then 30 days' notice. Business Website is a fixed-price project."),
    ("Can we buy online?", "Where you see a Subscribe button, yes. Otherwise send a request and we'll confirm the set-up and send a payment link, usually within one working day."),
]
wa_faq = "\n".join(f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in WA_FAQ)
wa_opts = "".join(f'<option value="{v}">{l}</option>' for v, l in [
    ("portal", "Member Portal (£99/month)"), ("portal-website", "Portal + Website (£179/month)"), ("portal-website-content", "Portal + Website + Content (£299/month)"),
    ("website", "Business Website (from £1,495)"), ("website-care", "Website Care (£49/month)"),
    ("content-starter", "Content Creation: Starter (£295/month)"), ("content-growth", "Content Creation: Growth (£595/month)"),
    ("content-leader", "Content Creation: Leader (£995/month)"), ("not-sure", "Not sure yet: please advise")])
portal_href = lambda t: f"websites-apps.html?product={t.lower().replace(' + ', '-').replace(' ', '-')}#request"

wa = f"""    <section class="hero home-hero">
      <div class="container hero-grid">
        <div>
          {label("Websites, apps and content · from £99 a month")}
          <h1>Your website, your members' app, <em class="ember">your content. Done for you.</em></h1>
          <p class="lead">Practical digital tools for clubs, schools, studios and small businesses: a member app, a clear website and content every month. Proven first at EmptyHands, our founder's own school.</p>
          <div class="hero-actions">
            {btn("See the Member Portal", "#portal", "btn-ember")}
            {btn("See the EmptyHands Case Study", "#emptyhands", "btn-line", arrow=False)}
          </div>
          <p class="tagline-strong">Simple monthly plans. No long contracts.</p>
        </div>
        <div class="hero-art">
          {horizon(["WEBSITE", "APP", "CONTENT", "GROWTH"], "A sun rising over a horizon, marking website, app, content and growth")}
        </div>
      </div>
    </section>

    <section class="sec sec-white" id="emptyhands" style="scroll-margin-top:100px">
      <div class="container split">
        <div class="reveal">
          {label("Case study · real, not illustrative")}
          <h2>EmptyHands, <em class="ember">Ilford.</em></h2>
          <p>EmptyHands is the karate, Tai Chi, yoga and Shiatsu school our founder has run since 2006. We built its website and the EmptyHands Portal, the app its students and parents use every week.</p>
          <p class="small muted">It's our own school, so it's where we test every feature before offering it to anyone else.</p>
          <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px">
            <a class="btn btn-primary" href="{EMPTYHANDS_URL}" target="_blank" rel="noopener">Visit emptyhands.co.uk {ARR}</a>
            <a class="btn btn-line" href="{EMPTYHANDS_APP_URL}" target="_blank" rel="noopener">See the EmptyHands Portal</a>
          </div>
        </div>
        <ul class="ticks reveal">
          <li><strong>Dojo calendar</strong>: training dates, days off and gradings, with a countdown to the next class</li>
          <li><strong>Messages from Sensei</strong>: notices, group chat, training journal and private messages</li>
          <li><strong>Homework</strong>: set by the instructor, ticked off by students</li>
          <li><strong>Fees</strong>: pay per lesson or per month by card or PayPal, with payment history</li>
          <li><strong>On every phone</strong>: installs to the home screen on Android and iPhone</li>
          <li><strong>Controlled sign-up</strong>: new students request an account and the instructor approves it</li>
        </ul>
      </div>
    </section>

    <section class="sec">
      <div class="container">
{product_block(PORTAL, extra='<p style="margin-top:10px" class="small">' + PORTAL_SETUP + '</p>', cta=lambda t: pay_cta("Member Portal", t, portal_href(t)))}
      </div>
    </section>

    <section class="sec sec-white" id="website" style="scroll-margin-top:100px">
      <div class="container">
        <div class="head">
          <div>{label("Websites")}<h2>A website that explains you <em class="ember">in ten seconds.</em></h2></div>
          <p>Written in plain English, built for phones first, and kept up to date afterwards.</p>
        </div>
        <div class="grid g2">
{offer_card(WEBSITE, "Request a Website Quote", "websites-apps.html?product=website#request", "Fixed price", "featured")}
{offer_card(WEBSITE_CARE, *pay_cta("Website Care", None, "websites-apps.html?product=website-care#request", "Request Website Care")[:2])}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="container">
{product_block(CONTENT, extra='<p style="margin-top:10px" class="small">' + CONTENT_NOTE + '</p>', cta=lambda t: pay_cta("Content Creation", t, f"websites-apps.html?product=content-{t.lower()}#request"))}
      </div>
    </section>

    <section class="sec sec-white" id="request" style="scroll-margin-top:100px">
      <div class="container contact-grid">
        <div class="reveal">
          {label("Request")}
          <h2>Tell us what <em class="ember">you need.</em></h2>
          <ol class="next-steps">
            <li>We reply within one working day, with any questions.</li>
            <li>We confirm the set-up and price in writing.</li>
            <li>You pay by secure payment link and we start, usually within five working days.</li>
          </ol>
          <p class="small muted">No payment is taken on this page.</p>
        </div>
        <form class="form reveal" id="build-form" data-email="{CONTACT_EMAIL}" data-endpoint="" data-event="build_request_submit" data-subject-from="product" novalidate>
          <input type="hidden" name="topic" value="websites-apps-content">
          <div class="form-row">
            <div class="field"><label for="wa-name">Name *</label><input id="wa-name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="wa-org">Business, club or school</label><input id="wa-org" name="organisation" type="text" autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="wa-email">Email *</label><input id="wa-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="wa-phone">Phone</label><input id="wa-phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>
          <div class="field"><label for="wa-product">What would you like? *</label><select id="wa-product" name="product" data-param="product" required>{wa_opts}</select></div>
          <div class="field"><label for="wa-message">Tell us a little more *</label><textarea id="wa-message" name="message" required placeholder="What you do, roughly how many members or customers you have, your current website (if any) and when you'd like to start."></textarea></div>
          <button class="btn btn-primary" type="submit">Send Request {ARR}</button>
          <p class="form-mode small"></p>
          <p class="form-note">We use your details only to respond to your request. See our <a href="privacy.html">privacy notice</a>.</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="container split">
        <div>{label("FAQs")}<h2>Websites, apps and content questions.</h2></div>
        <div class="faq">
{wa_faq}
        </div>
      </div>
    </section>

{cta("Want what EmptyHands has?", "Send a request and we'll confirm the set-up, price and start date within one working day.", ("Request the Member Portal", portal_href("Portal")), ("Visit emptyhands.co.uk", EMPTYHANDS_URL))}"""

page("websites-apps.html", "Websites, Apps and Content",
     "Member Portal app for clubs and schools, business websites and monthly content creation from Bespoke Vista. Proven at EmptyHands, Ilford. From £99 a month.",
     wa, full_title="Websites, Member Apps and Content Creation | Bespoke Vista",
     schema=[{"@type": "Service", "name": n, "provider": {"@id": BASE_URL + "#org"}, "areaServed": "GB", "description": d,
              "offers": {"@type": "Offer", "price": pr, "priceCurrency": "GBP"}}
             for n, d, pr in [("Member Portal", "Member app for clubs and schools: calendar, notices, homework and online fees.", "99"),
                              ("Business Website", "Fixed-price small business website.", "1495"),
                              ("Content Creation", "Monthly social posts, articles and newsletters.", "295")]]
            + [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in WA_FAQ]}])

# ============================================================== PRIVACY NOTICE
# Draft privacy notice. Have it reviewed (e.g. by a solicitor or data-protection adviser) before relying on it.
_analytics_on = bool(GA4_ID or CLARITY_ID)
_company_id = "Bespoke Vista Ltd, a company registered in England and Wales"
if COMPANY_NUMBER:
    _company_id += f" (company number {COMPANY_NUMBER})"
if REGISTERED_OFFICE:
    _company_id += f", whose registered office is at {REGISTERED_OFFICE}"

privacy = f"""    <section class="page-hero">
      <div class="container">
        {label("Privacy notice")}
        <h1>How we use <em class="ember">your information.</em></h1>
        <p class="lead">Last updated {PRIVACY_UPDATED}.</p>
      </div>
    </section>

    <section class="sec">
      <div class="container">
        <div class="article legal" style="padding-top:0">
          <h2>Who we are</h2>
          <p>This website is operated by {_company_id} ("Bespoke Vista", "we", "us"). We are the controller of the personal information described in this notice. You can contact us about privacy at <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>

          <h2>What we collect</h2>
          <ul>
            <li><strong>Enquiries:</strong> when you use a form or email us, we receive your name, work email, and any organisation, phone number, organisation size, topic and message you provide.</li>
            <li><strong>Scorecards:</strong> your answers are processed in your browser and are not sent to us. If you request a full report, we receive your name, email, organisation and a summary of your answers and result.</li>
            <li><strong>Bookings:</strong> if you book through our booking page, Microsoft Bookings collects the details you enter on our behalf.</li>
            <li><strong>Technical data:</strong> {"if you accept analytics cookies, Google Analytics and Microsoft Clarity collect information about how you use the site (see Cookies below)." if _analytics_on else "we do not use analytics or tracking cookies on this site."}</li>
          </ul>

          <h2>How we use it, and our lawful basis</h2>
          <ul>
            <li>To respond to your enquiry, send a report you requested and arrange a consultation: <em>legitimate interests</em> in responding to business enquiries, or <em>steps prior to entering into a contract</em> at your request.</li>
            <li>To provide services if you become a client: <em>performance of a contract</em>.</li>
            <li>To keep business records and meet legal obligations: <em>legal obligation</em> and <em>legitimate interests</em>.</li>
            {"<li>To understand how the site is used: <em>consent</em>, which you can withdraw at any time through Cookie settings.</li>" if _analytics_on else ""}
          </ul>
          <p>We do not sell your information or use it for automated decision-making. We will only send you marketing emails if you ask us to, and you can unsubscribe at any time.</p>

          <h2>Who we share it with</h2>
          <ul>
            <li>Our email, document and booking providers (Microsoft 365, including Microsoft Bookings), which process data on our behalf.</li>
            <li>{"The form service we use to receive website enquiries." if FORM_ENDPOINT else "Your own email provider, because our website forms currently open your email app to send your message."}</li>
            <li>Members of our team in our Lahore, Pakistan office who support enquiries and client work. This is an international transfer, protected by appropriate safeguards under UK data-protection law, such as the UK International Data Transfer Agreement or UK Addendum.</li>
            {"<li>Google and Microsoft, for analytics, only if you accept analytics cookies.</li>" if _analytics_on else ""}
            <li>Professional advisers and authorities where required by law.</li>
          </ul>

          <h2>How long we keep it</h2>
          <p>We keep enquiry information for up to 24 months after our last contact, unless you become a client, in which case we keep records for the duration of the contract and for six years afterwards for legal and accounting purposes.</p>

          <h2 id="cookies">Cookies and fonts</h2>
          <p>{"With your consent, we use analytics cookies from Google Analytics and Microsoft Clarity. Nothing is set until you accept, and you can change your choice at any time using Cookie settings in the footer. We store your choice in your browser." if _analytics_on else "We do not set analytics or advertising cookies."} Our pages load fonts from Google Fonts, which means your browser connects to Google's servers and shares your IP address with Google for that purpose.</p>

          <h2>Your rights</h2>
          <p>You have the right to access, correct or erase your personal information, to restrict or object to how we use it, and to data portability. Where we rely on consent, you can withdraw it at any time. To exercise these rights, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. We will respond within one month.</p>
          <p>If you are unhappy with how we handle your information, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/" rel="noopener">ico.org.uk</a>. We would appreciate the chance to resolve your concern first.</p>

          <h2>Changes to this notice</h2>
          <p>We will update this notice when our practices change. The date at the top shows when it was last revised.</p>
          <p class="small muted">This notice covers our website and enquiries. Client personal data processed during an engagement is governed by the Data Processing Agreement in your contract.</p>
        </div>
      </div>
    </section>"""

page("privacy.html", "Privacy Notice",
     "How Bespoke Vista Ltd collects, uses and protects personal information from website visitors and enquiries.",
     privacy)
