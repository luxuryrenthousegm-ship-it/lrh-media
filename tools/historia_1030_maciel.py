#!/usr/bin/env python3
"""Historia 30 s para @maciel.luxuryrh (estilo Jason): gancho con pregunta → Cana Pearl 1030. Subtítulos en caja tipo noticia (Oswald)."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S = "/tmp/claude-0/-home-claude/3b614509-f312-5864-9c46-7ad2dcf6e6f9/scratchpad"; F = f"{S}/fonts"; SRC = "/home/claude/lrh-media/src/1030"
OUT = f"{S}/h1030"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
osw = lambda wt, sz: ImageFont.truetype(f"{F}/oswald-latin-{wt}-normal.woff", sz)
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

# Maciel a pantalla completa
m = Image.open("/mnt/user-data/attachments/3b614509-f312-5864-9c46-7ad2dcf6e6f9/b5591c4a-image.jpg").convert("RGB")
mw, mh = m.size; top = 110; ch = mh - top; cw = int(ch * 9 / 16); x0 = (mw - cw) // 2
MAC = m.crop((x0, top, x0 + cw, mh)).resize((int(W * 1.06), int(H * 1.06)), Image.LANCZOS)

def photo(n, w=1080, h=810):
    im = Image.open(f"{SRC}/p{n}.jpg").convert("RGB"); iw, ih = im.size; r = w / h
    if iw / ih > r: cw_ = int(ih * r); im = im.crop(((iw - cw_) // 2, 0, (iw - cw_) // 2 + cw_, ih))
    else: ch_ = int(iw / r); im = im.crop((0, (ih - ch_) // 2, iw, (ih - ch_) // 2 + ch_))
    im = im.resize((int(w * 1.06), int(h * 1.06)), Image.LANCZOS)
    return ImageEnhance.Contrast(im).enhance(1.02)
PH = {n: photo(n) for n in (1, 3, 4, 7, 8, 10)}

def push(src, w, h, z):
    sw, sh = src.size; cw_, ch_ = int(w * (1.06 - 0.055 * z)), int(h * (1.06 - 0.055 * z))
    return src.crop(((sw - cw_) // 2, (sh - ch_) // 2, (sw - cw_) // 2 + cw_, (sh - ch_) // 2 + ch_)).resize((w, h), Image.BICUBIC)

def boxes(d, lines, y, t0, t, size=74, fg=(255, 255, 255), bg=(0, 0, 0), hi=None):
    f = osw(700, size)
    for k, ln in enumerate(lines):
        a = ease((t - t0 - k * 0.22) / 0.25)
        if a <= 0: continue
        tw = d.textlength(ln, font=f); pad = 26; x = (W - tw) / 2
        yy = y + k * (size + 34) + 18 * (1 - a)
        col = hi if (hi and k == len(lines) - 1) else bg
        d.rectangle([x - pad, yy - 8, x + tw + pad, yy + size + 22], fill=(*col, int(235 * a)))
        d.text((x, yy), ln, font=f, fill=(*fg, int(255 * a)))

ORO = (198, 152, 105)
# escenas: (inicio, fin, tipo, contenido)
ESC = [(0.0, 3.6, "m", (["TE VOY A HACER", "UNA PREGUNTA…"], 1250)),
       (3.6, 7.2, "m", (["SI PUDIERAS ELEGIR", "DÓNDE DESPERTAR…"], 1250)),
       (7.2, 10.2, "p", (1, ["¿FRENTE A UN", "CAMPO DE GOLF…"])),
       (10.2, 12.8, "m", (["…O CON TU CLUB", "DE PLAYA?"], 1250)),
       (12.8, 16.2, "m", (["¿Y SI TE DIGO QUE", "NO TIENES QUE ELEGIR?"], 1180)),
       (16.2, 18.2, "p", (1, ["CANA PEARL", "CANA BAY · BÁVARO"])),
       (18.2, 20.2, "p", (3, ["AMUEBLADO", "2 HABITACIONES · 2 BAÑOS"])),
       (20.2, 22.2, "p", (7, ["COCINA EQUIPADA"])),
       (22.2, 24.2, "p", (8, ["WALK-IN CLÓSET", "BALCÓN CON VISTA A LA PISCINA"])),
       (24.2, 26.2, "p", (4, ["GOLF DE 18 HOYOS", "MEMBRESÍA CLUB DE PLAYA"])),
       (26.2, 28.0, "p", (10, ["PISCINA INFINITY · GYM · SPA"])),
       (28.0, 31.0, "m", (["US$1,800 AL MES", "ESCRÍBEME: 849-247-2107"], 1180))]
DUR = 31.0

def frame(t):
    i = max(k for k, e in enumerate(ESC) if t >= e[0]); t0, t1, kind, c = ESC[i]; z = (t - t0) / (t1 - t0)
    if kind == "m":
        img = push(MAC, W, H, z).convert("RGBA")
        ov = Image.new("RGBA", (W, H)); od = ImageDraw.Draw(ov)
        for y in range(1000, H): od.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * ((y - 1000) / (H - 1000)))))
        img.alpha_composite(ov); d = ImageDraw.Draw(img)
        lines, y = c
        boxes(d, lines, y, t0, t, hi=ORO if i == len(ESC) - 1 else None)
        if i == len(ESC) - 1:
            f = osw(500, 30); s = "@MACIEL.LUXURYRH"; d.text(((W - d.textlength(s, font=f)) / 2, 1500), s, font=f, fill=(255, 255, 255, 230))
    else:
        n, lines = c
        img = Image.new("RGBA", (W, H), (12, 12, 12, 255))
        bg = push(PH[n], W, 810, z).resize((W // 8, 810 // 8)).resize((W, H)).filter(ImageFilter.GaussianBlur(30))
        img.paste(ImageEnhance.Brightness(bg).enhance(0.45), (0, 0))
        img.paste(push(PH[n], W, 810, z), (0, 555)); d = ImageDraw.Draw(img)
        boxes(d, lines, 1420, t0, t, size=64)
        f = osw(500, 26); s = "MACIEL · LUXURY RENT HOUSE"; d.text(((W - d.textlength(s, font=f)) / 2, 330), s, font=f, fill=(255, 255, 255, 210))
    return img.convert("RGB")

def render():
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-pix_fmt", "yuv420p", f"{OUT}/v.mp4"], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): enc.stdin.write(frame(k / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/v.mp4", "-i", "/home/claude/lrh-media/audio/historia_1030_musica.mp3", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={DUR - 1:.1f}:d=1", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    "-t", str(DUR), "-movflags", "+faststart", f"{S}/Historia_Maciel_CanaPearl.mp4"], check=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for tt in map(float, sys.argv[1:]): frame(tt).save(f"{OUT}/pv_{tt}.jpg", quality=88)
    else: render(); print("ok")
