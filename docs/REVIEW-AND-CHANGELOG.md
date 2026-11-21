# Bespoke Vista website: review, commercial assessment and change log

Prepared 21 November 2026. Scope: `index.html`, `scorecard.html` and the connected service, pricing and contact pages.
The previous implementation is preserved in git at commit `d2388d9` (restore with `git checkout d2388d9 -- .`).

---

## Commercial assessment: is the model appealing, cost-effective and marketable?

**Short answer: yes, it's marketable. It is also more credible than the previous broad "consulting + subscriptions + products" positioning. It will only be profitable if three constraints are managed.**

### Why it can sell
- **The problem is specific and common.** UK firms with 50–500 staff often run several projects with no PMO, no consistent business analysis and undocumented processes. They feel it every week, and a permanent hire is slow and expensive.
- **The offer is productised and priced.** Buyers can see "£1,950 a month for up to five projects", which is far easier to approve than an open-ended day rate.
- **The entry point is low-risk.** A £495 assessment, then a £1.5–2.5k pilot, are amounts most operations directors can sign off without a procurement process.
- **Transparency about Lahore is a differentiator.** Most offshore suppliers hide location or sell on price. Leading with UK accountability, office-based delivery and visible data-protection controls removes the main objection rather than avoiding it.
- **The founder's background matches the buyer.** Logistics, business architecture and PMO experience give credibility in the first conversation.

### Where the economics are tight (and what to do)
1. **The £495 assessment is underpriced for what it includes.** A workshop, suitability review, capacity model, cost model, pilot recommendation and written findings is realistically 1.5–2 days of senior time. Treat it as a paid qualification step, not a profit line. Keep the written findings to a templated 4–6 page report. After the first 5–10 assessments, consider £695–£995.
2. **The pilot is close to cost.** £1,500–£2,500 for 30 days only works if the scope is one bounded workflow, roughly half an analyst's month plus about two days of UK oversight. Track pilot-to-service conversion: below roughly 50%, pilots become an expensive sales channel.
3. **Azeem's time is the real capacity limit.** Each managed client needs senior UK time every month: service review, quality assurance, escalation and account growth, realistically one to two days. That caps the business at roughly 8–12 clients before a UK delivery or service manager is needed. Plan and price for that hire from the start.

### Monthly pricing sense-check
- **Effective day rates:** PMO-in-a-Box Foundation works out at about £325 per delivery day (£1,950 ÷ 6). Managed BA Essential is about £375 (£2,250 ÷ 6).
- **Against the market:** both sit below typical UK contractor day rates for PMO analysts and business analysts, and the client gets management, quality control and continuity included.
- **Margin:** good if the fully loaded Lahore cost per delivery day stays well below these figures. Check this against your actual salary, office and equipment costs before publishing prices.

### What to sell first
- **Lead with the Documentation Factory and PMO-in-a-Box for logistics firms.** Documentation is fixed-price, tangible and lower in data risk, and it showcases quality. It is also the natural precursor to every other service, because you can't hand over work that isn't written down.
- **Expect Managed Business Analysis to be the hardest sell.** It is the most stakeholder-facing, so buyers will want to know who runs workshops. The answer, the UK lead, needs to be explicit in proposals.

### Proof is the biggest gap
- **The site cannot yet show a real managed-service result.** Offer your first two or three clients a founding-client rate in exchange for a published case study and testimonial, with written permission.
- **Get Cyber Essentials early.** It is quick and inexpensive, and mid-market procurement will ask for it before signing any managed service.

### Channels that fit this model
- LinkedIn outreach to UK operations, transformation and PMO leads in logistics and professional services.
- Partnerships with warehouse-system, transport-system and Microsoft partners, who regularly need extra business analysis, PMO and documentation capacity on their implementations.
- The readiness scorecard as the main lead magnet, followed by a results-review call.

