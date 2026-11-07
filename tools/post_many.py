#!/usr/bin/env python3
"""Post único 1080x1350 con la Paleta Many sobre foto real (1038, de noche)."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
F = "/usr/share/fonts/opentype/inter/"
YEL, NOCHE, MARRON, TERRA, CLARO = (252, 242, 82), (13, 19, 15), (66, 34, 24), (128, 66, 46), (242, 239, 230)
W, H = 1080, 1350

im = Image.open("/home/claude/lrh-media/src/1038/p1.jpg").convert("RGB")
iw, ih = im.size; ch = int(iw * H / W); im = im.crop((0, ih - ch, iw, ih)).resize((W, H), Image.LANCZOS)
im = ImageEnhance.Contrast(im).enhance(1.05)
im = Image.blend(im, Image.new("RGB", (W, H), MARRON), 0.10)  # tono cálido de la paleta
im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2)).convert("RGBA")
ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
for y in range(H):
    a = 0
    if y < 420: a = 0.62 * (1 - y / 420) ** 1.1
    if y > 1000: a = max(a, 0.75 * ((y - 1000) / (H - 1000)) ** 1.2)
    d.line([(0, y), (W, y)], fill=(*NOCHE, int(255 * a)))
im.alpha_composite(ov); d = ImageDraw.Draw(im)

def ctext(y, t, f, fill, track=0):
    if track <= 0:  # usar el kerning de la fuente
        d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill); return
    ws = [d.textlength(c, font=f) for c in t]; x = (W - sum(ws) - track * (len(t) - 1)) / 2
    for c, w in zip(t, ws): d.text((x, y), c, font=f, fill=fill); x += w + track

head = ImageFont.truetype(F + "InterDisplay-Black.otf", 92)
ctext(70, "¿Tu apartamento", head, YEL)
ctext(170, "lleva meses vacío?", head, YEL)
ctext(1185, "Sin inquilino, no hay ingreso.", ImageFont.truetype(F + "InterDisplay-Bold.otf", 52), YEL)
ctext(1262, "LUXURY RENT HOUSE  ·  ADMINISTRACIÓN Y ALQUILER A LARGO PLAZO", ImageFont.truetype(F + "Inter-Medium.otf", 19), CLARO, 2)
im.convert("RGB").save(f"{S}/Post_Many_Propietarios.jpg", quality=95, subsampling=0)
print("ok")
