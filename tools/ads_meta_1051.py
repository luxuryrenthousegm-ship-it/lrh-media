#!/usr/bin/env python3
"""Creativos Meta Ads — Doral Residences 1051 (US$1,150). Estilo Oppenheim + Colores Luxury.
Salida 2x: feed 4:5 (2160x2700) y stories/reels 9:16 (2160x3840), con zonas seguras de Meta."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"
SRC = f"{S}/lp1051/img"; OUT = f"{S}/ads"; os.makedirs(OUT, exist_ok=True)
K = 2
VERDE, VERDE_P, PIEDRA, PIEDRA_C, BLANCO = (52, 59, 52), (42, 48, 42), (156, 152, 147), (225, 223, 226), (255, 255, 255)
LOGO = Image.open("/home/claude/lrh-media/brand/logo_lrh_blanco.png").convert("RGBA")
LOGO = LOGO.crop(LOGO.getbbox())
mont = lambda wt, sz: ImageFont.truetype(f"{F}/montserrat-latin-{wt}-normal.woff", int(sz * K))
def pit(sz):
    f = ImageFont.truetype(f"{F}/PlayfairItalic.ttf", int(sz * K))
    try: f.set_variation_by_axes([400])
    except Exception: pass
    return f

def photo(name, w, h, fy=0.5, fx=0.5):
    im = Image.open(f"{SRC}/{name}.jpg").convert("RGB"); iw, ih = im.size; r = w / h
    if iw / ih > r: cw = int(ih * r); x0 = int((iw - cw) * fx); im = im.crop((x0, 0, x0 + cw, ih))
    else: ch = int(iw / r); y0 = int((ih - ch) * fy); im = im.crop((0, y0, iw, y0 + ch))
    im = im.resize((w, h), Image.LANCZOS)
    return ImageEnhance.Contrast(im).enhance(1.02).filter(ImageFilter.UnsharpMask(radius=1.6, percent=30, threshold=2))

def grad(img, top=0.0, top_end=0.25, bottom=0.0, start=0.6):
    w, h = img.size; ov = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(ov)
    for y in range(h):
        a = 0
        if top and y < h * top_end: a = top * (1 - y / (h * top_end)) ** 1.3
        if bottom and y > h * start: a = max(a, bottom * ((y - h * start) / (h * (1 - start))) ** 1.1)
        if a: d.line([(0, y), (w, y)], fill=(*VERDE_P, int(255 * a)))
    img = img.convert("RGBA"); img.alpha_composite(ov); return img

def sp(d, w, y, t, f, fill, tr):
    tr *= K; ws = [d.textlength(c, font=f) for c in t]; x = (w - sum(ws) - tr * (len(t) - 1)) / 2
    for c, ww in zip(t, ws): d.text((x, y * K), c, font=f, fill=fill); x += ww + tr
def ct(d, w, y, t, f, fill): d.text(((w - d.textlength(t, font=f)) / 2, y * K), t, font=f, fill=fill)
def logo(img, y, hgt=70):
    lg = LOGO.resize((int(LOGO.width * hgt * K / LOGO.height), int(hgt * K)), Image.LANCZOS)
    img.alpha_composite(lg, ((img.width - lg.width) // 2, int(y * K)))
def save(img, n): img.convert("RGB").save(f"{OUT}/{n}.jpg", quality=95, subsampling=0); print(n)

FW, FH = 1080 * K, 1350 * K   # feed 4:5
SW, SH = 1080 * K, 1920 * K   # 9:16

# ---------- A. PRECIO (exterior) ----------
def precio(w, h, base, story=False):
    img = grad(photo("exterior", w, h, fy=0.45), top=0.75, top_end=0.3, bottom=0.92, start=0.5); d = ImageDraw.Draw(img)
    t0 = 270 if story else 70
    logo(img, t0, 64)
    sp(d, w, t0 + 100, "DORAL RESIDENCES  ·  COSTA BÁVARO", mont(500, 19), PIEDRA_C, 7)
    yb = (1920 - 700) if story else (1350 - 450)
    ct(d, w, yb, "2 habitaciones amuebladas", pit(54), BLANCO)
    sp(d, w, yb + 92, "US$1,150 AL MES", mont(500, 64), BLANCO, 9)
    sp(d, w, yb + 190, "MANTENIMIENTO E INTERNET INCLUIDOS", mont(500, 19), PIEDRA_C, 6)
    sp(d, w, yb + 232, "ENTREGA EN 36 HORAS  ·  CONTRATO US$100", mont(500, 19), PIEDRA_C, 6)
    save(img, base)
precio(FW, FH, "A_precio_4x5"); precio(SW, SH, "A_precio_9x16", story=True)

# ---------- B. CARRUSEL (recorrido) 4:5 ----------
cards = [("sala", "SALA AMUEBLADA", "Llegas con tu maleta y ya.", 0.55),
         ("comedor", "COMEDOR Y COCINA", "Nevera, estufa y microondas.", 0.5),
         ("habitacion", "2 HABITACIONES", "Espacio para todos, sin apretarse.", 0.5),
         ("bano", "2 BAÑOS", "Uno para ti, otro para la visita.", 0.55),
         ("exterior", "PISCINA Y SEGURIDAD 24 H", "Residencial cerrado en Costa Bávaro.", 0.45)]
for i, (n, cap, line, fy) in enumerate(cards, 1):
    img = grad(photo(n, FW, FH, fy), bottom=0.92, start=0.6); d = ImageDraw.Draw(img)
    sp(d, FW, 1150, cap, mont(500, 19), PIEDRA_C, 7)
    ct(d, FW, 1192, line, pit(46), BLANCO)
    save(img, f"B_carrusel_{i}")
img = Image.new("RGBA", (FW, FH), (*VERDE, 255)); d = ImageDraw.Draw(img)
logo(img, 120, 80)
sp(d, FW, 300, "DORAL RESIDENCES  ·  COSTA BÁVARO", mont(500, 19), PIEDRA_C, 7)
ct(d, FW, 350, "Todo esto, por", pit(60), BLANCO)
ct(d, FW, 440, "US$1,150", mont(500, 140), BLANCO)
sp(d, FW, 635, "AL MES  ·  LARGO PLAZO", mont(500, 20), PIEDRA_C, 8)
d.line([(FW / 2 - 40 * K, 700 * K), (FW / 2 + 40 * K, 700 * K)], fill=PIEDRA, width=2 * K)
for k, ln in enumerate(["Mantenimiento e internet incluidos", "73 m²  ·  2 hab.  ·  2 baños  ·  1 parqueo",
                        "Entrega en 36 horas  ·  Contrato US$100", "Quedan 3 unidades de 30"]):
    ct(d, FW, 740 + k * 52, ln, mont(300, 30), PIEDRA_C)
ct(d, FW, 1020, "Agenda tu visita hoy", pit(48), BLANCO)
sp(d, FW, 1110, "ESCRÍBENOS POR WHATSAPP", mont(500, 19), PIEDRA_C, 7)
save(img, "B_carrusel_6")

# ---------- C. TRASLADO (para Santo Domingo / ejecutivos) ----------
def traslado(w, h, base, story=False):
    ph_h = int(h * (0.52 if story else 0.5))
    img = Image.new("RGBA", (w, h), (*VERDE, 255))
    img.alpha_composite(photo("sala", w, ph_h, fy=0.6).convert("RGBA"), (0, h - ph_h)); d = ImageDraw.Draw(img)
    t0 = 270 if story else 60
    logo(img, t0, 52)
    ct(d, w, t0 + 88, "¿Te mudas a Punta Cana?", pit(62), BLANCO)
    sp(d, w, t0 + 185, "LLEGAS Y VIVES. NO AMUEBLAS NI INSTALAS NADA.", mont(500, 17), PIEDRA_C, 4)
    d.line([(w / 2 - 36 * K, (t0 + 245) * K), (w / 2 + 36 * K, (t0 + 245) * K)], fill=PIEDRA, width=2 * K)
    sp(d, w, t0 + 280, "US$1,150 AL MES", mont(500, 54), BLANCO, 9)
    sp(d, w, t0 + 365, "2 HAB. AMUEBLADAS  ·  MANTENIMIENTO E INTERNET INCLUIDOS", mont(500, 15), PIEDRA_C, 4)
    save(img, base)
traslado(FW, FH, "C_traslado_4x5"); traslado(SW, SH, "C_traslado_9x16", story=True)