### My view on the recommendations in the brief
Most of the brief was sound and is implemented. Where I deviated, and why:
- **Scorecard band name:** "Not yet ready for managed offshore delivery" became "Not yet ready for managed delivery". Leading with "offshore" in a negative result works against the positioning.
- **Review-cycle conflict:** the standard SOP definition (up to two review cycles) contradicted the Process Starter package (one review cycle). The site now says review cycles are "as stated in the package (a maximum of two per SOP)".
- **Section count:** sixteen homepage sections is long. They are all present but kept compact. Once analytics are live, check scroll depth and consider moving methodology and the company details lower or onto other pages.
- **Placeholders:** visible placeholders damage trust on a public site. They are controlled by one switch (`SHOW_OWNER_PLACEHOLDERS` in `build.py`): turn it off and missing items are hidden rather than shown.
- **Secondary offers:** subscriptions, DojoOS, training and the "Advise / Build / Run / Learn" framing were removed from the homepage. They remain on the pricing and services pages, so they no longer compete with the core offer.

---

## Part 1: Review of the site before these changes

| # | Severity | Issue | Why it matters | Change made | File / section |
|---|---|---|---|---|---|
| 1 | Critical | Forms had no backend; they opened the visitor's email app without saying so | Visitors could believe an enquiry was sent when it wasn't | Every form now states on screen that it opens the email app, and switches automatically to direct sending once `FORM_ENDPOINT` is set | `contact.html`, scorecards, `insights.html`, `main.js` |
| 2 | Critical | Prices contradicted the new commercial model (assessment £1,950, 60-day pilot £3,000, Managed PMO £1,500) | Mixed prices undermine trust and cause disputes | One price catalogue in `build.py` feeds every page | All pages |
| 3 | Critical | Security and contract claims stated as fact without evidence (DPA, transfer safeguards, confidentiality, "service credits") | Misrepresentation risk | Security section separates contractual commitments, controls being implemented and certification objectives, with owner confirmation notes; "service credits" removed | Home `#security`, `managed-teams.html` |
| 4 | Critical | "Lahore team working now" live status implied an active team | Potentially misleading if a team is not yet established | Changed to "Lahore office hours" | `main.js`, clocks |
| 5 | Critical | No privacy notice while collecting personal data | UK GDPR transparency requirement | Placeholder added; listed as required before publication | Contact form |
| 6 | High | Homepage sold everything (four pillars, three subscriptions, DojoOS, 13-sector marquee) | Dilutes the offer; the visitor can't tell what you do in 30 seconds | Homepage rebuilt around three managed services and the assessment → pilot route | `index.html` |
| 7 | High | Vague hero ("Strategy that gets done") | Didn't say what, for whom, where or how much | New hero with offer, delivery location, accountability and a price strip | Home hero |
| 8 | High | "Most popular" badges implied a sales history | Unsupported claim | Replaced with "Recommended" | `pricing.html` |
| 9 | High | Unqualified "mobilised in 2 to 4 weeks" | Over-promise | Qualified wording with dependencies listed | Home, delivery model, FAQ, about |
| 10 | High | No package boundaries (capacity, exclusions, term, licences) | Implies unlimited work and invites scope disputes | Boundaries and terms tables for each core service, plus a commercial-terms block | `pricing.html` |
| 11 | High | No founder credibility or proof on the homepage | Trust gap for a new provider | Founder section, illustrative scenario (clearly labelled), link to experience page | Home |
| 12 | High | Scorecard result gave a score but no risks, actions or next step; bands weren't about delivery readiness | Weak conversion; low perceived value | New 10-dimension, 13-question scorecard with four bands, risks, three actions, service, next step, download and email | `scorecard.html`, `main.js` |
| 13 | High | Keyboard bug: arrow keys auto-advanced scorecard questions | Keyboard users skipped questions | Auto-advance now only on pointer selection | `main.js` |
| 14 | High | No sample deliverables | Buyers can't see what they would receive | New `samples.html` with eight illustrative samples, each labelled | `samples.html` |
| 15 | Medium | No canonical URLs, structured data or absolute OG image | Weaker search and social previews | Canonical, OG and Twitter tags; Organization, ProfessionalService, Service, FAQPage and BreadcrumbList JSON-LD | `build.py` `page()` |
| 16 | Medium | No analytics or conversion events beyond dataLayer | Can't measure the funnel | GA4 and Clarity injected when IDs are set; events wired | `build.py`, `main.js` |
| 17 | Medium | Continuous animations (marquee, rotating ring) | Distracting; brief asked for minimal motion | Marquee removed from home; ring static; reduced-motion respected | CSS |
| 18 | Medium | "Book a call" and several competing CTAs | Diluted conversion | One principal CTA ("Book a Managed Operations Assessment") plus defined secondary CTAs | Site-wide |
| 19 | Medium | Footer lacked company number and registered office | Legal requirement for UK company websites | Config fields added; shown when completed | Footer |
| 20 | Low | Ember button text contrast 4.48:1 at the red end | Just under WCAG AA | Button gradient end adjusted (5.16:1) | CSS |
| 21 | Low | Long buttons overflowed small phones | Horizontal scroll | Buttons wrap on narrow screens | CSS |
| 22 | Low | Footer logo not lazy-loaded; script not deferred | Minor performance | `loading="lazy"`, `defer` | `build.py` |

