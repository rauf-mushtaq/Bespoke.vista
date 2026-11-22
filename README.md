# Bespoke Vista — website

Static website for Bespoke Vista Ltd. **We lead the change. Our team keeps it running.**

Proposition and growth recommendations: `docs/USP-AND-GROWTH.md`.

Positions Bespoke Vista as a hybrid business: senior UK consulting, AI services,
subscriptions, UK-led managed teams in Lahore, training, and the DojoOS product.

## Pages

| Page | Purpose |
|---|---|
| `index.html` | Homepage: value proposition, six services in three tiers + trust strip, urgent triggers, operating-model diagram, comparison, illustrative scenarios, final CTA |
| `scorecard.html` | Free Managed Delivery Readiness Scorecard (main lead magnet) |
| `pricing.html` | All prices, package boundaries and commercial terms |
| `samples.html` | Illustrative sample deliverables |
| `logistics.html` | Landing page for UK logistics, warehousing and 3PL businesses (for LinkedIn and paid campaigns) |
| `pmo-in-a-box.html` | Landing page for the PMO-in-a-Box service |
| `websites-apps.html` | Websites, Apps and Content: Member Portal (the app built for EmptyHands, £99–£299/month), Business Website (from £1,495), Website Care (£49/month), Content Creation (£295–£995/month), EmptyHands case study and request form |
| `virtual-consultancy.html` | Virtual Consultancy: £950 two-week work-package trial and monthly plans (Essentials £1,450, Professional £2,950, Partner £5,450), with a trial/plan request form |
| `privacy.html` | Privacy notice (draft: have it reviewed); updates itself when analytics or a form endpoint are configured |
| `services.html`, `managed-teams.html` (Delivery Model), `contact.html`, `ai-scorecard.html` | Supporting pages |
| `about.html`, `case-studies.html`, `insights.html` | Background pages |

Setting up Bookings, forms, CRM and analytics: `docs/INTEGRATIONS.md`.

See `docs/REVIEW-AND-CHANGELOG.md` for the full review, commercial assessment, QA results and the owner action list.

## Configuration (top of `build.py`)

`BASE_URL`, `CONTACT_EMAIL`, `BOOKING_URL` (Microsoft Bookings), `FORM_ENDPOINT` (Power Automate HTTP trigger or Formspree),
`GA4_ID`, `CLARITY_ID`, `COMPANY_NUMBER`, `REGISTERED_OFFICE`, `LAHORE_ADDRESS`, `LINKEDIN_URL`, and
`PAY_LINKS` (Stripe Payment Links per plan: a filled-in link turns that plan's button into "Subscribe"), `TRIAL_BOOKING_URL` and `SUBSCRIBE_URLS` (optional Bookings or Stripe Payment Links for Virtual Consultancy; blank uses the on-page request form),
`SHOW_EXTRA_OFFERS` (off: hides Executive AI Intelligence, AI Advisory, the Fractional Adviser and further managed services),
`SHOW_OWNER_PLACEHOLDERS` (off by default; switch on to see every missing item marked), `VAT_REGISTERED`, `FOUNDING_PLACES` and `PRIVACY_UPDATED`.

## Scorecards

Both scorecards run on one engine in `assets/js/main.js`. Questions, the service recommended for each area,
result bands and sector/size notes are defined in `build.py` (`OPS_QUIZ`, `AI_QUIZ`).
Results show the overall score, five area scores, the two weakest areas with matching services and prices,
and a results-review request form pre-filled with the answers. Answers stay in the browser unless the visitor submits.

Analytics: if Google Tag Manager or GA4 is installed, the site pushes `scorecard_start`, `scorecard_complete`
(with score and band) and `lead_submit` events to `dataLayer`.

## Editing

All content, prices and service names live in `build.py`. Edit there, then run:

```
python3 build.py
```

The generated `.html` files are committed, so the folder can be uploaded to any static host
(GitHub Pages, Netlify, Cloudflare Pages or a normal web server) with no build step.

```
assets/css/styles.css   design system (colours and fonts are variables at the top)
assets/js/main.js       menu, live clocks, timeline, price toggle, scorecard, forms
assets/img/             logo, favicon
```

## Design

- Warm paper background, deep ink, and an ember gradient taken from the logo (`#F7941D` to `#EE2A24`).
- Fonts: Fraunces (display), Inter (body), JetBrains Mono (labels), from Google Fonts.
- Signature elements: rising-sun horizon artwork, live London/Lahore clocks, follow-the-sun timeline,
  sector marquee, staircase funnel and "Balance. Discipline. Flow." principles.
- Respects reduced-motion settings; checked at desktop and phone widths.

## Before going live — please confirm

- **Email address**: `hello@bespokevista.co.uk` is a placeholder. Set `CONTACT_EMAIL` in `build.py`.
- **Forms**: without configuration, forms open the visitor's email app. To receive submissions directly,
  add a form-service URL (e.g. Formspree) to the `data-endpoint` attribute on the forms in `build.py`.
- **Prices and terms**: all prices, tier contents, the annual "2 months free" offer, 30-day notice
  and 3-month managed-service minimum are proposals. Check them before publishing.
- **Scorecard page commercial terms**: Operations Assessment £1,950 (credited against a pilot within 60 days), 60-day pilot from £3,000, managed service from £1,500/month with a three-month minimum, and "2 to 4 weeks" mobilisation are proposals.
- **Managed-team claims**: the SLA tiers and the trust and security list (data processing agreements,
  working in the client's Microsoft 365 tenant, confidentiality agreements) describe how the service
  should run. Make sure they match what you can contractually commit to.
- **Lahore working hours**: the clocks and timeline assume 09:00–18:00 Pakistan time, Monday to Friday.
  Change these in `assets/js/main.js` if needed.
- **Member Portal**: lists only features live in the EmptyHands Portal. Add new features in `build.py` (`PORTAL`) only once they work.
- **Executive AI Intelligence**: the site offers a sample briefing, so have one ready.
- **Company details, LinkedIn, founder photo**: add when available.
