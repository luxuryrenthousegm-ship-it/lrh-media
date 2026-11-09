#!/usr/bin/env python3
"""Carrusel 'Lo que US$800 al mes te alquila en Punta Cana' (1041 Panorama Park & Garden) + historia teaser. Estilo Oppenheim."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"
SRC = "/home/claude/lrh-media/src/1041"; OUT = f"{S}/carrusel1041"; os.makedirs(OUT, exist_ok=True)
K = 2; W, H = 1080 * K, 1350 * K
CARBON, NEGRO, PIEDRA, ARENA, CALIDA, BLANCO = (47, 44, 33), (20, 20, 13), (225, 223, 226), (203, 190, 180), (198, 152, 105), (255, 255, 255)
mont = lambda wt, sz: ImageFont.truetype(f"{F}/montserrat-latin-{wt}-normal.woff", sz * K)
def pit(sz):
    f = ImageFont.truetype(f"{F}/PlayfairItalic.ttf", sz * K)
    try: f.set_variation_by_axes([400])
    except Exception: pass
    return f

def photo(n, w, h, fy=0.5):
    im = Image.open(f"{SRC}/p{n}.jpg").convert("RGB"); iw, ih = im.size
    r = w / h
    if iw / ih > r: cw = int(ih * r); im = im.crop(((iw - cw) // 2, 0, (iw - cw) // 2 + cw, ih))
    else: ch = int(iw / r); y0 = int((ih - ch) * fy); im = im.crop((0, y0, iw, y0 + ch))
    im = im.resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=2))

def grad(img, top=0.0, bottom=0.0, start=0.62):
    w, h = img.size; ov = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(ov)
    for y in range(h):
        a = 0
        if top and y < h * 0.22: a = top * (1 - y / (h * 0.22))
        if bottom and y > h * start: a = max(a, bottom * ((y - h * start) / (h * (1 - start))) ** 1.1)
        d.line([(0, y), (w, y)], fill=(*NEGRO, int(255 * a)))
    img = img.convert("RGBA"); img.alpha_composite(ov); return img

def sp(d, w, y, t, f, fill, tr):
    tr *= K; ws = [d.textlength(c, font=f) for c in t]; x = (w - sum(ws) - tr * (len(t) - 1)) / 2
    for c, ww in zip(t, ws): d.text((x, y * K), c, font=f, fill=fill); x += ww + tr
def ct(d, w, y, t, f, fill): d.text(((w - d.textlength(t, font=f)) / 2, y * K), t, font=f, fill=fill)

def brand(d, w, y=56):
    sp(d, w, y, "LUXURY RENT HOUSE", mont(500, 15), BLANCO, 8)

def counter(d, w, i, n):
    t = f"{i}/{n}"; f = mont(500, 15); d.text((w - 70 * K - d.textlength(t, font=f), 56 * K), t, font=f, fill=BLANCO)

N = 6
def save(img, i): img.convert("RGB").save(f"{OUT}/{i:02d}.jpg", quality=95, subsampling=0)

# 1 portada
img = grad(photo(7, W, H), top=0.6, bottom=0.6, start=0.75); d = ImageDraw.Draw(img); brand(d, W); counter(d, W, 1, N)
sp(d, W, 150, "VISTA CANA  ·  PUNTA CANA", mont(500, 18), ARENA, 7)
ct(d, W, 190, "Lo que consigues con", pit(64), BLANCO)
sp(d, W, 285, "US$800 AL MES", mont(500, 54), BLANCO, 10)
ct(d, W, 360, "en Punta Cana", pit(64), BLANCO)
sp(d, W, 1250, "DESLIZA", mont(500, 16), PIEDRA, 8)
save(img, 1)

# 2-6 recorrido: foto limpia, una línea
pasos = [(3, "COCINA CON LÍNEA BLANCA", "Llegas y cocinas.", 0.5),
         (4, "1 HABITACIÓN", "Tu espacio, tus reglas.", 0.6),
         (5, "1.5 BAÑOS", "Uno para ti, medio para la visita.", 0.5),
         (6, "GIMNASIO EN EL RESIDENCIAL", "La excusa de \"no tengo gym\" se acabó.", 0.5)
]
for i, (n, cap, line, fy) in enumerate(pasos, start=2):
    img = grad(photo(n, W, H, fy), top=0.4, bottom=0.8, start=0.68); d = ImageDraw.Draw(img); brand(d, W); counter(d, W, i, N)
    sp(d, W, 1150, cap, mont(500, 18), ARENA, 7)
    ct(d, W, 1190, line, pit(46), BLANCO)
    save(img, i)

# 7 revelación y cierre (fondo carbón, sin foto)
img = Image.new("RGB", (W, H), CARBON); d = ImageDraw.Draw(img); brand(d, W); counter(d, W, 6, N)
sp(d, W, 300, "PANORAMA PARK & GARDEN", mont(500, 20), ARENA, 8)
ct(d, W, 350, "Todo esto, por", pit(60), BLANCO)
ct(d, W, 450, "US$800", ImageFont.truetype(f"{F}/montserrat-latin-500-normal.woff", 150 * K), BLANCO)
sp(d, W, 650, "AL MES  ·  LARGO PLAZO", mont(500, 20), CALIDA, 8)
d.line([(W / 2 - 40 * K, 715 * K), (W / 2 + 40 * K, 715 * K)], fill=CALIDA, width=2 * K)
for k, ln in enumerate(["1 habitación  ·  1.5 baños  ·  2 parqueos", "Línea blanca completa  ·  Acepta mascotas",
                        "Residencial cerrado con piscina, gimnasio,", "club, cancha, áreas verdes y seguridad 24 h"]):
    ct(d, W, 750 + k * 48, ln, mont(300, 28), PIEDRA)
ct(d, W, 1010, "¿Lo alquilarías? Comenta SÍ", pit(44), BLANCO)
sp(d, W, 1150, "WHATSAPP 849-247-2107", mont(500, 18), ARENA, 7)
sp(d, W, 1190, "@LUXURYRENTHOUSERD", mont(500, 16), PIEDRA, 7)
save(img, 6)

# historia teaser 1080x1920 (foto enmarcada para no perder calidad)
SW, SH = 1080 * K, 1920 * K
st = Image.new("RGB", (SW, SH), CARBON); d = ImageDraw.Draw(st)
sp(d, SW, 250, "LUXURY RENT HOUSE", mont(500, 16), PIEDRA, 8)
ph = photo(7, 760 * K, 950 * K); st.paste(ph, (160 * K, 340 * K))
d.rectangle([160 * K, 340 * K, 920 * K, 1290 * K], outline=ARENA, width=K)
sp(d, SW, 1360, "PREGUNTA SERIA", mont(500, 18), CALIDA, 8)
ct(d, SW, 1395, "¿Qué consigues con", pit(64), BLANCO)
sp(d, SW, 1480, "US$800 AL MES", mont(500, 50), BLANCO, 10)
ct(d, SW, 1545, "en Punta Cana?", pit(64), BLANCO)
ct(d, SW, 1650, "La respuesta te va a sorprender.", mont(300, 30), PIEDRA)
sp(d, SW, 1705, "MÍRALA EN NUESTRO ÚLTIMO POST", mont(500, 18), BLANCO, 6)
st.save(f"{OUT}/historia_teaser.jpg", quality=95, subsampling=0)
print("ok")