What already worked and was kept:
- The visual identity: paper, ink and ember, the Fraunces type and the rising-sun artwork.
- The data-driven scorecard engine.
- The London/Lahore clocks and follow-the-sun timeline.
- The sticky jump bars, mobile navigation and the single-source build.

---

## Part 2: Revised commercial positioning

- **Positioning statement:** Bespoke Vista gives UK organisations the business analysis, PMO and process capability they need without the cost and delay of building another internal department.
- **Headline:** Build the capability you need, without building another department.
- **Subheadline:** Bespoke Vista provides UK-led business analysis, PMO, process documentation and AI-enabled operational services, delivered by managed teams in our Lahore office.
- **Supporting message:** Senior UK oversight. Office-based delivery. Defined outputs, transparent pricing and accountable service management.
- **Trust line:** UK-managed. Lahore-delivered. AI-enabled.
- **Target customers:**
  - UK logistics and supply-chain businesses with 50 to 500 employees.
  - Organisations running 3 to 15 projects without a consistent PMO.
  - Change teams short of business analysts.
  - Organisations with undocumented processes.
  - Professional-services firms that need repeatable procedures.
  - Organisations that want practical AI automation.
- **Primary services:**
  - PMO-in-a-Box: £1,950 / £3,950 / from £7,500 a month.
  - Managed Business Analysis: £2,250 / £4,250 / from £7,500 a month.
  - Documentation Factory: £2,950 / £5,950 / from £9,500 fixed price.
- **Entry offer:** Managed Operations Assessment, £495, credited against a qualifying pilot commissioned within 30 days.
- **Paid pilot:** 30-Day Managed Delivery Pilot, £1,500–£2,500.
- **Secondary AI services:** AI Operations Discovery (£2,500) and AI Workflow Implementation (£5,000–£15,000).
- **Calls to action:**
  - Principal: "Book a Managed Operations Assessment".
  - Secondary: "Take the Free Readiness Scorecard", "Start a 30-Day Pilot", "View a Sample Deliverable" and "Discuss Your Project Portfolio".
- **Conversion journey:** Free scorecard → £495 assessment → £1,500–£2,500 pilot → managed service from £1,950 a month → further workstreams.

## Part 3: Replacement copy

The full, publication-ready copy is implemented in `index.html` and generated from `build.py`. The homepage sections are:

1. Hero with price strip.
2. Who we work with.
3. Six common problems.
4. Three services, each with tiers and boundaries.
5. Free readiness scorecard.
6. Low-risk route, with the assessment and pilot offers.
7. "UK-managed. Lahore-delivered. AI-enabled." delivery model, including mobilisation wording.
8. "See what you will receive" samples.
9. AI-enabled delivery, including AI rules and two AI services.
10. "How we protect your operations and data".
11. "Senior UK oversight from first conversation to final delivery".
12. Delivery methodology.
13. Evidence, with an illustrative delivery scenario and its required disclaimer.
14. Eighteen FAQs.
15. Final CTA.
16. Company and contact details.

