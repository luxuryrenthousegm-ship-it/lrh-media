#!/usr/bin/env python3
"""Genera historias 1080x1920 con texto animado y musica original para Luxury Rent House."""
import subprocess, sys, os, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SRC = os.path.join(os.path.dirname(__file__), "..", "src", "1038")
OUT = os.path.join(os.path.dirname(__file__), "..", "stories", "1038")
os.makedirs(OUT, exist_ok=True)
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + {"xb": "Inter-ExtraBold.otf", "b": "InterDisplay-Bold.otf", "sb": "Inter-SemiBold.otf"}[w], s)

GOLD = (212, 175, 55); WHITE = (255, 255, 255); BLACK = (15, 15, 15); RED = (220, 38, 38)

_cache = {}
def load(name):
    if name not in _cache:
        im = Image.open(os.path.join(SRC, name)).convert("RGB")
        # cubrir 1080x1920 con margen para el zoom
        sc = max(W * 1.12 / im.width, H * 1.12 / im.height)
        _cache[name] = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    return _cache[name]

def bg(name, t, dur, zoom_in=True, blur=0, dark=0.0):
    im = load(name)
    p = t / dur
    z = 1.0 + 0.10 * (p if zoom_in else 1 - p)
    cw, ch = int(im.width / 1.12 / z * 1.0), int(im.height / 1.12 / z)
    cw, ch = min(cw, im.width), min(ch, im.height)
    x = (im.width - cw) // 2; y = (im.height - ch) // 2
    fr = im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR)
    if blur: fr = fr.filter(ImageFilter.GaussianBlur(blur))
    if dark: fr = Image.blend(fr, Image.new("RGB", (W, H), (0, 0, 0)), dark)
    return fr

GRAD = None
def gradient():
    global GRAD
    if GRAD is None:
        a = np.zeros((H, W), np.uint8)
        for y in range(H):
            v = 0
            if y < 420: v = int(150 * (1 - y / 420))
            if y > H - 900: v = max(v, int(200 * ((y - (H - 900)) / 900)))
            a[y, :] = v
        GRAD = Image.fromarray(a, "L")
    return GRAD

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if draw.textlength(test, font=fnt) <= maxw: cur = test
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def text_block(img, t, el):
    """el: dict(text, at, y, size, w, style: 'pill'|'plain'|'gold'|'red', align)"""
    a = ease((t - el["at"]) / 0.45)
    if a <= 0: return
    d = ImageDraw.Draw(img, "RGBA")
    fnt = font(el.get("w", "xb"), el["size"])
    lines = wrap(d, el["text"], fnt, W - 180)
    lh = int(el["size"] * 1.22)
    y0 = el["y"] + int((1 - a) * 60)
    style = el.get("style", "pill")
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=fnt)
        x = (W - tw) / 2
        y = y0 + i * (lh + (18 if style != "plain" else 0))
        al = int(255 * a)
        if style in ("pill", "gold", "red"):
            fill = {"pill": (255, 255, 255, al), "gold": (*GOLD, al), "red": (*RED, al)}[style]
            pad = int(el["size"] * 0.35)
            d.rounded_rectangle([x - pad, y - pad * 0.55, x + tw + pad, y + lh - pad * 0.15], radius=int(el["size"] * 0.3), fill=fill)
            col = (*BLACK, al) if style != "red" else (*WHITE, al)
            d.text((x, y), ln, font=fnt, fill=col)
        else:
            d.text((x + 3, y + 3), ln, font=fnt, fill=(0, 0, 0, int(160 * a)))
            d.text((x, y), ln, font=fnt, fill=(255, 255, 255, al))

