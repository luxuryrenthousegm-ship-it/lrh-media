#!/usr/bin/env python3
"""Post estilo Oppenheim 1080x1350 — Panorama Park & Garden 1041 (solo fotos reales)."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
FS = f"{S}/fonts"; FI = "/usr/share/fonts/opentype/inter/"
GREEN, GOLD, IVORY, INK = (14, 34, 31), (176, 141, 87), (248, 245, 239), (40, 44, 42)
W, H, PH = 1080, 1350, 905

def play(sz, italic=False, w=400):
    f = ImageFont.truetype(f"{FS}/PlayfairItalic.ttf" if italic else f"{FS}/Playfair.ttf", sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
inter = lambda n, sz: ImageFont.truetype(FI + n, sz)

img = Image.new("RGB", (W, H), IVORY)
ph = Image.open("/home/claude/lrh-media/src/1041/p3.jpg").convert("RGB")
iw, ih = ph.size; r = W / PH; ch = int(iw / r); y0 = int((ih - ch) * 0.30)
ph = ph.crop((0, y0, iw, y0 + ch)).resize((W, PH), Image.LANCZOS)
ph = ImageEnhance.Contrast(ph).enhance(1.03); ph = ph.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2))
img.paste(ph, (0, 0))
d = ImageDraw.Draw(img)

def ctext(y, t, f, fill, track=0):
    if not track: d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill); return
    ws = [d.textlength(c, font=f) for c in t]; x = (W - sum(ws) - track * (len(t) - 1)) / 2
    for c, w_ in zip(t, ws): d.text((x, y), c, font=f, fill=fill); x += w_ + track

# etiqueta discreta sobre la foto
lab = "EN ALQUILER"; f = inter("Inter-Medium.otf", 20); tw = sum(d.textlength(c, font=f) for c in lab) + 5 * (len(lab) - 1)
d.rectangle([48, 48, 48 + tw + 44, 92], fill=(*IVORY,)); x = 70
for c in lab: d.text((x, 57), c, font=f, fill=GREEN); x += d.textlength(c, font=f) + 5

ctext(PH + 44, "Panorama Park & Garden", play(62, True), GREEN)
ctext(PH + 132, "VISTA CANA  ·  PUNTA CANA", inter("Inter-Medium.otf", 21), GOLD, 6)
d.line([(W / 2 - 34, PH + 180), (W / 2 + 34, PH + 180)], fill=GOLD, width=2)
ctext(PH + 205, "US$800 al mes", play(46, w=500), INK)
ctext(PH + 278, "1 habitación   ·   1.5 baños   ·   2 parqueos   ·   Acepta mascotas", inter("Inter-Light.otf", 25), INK)
ctext(PH + 345, "LUXURY RENT HOUSE", inter("Inter-Medium.otf", 18), GREEN, 8)
img.save(f"{S}/Post_Oppenheim_1041.jpg", quality=95, subsampling=0)
print("ok")