Unverified information appears only as clearly marked owner placeholders.

## Part 4: Page design

- **Desktop:**
  - Two-column hero: copy on the left, the horizon artwork (labelled Assess, Pilot, Run, Scale) on the right.
  - A four-column price and founder strip under the hero.
  - Alternating paper, white, sand and ink section bands.
  - Three equal-height service cards, each with tier rows and a link to its boundaries table.
  - A five-step ladder above the assessment and pilot offer cards.
  - An eight-point delivery grid, then the timeline beside the mobilisation text.
  - A three-column security grid with status chips.
  - The founder copy beside a profile card.
- **Mobile:**
  - Single column. The hero copy comes before the artwork, so the offer is read first.
  - Full-width buttons and a collapsible menu.
  - Tables scroll horizontally inside their own container, so the page never scrolls sideways.
- **Pricing:**
  - Starting prices on the homepage.
  - Full tiers, a boundaries table per service and the commercial terms on `pricing.html`.
  - Every price marked "ex VAT".
- **Calls to action:**
  - Header: the principal CTA ("Book an Assessment") and the scorecard.
  - Hero: both CTAs.
  - Each service card has its own CTA.
  - Assessment and pilot cards, the founder section and the final CTA band.
- **Trust signals:**
  - UK company details and the named founder.
  - Security status chips.
  - Illustrative labels on all samples.
  - No logos, stock photos or testimonials until verified.

## Part 5: Code implementation

Changed files are listed in Part 8. All pages are generated by `build.py` and committed as static HTML, which suits GitHub Pages. No third-party JavaScript is used, apart from optional GA4 and Clarity, which load only when their IDs are set.

## Part 6: Quality assurance results

| Check | Result |
|---|---|
| Desktop (1366px), tablet (820px), mobile (390px) | No horizontal overflow on any of the 11 pages |
| JavaScript errors | None (Playwright, all pages, three viewports) |
| Scorecard logic | All lowest answers → 0 (Not yet ready); all second → 33 (Controlled pilot); all third → 67 (Managed service); all highest → 100 (Scaled delivery). Band boundaries 30 / 55 / 75 |
| Result download | Generates `bespoke-vista-operations-scorecard-result.txt` |
| Keyboard | Arrow keys change the answer without skipping questions; Tab reaches Next; skip link, focus states and Escape-to-close menu work |
| Colour contrast | Body 11.5:1; muted 5.4:1; accent 4.7:1; slate on ink 7.3:1; button text 5.2–8.3:1 |
| Links and anchors | All internal links and anchors resolve (automated check) |
| Button destinations | All CTAs lead to real pages, anchors or the pre-filled contact form; the booking CTA switches to Microsoft Bookings when configured |
| Forms | Honest mode text; email-app fallback works; endpoint mode ready once configured |
| Metadata | Unique titles and descriptions, canonical, OG and Twitter tags on every page |
| Structured data | JSON-LD parses on every page: Organization, ProfessionalService, Service (×4 on home), FAQPage (home, scorecard), BreadcrumbList (inner pages) |
| Page weight | Homepage HTML about 61 KB; all assets about 273 KB; fonts from Google Fonts |
| GitHub Pages | Static files with relative paths; no build step on the server |

Not tested here:
- A real screen reader (the semantics were reviewed instead).
- A Lighthouse run against the live URL.
- Microsoft Bookings and the analytics integrations, which aren't configured yet.

## Part 7: Owner action list

