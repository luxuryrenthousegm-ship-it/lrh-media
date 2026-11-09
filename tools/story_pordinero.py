#!/usr/bin/env python3
"""Historia 1080x1920: dato curioso 'Por dinero' (Ley 139-97). Tipografía estilo Selling Sunset: Playfair Display Italic + Montserrat espaciada. Colores de la bandera."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"
W, H, SC = 1080, 1920, 2
AZUL, AZUL_OSC, ROJO, BLANCO = (0, 45, 98), (0, 28, 66), (206, 17, 38), (255, 255, 255)
mont = lambda wt, sz: ImageFont.truetype(f"{F}/montserrat-latin-{wt}-normal.woff", sz * SC)
def pit(sz):
    f = ImageFont.truetype(f"{F}/PlayfairItalic.ttf", sz * SC)
    try: f.set_variation_by_axes([400])
    except Exception: pass
    return f
w, h = W * SC, H * SC
yy = np.linspace(0, 1, h)[:, None, None]
bg = np.array(AZUL, np.float32) * (1 - yy) + np.array(AZUL_OSC, np.float32) * yy
bg = bg + np.random.default_rng(2).normal(0, 1.6, (h, w, 1))
img = Image.fromarray(np.repeat(bg, w, axis=1).clip(0, 255).astype(np.uint8) if bg.shape[1] == 1 else bg.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(img, "RGBA")
# cruz blanca muy sutil (eco de la bandera)

def sp(y, t, f, fill, tr):
    tr *= SC; ws = [d.textlength(c, font=f) for c in t]; x = (w - sum(ws) - tr * (len(t) - 1)) / 2
    for c, ww in zip(t, ws): d.text((x, y * SC), c, font=f, fill=fill); x += ww + tr
def spw(t, f, tr): return sum(d.textlength(c, font=f) for c in t) + tr * SC * (len(t) - 1)

sp(250, "LUXURY RENT HOUSE", mont(500, 18), BLANCO, 9)
sp(410, "Dato curioso del lunes feriado", pit(46), BLANCO, 3)
sp(510, "¿POR QUÉ EL FERIADO", mont(600, 38), BLANCO, 12)
sp(565, "SE MUEVE AL LUNES?", mont(600, 38), BLANCO, 12)
sp(690, "POR DINERO.", mont(600, 104), BLANCO, 14)

# panel rojo con la cifra
d.rectangle([90 * SC, 880 * SC, 990 * SC, 1290 * SC], fill=ROJO)
sp(930, "La propia ley calculó que cada día laborable aportaba", pit(30), BLANCO, 1)
sp(1000, "RD$400", mont(600, 150), BLANCO, 8)
sp(1185, "MILLONES AL PIB", mont(500, 34), BLANCO, 12)

lines = ["Un feriado a mitad de semana partía la semana",
         "en dos. Desde 1997, se pasa al lunes:",
         "el país sigue produciendo y tú ganas",
         "un fin de semana largo para viajar."]
for i, ln in enumerate(lines): sp(1380 + i * 52, ln, mont(300, 31), BLANCO, 0)
sp(1650, "LEY 139-97  ·  CIFRA DE 1997", mont(500, 18), (200, 212, 230), 7)
sp(1700, "@LUXURYRENTHOUSERD", mont(500, 18), BLANCO, 7)
img.resize((W, H), Image.LANCZOS).save(f"{S}/Historia_Por_Dinero.jpg", quality=95, subsampling=0)
print("ok")
