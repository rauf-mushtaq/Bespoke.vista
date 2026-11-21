# Connecting bookings, forms, CRM and analytics

All settings live at the top of `build.py`. After changing any of them, run `python3 build.py`, then commit and push.

## 1. Microsoft Bookings (assessment bookings)

1. In Microsoft 365, open **Bookings** and create a booking page called "Managed Operations Assessment".
2. Add a service:
   - **Name:** "Managed Operations Assessment (£495 ex VAT)".
   - **Duration:** 60 minutes, with a Teams meeting.
   - **Buffer:** add 15 minutes between bookings.
3. Add custom questions: organisation, organisation size, and "What would you like to hand over?".
4. Publish the page and copy its public URL.
5. In `build.py`, set `BOOKING_URL = "https://outlook.office365.com/book/..."`.

Every "Book a Managed Operations Assessment" button then opens Bookings, and clicks are tracked as `booking_start`.

**Booking completed:** Bookings runs on Microsoft's site, so the website can't see completed bookings. To track them, use a Power Automate flow triggered by "When a appointment is created" (Bookings connector). The flow can add the booking to your lead list, and, if you use GA4, send a `booking_completed` event through the GA4 Measurement Protocol.

## 2. Website forms → Power Automate → SharePoint list and email

The forms send JSON, which a Power Automate HTTP trigger reads directly.

1. **Create a SharePoint list called "Website Leads"** with these columns:
   - Name (text) and Email (text)
   - Organisation, Phone, Topic, Size (text)
   - Message (multiple lines)
   - Results (multiple lines)
   - Form, Page, SubmittedAt (text)
   - Status (choice: New / Contacted / Assessment booked / Pilot / Client / Closed)
2. **In Power Automate**, create an instant cloud flow using the trigger **When an HTTP request is received**. Set "Who can trigger the flow?" to **Anyone**, and use this request body JSON schema:

   ```json
   {
     "type": "object",
     "properties": {
       "form": {"type": "string"}, "page": {"type": "string"}, "submittedAt": {"type": "string"},
       "name": {"type": "string"}, "email": {"type": "string"}, "organisation": {"type": "string"},
       "phone": {"type": "string"}, "topic": {"type": "string"}, "size": {"type": "string"},
       "message": {"type": "string"}, "results": {"type": "string"}
     }
   }
   ```

3. **Add the flow's actions:**
   - **Create item** in the Website Leads list, mapping each field.
   - **Send an email (V2)** to you with the lead details. If the topic is `assessment` or `pilot`, mark the email high priority.
   - Optionally, **send an acknowledgement** to the visitor's email address.
   - **Response:** status code 200, with headers `Access-Control-Allow-Origin: *` and `Content-Type: application/json`, and body `{"ok": true}`.
4. **Save the flow,** copy the HTTP POST URL, and set `FORM_ENDPOINT` in `build.py` to it.

**Notes:**
- The URL contains a signature. Treat it like a password: don't share it, and regenerate it if it leaks. It must sit in the site's code to work, so the Power Automate side should only create list items and send emails.
- The hidden "website" field is a spam trap. Submissions that fill it are discarded in the browser.
- The HTTP trigger requires a Power Automate Premium licence. If that isn't available, Formspree (below) is a simpler option.

**Alternative: Formspree.** Create a form at formspree.io, copy its endpoint (for example `https://formspree.io/f/abcdwxyz`) and set it as `FORM_ENDPOINT`. Formspree accepts JSON and emails you each submission.

Until `FORM_ENDPOINT` is set, forms open the visitor's email app and say so on screen.

## 3. CRM

- **Simplest:** use the SharePoint list above as your pipeline, with a list view grouped by Status.
- **HubSpot Free CRM:** add a "Create or update contact" step to the Power Automate flow (HubSpot connector), or use HubSpot's own forms instead.

## 4. Analytics (GA4 and Microsoft Clarity)

1. **Publish and confirm the privacy notice** first (`privacy.html`); it updates automatically once analytics are configured.
2. **Google Analytics 4:** create a property and web data stream, then set `GA4_ID = "G-XXXXXXX"`.
3. **Microsoft Clarity:** create a project, then set `CLARITY_ID` to the project ID.
4. **Rebuild the site.** A cookie banner appears automatically, and nothing loads until the visitor accepts. A "Cookie settings" link appears in the footer.
5. **In GA4,** mark these events as key events (conversions):
   - `scorecard_complete`
   - `booking_start`
   - `assessment_enquiry_start`
   - `contact_submit`
   - `pilot_enquiry_submit`
   - `scorecard_lead_submit`

**All events sent by the site:**
- `scorecard_start`, `scorecard_complete` (with score and band), `result_download`, `result_email`
- `assessment_view`, `sample_view`, `booking_start`, `assessment_enquiry_start`, `pilot_cta`, `portfolio_cta`
- `contact_submit`, `pilot_enquiry_submit`, `scorecard_lead_submit`, `lead_submit`

## 5. Before publication

- **Company details:** set `COMPANY_NUMBER`, `REGISTERED_OFFICE`, `LAHORE_ADDRESS` and `LINKEDIN_URL`.
- **VAT:** confirm `VAT_REGISTERED`. If False, all "ex VAT" wording changes to "no VAT charged".
- **Founding clients:** set `FOUNDING_PLACES` to 0 to remove the founding-client offer once it's filled.
- **Review placeholders:** set `SHOW_OWNER_PLACEHOLDERS = True` to see every missing item marked on the pages, then back to `False` before publishing.
- **Privacy notice:** have it reviewed by a solicitor or data-protection adviser.