### Required before publication
1. Confirm the contact email works, or replace it (`CONTACT_EMAIL`).
2. Add the company number and registered office (`COMPANY_NUMBER`, `REGISTERED_OFFICE`).
3. Publish a privacy notice and link it from the forms.
4. If you enable GA4 or Clarity, add a cookie notice and consent mechanism first, as UK PECR requires.
5. Connect form submissions: either a Power Automate HTTP trigger feeding a SharePoint List, or Formspree (`FORM_ENDPOINT`).
6. Create a Microsoft Bookings page for the assessment (`BOOKING_URL`).
7. Confirm every price, tier inclusion, the 30-day credit, the three-month term and the 30-day notice period.
8. Confirm which security controls exist today, which are in progress and which are objectives, and edit the security section to match.
9. Founder content: a professional photograph, verified qualifications, certifications, memberships and the LinkedIn URL.
10. Set `SHOW_OWNER_PLACEHOLDERS = False` once the items above are done, or accept that the related blocks will be hidden.
11. Confirm the VAT position. If you aren't VAT-registered, "ex VAT" should become "VAT not applicable".

### Required before accepting managed-service clients
- Terms and conditions, and a service-definition template.
- A Data Processing Agreement, a UK IDTA or Addendum template, and a Transfer Risk Assessment.
- Confidentiality and IP-assignment agreements for the Lahore staff.
- Security controls in place: MFA, managed devices, endpoint protection, logging, and joiner, mover and leaver procedures.
- Cyber Essentials certification, recommended before your first managed-service contract.
- A business-continuity plan for the Lahore office.
- Professional indemnity and cyber insurance.
- Lahore office address and verified photographs.
- Real versions of the sample deliverables (PDF or XLSX), labelled as illustrative.

### Useful within the next 90 days
- First case studies and testimonials, published with permission.
- GA4 and Clarity IDs, plus a "booking completed" confirmation step via Bookings or Power Automate.
- HubSpot Free CRM or a SharePoint List for tracking leads.
- A custom domain, then updating `BASE_URL`.
- Lahore office photographs.
- Review pricing after the first 5–10 assessments.
- A UK delivery-manager hiring plan.

## Part 8: Change log

| File | Main changes | Reason |
|---|---|---|
| `build.py` | New configuration block (booking, form endpoint, analytics, company details, placeholder switch); one price catalogue for the new services; rebuilt home, services, delivery model, pricing, scorecard, contact; new samples page; SEO and JSON-LD in `page()` | Single source of truth; commercial focus; SEO |
| `index.html` | Rebuilt in the 16-section structure | Clarity, trust and conversion |
| `scorecard.html` | New readiness scorecard (10 dimensions, 13 questions, 4 bands) with risks, actions, service, next step, download and email; updated route and FAQ | Make it the central conversion tool |
| `ai-scorecard.html` | New result format; updated services | Consistency |
| `pricing.html` | Assessment and pilot first; core services with boundaries tables; SOP definition; commercial terms; secondary offers below | Package control and transparency |
| `services.html` | Core managed services first; AI services updated (Discovery, Workflow Implementation) | Focus |
| `managed-teams.html` | Retitled "Delivery Model"; qualified mobilisation; service levels without unverified credits; security link | Accuracy |
| `contact.html` | Assessment-first topics, "what happens next", organisation size, honest form mode, Bookings slot | Conversion; honesty |
| `samples.html` (new) | Eight illustrative deliverables, each labelled | Proof of output quality |
| `about.html`, `case-studies.html`, `insights.html` | Shared header, footer and meta only; one qualified mobilisation sentence on About; one wording fix on case studies | Consistency, accuracy |
| `assets/js/main.js` | Rewritten: analytics wrapper and events, keyboard-safe scorecard, results with download and email, honest forms, office-hours status | Function and accessibility |
| `assets/css/styles.css` | Styles for new sections; contrast fix; overflow fixes; static ring; mobile hero order | Design and accessibility |

**Still missing:** everything in Part 7. **Integrations still required:** Microsoft Bookings, the form endpoint (Power Automate or Formspree), the CRM, GA4 and Clarity with a consent mechanism.
**Couldn't be completed:** real photographs, testimonials, case studies, certifications and downloadable sample files, because they must come from the owner.

**Recommended next phase:**
1. Connect Bookings and the forms.
2. Add a privacy and cookie notice with consent.
3. Win founding clients and publish two verified case studies.
4. Add a dedicated logistics landing page and a PMO-in-a-Box landing page for paid and LinkedIn campaigns.
5. Review analytics after 60 days and trim the homepage accordingly.

