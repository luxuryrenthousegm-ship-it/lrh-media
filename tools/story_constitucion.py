#!/usr/bin/env python3
"""Historia 6 nov 2026 — Día de la Constitución (feriado trasladado al lunes 9). Estilo lujo LRH."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from reel_1044_sunset import play, LIGHT, MED, spaced, ease, music, GOLD, S

W, H, FPS, X = 1080, 1920, 30, 0.7
SRC = "/home/claude/lrh-media/src/d24/original_d24.mov"  # original del iPhone, sin recomprimir
OUT = f"{S}/st"; os.makedirs(OUT, exist_ok=True)
GREEN = (14, 34, 31)
CUTS = [(5.5, 5.6), (40.3, 5.6), (14.0, 5.8), (9.0, 5.0)]  # sala, habitación, terraza, sala: inicio, duración (tiempo real)
GRADE = "eq=contrast=1.04:saturation=1.06"  # corrección suave: sin grano, sin viñeta
starts = [0.0]
for i in range(1, len(CUTS)): starts.append(starts[-1] + CUTS[i - 1][1] - X)
TOTAL = starts[-1] + CUTS[-1][1]

def base():
    parts = []
    for i, (ss, du) in enumerate(CUTS):
        o = f"{OUT}/h{i}.mp4"; parts.append(o)
        if os.path.exists(o): continue
        vf = f"fps=30,scale=1080:1920:flags=lanczos,{GRADE},setsar=1"  # sin zoom ni cámara lenta
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(ss), "-t", str(du), "-i", SRC, "-an", "-vf", vf,
                        "-c:v", "libx264", "-crf", "8", "-preset", "medium", "-pix_fmt", "yuv420p", o], check=True)
    fc, last = [], "[0:v]"
    for i in range(1, len(parts)):
        lab = f"[v{i}]"; fc.append(f"{last}[{i}:v]xfade=transition=fade:duration={X}:offset={starts[i]:.3f}{lab}"); last = lab
    args = sum([["-i", p] for p in parts], [])
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", ";".join(fc), "-map", last,
                    "-c:v", "libx264", "-crf", "8", "-pix_fmt", "yuv420p", f"{OUT}/base.mp4"], check=True)

def ctext(d, y, text, fnt, fill):
    tw = d.textlength(text, font=fnt); d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

def kicker(d, y, text, a):
    f = MED(28); w = sum(d.textlength(c, font=f) for c in text) + 6 * (len(text) - 1) + 64
    d.rounded_rectangle([(W - w) / 2, y - 14, (W + w) / 2, y + 48], 31, fill=(*GREEN, int(230 * a)))
    spaced(d, W / 2, y, text, f, (*GOLD, int(255 * a)), 6, "c")

def fade(lt, a, b, dur): return ease((lt - a) / 0.7) * (1 - ease((lt - (dur - b)) / 0.5))

def shade(img, top=0.45, bottom=0.62):
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
    for y in range(H):
        a = 0
        if y < 760: a = top * (1 - y / 760)
        if y > 820: a = max(a, bottom * ((y - 820) / (H - 820)) ** 1.1)
        d.line([(0, y), (W, y)], fill=(6, 14, 12, int(255 * a)))
    return ov

SHADE = None
def draw(img, t):
    global SHADE
    if SHADE is None: SHADE = shade(img)
    img = img.convert("RGBA"); img.alpha_composite(SHADE)
    d = ImageDraw.Draw(img, "RGBA")
    spaced(d, W / 2, 268, "LUXURY RENT HOUSE", MED(24), (255, 255, 255, 215), 8, "c")
    d.line([(W / 2 - 40, 312), (W / 2 + 40, 312)], fill=(*GOLD, 200), width=2)
    seg = max(i for i, s in enumerate(starts) if t >= s); lt = t - starts[seg]; du = CUTS[seg][1]
    if seg == 0:
        a = fade(lt, 0.3, 0.6, du); b = fade(lt, 0.9, 0.6, du); c = fade(lt, 1.8, 0.6, du)
        if a: kicker(d, 1050, "LO QUE TU JEFE NO TE DIJO", a)
        if b:
            dy = int(30 * (1 - b))
            ctext(d, 1120 + dy, "El lunes 9", play(118, 600), (255, 255, 255, int(255 * b)))
            ctext(d, 1255 + dy, "no se trabaja.", play(118, 600, True), (255, 255, 255, int(255 * b)))
        if c:
            ctext(d, 1430, "El feriado del Día de la Constitución", LIGHT(36), (255, 255, 255, int(235 * c)))
            ctext(d, 1478, "se pasó para el lunes. Fin de semana largo.", LIGHT(36), (255, 255, 255, int(235 * c)))
    elif seg == 1:
        a = fade(lt, 0.5, 0.6, du); b = fade(lt, 1.3, 0.6, du)
        if a:
            kicker(d, 455, "HOY, 6 DE NOVIEMBRE", a)
            ctext(d, 520, "182 años de nuestra", play(70, 500), (255, 255, 255, int(255 * a)))
            ctext(d, 605, "Constitución", play(70, 500, True), (255, 255, 255, int(255 * a)))
        if b:
            dy = int(40 * (1 - b)); y0 = 1080 + dy
            d.rounded_rectangle([80, y0, W - 80, y0 + 400], 18, fill=(*GREEN, int(222 * b)), outline=(*GOLD, int(160 * b)), width=2)
            d.text((120, y0 + 10), "“", font=play(120, 500), fill=(*GOLD, int(255 * b)))
            for k, line in enumerate(["Toda persona tiene derecho", "a una vivienda digna con", "servicios básicos esenciales."]):
                ctext(d, y0 + 95 + k * 66, line, play(50, 500, True), (255, 255, 255, int(255 * b)))
            spaced(d, W / 2, y0 + 318, "CONSTITUCIÓN DOMINICANA · ART. 59", MED(24), (*GOLD, int(235 * b)), 4, "c")
    elif seg == 2:
        a = fade(lt, 0.5, 0.6, du); b = fade(lt, 1.4, 0.6, du); c = fade(lt, 2.3, 0.6, du)
        if a:
            ctext(d, 1000, "Nosotros nos lo", play(84, 500), (255, 255, 255, int(255 * a)))
            ctext(d, 1100, "tomamos en serio.", play(84, 500, True), (255, 255, 255, int(255 * a)))
        if b:
            y0 = 1290; d.rounded_rectangle([110, y0, W - 110, y0 + 150], 75, fill=(255, 255, 255, int(240 * b)))
            ctext(d, y0 + 26, "¿Y tú qué vas a hacer", MED(40), (*GREEN, int(255 * b)))
            ctext(d, y0 + 78, "con tu lunes libre?", MED(40), (*GREEN, int(255 * b)))
        if c:
            ctext(d, 1480, "Respóndenos aquí abajo", LIGHT(34), (255, 255, 255, int(235 * c)))
            kicker(d, 1545, "SÍGUENOS · @LUXURYRENTHOUSERD", c)
    else:  # tarjeta final: precio y detalles de la 1044
        a = fade(lt, 0.4, 0.0, 99); b = fade(lt, 0.9, 0.0, 99); c = fade(lt, 1.5, 0.0, 99)
        if a:
            ov = Image.new("RGBA", (W, H), (*GREEN, int(150 * a))); img.alpha_composite(ov); d = ImageDraw.Draw(img, "RGBA")
            kicker(d, 900, "DISPONIBLE · VENTURA GOLF, VISTA CANA", a)
        if b:
            dy = int(30 * (1 - b))
            ctext(d, 985 + dy, "US$1,195", play(150, 600), (*GOLD, int(255 * b)))
            spaced(d, W / 2, 1200 + dy, "AL MES · LARGO PLAZO", MED(28), (255, 255, 255, int(235 * b)), 6, "c")
        if c:
            d.line([(W / 2 - 60, 1278), (W / 2 + 60, 1278)], fill=(*GOLD, int(220 * c)), width=2)
            ctext(d, 1310, "Amueblado · Mantenimiento incluido", LIGHT(40), (255, 255, 255, int(245 * c)))
            ctext(d, 1370, "1 habitación · 1.5 baños · 110 m²", LIGHT(40), (255, 255, 255, int(245 * c)))
            spaced(d, W / 2, 1485, "ESCRÍBENOS AL 849-247-2107", MED(30), (255, 255, 255, int(245 * c)), 5, "c")
    return img.convert("RGB")

def render():
    base()
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{OUT}/base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-profile:v", "high", "-maxrate", "20M", "-bufsize", "40M", "-g", "60", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", f"{OUT}/ov.mp4"], stdin=subprocess.PIPE)
    n, size = 0, W * H * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size: break
        enc.stdin.write(draw(Image.frombytes("RGB", (W, H), buf), n / FPS).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    music(f"{OUT}/music.wav", n / FPS, bpm=108)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/ov.mp4", "-i", f"{OUT}/music.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                    f"{S}/Historia_06nov_Constitucion.mp4"], check=True)
    print("frames", n, "dur", n / FPS)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "frame":
        base()
        for tt in map(float, sys.argv[2:]):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(tt), "-i", f"{OUT}/base.mp4", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            draw(Image.frombytes("RGB", (W, H), raw), tt).save(f"{OUT}/pv_{tt}.jpg", quality=88)
    else:
        render()
