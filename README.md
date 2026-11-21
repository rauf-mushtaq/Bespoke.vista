# Bespoke Vista — website

Static website for Bespoke Vista Ltd. *Bridging Strategy and Execution.*

Positions Bespoke Vista as a hybrid business: senior UK consulting, AI services,
subscriptions, UK-led managed teams in Lahore, training, and the DojoOS product.

## Pages

| Page | Purpose |
|---|---|
| `index.html` | Home: hero, Advise / Build / Run / Learn, comparison with large consultancies, follow-the-sun timeline, subscriptions, "start where you are" ladder, principles, proof |
| `services.html` | Every service, grouped by pillar, with expandable details and prices |
| `managed-teams.html` | Outcome-priced managed services delivered from Lahore, SLA tiers, trust and security |
| `pricing.html` | Subscriptions (monthly/annual toggle), managed plans, fixed-price projects, training, DojoOS, FAQs |
| `scorecard.html` | Free interactive AI Readiness Scorecard (lead magnet); results link to a pre-filled enquiry |
| `about.html`, `case-studies.html`, `insights.html`, `contact.html` | Supporting pages |

## Visitor journey

Visitor → **Lead** (AI Scorecard, sample briefing) → **Subscriber** (Executive AI Intelligence, from £49/month)
→ **Client** (fixed-price assessment or project) → **Retainer** (AI Advisory, Fractional Architect, managed teams).
Every page ends with a call to action pointing at the next step.

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
- **Managed-team claims**: the SLA tiers and the trust and security list (data processing agreements,
  working in the client's Microsoft 365 tenant, confidentiality agreements) describe how the service
  should run. Make sure they match what you can contractually commit to.
- **Lahore working hours**: the clocks and timeline assume 09:00–18:00 Pakistan time, Monday to Friday.
  Change these in `assets/js/main.js` if needed.
- **DojoOS**: shown as "coming soon" with a founding-schools list.
- **Executive AI Intelligence**: the site offers a sample briefing, so have one ready.
- **Company details, LinkedIn, founder photo**: add when available.
