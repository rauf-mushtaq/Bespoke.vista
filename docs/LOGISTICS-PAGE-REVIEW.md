# Logistics page: review and repositioning

Page: `logistics.html` (generated from the `LOGISTICS LANDING PAGE` section of `build.py`). Updated 21 November 2026.
The previous version is preserved in git at commit `f3a8104`.

## Part 1: Review of the previous page

| Existing wording | Why it should change | Replacement |
|---|---|---|
| Title: "Logistics PMO and Process Documentation Services" | Framed the business as a logistics operations service provider | "Technology Transformation for Logistics \| Bespoke Vista" |
| Meta: "Managed PMO, warehouse SOP documentation and business analysis for UK logistics, warehousing and 3PL businesses…" | Warehouse-operations focus; wrong buyers | "Bespoke Vista helps logistics and operational organisations automate processes, adopt AI, strengthen cybersecurity, migrate technology and deliver complex change." |
| Label: "For logistics, warehousing and 3PL businesses" | Sector as the discipline | H1 kicker: "Technology-enabled transformation for logistics" |
| H1: "Keep projects and processes under control, through peak and growth." | "Peak" implies operational logistics advice | "Modernise operations. Simplify processes. Deliver change with confidence." |
| "Led by a founder whose career includes logistics and supply-chain operations." | Overstates logistics operations expertise | Trust line: "25+ years bridging business, technology and complex change." |
| Hero artwork labels: INBOUND / STORE / DISPATCH / REPORT | Warehouse-flow imagery reinforced the wrong positioning | PEOPLE / PROCESS / DATA / TECHNOLOGY |
| "Peak readiness: documented processes and training material so temporary staff are productive quickly…" | Operational workforce advice Azeem doesn't provide | Removed; replaced by transformation challenges (legacy systems, re-keying, AI governance, security, migration, competing programmes, manual reporting, no operating model) |
| "Multi-site consistency… document it once, agree the standard" | Operations-standards consulting | Covered instead by "Target operating-model design" and "Process simplification" |
| "Audit and accreditation evidence" | Implied compliance and accreditation expertise | Removed |
| Package "Warehouse SOP Starter: goods-in, put-away, picking, despatch and returns" | Sells warehouse process expertise | Removed. Packages are now Transformation Discovery, Automation and AI Opportunity Assessment, Target Operating-Model Sprint, Change Delivery Leadership and Fractional Transformation Adviser |
| Package "Site Operations Manual" | Same | Removed |
| Packages "Project control for change" and "Onboarding analysis" | Diluted the transformation offer with managed-service packages | Removed from this page; managed services remain on the homepage and pricing page |
| "Operational experience, not just templates… including logistics and supply-chain operations" | Overstated | Founder section: "Experience at the intersection of business, technology and change" |
| FAQ "When should we start before peak? Ideally eight to ten weeks before peak…" | Operational planning advice | Removed |
| FAQ "How do you price documentation across several sites?" | Documentation-service focus | Replaced by 15 transformation FAQs |
| Calls to action "Book a Managed Operations Assessment" and "Take the Free Readiness Scorecard" | Targeted managed-service buyers, not transformation leaders | Principal CTA "Book a Transformation Discovery Call", plus service-specific CTAs |
| Founding-client offer | Managed-service offer; off-message for transformation buyers | Removed from this page (kept on homepage and PMO page) |
| Scorecard sector note (on `scorecard.html`): "Logistics and supply chain is where our founder has spent much of his career, so we already understand warehouse and transport processes, peak planning…" | The same overstatement, on another page | "Our founder has worked in logistics and supply-chain environments… Our role is the business and technology change, not logistics operations advice." |

## Part 2: Revised page strategy

- **Positioning:** we help logistics and operational organisations simplify processes, implement technology and deliver complex change. Logistics is the client environment; business and technology transformation is the discipline.
- **Audience:**
  - Organisations: logistics, warehousing, distribution, freight and transport, supply-chain service providers, 3PLs and other operationally complex organisations.
  - Buyers: COO, CIO, CTO, Transformation, IT and Programme Directors, Heads of Change, Automation and Cybersecurity, and Business Architecture and Operational Excellence leaders.
- **Buyer problems:**
  - Legacy systems.
  - Manual re-keying.
  - Ungoverned AI.
  - Security requirements to deliver.
  - Risky migrations.
  - Competing programmes.
  - Manual reporting.
  - No agreed operating model.
- **Service hierarchy:**
  1. Process automation
  2. AI adoption and implementation
  3. Cybersecurity implementation
  4. Technology and data migration
  5. Target operating-model design
  6. Process simplification and cost reduction
  7. Complex change and programme delivery
  8. Remote and hybrid working
- **Packages:**
  - Transformation Discovery: £1,500–£3,000.
  - Automation and AI Opportunity Assessment: £2,500–£5,000.
  - Target Operating-Model Sprint: £7,500–£15,000.
  - Change Delivery Leadership: from £7,500 a month.
  - Fractional Transformation Adviser: £1,950–£4,500 a month.
  - All indicative and ex VAT.
- **Calls to action:**
  - Principal: "Book a Transformation Discovery Call".
  - Secondary: the eight service CTAs and the package CTAs.
