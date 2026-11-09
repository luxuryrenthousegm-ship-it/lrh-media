#!/usr/bin/env python3
"""Historia animada 1080x1920, 15 s: 'Dime dónde vivirías y te digo quién eres' — 4 zonas con ruleta. Colores Luxury + acento rojo."""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
F = f"{S}/fonts"; OUT = f"{S}/zonas"; os.makedirs(OUT, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 15.0
GREEN, DEEP, STONE, STONE_LT, IVORY, RED = (52, 59, 52), (38, 44, 38), (156, 152, 147), (220, 217, 212), (250, 248, 244), (214, 64, 46)
bod = lambda sz, it=False: ImageFont.truetype(f"{F}/bodoni-moda-latin-400-{'italic' if it else 'normal'}.woff", sz)
jost = lambda wt, sz: ImageFont.truetype(f"{F}/jost-latin-{wt}-normal.woff", sz)
ZONAS = [("Cocotal", "Golf, palmeras y paz.", "Tú madrugas el domingo."),
         ("Vista Cana", "Playa artificial y todo adentro.", "Tú no sales ni pa' la esquina."),
         ("Punta Cana Village", "Cafecito, tiendas y el aeropuerto cerca.", "Tú siempre vas de prisa."),
         ("Cap Cana", "Marina, playa y yates de vecino.", "Tú vas con todo.")]

def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3

# fondo fijo con textura sutil
rng = np.random.default_rng(5)
n = rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32)
n = np.asarray(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
yy = np.linspace(0, 1, H)[:, None, None]
bg = np.array(GREEN, np.float32) * (1 - 0.35 * yy) + np.array(DEEP, np.float32) * 0.35 * yy + (n[..., None] - .5) * 9 + rng.normal(0, 2, (H, W, 1))
BG = Image.fromarray(bg.clip(0, 255).astype(np.uint8))

def ct(d, y, t, f, fill): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)
def sp(d, y, t, f, fill, tr):
    ws = [d.textlength(c, font=f) for c in t]; x = (W - sum(ws) - tr * (len(t) - 1)) / 2
    for c, w in zip(t, ws): d.text((x, y), c, font=f, fill=fill); x += w + tr

# ruleta: 5.0 s → 10.6 s, se acelera y luego frena; se detiene sin elegir
spins = []
t = 5.0; step = 0.32
while t < 10.6:
    spins.append(t); t += step; step = max(0.09, step * 0.8) if t < 7.8 else step * 1.22
def highlighted(t):
    if t < 5.0 or t >= 10.6: return None
    k = sum(1 for s in spins if s <= t) - 1
    return k % 4

def frame(t):
    img = BG.copy().convert("RGBA"); d = ImageDraw.Draw(img, "RGBA")
    sp(d, 250, "LUXURY", bod(34), IVORY, 11); sp(d, 296, "RENT HOUSE", jost(400, 12), STONE_LT, 7)
    a = ease(t / 0.8)
    sp(d, 390 + 20 * (1 - a), "DIME DÓNDE VIVIRÍAS", jost(500, 30), (*RED, int(255 * a)), 7)
    b = ease((t - 0.4) / 0.8)
    ct(d, 440 + 20 * (1 - b), "y te digo quién eres", bod(76, True), (*IVORY, int(255 * b)))
    hl = highlighted(t)
    y0 = 600
    for i, (name, l1, l2) in enumerate(ZONAS):
        c = ease((t - 1.5 - i * 0.6) / 0.5)
        if c <= 0: y0 += 210; continue
        x0 = int(110 - 80 * (1 - c)) if i % 2 == 0 else int(110 + 80 * (1 - c))
        x1 = x0 + 860; y = y0
        on = hl == i
        fill = (*RED, int(240 * c)) if on else (*DEEP, int(235 * c))
        d.rectangle([x0, y, x1, y + 180], fill=fill, outline=(*((IVORY if on else STONE)), int(255 * c)), width=2)
        cx, cy, r = x0 + 72, y + 90, 44
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*(IVORY if on else RED), int(255 * c)), width=3)
        num = str(i + 1); f = bod(52)
        d.text((cx - d.textlength(num, font=f) / 2, cy - 38), num, font=f, fill=(*IVORY, int(255 * c)))
        d.text((x0 + 150, y + 22), name, font=bod(50), fill=(*IVORY, int(255 * c)))
        d.text((x0 + 150, y + 90), l1, font=jost(300, 27), fill=(*(IVORY if on else STONE_LT), int(255 * c)))
        d.text((x0 + 150, y + 128), l2, font=jost(500, 27), fill=(*(IVORY if on else RED), int(255 * c)))
        y0 += 210
    # pregunta final + caja para responder (aquí va el sticker si se publica desde la app)
    e = ease((t - 10.8) / 0.5)
    if e > 0:
        pulse = 1 + 0.03 * np.sin((t - 10.8) * 7) if t < 13 else 1
        ct(d, 1470, "¿Cuál es la tuya?", bod(int(70 * pulse), True), (*IVORY, int(255 * e)))
        bx0, bx1, by = 170, 910, 1575
        dash = 22
        for x in range(bx0, bx1, dash * 2):
            d.line([(x, by), (min(x + dash, bx1), by)], fill=(*RED, int(255 * e)), width=3)
            d.line([(x, by + 150), (min(x + dash, bx1), by + 150)], fill=(*RED, int(255 * e)), width=3)
        for yv in range(by, by + 150, dash * 2):
            d.line([(bx0, yv), (bx0, min(yv + dash, by + 150))], fill=(*RED, int(255 * e)), width=3)
            d.line([(bx1, yv), (bx1, min(yv + dash, by + 150))], fill=(*RED, int(255 * e)), width=3)
        ct(d, by + 34, "Responde con 1, 2, 3 o 4", jost(500, 38), (*IVORY, int(255 * e)))
        ct(d, by + 88, "y etiqueta a tu vecino ideal", jost(300, 28), (*STONE_LT, int(255 * e)))
    return img.convert("RGB")

def render():
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", f"{OUT}/v.mp4"], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): enc.stdin.write(frame(k / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    mus = "/home/claude/lrh-media/audio/historia_zonas_musica.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/v.mp4", "-i", mus, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={DUR - 0.8}:d=0.8", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    "-t", str(DUR), "-movflags", "+faststart", f"{S}/Historia_Zonas.mp4"], check=True)
    frame(14.5).save(f"{S}/Historia_Zonas_final.jpg", quality=95, subsampling=0)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for tt in map(float, sys.argv[1:]): frame(tt).save(f"{OUT}/pv_{tt}.jpg", quality=88)
    else:
        render(); print("ok")
