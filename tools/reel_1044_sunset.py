#!/usr/bin/env python3
"""Reel 1044 estilo cine de lujo: títulos serif, tercios inferiores, tarjeta final y música original."""
import json, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
W, H, FPS, X = 1080, 1920, 30, 0.6
GOLD = (201, 169, 110)
PF = f"{S}/fonts/Playfair.ttf"; PFI = f"{S}/fonts/PlayfairItalic.ttf"
FI = "/usr/share/fonts/opentype/inter/"

def play(s, w=500, italic=False):
    f = ImageFont.truetype(PFI if italic else PF, s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def inter(name, s): return ImageFont.truetype(FI + name, s)
LIGHT = lambda s: inter("Inter-Light.otf", s)
MED = lambda s: inter("Inter-Medium.otf", s)

segs = json.load(open(f"{S}/ss/segs.json"))
starts = [0.0]
for i in range(1, len(segs)): starts.append(starts[-1] + segs[i - 1][2] - X)
TOTAL = starts[-1] + segs[-1][2]

def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def spaced(d, x, y, text, fnt, fill, spacing, anchor="l"):
    widths = [d.textlength(c, font=fnt) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    if anchor == "c": x = x - total / 2
    for c, wd in zip(text, widths):
        d.text((x, y), c, font=fnt, fill=fill); x += wd + spacing
    return total

def ctext(d, y, text, fnt, fill):
    tw = d.textlength(text, font=fnt); d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

LOWER = {1: ("Totalmente", "amueblado"), 2: ("Terraza", ""), 3: ("Cocina", "equipada"), 4: ("1 habitación", ""), 5: ("1.5 baños", "")}

def draw(img, t):
    seg = max(i for i, s in enumerate(starts) if t >= s)
    lt = t - starts[seg]; d_seg = segs[seg][2]
    if seg == 8:
        k = ease((lt - 0.4) / 1.0)
        if k > 0:
            bl = img.filter(ImageFilter.GaussianBlur(12 * k))
            img = Image.blend(bl, Image.new("RGB", (W, H), (8, 8, 10)), 0.5 * k)
    # barras de cine
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, 96], fill=(0, 0, 0, 255)); d.rectangle([0, H - 96, W, H], fill=(0, 0, 0, 255))
    # marca discreta
    spaced(d, W / 2, 128, "LUXURY RENT HOUSE", MED(24), (255, 255, 255, 200), 7, "c")

    if seg == 0:  # apertura
        a1 = ease((lt - 0.3) / 0.9); a2 = ease((lt - 0.9) / 0.9); fade_out = 1 - ease((lt - (d_seg - 0.7)) / 0.6)
        if a1 > 0:
            al = int(255 * a1 * fade_out)
            spaced(d, W / 2, 1220, "PRESENTA", LIGHT(26), (255, 255, 255, al), 9, "c")
            f = play(120, 500, italic=True); tw = d.textlength("Ventura Golf", font=f)
            d.text(((W - tw) / 2 + 3, 1275 + 3), "Ventura Golf", font=f, fill=(0, 0, 0, int(al * 0.5)))
            d.text(((W - tw) / 2, 1275), "Ventura Golf", font=f, fill=(255, 255, 255, al))
        if a2 > 0:
            al = int(255 * a2 * fade_out); lw = 160 * a2
            d.line([(W / 2 - lw, 1440), (W / 2 + lw, 1440)], fill=(*GOLD, al), width=2)
            spaced(d, W / 2, 1468, "VISTA CANA  ·  PUNTA CANA", LIGHT(28), (255, 255, 255, al), 6, "c")
    if seg in LOWER:  # tercio inferior
        a = ease((lt - 0.35) / 0.6) * (1 - ease((lt - (d_seg - 0.75)) / 0.5))
        if a > 0:
            al = int(255 * a); x = 84 - (1 - a) * 20; y = 1530
            d.line([(x, y), (x, y + 150)], fill=(*GOLD, al), width=3)
            l1, l2 = LOWER[seg]
            d.text((x + 28 + 2, y - 4 + 2), l1, font=play(64, 500, True), fill=(0, 0, 0, int(al * .5)))
            d.text((x + 28, y - 4), l1, font=play(64, 500, True), fill=(255, 255, 255, al))
            if l2:
                d.text((x + 28 + 2, y + 72 + 2), l2, font=play(64, 500, True), fill=(0, 0, 0, int(al * .5)))
                d.text((x + 28, y + 72), l2, font=play(64, 500, True), fill=(255, 255, 255, al))
    if seg == 8:  # tarjeta final
        items = [(0.6, "t", "Ventura Golf", play(110, 500, True), (255, 255, 255), 560),
                 (0.9, "s", "VISTA CANA  ·  PUNTA CANA", LIGHT(28), (230, 230, 230), 705),
                 (1.2, "l", None, None, GOLD, 780),
                 (1.4, "s", "1 HABITACIÓN  ·  1.5 BAÑOS  ·  110 M²", LIGHT(28), (255, 255, 255), 830),
                 (1.6, "s", "AMUEBLADO  ·  MANTENIMIENTO INCLUIDO", LIGHT(28), (255, 255, 255), 885),
                 (1.8, "s", "MASCOTAS PERMITIDAS", LIGHT(28), (255, 255, 255), 940),
                 (2.2, "t", "US$1,195", play(118, 600), GOLD, 1030),
                 (2.3, "s", "AL MES", LIGHT(30), GOLD, 1180),
                 (2.8, "s", "WHATSAPP  849-247-2107", MED(34), (255, 255, 255), 1330)]
        for dl, kind, txt, f, col, y in items:
            a = ease((lt - dl) / 0.6)
            if a <= 0: continue
            al = int(255 * a); yy = y + (1 - a) * 18
            if kind == "t": ctext(d, yy, txt, f, (*col, al))
            elif kind == "s": spaced(d, W / 2, yy, txt, f, (*col, al), 5, "c")
            else:
                lw = 120 * a; d.line([(W / 2 - lw, yy), (W / 2 + lw, yy)], fill=(*col, al), width=2)
    # fundido de entrada y salida
    if t < 0.5: img = Image.blend(Image.new("RGB", (W, H)), img, ease(t / 0.5))
    if t > TOTAL - 0.6: img = Image.blend(img, Image.new("RGB", (W, H)), ease((t - (TOTAL - 0.6)) / 0.6))
    return img

