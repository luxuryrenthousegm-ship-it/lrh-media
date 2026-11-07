#!/usr/bin/env python3
"""Versión con la voz de Gregory: cortes sincronizados con lo que dice la voz."""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw
import reel_primo as r
from reel_primo import W, H, FPS, ease, ctext, label, endcard, play, MED, spaced, GOLD, GREEN, S

r.OUT = OUT = f"{S}/reel_primo_voz"; os.makedirs(OUT, exist_ok=True)
VOZ = "/home/claude/lrh-media/audio/reel_primo_voz.mp3"
MUS = "/home/claude/lrh-media/audio/reel_primo_musica_c.mp3"
# (inicio en el video, segundo en que empieza según la voz)
PLAN = [(0.3, 0.0), (9.0, 5.4), (15.0, 8.6), (37.8, 9.4), (40.0, 10.1), (47.3, 12.25), (54.8, 13.65), (71.0, 15.3), (78.6, 18.7)]
VID_T = 22.5; END = 3.8
STARTS = [p[1] for p in PLAN] + [VID_T]
r.CUTS = [(p[0], 0) for p in PLAN]; r.DUR = [STARTS[i + 1] - STARTS[i] for i in range(len(PLAN))]

def overlay(img, t):
    img = img.convert("RGBA")
    sh = Image.new("RGBA", (W, H)); sd = ImageDraw.Draw(sh)
    for y in range(0, 360): sd.line([(0, y), (W, y)], fill=(6, 14, 12, int(120 * (1 - y / 360))))
    for y in range(950, H): sd.line([(0, y), (W, y)], fill=(6, 14, 12, int(215 * ((y - 950) / (H - 950)) ** 0.9)))
    img.alpha_composite(sh); d = ImageDraw.Draw(img, "RGBA")
    spaced(d, W / 2, 250, "LUXURY RENT HOUSE", MED(22), (255, 255, 255, 215), 8)
    seg = max(i for i, s in enumerate(STARTS[:-1]) if t >= s); lt = t - STARTS[seg]
    if seg == 0:
        msg = ["Mi primo jura que en Punta", "Cana no hay na' decente por", "menos de 2 mil dólares…"]
        full = " ".join(msg); n = int(len(full) * min(1, lt / 4.6)); shown, k = [], 0
        for ln in msg:
            take = max(0, min(len(ln), n - k)); shown.append(ln[:take]); k += len(ln) + 1
        d.rounded_rectangle([90, 560, W - 90, 860], 36, fill=(255, 255, 255, 240))
        spaced(d, 150, 590, "PRIMO", MED(22), (*GOLD, 255), 4)
        y = 640
        for ln in shown: d.text((150, y), ln, font=MED(46), fill=(*GREEN, 255)); y += 62
    elif seg == 1:
        a = ease(lt / 0.3)
        ctext(d, 1180 + int(40 * (1 - a)), "Ven acá, primo.", play(96, True, 600), (255, 255, 255, int(255 * a)))
        if lt > 2.3: label(d, "Amueblado", lt - 2.3)
    elif seg == 2: label(d, "Terraza", lt)
    elif seg == 3: label(d, "Cocina", lt)
    elif seg == 4: label(d, "1 habitación · 1.5 baños", lt)
    elif seg == 5: label(d, "110 m²", lt)
    elif seg == 6: label(d, "Mantenimiento incluido", lt)
    elif seg == 7:
        a = ease(lt / 0.4)
        for k, ln in enumerate(["Y el proyecto tiene golf,", "playa artificial y gimnasio…"]):
            ctext(d, 1400 + k * 72 + int(30 * (1 - a)), ln, play(56, True), (255, 255, 255, int(255 * a)))
    elif seg == 8:
        a = ease((lt - 1.1) / 0.5); s = 1 + 0.15 * (1 - a)
        if lt < 1.1:
            ctext(d, 1300, "¿Y cuánto?", play(90, True, 600), (255, 255, 255, int(255 * ease(lt / 0.3))))
        if a > 0:
            d.rounded_rectangle([110, 1130, W - 110, 1500], 28, fill=(*GREEN, int(215 * a)), outline=(*GOLD, int(150 * a)), width=2)
            ctext(d, 1180, "US$1,195", play(int(150 * s), w=600), (*GOLD, int(255 * a)))
            spaced(d, W / 2, 1385, "AL MES · LARGO PLAZO", MED(30), (255, 255, 255, int(240 * a)), 7)
            spaced(d, W / 2, 1440, "VENTURA GOLF · VISTA CANA", MED(26), (*GOLD, int(230 * a)), 6)
    return img.convert("RGB")

def render(final):
    r.base()
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{OUT}/base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-profile:v", "high", "-maxrate", "20M", "-bufsize", "40M",
                            "-g", "60", "-pix_fmt", "yuv420p", f"{OUT}/ov.mp4"], stdin=subprocess.PIPE)
    n, size = 0, W * H * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size: break
        enc.stdin.write(overlay(Image.frombytes("RGB", (W, H), buf), n / FPS).tobytes()); n += 1
    for k in range(int(END * FPS)): enc.stdin.write(endcard(k / FPS).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    dur = n / FPS
    fc = (f"[1:a]volume=1.0,apad,asplit=2[vo1][vo2];[2:a]atrim=0:{dur:.2f},volume=0.55[m];"
          f"[m][vo1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];"
          f"[md][vo2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={dur - 1.0:.2f}:d=1.0[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/ov.mp4", "-i", VOZ, "-i", MUS, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    "-t", f"{dur:.2f}", "-movflags", "+faststart", final], check=True)
    print("frames", n, "dur", dur)

def mux(final, dur):
    pass

if __name__ == "__main__":
    render(f"{S}/Reel_Primo_VOZ_Gregory.mp4")
