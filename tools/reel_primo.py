#!/usr/bin/env python3
"""Reel 'El primo que todo lo sabe' — D2-4 Ventura Golf. Solo cortes, textos animados y música original (dembow suave)."""
import os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from make_images import play, LIGHT, MED, REG, spaced, GOLD, GREEN, WHITE, S

W, H, FPS = 1080, 1920, 30
SRC = "/home/claude/lrh-media/src/d24/marlenny_final.mp4"
OUT = f"{S}/reel_primo"; os.makedirs(OUT, exist_ok=True)
BPM = 105; B = 60 / BPM
# (inicio en el video, beats)
CUTS = [(0.3, 4), (4.5, 5), (15.0, 4), (56.5, 4), (39.0, 4), (47.3, 3), (71.0, 4), (78.6, 5)]
END_BEATS = 4
DUR = [b * B for _, b in CUTS]
STARTS = np.concatenate([[0], np.cumsum(DUR)]).tolist()
VID_T = STARTS[-1]; TOTAL = VID_T + END_BEATS * B

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def ctext(d, y, t, f, fill): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)

def base():
    parts = []
    for i, ((ss, _), du) in enumerate(zip(CUTS, DUR)):
        o = f"{OUT}/c{i}.mp4"; parts.append(o)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(ss), "-i", SRC, "-t", f"{du:.4f}", "-an",
                        "-vf", "fps=30,scale=1080:1920:flags=lanczos,eq=contrast=1.03:saturation=1.05,setsar=1",
                        "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-pix_fmt", "yuv420p", o], check=True)
    with open(f"{OUT}/list.txt", "w") as f:
        for p in parts: f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/list.txt",
                    "-c:v", "libx264", "-crf", "8", "-pix_fmt", "yuv420p", f"{OUT}/base.mp4"], check=True)

def label(d, txt, lt, y=1380):
    a = ease(lt / 0.35); x = int(-60 * (1 - a)) + 90
    f = MED(40); w = d.textlength(txt, font=f)
    d.rounded_rectangle([x, y, x + w + 70, y + 84], 14, fill=(*GREEN, int(225 * a)))
    d.rectangle([x, y, x + 8, y + 84], fill=(*GOLD, int(255 * a)))
    d.text((x + 38, y + 18), txt, font=f, fill=(255, 255, 255, int(255 * a)))

def overlay(img, t):
    img = img.convert("RGBA")
    sh = Image.new("RGBA", (W, H)); sd = ImageDraw.Draw(sh)
    for y in range(0, 360): sd.line([(0, y), (W, y)], fill=(6, 14, 12, int(120 * (1 - y / 360))))
    for y in range(950, H): sd.line([(0, y), (W, y)], fill=(6, 14, 12, int(215 * ((y - 950) / (H - 950)) ** 0.9)))
    img.alpha_composite(sh); d = ImageDraw.Draw(img, "RGBA")
    spaced(d, W / 2, 250, "LUXURY RENT HOUSE", MED(22), (255, 255, 255, 215), 8)
    seg = max(i for i, s in enumerate(STARTS[:-1]) if t >= s); lt = t - STARTS[seg]
    if seg == 0:  # gancho tipo mensaje
        msg = ["Mi primo jura que en Punta", "Cana no hay na' decente por", "menos de 2 mil dólares…"]
        full = " ".join(msg); n = int(len(full) * min(1, lt / 1.6)); shown, k = [], 0
        for ln in msg:
            take = max(0, min(len(ln), n - k)); shown.append(ln[:take]); k += len(ln) + 1
        d.rounded_rectangle([90, 560, W - 90, 860], 36, fill=(255, 255, 255, 240))
        spaced(d, 150, 590, "PRIMO", MED(22), (*GOLD, 255), 4)
        y = 640
        for ln in shown: d.text((150, y), ln, font=MED(46), fill=(*GREEN, 255)); y += 62
    elif seg == 1:
        a = ease(lt / 0.3)
        ctext(d, 1180 + int(40 * (1 - a)), "Ven acá, primo.", play(96, True, 600), (255, 255, 255, int(255 * a)))
        if lt > 1.4: label(d, "Amueblado", lt - 1.4)
    elif seg == 2: label(d, "Terraza", lt)
    elif seg == 3: label(d, "Cocina", lt)
    elif seg == 4: label(d, "1 habitación · 1.5 baños · 110 m²", lt)
    elif seg == 5: label(d, "Mantenimiento incluido", lt)
    elif seg == 6:
        a = ease(lt / 0.4)
        for k, ln in enumerate(["Y el proyecto tiene golf,", "playa artificial y gimnasio…"]):
            ctext(d, 1400 + k * 72 + int(30 * (1 - a)), ln, play(56, True), (255, 255, 255, int(255 * a)))
    elif seg == 7:
        a = ease((lt - 0.2) / 0.5); s = 1 + 0.15 * (1 - a)
        f = play(int(150 * s), w=600)
        if a > 0:
            d.rounded_rectangle([110, 1130, W - 110, 1500], 28, fill=(*GREEN, int(215 * a)), outline=(*GOLD, int(150 * a)), width=2)
            ctext(d, 1180, "US$1,195", f, (*GOLD, int(255 * a)))
            spaced(d, W / 2, 1385, "AL MES · LARGO PLAZO", MED(30), (255, 255, 255, int(240 * a)), 7)
            spaced(d, W / 2, 1440, "VENTURA GOLF · VISTA CANA", MED(26), (*GOLD, int(230 * a)), 6)
    return img.convert("RGB")

