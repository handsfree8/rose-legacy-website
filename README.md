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

The owner-approved FormSubmit integration emails `roselegacyhs@icloud.com`. Name, phone, service and city/ZIP are required; email and description are optional. The owner confirmed activation and receipt of the original local-preview form's test email on September 19, 2026. Activation is tied to the form's origin: localhost activation does not prove the production domain is active. The production AJAX test returned `success: false` with `This form needs Activation`; FormSubmit sent a separate activation email for `https://roselegacyhs.com/`. Activate the exact production origin and verify it with a real request before declaring delivery healthy.

With JavaScript, `assets/contact.js` submits JSON to the documented AJAX endpoint without leaving the page. A persistent dismissible notice reports pending, accepted or uncertain delivery. Only HTTP success plus an explicit `success: true` (boolean or string) clears the form. Provider rejection, malformed responses, network failure and a 20-second timeout preserve all entered data. Controls are disabled while sending to prevent duplicate requests and edits being lost. No automatic retries are made; timeout messaging explains that acceptance may already have happened. Honeypot and the provider's filtering remain in use; AJAX does not display the hosted CAPTCHA screen. No `_captcha=false` override is sent.

Without JavaScript, native POST and the provider's hosted spam check remain available, with `thank-you.html` as the return page. The noindex return page explains that appointments require confirmation. The form discloses the mail processor and links to its privacy terms. No email API key is exposed or needed in Vercel.

Run `node --test tests/test_contact.cjs` for submission-state tests in addition to the static checks above. These isolate the external network; they do not prove email delivery. Verify a real AJAX request in the owner's inbox after deployment. Documentation: https://formsubmit.co/ajax-documentation and https://formsubmit.co/documentation

## Background playback

The muted, inline video starts after DOM parsing rather than waiting for all page assets. The pause/play control is a compact 44px circular icon with accessible labels and tooltips; it stays hidden during initial loading. Explicit user pause survives orientation changes and tab switches. Reduced-motion and data-saving preferences still avoid the initial download. If autoplay is blocked, the first pointer/keyboard interaction retries only when preferences allow it; the play icon remains as a browser-policy fallback. Run `node --test tests/test_video.cjs` to check these lifecycle rules.
