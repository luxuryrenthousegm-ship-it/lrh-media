#!/usr/bin/env python3
"""Post gráfico 1080x1350 con la Paleta Many: un arco/puerta con atardecer (sin fotos)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
F = "/usr/share/fonts/opentype/inter/"
YEL, NOCHE, SOFA, OLIVA = (252, 242, 82), (13, 19, 15), (27, 33, 21), (51, 48, 30)
NAR, TERRA, ROSA, CLARO_R, CHOC, MOSC = (197, 109, 56), (128, 66, 46), (151, 82, 65), (165, 108, 87), (89, 55, 40), (66, 34, 24)
CREMA = (242, 239, 230)
W, H = 1080, 1350; SC = 2  # supermuestreo para bordes finos
w, h = W * SC, H * SC

yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
# fondo: verde noche con un resplandor cálido muy suave detrás del arco
r = np.sqrt(((xx - w / 2) / w) ** 2 + ((yy - h * 0.56) / h) ** 2)
glow = np.clip(1 - r / 0.55, 0, 1) ** 2
bg = np.array(NOCHE, np.float32) * (1 - glow[..., None] * 0.9) + np.array(SOFA, np.float32) * glow[..., None] * 0.9
img = Image.fromarray(bg.clip(0, 255).astype(np.uint8))

# arco (puerta)
ax0, ax1 = int(w * 0.27), int(w * 0.73); aw = ax1 - ax0
atop, abot = int(h * 0.33), int(h * 0.78)
mask = Image.new("L", (w, h), 0); md = ImageDraw.Draw(mask)
md.rectangle([ax0, atop + aw // 2, ax1, abot], fill=255); md.ellipse([ax0, atop, ax1, atop + aw], fill=255)
# interior: atardecer
t = np.clip((yy - atop) / (abot - atop), 0, 1)
horizon = 0.62
sky = np.where(t[..., None] < horizon,
               np.array(CLARO_R) * (1 - t[..., None] / horizon) + np.array(NAR) * (t[..., None] / horizon),
               np.array(TERRA) * (1 - (t[..., None] - horizon) / (1 - horizon)) + np.array(MOSC) * ((t[..., None] - horizon) / (1 - horizon)))
scene = Image.fromarray(sky.clip(0, 255).astype(np.uint8))
sd = ImageDraw.Draw(scene)
hy = atop + int((abot - atop) * horizon); sr = int(aw * 0.17)
sd.ellipse([w // 2 - sr, hy - sr, w // 2 + sr, hy + sr], fill=YEL)            # sol
sd.rectangle([0, hy, w, h], fill=ROSA)                                         # mar al atardecer
for k in range(9):                                                             # reflejos del sol
    yk = hy + 18 * SC + k * 22 * SC; ww = int(sr * (1.4 - k * 0.12))
    sd.rounded_rectangle([w // 2 - ww, yk, w // 2 + ww, yk + 6 * SC], 3 * SC, fill=(*YEL,))
# palmera en silueta (dentro del arco)
px, py = int(ax1 - aw * 0.2), hy + 4 * SC
trunk = []
for i in range(60):
    tt = i / 59; trunk.append((px + int(26 * SC * tt ** 2), py - int(aw * 0.52 * tt)))
for i, (x, y) in enumerate(trunk):
    rr = int((9 - 4 * i / 59) * SC); sd.ellipse([x - rr, y - rr, x + rr, y + rr], fill=NOCHE)
top = trunk[-1]
for ang, L in [(-175, .30), (-150, .32), (-122, .26), (-60, .26), (-30, .32), (-5, .30), (-95, .18)]:
    a = np.radians(ang); L *= aw; pts_up, pts_dn = [], []
    for s_ in np.linspace(0, 1, 18):
        cx = top[0] + np.cos(a) * L * s_; cy = top[1] + np.sin(a) * L * s_ + L * 0.45 * s_ * s_
        wid = 9 * SC * np.sin(np.pi * min(1, s_ * 1.1)) + 1
        nx, ny = -np.sin(a), np.cos(a)
        pts_up.append((cx + nx * wid, cy + ny * wid)); pts_dn.append((cx - nx * wid, cy - ny * wid))
    sd.polygon(pts_up + pts_dn[::-1], fill=NOCHE)
img.paste(scene, (0, 0), mask)
d = ImageDraw.Draw(img)
# marco del arco
fw = 14 * SC
d.arc([ax0 - fw, atop - fw, ax1 + fw, atop + aw + fw], 180, 360, fill=TERRA, width=fw)
d.line([(ax0 - fw // 2, atop + aw // 2), (ax0 - fw // 2, abot)], fill=TERRA, width=fw)
d.line([(ax1 + fw // 2, atop + aw // 2), (ax1 + fw // 2, abot)], fill=TERRA, width=fw)
# piso / alfombra
d.line([(int(w * 0.18), abot + fw // 2), (int(w * 0.82), abot + fw // 2)], fill=TERRA, width=4 * SC)
img = img.resize((W, H), Image.LANCZOS)

# grano fino para que no se vea plano
rng = np.random.default_rng(7); a = np.asarray(img).astype(np.float32)
a += rng.normal(0, 4.0, (H, W, 1)); img = Image.fromarray(a.clip(0, 255).astype(np.uint8))

d = ImageDraw.Draw(img)
def ctext(y, s, f, fill): d.text(((W - d.textlength(s, font=f)) / 2, y), s, font=f, fill=fill)
head = ImageFont.truetype(F + "InterDisplay-Black.otf", 84)
ctext(78, "¿Mudarte a Punta Cana", head, YEL)
ctext(172, "está en tu lista del 2027?", head, YEL)
ctext(1170, "Empieza por la puerta correcta.", ImageFont.truetype(F + "InterDisplay-Bold.otf", 50), YEL)
sm = ImageFont.truetype(F + "Inter-Medium.otf", 19); s = "LUXURY RENT HOUSE  ·  ALQUILER A LARGO PLAZO EN BÁVARO Y PUNTA CANA"
x = (W - (sum(d.textlength(c, font=sm) for c in s) + 2 * (len(s) - 1))) / 2
for c in s: d.text((x, 1258), c, font=sm, fill=CREMA); x += d.textlength(c, font=sm) + 2
img.save(f"{S}/Post_Many_Puerta_2027.jpg", quality=95, subsampling=0)
print("ok")
