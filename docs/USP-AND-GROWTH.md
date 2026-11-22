# Proposition and growth recommendations

## The proposition

**We lead the change. Our team keeps it running.**

Senior UK transformation leadership (Azeem Mushtaq) combined with a managed delivery team in Lahore, under one UK contract with one accountable lead.

This fills the gap between:
- large consultancies, whose juniors deliver at enterprise prices;
- independent contractors, who are senior but have no extra capacity;
- offshore IT suppliers, who provide capacity but little business-change leadership, and you manage the staff.

## Changes made to the site (21 November 2026)

| # | Recommendation | Implemented |
|---|---|---|
| 1 | Use one proposition everywhere | New homepage H1; header tagline; footer; services hero; logistics "After go-live" section; Delivery Model intro; homepage title, description and structured data |
| 2 | Show both halves of the model | Homepage "How we're different" section: *We lead the change* (UK) and *Our team keeps it running* (Lahore), joined by "One contract · One accountable lead · One plan", each with its prices |
| 3 | Help visitors self-select | "Where to start" chooser under the hero: need change led / need capacity / not sure |
| 4 | Packages only a lead-and-run firm can offer | Design & Run, Migrate & Run and Automate & Run, built from existing priced services; each step contracted separately |
| 5 | Make the competitive gap explicit | Four-way comparison: large consultancy, independent contractor, offshore IT supplier, Bespoke Vista |
| 6 | Remove contradictory prices | The transformation packages are now the site-wide prices (see the table below) |
| 7 | One low-friction main CTA | "Book a Discovery Call" (free, 30 minutes) in the header, the closing CTA band and the founder section; sticky version on phones |
| 8 | A focused homepage | Problems reworked to cover both change and capacity; methodology moved off the homepage (it remains on the Delivery Model page) |
| 9 | Services page structure | "Lead the change" (8 transformation services) first, then "Keep it running" (managed services), then assess and advise, AI and training |
| 10 | Pricing page structure | Transformation packages first, then the managed-services route and packages |

### Price alignment

| Before | Now (site-wide) |
|---|---|
| AI Operations Discovery: £2,500 | Automation and AI Opportunity Assessment: £2,500–£5,000 |
| Target Operating Model Design: from £12,000 | Target Operating-Model Sprint: £7,500–£15,000 |
| Fractional Business Architect: £995–£3,995/month | Fractional Transformation Adviser: £1,950–£4,500/month |
| No listed entry for transformation | Transformation Discovery: £1,500–£3,000; Change Delivery Leadership: from £7,500/month |

## For the owner to confirm

- **Discovery calls:** that Azeem will take free 30-minute discovery calls. Set `DISCOVERY_BOOKING_URL` to a Microsoft Bookings page for them.
- **Prices:** the new site-wide prices above.
- **Automation upkeep:** that the Lahore team can take on automation upkeep ("Automate & Run" step 3), or remove that step.

## Recommendations beyond the website (to attract business)

1. **Publish proof quickly.** Two or three founding clients on reduced terms, in exchange for case studies. Even one real "lead and run" story will outperform any copy.
2. **Use LinkedIn as the main channel.** Azeem's profile headline should match the site: "We lead the change; our team keeps it running." Post weekly on one theme (migrations, Copilot adoption, process simplification), with a link to the scorecard.
3. **Target trigger events.** Organisations with an end-of-support system, a new CIO or COO, a merger, a failed audit or a cyber incident. These buy transformation help within months.
4. **Run a referral partner programme.** Microsoft partners, warehouse-system and transport-system implementers, and cyber firms often need someone to lead business change, and their clients need follow-on capacity.
5. **Turn the scorecard into a conversation.** Follow up every completed report request personally within one working day.
6. **Make one landing page per campaign.** `logistics.html` and `pmo-in-a-box.html` exist. Next: a Microsoft 365 migration page and a Copilot adoption page.
7. **Plan for capacity.** Azeem's time limits transformation work. Track hours per client, and plan a second senior lead or a UK service manager once there are 8–12 active clients.

## Virtual Consultancy (added 21 November 2026)

New page `virtual-consultancy.html`, in the main navigation (replacing Samples, which stays in the footer and homepage).

- **Two-Week Work Package Trial: £950 fixed.** Kick-off with Azeem, a work-package plan, RAID and action log, two weeks of follow-up, two check-ins, two status reports and an end-of-trial recommendation. Credited in full against the first month if the client subscribes within 30 days.
- **Monthly plans:** Essentials £1,450 (1 work package, 4 senior hours, 3 coordinator days), Professional £2,950 (3 packages, 8 hours, 6 days), Partner £5,450 (6 packages, 16 hours, 12 days). One-month minimum, then 30 days' notice; hours don't roll over.
- **Booking:** an on-page request form (plan pre-selected from each button). No payment is taken on the site; scope is confirmed first. To take bookings or payments directly, set `TRIAL_BOOKING_URL` and `SUBSCRIBE_URLS` in `build.py`.
- Also linked from: a fourth homepage "Where to start" choice, the pricing page (new section), the services page, the footer and two new contact topics.

