#!/usr/bin/env python3
"""Carrusel (1080x1350) e historias (1080x1920) con fotos reales — línea de marca LRH."""
import os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
SRC = "/home/claude/lrh-media/src/1038"
OUT = f"{S}/contenido_09nov"; os.makedirs(OUT, exist_ok=True)
GOLD = (201, 169, 110); GREEN = (14, 34, 31); WHITE = (255, 255, 255)
PF, PFI = f"{S}/fonts/Playfair.ttf", f"{S}/fonts/PlayfairItalic.ttf"
FI = "/usr/share/fonts/opentype/inter/"

def play(s, italic=False, w=500):
    f = ImageFont.truetype(PFI if italic else PF, s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
LIGHT = lambda s: ImageFont.truetype(FI + "Inter-Light.otf", s)
REG = lambda s: ImageFont.truetype(FI + "Inter-Regular.otf", s)
MED = lambda s: ImageFont.truetype(FI + "Inter-Medium.otf", s)

def photo(n, W, H, focus=0.5):
    im = Image.open(f"{SRC}/p{n}.jpg").convert("RGB")
    r = W / H; iw, ih = im.size
    if iw / ih > r:
        cw = int(ih * r); x = int((iw - cw) * focus); im = im.crop((x, 0, x + cw, ih))
    else:
        ch = int(iw / r); im = im.crop((0, 0, iw, ch))
    im = im.resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.04); im = ImageEnhance.Color(im).enhance(1.05)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))

def grad(W, H, start, strength, top=0.0, ex=1.2):
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
    for y in range(H):
        a = 0.0
        if y > start: a = strength * ((y - start) / (H - start)) ** ex
        if top and y < 300: a = max(a, top * (1 - y / 300))
        d.line([(0, y), (W, y)], fill=(*GREEN, int(255 * min(a, 1))))
    return ov

def spaced(d, cx, y, text, f, fill, sp):
    ws = [d.textlength(c, font=f) for c in text]; x = cx - (sum(ws) + sp * (len(text) - 1)) / 2
    for c, w in zip(text, ws): d.text((x, y), c, font=f, fill=fill); x += w + sp

def ctext(d, W, y, text, f, fill): d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)

def wrap(d, text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def pill(d, W, y, text, f=None, sp=5, fill=GREEN, color=GOLD):
    f = f or MED(26); w = sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1) + 60
    d.rounded_rectangle([(W - w) / 2, y - 14, (W + w) / 2, y + 46], 30, fill=(*fill, 235))
    spaced(d, W / 2, y, text, f, color, sp)

def brand(d, W, y):
    spaced(d, W / 2, y, "LUXURY RENT HOUSE", MED(22), (255, 255, 255, 225), 8)
    d.line([(W / 2 - 36, y + 40), (W / 2 + 36, y + 40)], fill=GOLD, width=2)

def lines(d, W, y, txts, f, fill, lh):
    for t in txts: ctext(d, W, y, t, f, fill); y += lh
    return y

# ---------------- CARRUSEL 1080x1350 ----------------
CW, CH = 1080, 1350
def slide(i, n, ph, draw_fn, start=640, strength=0.97, focus=0.5):
    im = photo(ph, CW, CH, focus).convert("RGBA"); im.alpha_composite(grad(CW, CH, start, strength, top=0.45, ex=0.95))
    d = ImageDraw.Draw(im); brand(d, CW, 54)
    d.text((CW - 92, 58), f"{i}/{n}", font=MED(22), fill=(255, 255, 255, 200))
    draw_fn(d); im.convert("RGB").save(f"{OUT}/carrusel_{i:02d}.jpg", quality=95, subsampling=0)

N = 8
def sign(num, txt, ph, focus=0.5):
    def f(d):
        ctext(d, CW, 900, num, play(64, w=600), GOLD)
        y = 990
        for t in wrap(d, txt, play(54, True), 820): ctext(d, CW, y, t, play(54, True), WHITE); y += 70
    return f

