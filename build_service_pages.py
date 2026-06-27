#!/usr/bin/env python3
"""Generate SEO service landing pages for Rose Legacy Home Solutions."""
import html, json, os

SITE = "https://roselegacyhs.com"
PHONE_DISPLAY = "(816) 298-4828"
PHONE_TEL = "tel:+18162984828"
WA = "https://wa.me/14849512588"
FB = "https://www.facebook.com/profile.php?id=61576740384735"
IG = "https://www.instagram.com/roselegacyhvac"

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

WSP_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.77.46 3.45 1.34 4.95L2 22l5.29-1.39a9.9 9.9 0 0 0 4.75 1.21h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2Zm5.78 14.04c-.24.68-1.4 1.32-1.93 1.39-.49.07-1.12.1-1.81-.11-.42-.13-.95-.3-1.64-.59-2.88-1.24-4.76-4.13-4.9-4.32-.14-.19-1.18-1.57-1.18-3 0-1.42.75-2.12 1.01-2.41.27-.29.58-.36.78-.36.19 0 .39 0 .56.01.18.01.42-.07.65.5.24.58.81 2 .88 2.14.07.14.12.31.02.5-.1.19-.15.31-.29.48-.15.17-.31.37-.44.5-.15.14-.3.3-.13.59.17.29.76 1.25 1.63 2.02 1.12.99 2.06 1.31 2.36 1.45.29.15.46.13.63-.07.17-.21.72-.84.91-1.13.19-.29.39-.24.65-.14.27.1 1.69.8 1.98.94.29.15.48.21.55.34.07.13.07.74-.17 1.42Z"/></svg>'
FB_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12.06C22 6.5 17.52 2 11.94 2 6.36 2 1.88 6.5 1.88 12.06c0 5.02 3.66 9.18 8.45 9.94v-7.03H7.9v-2.91h2.43V9.94c0-2.4 1.43-3.73 3.62-3.73 1.05 0 2.15.19 2.15.19v2.36h-1.21c-1.2 0-1.57.74-1.57 1.5v1.8h2.67l-.43 2.91h-2.24v7.03c4.79-.76 8.45-4.92 8.45-9.94Z"/></svg>'
IG_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.2" fill="currentColor" stroke="none"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>'

HEADER = f'''<header id="site-header">
  <div class="nav">
    <a class="brand" href="/">
      <img class="brand-mark" src="/logo.png" alt="Rose Legacy Home Solutions logo" width="52" height="52"/>
      <span>
        <span class="brand-name" style="display:block;">Rose Legacy</span>
        <span class="brand-sub">Home Solutions LLC</span>
      </span>
    </a>
    <nav class="nav-links" id="primary-nav" aria-label="Primary">
      <a href="/#services">HVAC Services</a>
      <a href="/#beyond">Plumbing &amp; Electrical</a>
      <a href="/#plans">Maintenance Plans</a>
      <a href="/#area">Service Area</a>
      <a href="/#gallery">Gallery</a>
      <a href="/#contact">Contact</a>
    </nav>
    <div class="nav-right">
      <div class="social-icons">
        <a class="wsp" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="Message us on WhatsApp">{WSP_SVG}</a>
        <a class="fb" href="{FB}" target="_blank" rel="noopener noreferrer" aria-label="Visit our Facebook page">{FB_SVG}</a>
        <a class="ig" href="{IG}" target="_blank" rel="noopener noreferrer" aria-label="Follow us on Instagram">{IG_SVG}</a>
      </div>
      <a class="nav-call" href="{PHONE_TEL}">{PHONE_SVG}{PHONE_DISPLAY}</a>
      <button class="menu-btn" id="menu-btn" aria-label="Toggle menu" aria-expanded="false" aria-controls="primary-nav">
        <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
    </div>
  </div>
</header>'''

FOOTER = f'''<footer>
  <div class="wrap footer-inner">
    <p>© <span id="year"></span> Rose Legacy Home Solutions LLC · Overland Park, KS · HVAC · Plumbing · Electrical · Handyman</p>
    <div class="social-icons">
      <a class="wsp" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="Message us on WhatsApp">{WSP_SVG}</a>
      <a class="fb" href="{FB}" target="_blank" rel="noopener noreferrer" aria-label="Visit our Facebook page">{FB_SVG}</a>
      <a class="ig" href="{IG}" target="_blank" rel="noopener noreferrer" aria-label="Follow us on Instagram">{IG_SVG}</a>
    </div>
    <div class="footer-links">
      <a href="{PHONE_TEL}">{PHONE_DISPLAY}</a>
      <a href="mailto:roselegacyhs@icloud.com">roselegacyhs@icloud.com</a>
      <a href="/">Home ↑</a>
    </div>
  </div>
</footer>'''

