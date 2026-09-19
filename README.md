# Rose Legacy Home Solutions

Static website deployed by Vercel. `vercel.json` preserves extensionless service URLs.

## Design

The homepage uses an edited 7.1-second loop of the owner's footage, with responsive horizontal/vertical versions, a still-image fallback, and a pause control. Reduced-motion and data-saving preferences suppress the initial video download. The four service pages use the matching still background without downloading video.

The original logo, business sections, eight gallery photos, service routes, contact destinations, metadata, structured data, sitemap, and Search Console verification remain available. Three owner-provided project photographs are highlighted above the expandable original gallery. The native photo dialog supports keyboard navigation and Escape.

## Files

- `index.html`: homepage content.
- `assets/styles.css`: shared responsive design.
- `assets/site.js`: navigation, gallery, and homepage video.
- `assets/media/`: optimized owner-provided media; original MOV files are not required for deployment.
- `build_service_pages.py`: source of truth for the four service pages.

After editing service-page content or templates, run `python3 build_service_pages.py` and commit the resulting HTML files too.

## Checks

```sh
python3 -m unittest discover -s tests -v
node --check assets/site.js
```

The dependency-free tests check internal destinations/assets, original sections and photos, canonical/structured metadata, verification assets, video budgets, and service-page generation. Browser review should cover desktop/mobile layouts, menu open/close, gallery navigation/focus, video pause/resume, motion preferences, and service-page links.

For basic local viewing run `python3 -m http.server 8000`. With that server, open service pages using their `.html` filenames; Vercel serves their existing extensionless routes.

## Service requests

The homepage uses a native POST to FormSubmit, addressed to `roselegacyhs@icloud.com` (approved by the owner). Name, phone, service and city/ZIP are required; email and a short description are optional. The provider's default reCAPTCHA stays enabled, with an additional honeypot. The form discloses the mail processor and links to its privacy terms. No email API key is exposed or needed in Vercel.

FormSubmit must be activated before production launch: submit a clearly labelled test, open the activation email in the owner's iCloud inbox (check Junk), and confirm it. Then submit another test and verify the actual request email arrives with all fields. Activation and inbox delivery have not yet been verified. Never treat local field validation or the return page as proof of mail delivery. Do not disable the CAPTCHA for testing.

The provider returns visitors to `thank-you.html`. JavaScript sets this return URL to the current origin for local/Vercel previews; without JavaScript it uses the production domain. The confirmation page is excluded from search indexing and explains that appointments require a reply. The native form also works without JavaScript; any submission or CAPTCHA errors are displayed by FormSubmit. Users can go Back to correct/retry or use the displayed phone/email.

Documentation: https://formsubmit.co/documentation and https://formsubmit.co/help