**Owner to confirm:** the trial price and credit, the plan prices and allowances, the one-month minimum term (other managed services have three months), the response times, and that a named Lahore coordinator can be assigned to each client.

## Websites, Apps and Content (added 21 November 2026)

New page `websites-apps.html`, in the main navigation. "Logistics" and "Delivery Model" moved from the top menu to the footer so the menu fits and stays simple: Services · Virtual Consultancy · Websites & Apps · Pricing · About.

- **EmptyHands case study (real):** the website and the EmptyHands Portal, built by Bespoke Vista for the Ilford school Azeem has run since 2006. Disclosed as the founder's own school. Also added to `case-studies.html` and to a homepage band.
- **Member Portal** replaces the "DojoOS: coming soon" block, listing only features live at EmptyHands: £99 / £179 / £299 a month, set-up from £495.
- **Business Website** from £1,495 fixed; **Website Care** £49/month.
- **Content Creation** £295 / £595 / £995 a month.
- **Instant purchase:** `PAY_LINKS` in `build.py`. Create a Stripe Payment Link per plan, paste it in, rebuild, and that plan's button becomes "Subscribe to …". Blank plans keep the request form.

**Owner to confirm:** all prices above; whether the portal can be set up for other clubs as a separate copy (multi-tenant or per-club install); member limits; who produces content (UK or Lahore) and capacity; card/PayPal payments going to each club's own account.

## Is the offer simple enough? (review)

Not yet. The site lists around 30 priced products. Recommended next step: present everything as four doors, and cut or hide anything that hasn't sold within six months.

1. **Lead the change:** discovery call, then Transformation Discovery.
2. **Keep it running:** £495 assessment, then managed PMO, BA and documentation.
3. **Virtual Consultancy:** £950 trial, then monthly plans.
4. **Websites, apps and content:** Member Portal, website, content.

Candidates to remove or hide from public pages: Executive AI Intelligence and AI Advisory (overlap with Virtual Consultancy and the Fractional Adviser), the secondary managed services, the Transformation Health Check, and some training.

## Homepage refactor (22 November 2026)

The homepage now follows one narrative, about half its previous length:

1. Hero
2. Why change stalls, plus four urgent triggers
3. Two entry paths and a scorecard callout
4. UK + Lahore trust and governance block
5. Compact comparison
6. Three illustrative mid-market scenarios
7. Final CTA

- **Four urgent triggers:** audit and cyber readiness (ISO 27001, Cyber Essentials Plus, client vendor audits); stalled ERP or WMS rollouts (NetSuite, Dynamics 365, SAP); margin and headcount pressure (employer National Insurance); M&A integration and exit readiness. Each links to a pre-selected contact topic.
- **Two paths:** A, Lead and deliver change; B, Keep operations and projects running.
- **Moved off the homepage:** the founder section (moved to the About page), the full FAQ and security sections (now on `managed-teams.html#faq` and `#security`), the assessment and pilot cards (now `pricing.html#assessment` and `#pilot`), samples, AI rules, and the Virtual Consultancy and Websites & Apps promos (now a one-line link and the footer).
- **Stalled System Rescue Review (£4,950, 2 weeks)** replaces the Transformation Health Check, at the same price.
- **Discovery call:** now 20 minutes site-wide.
- **Demand-led copy:** PMO-in-a-Box, Managed BA, Documentation Factory, automation, cyber and migration descriptions are rewritten around the triggers.

**Owner to confirm:**
- The three scenarios are composites and labelled illustrative. Replace them with verified case studies when available.
- That Azeem is comfortable leading ERP and WMS rescues alongside implementation partners. Configuration stays with the partner.
- The employer National Insurance framing.
- That 20 minutes is the right discovery-call length.

## Four core services, fewer names, less Lahore (22 November 2026)

**Four core services**, defined once in `build.py` (`FOUR`) and shown in the same order on the homepage, Services and Pricing:

| # | Service | Start with | Then |
|---|---|---|---|
| 01 | Lead the change | Transformation Discovery £1,500–£3,000 | Change Delivery Leadership from £7,500/month |
| 02 | Keep it running | Managed Operations Assessment £495 | PMO-in-a-Box from £1,950/month |
| 03 | Virtual Consultancy | Two-Week Work Package Trial £950 | Monthly plans from £1,450/month |
| 04 | Websites, apps and content | Business Website from £1,495 | Member Portal from £99/month |

The Services and Pricing pages also follow this order. Supporting services (assessments, AI projects, training) follow as "Supporting services".

**Hidden** (switch `SHOW_EXTRA_OFFERS = True` to restore): Executive AI Intelligence, AI Advisory, the Fractional Transformation Adviser, and further managed services. Insights now ends with the scorecard and discovery-call CTA.

**Founder mentions:** these now describe the role ("a senior UK consultant", "your accountable lead"). Azeem is named on the About page, the logistics founder section, one founder line under the homepage model diagram, and in structured data.

**Lahore mentions:** removed from headlines, taglines, price cards, footer tagline and clocks, and the Virtual Consultancy and contact pages. Kept where it explains the model: the homepage diagram and time-zone point, the Delivery Model page and FAQs, the About page's delivery-hub section, privacy, and the footer contact line.