SCRIPT = '''<script>
  document.getElementById('year').textContent = new Date().getFullYear();
  const header = document.getElementById('site-header');
  window.addEventListener('scroll', () => { header.classList.toggle('scrolled', window.scrollY > 12); }, { passive:true });
  (function(){
    const btn = document.getElementById('menu-btn');
    const nav = document.getElementById('primary-nav');
    if(!btn || !nav) return;
    const setOpen = (o) => { header.classList.toggle('menu-open', o); btn.setAttribute('aria-expanded', o?'true':'false'); };
    btn.addEventListener('click', () => setOpen(!header.classList.contains('menu-open')));
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setOpen(false)));
    document.addEventListener('click', (e) => { if(header.classList.contains('menu-open') && !header.contains(e.target)) setOpen(false); });
    document.addEventListener('keydown', (e) => { if(e.key === 'Escape') setOpen(false); });
  })();
  const revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => { entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: 0.16, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(el => io.observe(el));
  } else { revealEls.forEach(el => el.classList.add('in')); }
</script>'''


def page(slug, title, desc, city, region, eyebrow, h1_main, h1_em, lede,
         included_heading, included, why, faqs, related):
    url = f"{SITE}/{slug}"
    feats = "\n".join(f"      <li>{CHECK}<span>{html.escape(x)}</span></li>" for x in included)
    why_feats = "\n".join(f"      <li>{CHECK}<span>{html.escape(x)}</span></li>" for x in why)
    faq_html = "\n".join(
        f'    <div class="faq-item" data-reveal>\n      <h3>{html.escape(q)}</h3>\n      <p>{html.escape(a)}</p>\n    </div>'
        for q, a in faqs)
    related_html = "\n".join(f'      <a href="/{s}">{html.escape(t)}</a>' for s, t in related)

    service_schema = {
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": title.split("|")[0].strip(),
        "provider": {"@type": "HVACBusiness", "name": "Rose Legacy Home Solutions LLC",
                     "telephone": "+1-816-298-4828", "url": SITE + "/"},
        "areaServed": {"@type": "City", "name": city},
        "url": url, "description": desc,
    }
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }
    breadcrumb_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": h1_main, "item": url},
        ],
    }

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="{url}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Rose Legacy Home Solutions LLC"/>
<meta property="og:title" content="{html.escape(title)}"/>
<meta property="og:description" content="{html.escape(desc)}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:image" content="{SITE}/logo.png"/>
<meta name="geo.region" content="US-{region}"/>
<meta name="geo.placename" content="{html.escape(city)}"/>
<meta name="theme-color" content="#4a2080"/>
<script type="application/ld+json">{json.dumps(service_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_schema)}</script>
<link rel="icon" type="image/png" href="/logo.png"/>
<link rel="apple-touch-icon" href="/logo.png"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css"/>
</head>
<body>

{HEADER}

<main id="top">
  <section class="sp-hero">
    <div class="wrap">
      <div class="breadcrumb"><a href="/">Home</a> &nbsp;›&nbsp; {html.escape(h1_main)}</div>
      <span class="eyebrow"><span class="dot"></span> {html.escape(eyebrow)}</span>
      <h1>{html.escape(h1_main)} <em>{html.escape(h1_em)}</em></h1>
      <p class="lede">{html.escape(lede)}</p>
      <div class="hero-actions">
        <a class="btn-primary" href="{PHONE_TEL}">Call {PHONE_DISPLAY} {ARROW}</a>
        <a class="text-link" href="/#contact">Request service <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap sp-grid">
      <div data-reveal>
        <span class="kicker">{html.escape(included_heading)}</span>
        <h2>What we handle on every {html.escape(city)} call.</h2>
        <ul class="feature-list">
{feats}
        </ul>

        <span class="kicker" style="margin-top:40px; display:inline-block;">Why Rose Legacy</span>
        <ul class="feature-list">
{why_feats}
        </ul>
      </div>

      <aside class="sp-aside" data-reveal>
        <h3>Need it fixed today?</h3>
        <p>Real people answer the phone — no call center, no runaround. Tell us what's going on and we'll get you on the schedule.</p>
        <a class="btn-primary" href="{PHONE_TEL}">Call {PHONE_DISPLAY} {ARROW}</a>
        <div class="aside-meta">
          <div><strong>Serving:</strong> {html.escape(city)} &amp; KC Metro</div>
          <div><strong>Hours:</strong> Open 24/7 for emergencies</div>
          <div><strong>Local &amp; licensed:</strong> Overland Park based</div>
        </div>
      </aside>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head" data-reveal>
        <span class="kicker">Questions</span>
        <h2>{html.escape(city)} {html.escape(h1_main.split(' in ')[0].split(' Repair')[0])} FAQs.</h2>
      </div>
{faq_html}
      <div class="related-services" data-reveal>
        <span style="font-size:14px;color:var(--ink-soft);align-self:center;margin-right:4px;">Related:</span>
{related_html}
      </div>
    </div>
  </section>
