#!/usr/bin/env python3
"""Reel propiedad 1044 (Ventura Golf, Vista Cana): overlays, subtítulos karaoke, tarjeta final y audio."""
import json, subprocess, sys, os, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"
REPO = "/home/claude/lrh-media"
W, H, FPS = 1080, 1920, 30
VOFF = 0.3  # retraso de la voz
GOLD = (212, 175, 55)
FI = "/usr/share/fonts/opentype/inter/"
PF = f"{S}/fonts/Playfair.ttf"

def inter(w, s): return ImageFont.truetype(FI + {"xb": "Inter-ExtraBold.otf", "b": "Inter-Bold.otf", "sb": "Inter-SemiBold.otf", "m": "Inter-Medium.otf"}[w], s)
def play(s, wght=700):
    f = ImageFont.truetype(PF, s)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

segs = json.load(open(f"{S}/segs.json"))
bounds = []; t = 0
for a, b, d in segs: bounds.append((t, t + d)); t += d
TOTAL = t
cuts = [b0 for b0, _ in bounds[1:]]
words = json.load(open(f"{REPO}/audio/reel_1044_words.json"))
words = [(w, s + VOFF, e + VOFF) for w, s, e in words]

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def pill(d, cx, y, text, fnt, fill, color, alpha=255, pad=(34, 18)):
    tw = d.textlength(text, font=fnt); asc, desc = fnt.getmetrics()
    x0 = cx - tw / 2 - pad[0]; x1 = cx + tw / 2 + pad[0]
    d.rounded_rectangle([x0, y, x1, y + asc + desc + pad[1] * 2], radius=(asc + desc) // 2 + pad[1], fill=(*fill, alpha))
    d.text((cx - tw / 2, y + pad[1]), text, font=fnt, fill=(*color, alpha))

def ctext(d, cx, y, text, fnt, color, alpha=255, shadow=True):
    tw = d.textlength(text, font=fnt)
    if shadow: d.text((cx - tw / 2 + 3, y + 3), text, font=fnt, fill=(0, 0, 0, int(alpha * 0.55)))
    d.text((cx - tw / 2, y), text, font=fnt, fill=(*color, alpha))

GRAD = None
def grad():
    global GRAD
    if GRAD is None:
        a = np.zeros((H, W), np.float32)
        y = np.arange(H)[:, None]
        a += np.clip(1 - y / 520, 0, 1) * 150
        a += np.clip((y - (H - 760)) / 760, 0, 1) * 190
        GRAD = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "L")
    return GRAD

LABELS = {1: "Totalmente amueblado", 2: "Terraza", 3: "Cocina equipada", 4: "1 habitación", 5: "1.5 baños"}

def caption_groups():
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w[0][-1] in ".,:":
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    return groups
GROUPS = caption_groups()