SR = 44100
def music(path, dur, bpm=116):
    n = int(SR * dur); tt = np.arange(n) / SR; out = np.zeros(n)
    beat = 60 / bpm; bar = beat * 4
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]  # Am7 Fmaj7 Cmaj7 G7
    bass = [45, 41, 36, 43]
    # pad: ondas de sierra suaves y desafinadas, con filtro paso bajo simple
    b = 0
    while b * bar < dur:
        st = int(b * bar * SR); L = min(int(bar * SR), n - st)
        if L <= 0: break
        t0 = np.arange(L) / SR; ch = prog[b % 4]; s = np.zeros(L)
        for m in ch:
            for det in (-0.08, 0.08):
                f = hz(m + det)
                s += 2 * (t0 * f - np.floor(0.5 + t0 * f))
        k = np.ones(40) / 40; s = np.convolve(s, k, "same")
        env = np.minimum(1, t0 / 0.25) * np.minimum(1, (bar - t0) / 0.25)
        out[st:st + L] += s * env * 0.035
        # bajo pulsante
        for q in range(8):
            qs = int((b * bar + q * beat / 2) * SR)
            if qs >= n: continue
            Lq = int(0.2 * SR); tq = np.arange(Lq) / SR
            sb = np.sin(2 * np.pi * hz(bass[b % 4]) * tq) * np.exp(-tq * 9) * 0.22
            e = min(Lq, n - qs); out[qs:qs + e] += sb[:e]
        # arpegio brillante
        for q in range(16):
            qs = int((b * bar + q * beat / 4) * SR)
            if qs >= n: continue
            Lq = int(0.18 * SR); tq = np.arange(Lq) / SR
            note = ch[(q * 3) % 4] + 12
            sa = np.sin(2 * np.pi * hz(note) * tq) * np.exp(-tq * 18) * 0.05
            e = min(Lq, n - qs); out[qs:qs + e] += sa[:e]
        b += 1
    # batería suave a partir del compás 1
    k = 0
    while k * beat < dur:
        st = int(k * beat * SR)
        if k * beat >= bar * 0.5:
            L = int(0.22 * SR); t0 = np.arange(L) / SR
            kick = np.sin(2 * np.pi * (48 + 70 * np.exp(-t0 * 35)) * t0) * np.exp(-t0 * 10) * 0.55
            e = min(L, n - st); out[st:st + e] += kick[:e]
            if k % 2 == 1:
                Lc = int(0.12 * SR); rng = np.random.default_rng(k)
                clap = rng.standard_normal(Lc) * np.exp(-np.linspace(0, 9, Lc)) * 0.12
                e = min(Lc, n - st); out[st:st + e] += clap[:e]
        hs = int((k + 0.5) * beat * SR)
        if hs < n:
            Lh = int(0.05 * SR); rng = np.random.default_rng(k + 99)
            hat = np.diff(np.concatenate([[0], rng.standard_normal(Lh)])) * np.exp(-np.linspace(0, 8, Lh)) * 0.06
            e = min(Lh, n - hs); out[hs:hs + e] += hat[:e]
        k += 1
    fi, fo = int(1.2 * SR), int(2.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo)
    out = np.tanh(out * 1.3) * 0.85
    st = np.stack([out, np.roll(out, 220)], 1)  # leve estéreo
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def render():
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", f"{S}/ss/x8.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", f"{S}/ss/ov.mp4"], stdin=subprocess.PIPE)
    n = 0; size = W * H * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size: break
        enc.stdin.write(draw(Image.frombytes("RGB", (W, H), buf), n / FPS).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    music(f"{S}/ss/music.wav", TOTAL)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{S}/ss/ov.mp4", "-i", f"{S}/ss/music.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{S}/Reel_1044_Estilo_Lujo.mp4"], check=True)
    print("frames", n, "total", TOTAL)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "frame":
        for tt in map(float, sys.argv[2:]):
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(tt), "-i", f"{S}/ss/x8.mp4", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            draw(Image.frombytes("RGB", (W, H), raw), tt).save(f"{S}/ss/pv_{tt}.jpg", quality=85)
    else:
        render()