def endcard(t):
    img = Image.new("RGBA", (W, H), (*GREEN, 255)); d = ImageDraw.Draw(img, "RGBA")
    a = ease(t / 0.4); b = ease((t - 0.5) / 0.4); c = ease((t - 1.0) / 0.4)
    spaced(d, W / 2, 420, "LUXURY RENT HOUSE", MED(26), (255, 255, 255, int(220 * a)), 9)
    d.line([(W / 2 - 40, 470), (W / 2 + 40, 470)], fill=(*GOLD, int(255 * a)), width=2)
    ctext(d, 760, "¿Primo, y ahora?", play(96, True, 600), (255, 255, 255, int(255 * a)))
    if b > 0:
        ctext(d, 930, "Etiqueta a ese primo.", LIGHT(46), (*GOLD, int(255 * b)))
        ctext(d, 1000, "Amueblado · Mascotas · Entrega inmediata", LIGHT(36), (255, 255, 255, int(220 * b)))
    if c > 0:
        d.rounded_rectangle([(W - 640) / 2, 1160, (W + 640) / 2, 1250], 45, fill=(255, 255, 255, int(245 * c)))
        ctext(d, 1180, "WhatsApp 849-247-2107", MED(40), (*GREEN, int(255 * c)))
        spaced(d, W / 2, 1300, "@LUXURYRENTHOUSERD", MED(26), (255, 255, 255, int(220 * c)), 6)
    return img.convert("RGB")

SR = 48000
def music(path, dur):
    n = int(SR * dur); out = np.zeros(n); s16 = B / 4
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def add(st, sig):
        i = int(st * SR)
        if i >= n: return
        e = min(len(sig), n - i); out[i:i + e] += sig[:e]
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]; bass = [45, 41, 36, 43]
    bars = int(dur / (4 * B)) + 1
    for bar in range(bars):
        t0 = bar * 4 * B; ch = prog[bar % 4]
        for q in range(16):
            tq = t0 + q * s16
            if q % 4 == 0:  # bombo en cada tiempo
                L = int(0.25 * SR); x = np.arange(L) / SR
                add(tq, np.sin(2 * np.pi * (45 + 80 * np.exp(-x * 30)) * x) * np.exp(-x * 9) * 0.7)
            if q in (3, 6, 11, 14):  # caja dembow
                L = int(0.14 * SR); rng = np.random.default_rng(bar * 16 + q); x = np.arange(L) / SR
                add(tq, (rng.standard_normal(L) * 0.5 + np.sin(2 * np.pi * 190 * x)) * np.exp(-x * 28) * 0.22)
            if q % 2 == 1:  # hi-hat
                L = int(0.04 * SR); rng = np.random.default_rng(999 + bar * 16 + q)
                add(tq, np.diff(np.concatenate([[0], rng.standard_normal(L)])) * np.exp(-np.linspace(0, 6, L)) * 0.05)
            if q in (0, 3, 6, 8, 11, 14):  # bajo 808
                L = int(0.3 * SR); x = np.arange(L) / SR
                add(tq, np.tanh(2 * np.sin(2 * np.pi * hz(bass[bar % 4] - 12) * x)) * np.exp(-x * 6) * 0.28)
            if q in (2, 6, 10, 14):  # acordes cortos
                L = int(0.12 * SR); x = np.arange(L) / SR
                add(tq, sum(np.sin(2 * np.pi * hz(m + 12) * x) for m in ch) * np.exp(-x * 20) * 0.05)
    for k in range(len(STARTS) - 1):  # golpe suave en cada corte
        L = int(0.25 * SR); rng = np.random.default_rng(500 + k); x = np.arange(L) / SR
        add(STARTS[k + 1] - 0.12, rng.standard_normal(L) * np.sin(np.pi * x / 0.25) * 0.05)
    fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)
    out = np.tanh(out * 1.4) * 0.85; st = np.stack([out, np.roll(out, 180)], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())

def render(final):
    base()
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{OUT}/base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-profile:v", "high", "-maxrate", "20M", "-bufsize", "40M",
                            "-g", "60", "-pix_fmt", "yuv420p", f"{OUT}/ov.mp4"], stdin=subprocess.PIPE)
    n, size = 0, W * H * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size: break
        enc.stdin.write(overlay(Image.frombytes("RGB", (W, H), buf), n / FPS).tobytes()); n += 1
    for k in range(int(END_BEATS * B * FPS)): enc.stdin.write(endcard(k / FPS).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    music(f"{OUT}/music.wav", n / FPS)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/ov.mp4", "-i", f"{OUT}/music.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-shortest", "-movflags", "+faststart", final], check=True)
    # versión sin música, para poner el audio en tendencia desde la app
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/ov.mp4", "-c:v", "copy", "-an", "-movflags", "+faststart",
                    final.replace(".mp4", "_SIN_MUSICA.mp4")], check=True)
    print("frames", n, "dur", n / FPS)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "frame":
        base()
        for tt in map(float, sys.argv[2:]):
            if tt >= VID_T: endcard(tt - VID_T).save(f"{OUT}/pv_{tt}.jpg", quality=88); continue
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(tt), "-i", f"{OUT}/base.mp4", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            overlay(Image.frombytes("RGB", (W, H), raw), tt).save(f"{OUT}/pv_{tt}.jpg", quality=88)
    else:
        render(f"{S}/Reel_Primo_Ventura_Golf.mp4")
