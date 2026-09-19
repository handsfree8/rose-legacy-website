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
