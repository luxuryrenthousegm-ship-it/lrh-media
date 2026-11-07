#!/usr/bin/env python3
"""Post 1080x1350 con la línea del feed de @luxuryrenthouserd: foto a sangre, serif fino espaciado abajo."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
FS = f"{S}/fonts"; FI = "/usr/share/fonts/opentype/inter/"
W, H = 1080, 1350
corm = lambda wt, sz: ImageFont.truetype(f"{FS}/cormorant-garamond-latin-{wt}-normal.woff", sz)
inter = lambda n, sz: ImageFont.truetype(FI + n, sz)

ph = Image.open("/home/claude/lrh-media/src/1041/p3.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
ph = ImageEnhance.Contrast(ph).enhance(1.04); ph = ImageEnhance.Color(ph).enhance(1.03)
ph = ph.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2)).convert("RGBA")
ov = Image.new("RGBA", (W, H)); od = ImageDraw.Draw(ov)
for y in range(H):
    a = 0.0
    if y < 260: a = 0.28 * (1 - y / 260)
    if y > 800: a = max(a, 0.88 * ((y - 800) / (H - 800)) ** 1.0)
    od.line([(0, y), (W, y)], fill=(10, 14, 13, int(255 * a)))
ph.alpha_composite(ov); d = ImageDraw.Draw(ph)

def spaced(y, t, f, fill, track):
    ws = [d.textlength(c, font=f) for c in t]; x = (W - sum(ws) - track * (len(t) - 1)) / 2
    for c, w in zip(t, ws): d.text((x, y), c, font=f, fill=fill); x += w + track

WHITE = (255, 255, 255)
spaced(52, "LUXURY", corm(500, 34), (255, 255, 255, 235), 9)
spaced(94, "RENT HOUSE", inter("Inter-Regular.otf", 11), (255, 255, 255, 220), 5)
spaced(1078, "FOR RENT", inter("Inter-Medium.otf", 17), (255, 255, 255, 235), 6)
spaced(1108, "PANORAMA PARK", corm(400, 88), WHITE, 12)
spaced(1232, "VISTA CANA   -   1 HABITACIÓN   -   1.5 BAÑOS   -   MASCOTAS", inter("Inter-Regular.otf", 16), (255, 255, 255, 230), 4)
ph.convert("RGB").save(f"{S}/Post_Feed_1041.jpg", quality=95, subsampling=0)
print("ok")
