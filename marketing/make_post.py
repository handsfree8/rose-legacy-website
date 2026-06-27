#!/usr/bin/env python3
"""Temperate Order — Instagram post for Rose Legacy Home Solutions."""
import math
from PIL import Image, ImageDraw, ImageFont

FONTS = "/Users/roselegacyhomesolutions/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/57b43424-1588-4837-81b8-f3ddec6237a7/34a3d5b6-b729-4891-960b-5eb8a25d326d/skills/canvas-design/canvas-fonts"

# ---- palette (brand) ----
CREAM   = (250, 248, 244)
CREAM2  = (244, 240, 233)
PURPLE  = (74, 32, 128)
PDEEP   = (52, 23, 96)
COPPER  = (193, 105, 63)
INK     = (44, 38, 56)
MUTE    = (150, 140, 158)

S = 1080
SS = 3  # supersample
W = S * SS

img = Image.new("RGB", (W, W), CREAM)
d = ImageDraw.Draw(img)

def f(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size * SS)

gloock   = lambda s: f("Gloock-Regular.ttf", s)
italiana = lambda s: f("Italiana-Regular.ttf", s)
mono     = lambda s: f("DMMono-Regular.ttf", s)
sans     = lambda s: f("InstrumentSans-Regular.ttf", s)
sansb    = lambda s: f("InstrumentSans-Bold.ttf", s)

def ctext(cx, y, s, font, fill, tracking=0, anchor="mm"):
    if tracking == 0:
        d.text((cx, y), s, font=font, fill=fill, anchor=anchor)
        return
    # letter-spaced, centered
    widths = [d.textlength(ch, font=font) + tracking for ch in s]
    total = sum(widths) - tracking
    x = cx - total / 2
    for ch, wd in zip(s, widths):
        d.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += wd

# ---- subtle vertical warm gradient at very edges (whisper) ----
for i in range(W):
    t = i / W
    # faint warming toward bottom
    r = int(CREAM[0] + (CREAM2[0]-CREAM[0]) * t)
    g = int(CREAM[1] + (CREAM2[1]-CREAM[1]) * t)
    b = int(CREAM[2] + (CREAM2[2]-CREAM[2]) * t)
    d.line([(0, i), (W, i)], fill=(r, g, b))

M = 84 * SS  # margin
PX = SS      # 1 logical px
# ---- thin frame ----
d.rectangle([M, M, W-M, W-M], outline=(74,32,128), width=1*SS)

# ---- top labels ----
ctext(W//2, 150*PX, "ROSE LEGACY HOME SOLUTIONS LLC", mono(19), PURPLE, tracking=8*SS)
d.line([(W//2-140*SS, 176*PX), (W//2+140*SS, 176*PX)], fill=COPPER, width=2*SS)
ctext(W//2, 200*PX, "INSTITUTE FOR THE STUDY OF COMFORT  ·  KC METRO", mono(14), MUTE, tracking=4*SS)

# ================= THE DIAL (focal instrument) =================
cx, cy = W//2, 448*PX
R = 218 * SS
start_ang = 150   # degrees
end_ang = 390     # 30 -> sweep 240
sweep = end_ang - start_ang

# graduated tick marks (patient repetition)
N = 61
for i in range(N):
    a = math.radians(start_ang + sweep * i / (N-1))
    major = (i % 10 == 0)
    r1 = R
    r2 = R - (44*SS if major else 22*SS)
    # color ramps purple->copper around arc (cool to warm)
    t = i/(N-1)
    col = tuple(int(PURPLE[k] + (COPPER[k]-PURPLE[k])*t) for k in range(3))
    wlin = 4*SS if major else 2*SS
    x1, y1 = cx + R*math.cos(a), cy + R*math.sin(a)
    x2, y2 = cx + r2*math.cos(a), cy + r2*math.sin(a)
    d.line([(x1,y1),(x2,y2)], fill=col, width=wlin)

# outer arc
bbox = [cx-R, cy-R, cx+R, cy+R]
d.arc(bbox, start_ang, end_ang, fill=PDEEP, width=2*SS)

# the needle -> points to 72 (comfort), positioned in cool-warm balance
needle_t = 0.5
na = math.radians(start_ang + sweep*needle_t)
nx, ny = cx + (R-70*SS)*math.cos(na), cy + (R-70*SS)*math.sin(na)
d.line([(cx,cy),(nx,ny)], fill=PDEEP, width=6*SS)
# hub
d.ellipse([cx-16*SS, cy-16*SS, cx+16*SS, cy+16*SS], fill=PDEEP)
d.ellipse([cx-7*SS, cy-7*SS, cx+7*SS, cy+7*SS], fill=CREAM)

# center reading
ctext(cx, cy + 92*SS, "72°", gloock(104), PDEEP)
ctext(cx, cy + 162*SS, "PERFECTLY COMFORTABLE", mono(16), COPPER, tracking=6*SS)

# arc end labels
ctext(cx - R - 34*SS, cy + R*0.5, "COOL", mono(14), PURPLE, tracking=3*SS)
ctext(cx + R + 34*SS, cy + R*0.5, "HEAT", mono(14), COPPER, tracking=3*SS)

# ================= headline =================
ctext(W//2, 738*PX, "It's 97° outside.", gloock(66), INK)
ctext(W//2, 810*PX, "We pick up the phone.", italiana(70), COPPER)

# ================= bottom data row =================
by = 930*PX
d.line([(M+40*SS, by-44*SS), (W-M-40*SS, by-44*SS)], fill=(74,32,128), width=1*SS)

cols = [
    ("FIG. 01", "AC TUNE-UPS"),
    ("CALL", "(816) 298-4828"),
    ("WEB", "roselegacyhs.com"),
]
n = len(cols)
seg = (W - 2*M - 80*SS) / n
x0 = M + 40*SS
for i,(lab,val) in enumerate(cols):
    cxx = x0 + seg*(i+0.5)
    ctext(cxx, by, lab, mono(15), MUTE, tracking=4*SS)
    ctext(cxx, by + 40*SS, val, sansb(26), PDEEP)
    if i < n-1:
        xx = x0 + seg*(i+1)
        d.line([(xx, by-18*SS), (xx, by+58*SS)], fill=(200,190,180), width=1*SS)

# downscale
out = img.resize((S, S), Image.LANCZOS)
out.save("/Users/roselegacyhomesolutions/Desktop/rose-legacy-website/marketing/rose-legacy-ig-post.png")
print("saved")