def brand(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = font("sb", 34)
    s = "LUXURY RENT HOUSE"
    tw = d.textlength(s, font=f)
    d.text(((W - tw) / 2, 190), s, font=f, fill=(255, 255, 255, 235))
    d.line([((W - 120) / 2, 245), ((W + 120) / 2, 245)], fill=(*GOLD, 255), width=4)

# ---------------- musica original (sintetizada, sin derechos de terceros) ----------------
SR = 44100
def music(dur, path, bpm=104, seed=0):
    n = int(SR * dur); t = np.arange(n) / SR
    beat = 60 / bpm; out = np.zeros(n)
    def env(length, a=0.005, r=None):
        L = int(SR * length); e = np.ones(L)
        A = max(1, int(SR * a)); e[:A] = np.linspace(0, 1, A)
        e *= np.exp(-np.linspace(0, 5 if r is None else r, L)); return e
    # acordes Am - F - C - G  (tropical house)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    bass = [45, 41, 48, 43]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = beat * 4
    k = 0
    while k * beat < dur:
        st = int(k * beat * SR)
        # kick
        L = int(0.25 * SR); tt = np.arange(L) / SR
        kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
        e = min(L, n - st); out[st:st + e] += 0.9 * kick[:e]
        # hat offbeat
        hs = int((k + 0.5) * beat * SR)
        if hs < n:
            L = int(0.06 * SR); rng = np.random.default_rng(k + seed)
            hat = rng.standard_normal(L) * np.exp(-np.linspace(0, 8, L)) * 0.18
            hat = np.diff(np.concatenate([[0], hat]))
            e = min(L, n - hs); out[hs:hs + e] += hat[:e]
        k += 1
    b = 0
    while b * bar < dur:
        ci = b % 4
        for step in [0, 1.5, 2.5, 3]:  # stabs sincopados
            st = int((b * bar + step * beat) * SR)
            if st >= n: continue
            L = int(0.32 * SR); tt = np.arange(L) / SR
            s = sum(np.sign(np.sin(2 * np.pi * hz(m + 12) * tt)) * 0.3 + np.sin(2 * np.pi * hz(m + 12) * tt) for m in chords[ci])
            s *= env(0.32, 0.004, 6) * 0.07
            e = min(L, n - st); out[st:st + e] += s[:e]
        # bajo
        for step in [0, 1, 2, 3]:
            st = int((b * bar + step * beat + beat / 2) * SR)
            if st >= n: continue
            L = int(0.22 * SR); tt = np.arange(L) / SR
            s = np.sin(2 * np.pi * hz(bass[ci]) * tt) * env(0.22, 0.004, 4) * 0.35
            e = min(L, n - st); out[st:st + e] += s[:e]
        b += 1
    fade = int(0.6 * SR)
    out[:fade] *= np.linspace(0, 1, fade); out[-fade:] *= np.linspace(1, 0, fade)
    out = np.tanh(out * 1.2) * 0.8
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# ---------------- historias ----------------
def render(name, segments, bpm=104):
    dur = sum(s["dur"] for s in segments)
    wav = os.path.join(OUT, name + ".wav"); music(dur, wav, bpm, seed=len(name))
    mp4 = os.path.join(OUT, name + ".mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    g = gradient(); black = Image.new("RGB", (W, H), (0, 0, 0))
    for si, seg in enumerate(segments):
        nf = int(seg["dur"] * FPS)
        for f in range(nf):
            t = f / FPS
            img = bg(seg["img"], t, seg["dur"], seg.get("zin", si % 2 == 0), seg.get("blur", 0), seg.get("dark", 0))
            img = Image.composite(black, img, g)
            if t < 0.2 and si > 0:  # flash de transicion
                img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), (0.2 - t) / 0.2 * 0.6)
            brand(img)
            for el in seg["texts"]: text_block(img, t, el)
            ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait(); os.remove(wav)
    print("ok", mp4)