def carousel():
    def s1(d):
        pill(d, CW, 830, "UN CHIN DE HUMOR (Y DE VERDAD)")
        ctext(d, CW, 905, "Señales de que", play(88, w=600), WHITE)
        ctext(d, CW, 1010, "ya te toca", play(88, w=600), WHITE)
        ctext(d, CW, 1115, "independizarte.", play(88, True, 600), GOLD)
        spaced(d, CW / 2, 1262, "DESLIZA  →", MED(24), (255, 255, 255, 220), 6)
    slide(1, N, 1, s1, start=520)
    slide(2, N, 3, sign("01", "Tienes 30 años y todavía pides permiso para usar la sala.", 3))
    slide(3, N, 5, sign("02", "Tu cuarto también es el depósito de la casa.", 5))
    slide(4, N, 2, sign("03", "Cocinas algo y alguien pregunta: “¿Y eso pa’ quién es?”", 2))
    slide(5, N, 4, sign("04", "Todavía te preguntan: “¿Y a qué hora tú vienes?”", 4), start=520)
    def s6(d):
        pill(d, CW, 760, "Y NO LO DECIMOS NOSOTROS")
        y = lines(d, CW, 850, ["“Toda persona tiene derecho", "a una vivienda digna con", "servicios básicos esenciales.”"], play(56, True), WHITE, 74)
        spaced(d, CW / 2, y + 30, "CONSTITUCIÓN DOMINICANA · ART. 59", MED(24), GOLD, 4)
        ctext(d, CW, y + 90, "182 años desde su proclamación, el 6 de noviembre de 1844.", LIGHT(30), (255, 255, 255, 230))
    slide(6, N, 8, s6, start=480)
    def s7(d):
        pill(d, CW, 610, "TU INDEPENDENCIA EMPIEZA AQUÍ")
        ctext(d, CW, 690, "Doral Residences", play(72, True), WHITE)
        spaced(d, CW / 2, 790, "COSTA BÁVARO · PUNTA CANA", MED(24), (255, 255, 255, 220), 6)
        ctext(d, CW, 845, "US$1,175", play(124, w=600), GOLD)
        spaced(d, CW / 2, 1000, "AL MES · LARGO PLAZO", MED(26), WHITE, 6)
        d.line([(CW / 2 - 50, 1058), (CW / 2 + 50, 1058)], fill=GOLD, width=2)
        lines(d, CW, 1082, ["2 habitaciones · 2 baños · 94.75 m²", "Amueblado · Piscina · Coworking", "Mantenimiento incluido"], LIGHT(34), WHITE, 48)
        spaced(d, CW / 2, 1250, "WHATSAPP 849-247-2107", MED(26), GOLD, 5)
    slide(7, N, 7, s7, start=360, strength=1.0)
    def s8(d):
        ctext(d, CW, 780, "¿Cuántas te pasaron?", play(80, w=600), WHITE)
        ctext(d, CW, 880, "Sé honesto…", play(80, True, 600), GOLD)
        lines(d, CW, 1010, ["Cuéntanos en los comentarios y etiqueta", "a quien ya le toca independizarse."], LIGHT(36), WHITE, 52)
        pill(d, CW, 1180, "SÍGUENOS · @LUXURYRENTHOUSERD")
    slide(8, N, 6, s8, start=460, strength=1.0)

# ---------------- HISTORIAS 1080x1920 ----------------
SW, SH = 1080, 1920
def story(name, ph, draw_fn, start=900, strength=0.95, focus=0.5):
    im = photo(ph, SW, SH, focus).convert("RGBA"); im.alpha_composite(grad(SW, SH, 560, 1.0, top=0.5, ex=0.75))
    d = ImageDraw.Draw(im); brand(d, SW, 250); draw_fn(d)
    im.convert("RGB").save(f"{OUT}/historia_{name}.jpg", quality=95, subsampling=0)

