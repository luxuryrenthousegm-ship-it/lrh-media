#!/usr/bin/env python3
"""Creativos Meta Ads desde @maciel.luxuryrh (Estilo Jason): Doral 1051, US$1,150.
Español (conjunto 1) e inglés (conjunto 2). Feed 4:5 y Stories/Reels 9:16, salida 2x."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"
SRC = f"{S}/lp1051/img"; OUT = f"{S}/ads_maciel"; os.makedirs(OUT, exist_ok=True)
K = 2
NEGRO, CALIDO, BLANCO, CREMA = (14, 14, 12), (198, 152, 105), (255, 255, 255), (245, 238, 228)
osw = lambda wt, sz: ImageFont.truetype(f"{F}/oswald-latin-{wt}-normal.woff", int(sz * K))
mont = lambda wt, sz: ImageFont.truetype(f"{F}/montserrat-latin-{wt}-normal.woff", int(sz * K))

def photo(name, w, h, fy=0.5):
    im = Image.open(f"{SRC}/{name}.jpg").convert("RGB"); iw, ih = im.size; r = w / h
    if iw / ih > r: cw = int(ih * r); im = im.crop(((iw - cw) // 2, 0, (iw - cw) // 2 + cw, ih))
    else: ch = int(iw / r); y0 = int((ih - ch) * fy); im = im.crop((0, y0, iw, y0 + ch))
    im = im.resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.06)  # cálido y vivo, sin exagerar
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=30, threshold=2)).convert("RGBA")

def shade(img, top=0.0, bottom=0.0, start=0.55):
    w, h = img.size; ov = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(ov)
    for y in range(h):
        a = 0
        if top and y < h * 0.22: a = top * (1 - y / (h * 0.22))
        if bottom and y > h * start: a = max(a, bottom * (y - h * start) / (h * (1 - start)))
        if a: d.line([(0, y), (w, y)], fill=(*NEGRO, int(255 * a)))
    img.alpha_composite(ov); return img

def box(d, w, y, text, size, bg=NEGRO, fg=BLANCO, pad=24):
    f = osw(700, size); tw = d.textlength(text, font=f); x = (w - tw) / 2
    d.rectangle([x - pad * K, (y - 6) * K, x + tw + pad * K, (y + size * 1.32) * K], fill=bg)
    d.text((x, y * K - size * K * 0.08), text, font=f, fill=fg)
    return y + size * 1.32 + 14

def tag(d, w, y, text, size=18):
    f = mont(600, size); sp = 4 * K
    ws = [d.textlength(c, font=f) for c in text]; x = (w - sum(ws) - sp * (len(text) - 1)) / 2
    for c, ww in zip(text, ws): d.text((x, y * K), c, font=f, fill=BLANCO); x += ww + sp

def save(img, n): img.convert("RGB").save(f"{OUT}/{n}.jpg", quality=95, subsampling=0); print(n)

T = {"es": dict(top="MACIEL · LUXURY RENT HOUSE", hook=["¿BUSCAS APARTAMENTO", "EN BÁVARO?"],
                l1="2 HAB. AMUEBLADAS", l2="US$1,150 TODO INCLUIDO", l3="MANTENIMIENTO + INTERNET · ENTREGA EN 36 H"),
     "en": dict(top="MACIEL · LUXURY RENT HOUSE", hook=["MOVING TO", "PUNTA CANA?"],
                l1="FURNISHED 2-BEDROOM", l2="US$1,150/MO ALL-IN", l3="MAINTENANCE + INTERNET · MOVE IN 36 H")}

def single(lang, w, h, base, story=False):
    t = T[lang]
    img = shade(photo("sala" if lang == "es" else "comedor", w, h, fy=0.55), top=0.55, bottom=0.85, start=0.5)
    d = ImageDraw.Draw(img)
    t0 = 260 if story else 60
    tag(d, w, t0, t["top"], 16)
    y = t0 + 60
    for ln in t["hook"]: y = box(d, w, y, ln, 66 if not story else 72)
    yb = (1920 - 860) if story else (1350 - 330)
    y = box(d, w, yb, t["l1"], 46)
    y = box(d, w, y, t["l2"], 58, bg=CALIDO, fg=NEGRO)
    tag(d, w, y + 14, t["l3"], 16)
    save(img, base)

for lang in ("es", "en"):
    single(lang, 1080 * K, 1350 * K, f"M_{lang}_4x5")
    single(lang, 1080 * K, 1920 * K, f"M_{lang}_9x16", story=True)

# Carrusel 4:5 (6 tarjetas) en los dos idiomas
CAR = {"es": [("exterior", "DORAL RESIDENCES", "PISCINA Y SEGURIDAD 24 H", 0.45), ("sala", "SALA AMUEBLADA", "LLEGAS CON TU MALETA Y YA", 0.55),
              ("comedor", "COCINA EQUIPADA", "NEVERA, ESTUFA Y MICROONDAS", 0.5), ("habitacion", "2 HABITACIONES", "ESPACIO PARA TODOS", 0.5),
              ("bano", "2 BAÑOS", "UNO PARA TI, OTRO PARA LA VISITA", 0.55)],
       "en": [("exterior", "DORAL RESIDENCES", "POOL & 24/7 SECURITY", 0.45), ("sala", "FULLY FURNISHED", "JUST BRING YOUR SUITCASE", 0.55),
              ("comedor", "EQUIPPED KITCHEN", "FRIDGE, STOVE & MICROWAVE", 0.5), ("habitacion", "2 BEDROOMS", "ROOM FOR EVERYONE", 0.5),
              ("bano", "2 BATHROOMS", "ONE FOR YOU, ONE FOR GUESTS", 0.55)]}
END = {"es": ["US$1,150 AL MES", "MANTENIMIENTO E INTERNET INCLUIDOS", "QUEDAN 3 DE 30 · ESCRÍBEME"],
       "en": ["US$1,150 PER MONTH", "MAINTENANCE & INTERNET INCLUDED", "ONLY 3 OF 30 LEFT · MESSAGE ME"]}
W, H = 1080 * K, 1350 * K
for lang in ("es", "en"):
    for i, (n, a, b, fy) in enumerate(CAR[lang], 1):
        img = shade(photo(n, W, H, fy), bottom=0.8, start=0.6); d = ImageDraw.Draw(img)
        y = box(d, W, 1090, a, 50); box(d, W, y, b, 38, bg=CALIDO, fg=NEGRO)
        save(img, f"M_{lang}_car_{i}")
    img = Image.new("RGBA", (W, H), (*NEGRO, 255)); d = ImageDraw.Draw(img)
    tag(d, W, 120, "MACIEL · LUXURY RENT HOUSE", 16)
    y = box(d, W, 420, END[lang][0], 84, bg=CALIDO, fg=NEGRO)
    tag(d, W, y + 30, END[lang][1], 20)
    box(d, W, y + 120, END[lang][2], 44)
    tag(d, W, 1180, "@MACIEL.LUXURYRH", 18)
    save(img, f"M_{lang}_car_6")
