#!/usr/bin/env python3
"""Historia 1080x1920 — feriado del Día de la Constitución, dato curioso. Colores de la bandera dominicana."""
from PIL import Image, ImageDraw, ImageFont
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"
W, H, SC = 1080, 1920, 2
AZUL, ROJO, BLANCO, CREMA = (0, 45, 98), (206, 17, 38), (255, 255, 255), (246, 244, 240)
bod = lambda sz, it=False: ImageFont.truetype(f"{F}/bodoni-moda-latin-400-{'italic' if it else 'normal'}.woff", sz * SC)
jost = lambda wt, sz: ImageFont.truetype(f"{F}/jost-latin-{wt}-normal.woff", sz * SC)
img = Image.new("RGB", (W * SC, H * SC), BLANCO); d = ImageDraw.Draw(img)
Y1, Y2 = 690, 1290
d.rectangle([0, 0, W * SC, Y1 * SC], fill=AZUL)
d.rectangle([0, Y2 * SC, W * SC, H * SC], fill=ROJO)

def ct(y, t, f, fill): d.text(((W * SC - d.textlength(t, font=f)) / 2, y * SC), t, font=f, fill=fill)
def sp(y, t, f, fill, tr):
    tr *= SC; ws = [d.textlength(c, font=f) for c in t]; x = (W * SC - sum(ws) - tr * (len(t) - 1)) / 2
    for c, w in zip(t, ws): d.text((x, y * SC), c, font=f, fill=fill); x += w + tr

# Azul: marca y gancho
sp(250, "LUXURY", bod(32), BLANCO, 11); sp(293, "RENT HOUSE", jost(400, 12), (200, 210, 225), 7)
sp(380, "FELIZ LUNES FERIADO", jost(500, 22), (200, 210, 225), 7)
ct(425, "Hoy no se trabaja", bod(66), BLANCO)
ct(505, "por la Constitución…", bod(66), BLANCO)
ct(595, "…pero ¿sabías esto?", bod(46, True), (200, 210, 225))

# Blanco: el dato
sp(745, "DATO CURIOSO", jost(500, 22), ROJO, 8)
for k, ln in enumerate(["En el centro del escudo de", "nuestra bandera hay una Biblia", "abierta en Juan 8:32."]):
    ct(795 + k * 68, ln, bod(52), AZUL)
d.line([(W * SC / 2 - 50 * SC, 1027 * SC), (W * SC / 2 + 50 * SC, 1027 * SC)], fill=ROJO, width=2 * SC)
ct(1060, "“Y conoceréis la verdad,", bod(44, True), ROJO)
ct(1118, "y la verdad os hará libres.”", bod(44, True), ROJO)
sp(1190, "JUAN 8:32", jost(500, 18), AZUL, 6)

# Rojo: cierre y participación
ct(1360, "Tu casa, tus reglas:", bod(58), BLANCO)
ct(1432, "también merecen su constitución.", bod(46, True), BLANCO)
d.rounded_rectangle([(W / 2 - 330) * SC, 1560 * SC, (W / 2 + 330) * SC, 1660 * SC], 50 * SC, fill=BLANCO)
ct(1584, "¿Lo sabías? Responde Sí o No", jost(500, 36), ROJO)
sp(1720, "@LUXURYRENTHOUSERD", jost(500, 18), BLANCO, 6)
img.resize((W, H), Image.LANCZOS).save(f"{S}/Historia_Constitucion_Dato.jpg", quality=95, subsampling=0)
print("ok")
