#!/usr/bin/env python3
"""Reel 1080x1920 con fotos (1041): foto 4:5 a todo el ancho sobre carbón, movimiento suave, textos editoriales, cortes a 96 BPM."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"; SRC = "/home/claude/lrh-media/src/1041"
OUT = f"{S}/reel1041"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
CARBON, PIEDRA, ARENA, CALIDA, BLANCO = (47, 44, 33), (225, 223, 226), (203, 190, 180), (198, 152, 105), (255, 255, 255)
B = 60 / 96; SEG = 4 * B  # 2.5 s por escena
mont = lambda wt, sz: ImageFont.truetype(f"{F}/montserrat-latin-{wt}-normal.woff", sz)
def pit(sz):
    f = ImageFont.truetype(f"{F}/PlayfairItalic.ttf", sz)
    try: f.set_variation_by_axes([400])
    except Exception: pass
    return f
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

PH_W, PH_H, PH_Y = 1080, 1350, 300
def card(n):
    im = Image.open(f"{SRC}/p{n}.jpg").convert("RGB")
    im = im.resize((int(PH_W * 1.06), int(PH_H * 1.06)), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=35, threshold=2))
CARDS = {n: card(n) for n in (7, 3, 4, 5, 6)}

ESC = [(7, None, None), (3, "COCINA CON LÍNEA BLANCA", "Llegas y cocinas."), (4, "1 HABITACIÓN", "Tu espacio, tus reglas."),
       (5, "1.5 BAÑOS", "Uno para ti, medio para la visita."), (6, "GIMNASIO EN EL RESIDENCIAL", "La excusa de \"no tengo gym\" se acabó.")]
T_REVEAL = SEG * len(ESC); DUR = T_REVEAL + 6 * B + 0.4

def sp(d, y, t, f, fill, tr):
    ws = [d.textlength(c, font=f) for c in t]; x = (W - sum(ws) - tr * (len(t) - 1)) / 2
    for c, ww in zip(t, ws): d.text((x, y), c, font=f, fill=fill); x += ww + tr
def ct(d, y, t, f, fill): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)

def frame(t):
    img = Image.new("RGBA", (W, H), (*CARBON, 255)); d = ImageDraw.Draw(img)
    sp(d, 190, "LUXURY RENT HOUSE", mont(500, 17), (*PIEDRA, 255), 8)
    if t < T_REVEAL:
        i = int(t // SEG); lt = t - i * SEG; n, cap, line = ESC[i]
        z = lt / SEG  # empuje suave 0 → 6 %
        src = CARDS[n]; sw, sh = src.size
        cw, ch = int(sw / (1.0 + 0.0 * z) / 1.06 * (1.06 - 0.05 * z)), 0
        cw = int(PH_W * (1.06 - 0.055 * z)); ch = int(PH_H * (1.06 - 0.055 * z))
        x0, y0 = (sw - cw) // 2, (sh - ch) // 2
        ph = src.crop((x0, y0, x0 + cw, y0 + ch)).resize((PH_W, PH_H), Image.BICUBIC)
        a = ease(lt / 0.25) if i > 0 else 1
        img.paste(Image.blend(Image.new("RGB", (PH_W, PH_H), CARBON), ph, a), (0, PH_Y))
        d = ImageDraw.Draw(img)
        if i == 0:
            ov = Image.new("RGBA", (W, H)); od = ImageDraw.Draw(ov)
            for y in range(PH_Y, PH_Y + 520): od.line([(0, y), (W, y)], fill=(20, 20, 13, int(200 * (1 - (y - PH_Y) / 520))))
            img.alpha_composite(ov); d = ImageDraw.Draw(img)
            b1, b2, b3 = ease((lt - 0.15) / 0.5), ease((lt - 0.55) / 0.5), ease((lt - 0.95) / 0.5)
            sp(d, 360, "VISTA CANA  ·  PUNTA CANA", mont(500, 19), (*ARENA, int(255 * b1)), 7)
            ct(d, 400 + 20 * (1 - b1), "Lo que consigues con", pit(66), (*BLANCO, int(255 * b1)))
            sp(d, 500 + 20 * (1 - b2), "US$800 AL MES", mont(500, 58), (*BLANCO, int(255 * b2)), 10)
            ct(d, 580 + 20 * (1 - b3), "en Punta Cana", pit(66), (*BLANCO, int(255 * b3)))
        else:
            b1, b2 = ease((lt - 0.2) / 0.45), ease((lt - 0.45) / 0.45)
            sp(d, 1700 + 14 * (1 - b1), cap, mont(500, 21), (*ARENA, int(255 * b1)), 8)
            ct(d, 1745 + 14 * (1 - b2), line, pit(46), (*BLANCO, int(255 * b2)))
    else:
        lt = t - T_REVEAL
        a, b, c, e = ease(lt / 0.4), ease((lt - B) / 0.45), ease((lt - 2 * B) / 0.5), ease((lt - 4 * B) / 0.5)
        sp(d, 560, "PANORAMA PARK & GARDEN", mont(500, 22), (*ARENA, int(255 * a)), 8)
        ct(d, 615, "Todo esto, por", pit(70), (*BLANCO, int(255 * a)))
        s = 1 + 0.12 * (1 - b)
        f = mont(500, int(170 * s)); ct(d, 735 - 20 * (s - 1) * 10, "US$800", f, (*BLANCO, int(255 * b)))
        sp(d, 960, "AL MES  ·  LARGO PLAZO", mont(500, 22), (*CALIDA, int(255 * b)), 8)
        for k, ln in enumerate(["1 habitación  ·  1.5 baños  ·  2 parqueos", "Línea blanca  ·  Acepta mascotas",
                                "Piscina, gimnasio, club, cancha", "y seguridad 24 h"]):
            ct(d, 1040 + k * 50, ln, mont(300, 31), (*PIEDRA, int(255 * c)))
        ct(d, 1330, "¿Lo alquilarías? Comenta SÍ", pit(52), (*BLANCO, int(255 * e)))
        sp(d, 1440, "WHATSAPP 849-247-2107", mont(500, 21), (*ARENA, int(255 * e)), 7)
    return img.convert("RGB")

def render():
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", f"{OUT}/v.mp4"], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): enc.stdin.write(frame(k / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    mus = "/home/claude/lrh-media/audio/reel_1041_musica.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/v.mp4", "-i", mus, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={DUR - 1.0:.2f}:d=1.0", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    "-t", f"{DUR:.2f}", "-movflags", "+faststart", f"{S}/Reel_1041_US800.mp4"], check=True)
    print("dur", DUR)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for tt in map(float, sys.argv[1:]): frame(tt).save(f"{OUT}/pv_{tt}.jpg", quality=88)
    else: render()