def draw_frame(img, t):
    seg = next(i for i, (b0, b1) in enumerate(bounds) if b0 <= t < b1 or i == len(bounds) - 1)
    b0, b1 = bounds[seg]; lt = t - b0
    # punch-in en cada corte
    if seg > 0 and lt < 0.22:
        z = 1 + 0.07 * (1 - lt / 0.22)
        cw, ch = int(W / z), int(H / z)
        img = img.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
    if seg == 6:  # amenidades: fondo oscuro
        img = Image.blend(img, Image.new("RGB", (W, H)), 0.5)
    if seg == 8:  # tarjeta final
        img = img.filter(ImageFilter.GaussianBlur(14))
        img = Image.blend(img, Image.new("RGB", (W, H), (10, 12, 14)), 0.55)
    img = Image.composite(Image.new("RGB", (W, H)), img, grad())
    if seg > 0 and lt < 0.1:
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.35 * (1 - lt / 0.1))
    d = ImageDraw.Draw(img, "RGBA")
    # marca
    bf = play(38, 600); s = "LUXURY RENT HOUSE"
    ctext(d, W / 2, 150, s, bf, (255, 255, 255), 235)
    d.line([(W / 2 - 70, 205), (W / 2 + 70, 205)], fill=(*GOLD, 255), width=3)

    if seg == 0:
        a = ease(lt / 0.5)
        ctext(d, W / 2, 330 + (1 - a) * 40, "Vista Cana", play(118, 800), (255, 255, 255), int(255 * a))
        a2 = ease((lt - 0.7) / 0.45)
        if a2 > 0: pill(d, W / 2, 500 + (1 - a2) * 30, "US$1,195 al mes", inter("xb", 62), GOLD, (15, 15, 15), int(255 * a2))
    if seg in LABELS:
        a = ease(lt / 0.3)
        pill(d, W / 2, 330 - (1 - a) * 30, LABELS[seg], inter("xb", 60), (255, 255, 255), (15, 15, 15), int(255 * a))
    if seg == 6:
        a = ease(lt / 0.35)
        ctext(d, W / 2, 470, "En el residencial", play(84, 700), (255, 255, 255), int(255 * a))
        items = [("Campo de golf", 13.3), ("Gimnasio", 14.4), ("Playa artificial", 15.2), ("Piscina", 16.3)]
        for k, (txt, ws) in enumerate(items):
            ai = ease((t - (ws + VOFF)) / 0.3)
            if ai > 0:
                y = 640 + k * 130
                pill(d, W / 2, y + (1 - ai) * 25, txt, inter("b", 58), GOLD if k % 2 == 0 else (255, 255, 255), (15, 15, 15), int(255 * ai))
    if seg == 7:
        txt = "Mantenimiento incluido" if t < 18.9 else "Mascotas permitidas"
        st = b0 if t < 18.9 else 18.9
        a = ease((t - st) / 0.3)
        pill(d, W / 2, 330 - (1 - a) * 30, txt, inter("xb", 58), GOLD, (15, 15, 15), int(255 * a))
    if seg == 8:
        lines = [(0.0, "Ventura Golf", play(104, 800), (255, 255, 255), "t", 430),
                 (0.25, "Vista Cana · Punta Cana", inter("sb", 46), (235, 235, 235), "t", 575),
                 (0.55, "US$1,195 al mes", inter("xb", 78), GOLD, "p", 680),
                 (0.9, "1 habitación · 1.5 baños · 110 m²", inter("sb", 46), (255, 255, 255), "t", 860),
                 (1.1, "Amueblado · Mantenimiento incluido", inter("sb", 46), (255, 255, 255), "t", 930),
                 (1.3, "Mascotas permitidas · Entrega inmediata", inter("sb", 46), (255, 255, 255), "t", 1000),
                 (1.7, "WhatsApp 849-247-2107", inter("xb", 60), (255, 255, 255), "w", 1110)]
        for dl, txt, f, col, kind, y in lines:
            a = ease((lt - dl) / 0.4)
            if a <= 0: continue
            yy = y + (1 - a) * 30
            if kind == "t": ctext(d, W / 2, yy, txt, f, col, int(255 * a))
            elif kind == "p": pill(d, W / 2, yy, txt, f, GOLD, (15, 15, 15), int(255 * a))
            else: pill(d, W / 2, yy, txt, f, (37, 211, 102), (255, 255, 255), int(255 * a))
    # subtítulos karaoke
    g = next((g for g in GROUPS if g[0][1] - 0.05 <= t <= g[-1][2] + 0.25), None)
    if g:
        f = inter("xb", 70); sp = d.textlength(" ", font=f)
        widths = [d.textlength(w.upper(), font=f) for w, _, _ in g]
        x = (W - (sum(widths) + sp * (len(g) - 1))) / 2; y = 1430 if seg != 8 else 1520
        for (w, ws, we), wd in zip(g, widths):
            on = ws <= t
            col = GOLD if (ws <= t <= we + 0.08) else (255, 255, 255)
            al = 255 if on else 110
            d.text((x + 4, y + 4), w.upper(), font=f, fill=(0, 0, 0, int(al * 0.7)))
            d.text((x, y), w.upper(), font=f, fill=(*col, al))
            x += wd + sp
    return img

def video():
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", f"{S}/base1044.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", f"{S}/ov1044.mp4"], stdin=subprocess.PIPE)
    n = 0; size = W * H * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size: break
        img = Image.frombytes("RGB", (W, H), buf)
        enc.stdin.write(draw_frame(img, n / FPS).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait(); print("frames", n)

SR = 44100
def music(path, dur, bpm=112):
    sys.path.insert(0, f"{REPO}/tools"); import make_stories as m
    m.music(dur, path, bpm, seed=11)

def whoosh(path, dur):
    n = int(SR * dur); out = np.zeros(n)
    rng = np.random.default_rng(3)
    for c in cuts:
        L = int(0.32 * SR); st = int((c - 0.16) * SR)
        noise = rng.standard_normal(L)
        env = np.sin(np.linspace(0, np.pi, L)) ** 2
        # barrido de filtro simple: suavizado variable
        k = np.convolve(noise, np.ones(6) / 6, mode="same")
        s = (noise - k) * env * 0.22
        e = min(L, n - st); out[st:st + e] += s[:e]
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def audio_mux():
    music(f"{S}/m1044.wav", TOTAL); whoosh(f"{S}/sfx1044.wav", TOTAL)
    out = f"{S}/reel_1044_final.mp4"
    fc = (f"[2:a]adelay={int(VOFF*1000)}|{int(VOFF*1000)},aresample=44100,volume=1.7,asplit=2[v][vk];"
          f"[1:a]volume=0.32[m];[m][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=250[md];"
          f"[3:a]volume=0.9[s];[md][v][s]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{S}/ov1044.mp4", "-i", f"{S}/m1044.wav", "-i", f"{REPO}/audio/reel_1044_voz.mp3", "-i", f"{S}/sfx1044.wav",
                    "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("ok", out)

if __name__ == "__main__":
    if "frame" in sys.argv:
        for tt in map(float, sys.argv[2:]):
            dec = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(tt), "-i", f"{S}/base1044.mp4", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            draw_frame(Image.frombytes("RGB", (W, H), dec), tt).save(f"{S}/pv_{tt}.jpg", quality=85)
    else:
        video(); audio_mux()
