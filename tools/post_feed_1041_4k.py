#!/usr/bin/env python3
"""1041 en 2160x2700 (4:5): foto ampliada con Real-ESRGAN + revelado natural tipo DSLR + diseño del feed."""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
FS = f"{S}/fonts"; FI = "/usr/share/fonts/opentype/inter/"
W, H, K = 2160, 2700, 2  # K = escala respecto al diseño de 1080
SRC = "/home/claude/lrh-media/src/1041/original/"

def develop():
    """Revelado natural sin IA generativa: limpieza de ruido/JPEG en tamaño original, luego ampliación Lanczos."""
    u8 = cv2.imread(SRC + "p1.jpg")
    u8 = cv2.fastNlMeansDenoisingColored(u8, None, 2, 2, 7, 21)          # ruido y bloques JPEG, suave
    lab = cv2.cvtColor(u8, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    m = (L > 170) & (np.abs(A - 128) < 12) & (np.abs(B - 128) < 18)    # balance de blancos: 30% hacia neutro
    if m.any(): A -= (A[m].mean() - 128) * 0.3; B -= (B[m].mean() - 128) * 0.3
    x = L / 255                                                         # HDR suave: sombras arriba, altas protegidas
    x = x + 0.05 * np.clip(0.5 - x, 0, 1) * 2 * (1 - x) - 0.03 * x ** 8
    L = x * 255
    out = cv2.cvtColor(np.dstack([L, A, B]).clip(0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    out = cv2.resize(out, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    bb = cv2.GaussianBlur(out, (0, 0), 30); out = out + (out - bb) * 0.08           # microcontraste
    bs = cv2.GaussianBlur(out, (0, 0), 1.6); out = out + (out - bs) * 0.45          # nitidez
    return Image.fromarray(cv2.cvtColor(out.clip(0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))

ph = develop()
ph.save(f"{S}/1041_cocina_revelada_4k.png")
ph = ph.convert("RGBA")
ov = Image.new("RGBA", (W, H)); od = ImageDraw.Draw(ov)
for y in range(H):
    a = 0.0
    if y < 260 * K: a = 0.28 * (1 - y / (260 * K))
    if y > 700 * K: a = max(a, 0.9 * ((y - 700 * K) / (H - 700 * K)) ** 0.95)
    od.line([(0, y), (W, y)], fill=(10, 14, 13, int(255 * a)))
ph.alpha_composite(ov); d = ImageDraw.Draw(ph)
corm = lambda wt, sz: ImageFont.truetype(f"{FS}/cormorant-garamond-latin-{wt}-normal.woff", sz * K)
inter = lambda n, sz: ImageFont.truetype(FI + n, sz * K)

def spaced(y, t, f, fill, track):
    track *= K; ws = [d.textlength(c, font=f) for c in t]; x = (W - sum(ws) - track * (len(t) - 1)) / 2
    for c, w in zip(t, ws): d.text((x, y * K), c, font=f, fill=fill); x += w + track

spaced(52, "LUXURY", corm(500, 34), (255, 255, 255, 235), 9)
spaced(94, "RENT HOUSE", inter("Inter-Regular.otf", 11), (255, 255, 255, 220), 5)
hook = ImageFont.truetype(f"{FS}/cormorant-garamond-latin-500-italic.woff", 50 * K)
for k, ln in enumerate(["¿Y si vivieras donde hay", "golf, piscina y gimnasio?"]):
    d.text(((W - d.textlength(ln, font=hook)) / 2, (930 + k * 58) * K), ln, font=hook, fill=(255, 255, 255, 245))
spaced(1078, "FOR RENT", inter("Inter-Medium.otf", 17), (255, 255, 255, 235), 6)
spaced(1108, "PANORAMA PARK", corm(400, 88), (255, 255, 255), 12)
spaced(1232, "VISTA CANA   -   1 HABITACIÓN   -   1.5 BAÑOS   -   MASCOTAS", inter("Inter-Regular.otf", 16), (255, 255, 255, 230), 4)
ph.convert("RGB").save(f"{S}/Post_Feed_1041_4K.jpg", quality=95, subsampling=0)
print("ok")