def stories():
    def h1(d):
        pill(d, SW, 1060, "TODO DOMINICANO LO HA ESCUCHADO")
        ctext(d, SW, 1140, "“Mientras tú vivas", play(84, True, 600), WHITE)
        ctext(d, SW, 1240, "en esta casa…”", play(84, True, 600), WHITE)
        ctext(d, SW, 1380, "Ya tú sabes cómo termina.", LIGHT(40), WHITE)
        ctext(d, SW, 1436, "¿Y tú qué estás esperando pa’ independizarte?", LIGHT(36), GOLD)
        pill(d, SW, 1560, "RESPÓNDENOS AQUÍ ABAJO", fill=(255, 255, 255), color=GREEN)
    story("1_humor", 8, h1, focus=0.35)
    def h2(d):
        pill(d, SW, 980, "HOY, 6 DE NOVIEMBRE")
        ctext(d, SW, 1055, "182 años de nuestra", play(76, w=600), WHITE)
        ctext(d, SW, 1145, "Constitución", play(76, True, 600), GOLD)
        y = lines(d, SW, 1290, ["“Toda persona tiene derecho a una", "vivienda digna con servicios", "básicos esenciales.”"], play(48, True), WHITE, 64)
        spaced(d, SW / 2, y + 26, "ART. 59", MED(26), GOLD, 6)
        ctext(d, SW, y + 100, "Nosotros nos lo tomamos en serio.", LIGHT(38), WHITE)
    story("2_constitucion", 5, h2, start=760, focus=0.4)
    def h3(d):
        pill(d, SW, 1080, "LO QUE TU JEFE NO TE DIJO")
        ctext(d, SW, 1160, "El lunes 9", play(116, w=600), WHITE)
        ctext(d, SW, 1290, "no se trabaja.", play(116, True, 600), GOLD)
        lines(d, SW, 1460, ["El descanso del Día de la Constitución", "se pasó para el lunes. Fin de semana largo."], LIGHT(36), WHITE, 50)
        ctext(d, SW, 1600, "¿Qué vas a hacer con tu lunes libre?", MED(38), WHITE)
    story("3_feriado", 4, h3, start=820, focus=0.5)
    def h4(d):
        pill(d, SW, 900, "ANTES DE ALQUILAR")
        ctext(d, SW, 975, "3 cosas que nunca", play(76, w=600), WHITE)
        ctext(d, SW, 1065, "debes saltarte", play(76, True, 600), GOLD)
        items = [("1", "Ve la propiedad en persona", "o por videollamada en vivo."), ("2", "Pide el contrato por escrito", "con todo bien detallado."),
                 ("3", "No pagues nada sin recibo", "y a nombre de quien corresponde.")]
        y = 1220
        for n, a, b in items:
            d.ellipse([150, y + 4, 214, y + 68], outline=GOLD, width=2); ctext_x(d, 182, y + 10, n, play(40, w=600), GOLD)
            d.text((250, y), a, font=MED(40), fill=WHITE); d.text((250, y + 52), b, font=LIGHT(34), fill=(255, 255, 255, 220)); y += 140
        ctext(d, SW, y + 20, "¿Te ha pasado algo? Cuéntanos.", LIGHT(36), GOLD)
    story("4_educativo", 2, h4, start=640, strength=1.0, focus=0.55)
    def h5(d):
        pill(d, SW, 980, "DISPONIBLE · COSTA BÁVARO")
        ctext(d, SW, 1060, "Doral Residences", play(80, True), WHITE)
        ctext(d, SW, 1160, "US$1,175", play(150, w=600), GOLD)
        spaced(d, SW / 2, 1345, "AL MES · LARGO PLAZO", MED(28), WHITE, 6)
        d.line([(SW / 2 - 60, 1410), (SW / 2 + 60, 1410)], fill=GOLD, width=2)
        lines(d, SW, 1440, ["2 habitaciones · 2 baños · Amueblado", "Piscina · Coworking · Mantenimiento incluido"], LIGHT(36), WHITE, 52)
        pill(d, SW, 1590, "ESCRÍBENOS 849-247-2107", fill=(255, 255, 255), color=GREEN)
    story("5_venta", 1, h5, start=700, strength=1.0, focus=0.3)

def ctext_x(d, cx, y, t, f, fill): d.text((cx - d.textlength(t, font=f) / 2, y), t, font=f, fill=fill)

if __name__ == "__main__":
    carousel(); stories(); print("ok", sorted(os.listdir(OUT)))