- **Conversion journey:**
  1. Discovery call.
  2. Fixed-price Transformation Discovery, or an Automation and AI Assessment.
  3. Target Operating-Model Sprint, or Change Delivery Leadership.
  4. Optionally, a Fractional Transformation Adviser, plus managed PMO, analysis and documentation capacity.

## Part 3: Replacement copy

The full, publication-ready copy is in `logistics.html` (source: `build.py`). Sections in order:

1. Hero
2. Who we work with
3. Common challenges
4. Eight services (each with scope, technologies, partner boundaries and a CTA)
5. Why operational complexity matters, including "What we don't do"
6. Engagement packages
7. Delivery approach (Understand, Simplify, Design, Deliver, Embed)
8. Outcomes and measurement
9. Founder
10. Illustrative transformation scenario
11. 15 FAQs
12. Final CTA
13. Company and contact details

## Part 4: Implementation

| File | Change |
|---|---|
| `build.py` | Logistics section rewritten; `DISCOVERY_BOOKING_URL` / `DISCOVERY_HREF` added; nine contact topics added; scorecard sector note corrected |
| `logistics.html` | Regenerated |
| `contact.html` | Regenerated with the new topics (needed for the page's CTAs to pre-select the right enquiry) |
| `scorecard.html` | Regenerated with the corrected sector note |
| `assets/css/styles.css` | H1 kicker, expandable service scope, "What we don't do" box, link style in scorecard notes |
| `assets/js/main.js` | Scorecard notes rendered as HTML so the note can link to the logistics page |

The other pages only change through the shared header, footer and contact topics.

## Part 5: Quality review

| Check | Result |
|---|---|
| No specialist logistics-operations claims | Confirmed. The terms route optimisation, warehouse layout, fleet, customs, freight forwarding, demand forecasting, inventory, transport procurement and network design appear only in "we don't provide" statements |
| Reflects Azeem's experience | Services and founder copy follow the stated core expertise only |
| Logistics as client environment | Yes, in the H1 kicker, the context section and the FAQ "Are you a logistics operations consultancy? No." |
| Supportable service claims | Partner boundaries stated for testing, specialist migration and platform configuration; no proprietary machine-learning claims |
| Prices indicative | Yes, with the scope dependencies stated |
| CTAs | 14 distinct CTAs; each resolves to a page, an anchor, the AI scorecard, or the contact form with a matching pre-selected topic |
| Responsive | No horizontal overflow at 1366, 820 or 390px |
| British English | Yes (modernise, organisations, optimisation, programme) |
| Metadata | Title, description, canonical, Open Graph, Service, FAQPage and BreadcrumbList JSON-LD updated |
| Invented evidence | None. The scenario is labelled "Illustrative transformation scenario" with the required disclaimer, and no results or statistics are given |
| Contrast and accessibility | Uses the existing tokens (body 11.5:1, muted 5.4:1, accent 4.7:1); single H1; expandable scope uses native `<details>` |

## Part 6: Change log and owner actions

- **Content removed:** warehouse SOP packages, peak readiness, multi-site standards, audit and accreditation, managed-service packages, the founding-client offer, the logistics-operations founder claim, warehouse-flow artwork labels, and operational FAQs.
- **Content added:** the transformation hero, organisations and buyers, eight challenges, eight services, the context section with "What we don't do", five packages, the five-stage method, outcomes and measures, the founder section, the illustrative scenario, 15 FAQs, and company details.

**Claims requiring owner verification:**
- Each of the eight services is something Azeem will personally lead. Confirm in particular: cybersecurity implementation, migration leadership, and remote and hybrid working enablement.
- Workflow automation in Microsoft 365 and Power Automate "can be delivered directly where suitable" (FAQ 3). Confirm whether you build flows yourself or through partners.
- Availability of verified technical partners for penetration testing, specialist migration and platform configuration.
- "A Transformation Discovery can usually begin within one to two weeks."
- Package prices and inclusions.

**Price consistency to decide.** These packages overlap with prices on `pricing.html` and `services.html`, which I did not change because you asked me not to edit unrelated pages:
- **Operating model:** Target Operating-Model Sprint £7,500–£15,000 here vs "Target Operating Model Design, from £12,000" on the pricing page.
- **AI and automation:** Automation and AI Opportunity Assessment £2,500–£5,000 here vs AI Operations Discovery £2,500 fixed.
- **Fractional:** Fractional Transformation Adviser £1,950–£4,500 a month here vs Fractional Business Architect £995–£3,995 a month.

Recommendation: either adopt these as the site-wide transformation packages, or rename them so visitors don't see two prices for similar services.

**Images:**
- The page uses only the brand's horizon artwork; no stock photographs were added.
- If you add imagery later, use transformation workshops, process design or secure collaboration, and don't imply that stock photos show Bespoke Vista staff or client sites.
- Verified photographs of Azeem and of real workshops are preferred.

**Links requiring configuration:**
- `DISCOVERY_BOOKING_URL`: a Microsoft Bookings page for discovery calls. Until it's set, the button goes to the contact form with the "Transformation Discovery Call" topic selected.
- `FORM_ENDPOINT`: see `docs/INTEGRATIONS.md`.
- `LINKEDIN_URL`.
- Company number and registered office.

**Placeholders (hidden while `SHOW_OWNER_PLACEHOLDERS = False`):**
- Founder photograph.
- LinkedIn profile.
- Verified projects, industry experience, qualifications, certifications and recommendations.
- Verified anonymised case studies.
