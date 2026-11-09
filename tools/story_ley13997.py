#!/usr/bin/env python3
"""Serie de 4 historias 1080x1920, estilo editorial moderno (broker de EE. UU.): ¿Por qué el feriado se mueve? Ley 139-97."""
from PIL import Image, ImageDraw, ImageFont
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"; FI = "/usr/share/fonts/opentype/inter/"
W, H, SC = 1080, 1920, 2
PAPER, INK, MUTED, GREEN, RULE = (244, 242, 238), (17, 18, 17), (110, 112, 108), (52, 59, 52), (205, 202, 196)
black = lambda sz: ImageFont.truetype(FI + "InterDisplay-Black.otf", sz * SC)
bold = lambda sz: ImageFont.truetype(FI + "InterDisplay-Bold.otf", sz * SC)
med = lambda sz: ImageFont.truetype(FI + "Inter-Medium.otf", sz * SC)
reg = lambda sz: ImageFont.truetype(FI + "Inter-Regular.otf", sz * SC)
ital = lambda sz: ImageFont.truetype(f"{F}/bodoni-moda-latin-400-italic.woff", sz * SC)
X0, X1 = 90, 990  # márgenes

def wrap(d, text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw * SC: line = t
        else: out.append(line); line = w
    out.append(line); return out

def para(d, y, text, f, fill, lh, maxw=X1 - X0):
    for ln in wrap(d, text, f, maxw): d.text((X0 * SC, y * SC), ln, font=f, fill=fill); y += lh
    return y

def frame(n, dark=False):
    bg, fg = (GREEN, PAPER) if dark else (PAPER, INK)
    img = Image.new("RGB", (W * SC, H * SC), bg); d = ImageDraw.Draw(img)
    # cabecera editorial
    d.text((X0 * SC, 240 * SC), "LUXURY RENT HOUSE", font=med(18), fill=fg)
    t = f"DATO {n}/4"; d.text((X1 * SC - d.textlength(t, font=med(18)), 240 * SC), t, font=med(18), fill=fg)
    d.line([(X0 * SC, 280 * SC), (X1 * SC, 280 * SC)], fill=fg if dark else INK, width=2 * SC)
    # barra de progreso de la serie
    seg = (X1 - X0 - 30) / 4
    for i in range(4):
        x = X0 + i * (seg + 10)
        d.rectangle([x * SC, 300 * SC, (x + seg) * SC, 306 * SC], fill=(fg if i < n else (RULE if not dark else (90, 98, 90))))
    return img, d, fg

def foot(d, fg, text="@LUXURYRENTHOUSERD"):
    d.line([(X0 * SC, 1690 * SC), (X1 * SC, 1690 * SC)], fill=fg, width=1 * SC)
    d.text((X0 * SC, 1710 * SC), text, font=med(18), fill=fg)
    t = "DESLIZA →"; d.text((X1 * SC - d.textlength(t, font=med(18)), 1710 * SC), t, font=med(18), fill=fg)

def save(img, name): img.resize((W, H), Image.LANCZOS).save(f"{S}/ley13997/{name}.jpg", quality=95, subsampling=0)

import os; os.makedirs(f"{S}/ley13997", exist_ok=True)

# 1 — gancho
img, d, fg = frame(1)
d.text((X0 * SC, 420 * SC), "FERIADO · 9 NOV 2026", font=med(22), fill=MUTED)
y = 480
for ln in ["La Constitución", "es el 6 de", "noviembre.", "¿Por qué el", "feriado fue hoy?"]:
    d.text((X0 * SC, y * SC), ln, font=black(104), fill=INK); y += 118
d.text((X0 * SC, (y + 40) * SC), "Casi nadie sabe la respuesta.", font=ital(52), fill=GREEN)
foot(d, INK); save(img, "1_gancho")

# 2 — la ley
img, d, fg = frame(2)
d.text((X0 * SC, 400 * SC), "LA RESPUESTA TIENE NÚMERO", font=med(22), fill=MUTED)
d.text(((X0 - 8) * SC, 440 * SC), "139-97", font=black(250), fill=INK)
y = para(d, 760, "Es la ley que mueve los feriados en República Dominicana.", bold(46), INK, 60)
d.line([(X0 * SC, (y + 30) * SC), (X1 * SC, (y + 30) * SC)], fill=RULE, width=2 * SC)
rows = [("Promulgada", "19 de junio de 1997"), ("Firmada por", "el presidente Leonel Fernández"),
        ("Si cae martes o miércoles", "se pasa al lunes anterior"), ("Si cae jueves o viernes", "se pasa al lunes siguiente")]
y += 60
for k, v in rows:
    d.text((X0 * SC, y * SC), k.upper(), font=med(19), fill=MUTED)
    d.text((X0 * SC, (y + 32) * SC), v, font=bold(40), fill=INK); y += 118
foot(d, INK, "FUENTE: LEY NO. 139-97"); save(img, "2_ley")

# 3 — el porqué
img, d, fg = frame(3, dark=True)
d.text((X0 * SC, 400 * SC), "¿Y POR QUÉ LA HICIERON?", font=med(22), fill=(200, 205, 198))
d.text((X0 * SC, 440 * SC), "Por dinero.", font=black(130), fill=PAPER)
y = para(d, 640, "La propia ley calculó que cada día laborable aportaba", reg(40), (225, 228, 222), 54)
d.text((X0 * SC, (y + 10) * SC), "RD$400", font=black(190), fill=PAPER)
d.text((X0 * SC, (y + 230) * SC), "millones al PIB (cifra de 1997).", font=bold(44), fill=PAPER)
y += 330
y = para(d, y, "Un feriado a mitad de semana rompía dos días de trabajo. Moviéndolo al lunes, la producción sigue y la gente gana un fin de semana largo para viajar dentro del país.", reg(36), (215, 220, 212), 52)
foot(d, PAPER, "FUENTE: LEY NO. 139-97, CONSIDERANDOS"); save(img, "3_porque")

# 4 — dato extra + cierre
img, d, fg = frame(4)
d.text((X0 * SC, 400 * SC), "EL DETALLE QUE CASI NADIE SABE", font=med(22), fill=MUTED)
y = para(d, 450, "El descanso se mueve, pero la fecha no se olvida.", black(70), INK, 82)
y = para(d, y + 30, "La ley pide que el día exacto (este año, el viernes 6) escuelas y lugares de trabajo hagan actividades para honrar la Constitución.", reg(36), INK, 52)
d.line([(X0 * SC, (y + 30) * SC), (X1 * SC, (y + 30) * SC)], fill=RULE, width=2 * SC)
d.text((X0 * SC, (y + 60) * SC), "ESTOS NUNCA SE MUEVEN", font=med(19), fill=MUTED)
y += 100
for f_ in ["1 de enero · 21 de enero · 27 de febrero", "24 de septiembre · 25 de diciembre"]:
    d.text((X0 * SC, y * SC), f_, font=bold(38), fill=INK); y += 56
d.rounded_rectangle([X0 * SC, (y + 50) * SC, X1 * SC, (y + 170) * SC], 60 * SC, fill=GREEN)
t = "¿Lo sabías? Responde Sí o No"; f = bold(40)
d.text(((W * SC - d.textlength(t, font=f)) / 2, (y + 84) * SC), t, font=f, fill=PAPER)
d.line([(X0 * SC, 1690 * SC), (X1 * SC, 1690 * SC)], fill=INK, width=1 * SC)
d.text((X0 * SC, 1710 * SC), "SÍGUENOS PARA MÁS DATOS QUE NADIE TE CUENTA", font=med(18), fill=INK)
save(img, "4_cierre")
print("ok")