---

## Final decision standard

| Question | Status |
|---|---|
| Offer understood within 30 seconds? | Yes: hero, subheadline and price strip |
| Clear who it is for? | Yes: "Who we work with" |
| Lahore location transparent? | Yes: hero, delivery model, FAQ |
| UK accountability clear? | Yes: hero, delivery model, founder, FAQ |
| Sold as outcomes, not people? | Yes |
| Package limits controlled? | Yes: capacity, scope, review cycles and exclusions on every tier |
| Prices and contract assumptions visible? | Yes |
| Perceived outsourcing risk reduced? | Yes: assessment, pilot, security section, FAQs |
| Founder role and credibility clear? | Partly: the role is clear; verified credentials are needed from the owner |
| Verifiable proof? | Not yet: the scenario is clearly illustrative; real case studies needed |
| Security and data transfer addressed? | Yes, with honest status labels; owner confirmation needed |
| Every CTA works? | Yes; booking and forms use working fallbacks until configured |
| Low-risk route in? | Yes: £495 assessment, then pilot |
| Leads to a paid assessment or pilot? | Yes |
| Avoids invented evidence? | Yes: illustrative content is labelled; no testimonials, logos or results invented |

---

## Update: recommendations applied (21 November 2026)

| Recommendation | What was done | Files |
|---|---|---|
| Don't show placeholders on a public site | `SHOW_OWNER_PLACEHOLDERS` now defaults to `False`. Missing items are hidden, and the testimonials block only appears when there are testimonials | `build.py` |
| Lead with PMO-in-a-Box and the Documentation Factory | Service order on the homepage is now PMO, Documentation Factory, Business Analysis; problems reordered to match | `build.py`, `index.html` |
| Logistics and PMO landing pages for campaigns | New `logistics.html` (six logistics situations, four logistics packages, founder relevance, scenario, route, FAQs) and `pmo-in-a-box.html` (weekly PMO rhythm, tiers and boundaries, "what it isn't", samples, FAQs); "Logistics" added to the main menu | new pages, nav |
| Win founding clients for proof | Founding-client offer (first `FOUNDING_PLACES` = 3 clients; reduced first-term rate agreed individually, in return for a reference and an approved case study) on home, logistics and PMO pages; contact topic added | `build.py` |
| Privacy notice before collecting data | Draft UK GDPR privacy notice at `privacy.html`, linked from every form and the footer. The text adapts to whether analytics or a form service are configured | `privacy.html` |
| Cookie consent before analytics | GA4 and Clarity now load only after the visitor accepts; a banner appears automatically when IDs are set; "Cookie settings" link in the footer | `build.py`, `main.js` |
| Forms ready for Power Automate | Forms send JSON (works with a Power Automate HTTP trigger and Formspree); hidden spam-trap field | `main.js` |
| Confirm the VAT position | `VAT_REGISTERED` switch rewrites all "ex VAT" wording if you are not registered | `build.py` |
| Integration set-up | Step-by-step guide for Bookings, Power Automate with SharePoint, Formspree, HubSpot, GA4 key events and Clarity | `docs/INTEGRATIONS.md` |
| Menu fit | Six-link menu tightened; collapses below 1180px; no wrapping or sideways scroll at any width | CSS |

**QA after these changes:**
- 14 pages, with no horizontal overflow at 1366, 820 and 390px, and the menu checked at 1179, 1181, 1220 and 1280px.
- No JavaScript errors, and all links and anchors resolve.
- Scorecard bands verified.
- In a test build:
  - The consent banner blocks Google Analytics until the visitor accepts.
  - The JSON form post was received by a mock endpoint.
  - The spam trap blocked a bot-style submission.

**Recommendations that are business decisions, not code (still with you):**
- Raise the assessment price after the first 5–10 sales.
- Check delivery cost per day against the monthly prices.
- Plan a UK service-manager hire at around 8–12 clients.
- Get Cyber Essentials before the first managed-service contract.
- Have the privacy notice reviewed.
