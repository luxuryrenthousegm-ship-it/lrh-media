#!/usr/bin/env python3
"""Historia interactiva 1080x1920 (sin propiedades) — Colores Luxury. Sábado en la noche: ¿A, B o C?"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
F = f"{S}/fonts"
GREEN, DEEP, STONE, STONE_LT, WHITE = (52, 59, 52), (42, 48, 42), (156, 152, 147), (220, 217, 212), (255, 255, 255)
W, H, SC = 1080, 1920, 2
w, h = W * SC, H * SC
bod = lambda sz, it=False: ImageFont.truetype(f"{F}/bodoni-moda-latin-400-{'italic' if it else 'normal'}.woff", sz * SC)
jost = lambda wt, sz: ImageFont.truetype(f"{F}/jost-latin-{wt}-normal.woff", sz * SC)

# fondo verde Luxury con textura de piedra muy sutil
rng = np.random.default_rng(3)
n = rng.normal(0, 1, (h // 8, w // 8)).astype(np.float32)
n = np.asarray(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6 * SC)), np.float32) / 255
yy = np.linspace(0, 1, h)[:, None]
base = np.array(GREEN, np.float32) * (1 - 0.25 * yy[..., None]) + np.array(DEEP, np.float32) * 0.25 * yy[..., None]
base = base + (n[..., None] - 0.5) * 10 + rng.normal(0, 2.2, (h, w, 1))
img = Image.fromarray(base.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)

def sp(y, t, f, fill, track):
    track *= SC; ws = [d.textlength(c, font=f) for c in t]; x = (w - sum(ws) - track * (len(t) - 1)) / 2
    for c, ww in zip(t, ws): d.text((x, y * SC), c, font=f, fill=fill); x += ww + track
def ct(y, t, f, fill): d.text(((w - d.textlength(t, font=f)) / 2, y * SC), t, font=f, fill=fill)

# marca
sp(250, "LUXURY", bod(34), WHITE, 11)
sp(296, "RENT HOUSE", jost(400, 12), STONE_LT, 7)
# arco fino de fondo (eco del logo, sin usar el logo)
ax0, ax1, atop = int(w * 0.16), int(w * 0.84), 380 * SC
d.arc([ax0, atop, ax1, atop + (ax1 - ax0)], 180, 360, fill=(*STONE,), width=2 * SC)
d.line([(ax0, atop + (ax1 - ax0) // 2), (ax0, 1560 * SC)], fill=STONE, width=2 * SC)
d.line([(ax1, atop + (ax1 - ax0) // 2), (ax1, 1560 * SC)], fill=STONE, width=2 * SC)

sp(520, "SÁBADO EN LA NOCHE", jost(500, 22), STONE_LT, 8)
ct(575, "¿Tú eres de…?", bod(86, True), WHITE)

opts = [("A", "Cena fuera", "un buen restaurante en Bávaro"),
        ("B", "Plan de casa", "sofá, película y algo de picar"),
        ("C", "Atardecer en la playa", "y después ya veremos")]
y = 790
for letter, title, sub in opts:
    x0, x1 = int(w * 0.22), int(w * 0.78)
    d.rectangle([x0, y * SC, x1, (y + 170) * SC], fill=(*DEEP,), outline=STONE, width=2 * SC)
    cx = x0 + 70 * SC; cy = (y + 85) * SC; r = 42 * SC
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=STONE_LT, width=2 * SC)
    f = bod(46); d.text((cx - d.textlength(letter, font=f) / 2, cy - 34 * SC), letter, font=f, fill=WHITE)
    d.text((x0 + 140 * SC, (y + 38) * SC), title, font=bod(40), fill=WHITE)
    d.text((x0 + 140 * SC, (y + 98) * SC), sub, font=jost(300, 26), fill=STONE_LT)
    y += 200

ct(1410, "Respóndenos con A, B o C", jost(500, 36), WHITE)
ct(1462, "y te leemos todas.", jost(300, 30), STONE_LT)
sp(1640, "TU CASA PARA CUALQUIERA DE LAS TRES", jost(400, 18), STONE_LT, 5)
sp(1676, "@LUXURYRENTHOUSERD", jost(500, 18), WHITE, 6)

img = img.resize((W, H), Image.LANCZOS)
img.save(f"{S}/Historia_Sabado_ABC.jpg", quality=95, subsampling=0)
print("ok")