STORIES = {
 "s1_humor": [
   {"img": "p7.jpg", "dur": 3.2, "dark": 0.65, "blur": 22, "texts": [
     {"text": "POV: llevas meses buscando apartamento en Bávaro", "at": 0.2, "y": 1180, "size": 66, "style": "pill"},
     {"text": "y todos son caros, vacíos o no aceptan a tu perro", "at": 1.4, "y": 1500, "size": 48, "style": "plain", "w": "b"}]},
   {"img": "p1.jpg", "dur": 4.8, "texts": [
     {"text": "...hasta que aparece este", "at": 0.3, "y": 1150, "size": 62, "style": "gold"},
     {"text": "Amueblado · Piscina · Mascotas permitidas", "at": 1.5, "y": 1400, "size": 50, "style": "plain", "w": "b"},
     {"text": "Costa Bávaro", "at": 2.4, "y": 1600, "size": 46, "style": "pill"}]}],
 "s2_ultimo_minuto": [
   {"img": "p3.jpg", "dur": 4.0, "dark": 0.45, "blur": 2, "texts": [
     {"text": "ÚLTIMO MINUTO", "at": 0.1, "y": 900, "size": 60, "style": "red"},
     {"text": "Hoy en Punta Cana: hasta 30°C y 75% de probabilidad de lluvia", "at": 0.6, "y": 1080, "size": 60, "style": "pill"},
     {"text": "Aguaceros entre 11:00 a. m. y 2:00 p. m.", "at": 1.8, "y": 1480, "size": 46, "style": "plain", "w": "b"},
     {"text": "Fuente: Bávaro Digital, 6 nov. 2026", "at": 2.2, "y": 1650, "size": 32, "style": "plain", "w": "sb"}]},
   {"img": "p8.jpg", "dur": 4.5, "texts": [
     {"text": "Plan inteligente: ver apartamentos sin mojarte", "at": 0.3, "y": 1150, "size": 62, "style": "gold"},
     {"text": "Escríbenos y te enviamos el video por WhatsApp", "at": 1.6, "y": 1470, "size": 50, "style": "plain", "w": "b"}]}],
 "s3_educativo": [
   {"img": "p8.jpg", "dur": 3.5, "dark": 0.5, "blur": 3, "texts": [
     {"text": "¿Te vas a mudar en Bávaro?", "at": 0.2, "y": 820, "size": 70, "style": "gold"},
     {"text": "Ten este dinero listo antes de firmar", "at": 1.2, "y": 1080, "size": 56, "style": "plain", "w": "b"}]},
   {"img": "p3.jpg", "dur": 4.5, "dark": 0.5, "blur": 3, "texts": [
     {"text": "Muchos propietarios piden:", "at": 0.1, "y": 700, "size": 52, "style": "plain", "w": "b"},
     {"text": "1 mes de adelanto + 1 depósito", "at": 0.6, "y": 860, "size": 58, "style": "pill"},
     {"text": "o", "at": 1.4, "y": 1030, "size": 52, "style": "plain", "w": "b"},
     {"text": "2 depósitos + el primer mes", "at": 1.8, "y": 1140, "size": 58, "style": "pill"},
     {"text": "Fuente: Bávaro Digital, oct. 2026", "at": 2.4, "y": 1650, "size": 32, "style": "plain", "w": "sb"}]},
   {"img": "p2.jpg", "dur": 3.0, "dark": 0.3, "texts": [
     {"text": "Consejo: pregunta siempre qué incluye el precio", "at": 0.2, "y": 1250, "size": 58, "style": "gold"}]}],
 "s4_tour": [
   {"img": "p2.jpg", "dur": 2.0, "texts": [{"text": "Cocina equipada", "at": 0.15, "y": 1450, "size": 64, "style": "pill"}]},
   {"img": "p3.jpg", "dur": 2.0, "texts": [{"text": "Sala y comedor amueblados", "at": 0.15, "y": 1450, "size": 64, "style": "pill"}]},
   {"img": "p5.jpg", "dur": 2.0, "texts": [{"text": "2 habitaciones", "at": 0.15, "y": 1450, "size": 64, "style": "pill"}]},
   {"img": "p6.jpg", "dur": 2.0, "texts": [{"text": "2 baños", "at": 0.15, "y": 1450, "size": 64, "style": "pill"}]},
   {"img": "p4.jpg", "dur": 2.5, "texts": [{"text": "Terraza privada", "at": 0.15, "y": 1450, "size": 64, "style": "gold"}]}],
 "s5_precio": [
   {"img": "p1.jpg", "dur": 8.0, "texts": [
     {"text": "Doral Residences · Costa Bávaro", "at": 0.2, "y": 900, "size": 52, "style": "plain", "w": "b"},
     {"text": "US$1,175 al mes", "at": 0.8, "y": 1020, "size": 88, "style": "gold"},
     {"text": "2 hab · 2 baños · Amueblado", "at": 1.6, "y": 1210, "size": 52, "style": "pill"},
     {"text": "Mantenimiento incluido · Vigilancia 24 h", "at": 2.3, "y": 1350, "size": 44, "style": "plain", "w": "b"},
     {"text": "WhatsApp 849-247-2107", "at": 3.2, "y": 1560, "size": 62, "style": "pill"}]}],
}

if __name__ == "__main__":
    only = sys.argv[1:] or list(STORIES)
    for k in only: render(k, STORIES[k])