</main>

{FOOTER}

{SCRIPT}

</body>
</html>
'''


PAGES = []

PAGES.append(dict(
    slug="hvac-repair-overland-park",
    title="HVAC Repair Overland Park, KS | Rose Legacy Home Solutions",
    desc="Fast HVAC repair in Overland Park, KS. AC and furnace diagnosis, repair and tune-ups from a local crew that answers the phone. Call (816) 298-4828.",
    city="Overland Park", region="KS",
    eyebrow="HVAC Repair · Overland Park, KS",
    h1_main="HVAC Repair in Overland Park, KS", h1_em="we pick up the phone.",
    lede="When the AC quits in July or the furnace dies in January, you need someone who shows up, diagnoses it straight, and fixes it for keeps. Rose Legacy is your local Overland Park HVAC crew — same-week service and honest answers.",
    included_heading="What's included",
    included=[
        "AC repair — short cycling, warm air, frozen coils, no cooling",
        "Furnace & heating repair — no heat, blower issues, ignition faults",
        "Refrigerant leak diagnosis and recharge",
        "Thermostat troubleshooting and replacement",
        "Capacitor, contactor and compressor repairs",
        "Seasonal tune-ups before the heat or cold hits",
    ],
    why=[
        "Local Overland Park crew — fast response across the KC Metro",
        "Real people answer the phone, every time",
        "Straight diagnosis — no upselling repairs you don't need",
        "Open 24/7 for true HVAC emergencies",
    ],
    faqs=[
        ("How fast can you repair my AC in Overland Park?",
         "In most cases we offer same-week service, and we keep slots open for emergencies. Call (816) 298-4828 and we'll tell you our soonest availability when you reach out."),
        ("Do you repair both AC and furnace systems?",
         "Yes. HVAC is our specialty — we handle air conditioning and heating across all major brands, from quick repairs to full system replacements."),
        ("What does an HVAC repair cost?",
         "It depends on the issue, but we always diagnose first and explain the fix before any work begins — no surprise charges. You'll know the cost before we start."),
    ],
    related=[("ac-installation-kansas-city", "AC Installation"),
             ("water-heater-replacement-kansas-city", "Water Heater Replacement"),
             ("plumbing-lees-summit", "Plumbing")],
))

PAGES.append(dict(
    slug="ac-installation-kansas-city",
    title="AC Installation Kansas City | Rose Legacy Home Solutions",
    desc="New AC installation across the Kansas City Metro. Right-sized, properly installed air conditioning systems from a local crew. Call (816) 298-4828.",
    city="Kansas City", region="MO",
    eyebrow="AC Installation · KC Metro",
    h1_main="AC Installation in Kansas City", h1_em="done right the first time.",
    lede="A new air conditioner is only as good as the install. Rose Legacy sizes your system correctly, installs it clean, and makes sure your home actually cools the way it should — across Overland Park, Lee's Summit and the wider KC Metro.",
    included_heading="What's included",
    included=[
        "Free, no-pressure system assessment and sizing",
        "New central AC and condenser installation",
        "Old unit removal and clean haul-away",
        "Proper refrigerant charge and airflow balancing",
        "Smart thermostat setup",
        "Honest options at multiple price points",
    ],
    why=[
        "Correct sizing — no oversized units that short-cycle",
        "Clean, code-compliant installs that last",
        "One local crew from quote to cleanup",
        "Maintenance plans to protect your investment",
    ],
    faqs=[
        ("How much does a new AC install cost in Kansas City?",
         "It varies by home size and system, which is why we assess your space first and give you clear options at different price points — no obligation. Call (816) 298-4828 to get started."),
        ("How long does an AC installation take?",
         "Most residential installs are completed in a single day. We'll confirm the timeline when we assess your home."),
        ("Do you remove my old AC unit?",
         "Yes — removal and haul-away of the old equipment is part of the job, and we leave the area clean."),
    ],
    related=[("hvac-repair-overland-park", "HVAC Repair"),
             ("water-heater-replacement-kansas-city", "Water Heater Replacement"),
             ("plumbing-lees-summit", "Plumbing")],
))

PAGES.append(dict(
    slug="water-heater-replacement-kansas-city",
    title="Water Heater Replacement Kansas City | Rose Legacy Home Solutions",
    desc="Water heater replacement and installation across Kansas City Metro. Fast swaps for tank and tankless units from a local crew. Call (816) 298-4828.",
    city="Kansas City", region="MO",
    eyebrow="Water Heaters · KC Metro",
    h1_main="Water Heater Replacement in Kansas City", h1_em="hot water, fast.",
    lede="No hot water, a leaking tank, or a unit on its last leg? Rose Legacy replaces and installs water heaters across the KC Metro — tank and tankless — usually within a day, so your home is back to normal fast.",
    included_heading="What's included",
    included=[
        "Tank water heater replacement (gas & electric)",
        "Tankless water heater installation",
        "Leaking or failed unit removal and disposal",
        "Correct sizing for your household's hot water needs",
        "Code-compliant connections and venting",
        "Upfront pricing before any work begins",
    ],
    why=[
        "Fast turnaround — often same-day replacement",
        "Tank and tankless expertise",
        "Local crew serving the whole KC Metro",
        "Clean install, honest pricing, no surprises",
    ],
    faqs=[
        ("How quickly can you replace my water heater?",
         "In most cases we can replace a failed water heater the same day or next day. Call (816) 298-4828 and we'll confirm availability."),
        ("Should I get a tank or tankless water heater?",
         "It depends on your household size, hot water demand and budget. We'll walk you through the trade-offs and recommend what genuinely fits your home."),
        ("Do you remove the old water heater?",
         "Yes — we remove and dispose of the old unit as part of the replacement, and leave everything clean."),
    ],
    related=[("hvac-repair-overland-park", "HVAC Repair"),
             ("ac-installation-kansas-city", "AC Installation"),
             ("plumbing-lees-summit", "Plumbing")],
))

PAGES.append(dict(
    slug="plumbing-lees-summit",
    title="Plumber in Lee's Summit, MO | Rose Legacy Home Solutions",
    desc="Local plumbing in Lee's Summit, MO — repairs, water heaters, fixtures and make-ready work. A crew that answers the phone. Call (816) 298-4828.",
    city="Lee's Summit", region="MO",
    eyebrow="Plumbing · Lee's Summit, MO",
    h1_main="Plumbing in Lee's Summit, MO", h1_em="one crew you can reach.",
    lede="From a dripping faucet to a failed water heater or a full make-ready turn, Rose Legacy handles residential plumbing across Lee's Summit and the KC Metro — reliable, tidy, and easy to get on the phone.",
    included_heading="What's included",
    included=[
        "Leak detection and repair",
        "Faucet, fixture and toilet repair & replacement",
        "Water heater repair and replacement",
        "Drain clearing and clogs",
        "Make-ready plumbing for rentals and turns",
        "Shut-off valves and supply line work",
    ],
    why=[
        "Local crew covering Lee's Summit & KC Metro",
        "Great fit for property managers and make-readies",
        "Honest, upfront pricing",
        "Real people answer the phone",
    ],
    faqs=[
        ("Do you handle make-ready plumbing for rentals?",
         "Yes — make-ready and turn work for property managers is a core part of what we do. We can knock out plumbing punch lists fast so units are rent-ready."),
        ("Can you come out for a plumbing emergency in Lee's Summit?",
         "We're available 24/7 for emergencies. Call (816) 298-4828 and we'll get to you as fast as we can."),
        ("Do you do both plumbing and HVAC?",
         "Yes. Rose Legacy is one crew for HVAC, plumbing, electrical and handyman make-ready work — so you're not juggling multiple contractors."),
    ],
    related=[("hvac-repair-overland-park", "HVAC Repair"),
             ("water-heater-replacement-kansas-city", "Water Heater Replacement"),
             ("ac-installation-kansas-city", "AC Installation")],
))

base = os.path.dirname(os.path.abspath(__file__))
for p in PAGES:
    out = page(**p)
    with open(os.path.join(base, p["slug"] + ".html"), "w") as f:
        f.write(out)
    print("wrote", p["slug"] + ".html")
print("done:", len(PAGES), "pages")
