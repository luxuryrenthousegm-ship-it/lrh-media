#!/usr/bin/env python3
"""Semana 12-18 nov 2026: feed 4:5 en 2160x2700 e historias 1080x1920 para @luxuryrenthouserd (Estilo Oppenheim)
y @maciel.luxuryrh (Estilo Jason). Solo fotos reales de AlterEstate; datos tomados de cada ficha."""
import os, sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

R = "/home/claude/lrh-media"
FS = os.environ.get("LRH_FONTS", "/tmp/claude-0/-home-claude/1c10acf7-2a96-58d8-b988-ee5a98c89150/scratchpad/st/node_modules/@fontsource")
FI = "/usr/share/fonts/opentype/inter/"
OUT = f"{R}/media/semana_1112"; os.makedirs(OUT, exist_ok=True)
GOLD, GREEN, WHITE = (201, 169, 110), (14, 34, 31), (255, 255, 255)
LUX, LUXD, PIEDRA = (52, 59, 52), (42, 48, 42), (164, 160, 156)
INKJ, AMBAR, CREMA = (20, 20, 13), (198, 152, 105), (243, 239, 234)
WA = "849-247-2107"

def ff(fam, wt, it=False): return f"{FS}/{fam}/files/{fam}-latin-{wt}-{'italic' if it else 'normal'}.woff"
corm = lambda s, w=400, it=False: ImageFont.truetype(ff("cormorant-garamond", w, it), s)
play = lambda s, it=False, w=500: ImageFont.truetype(ff("playfair-display", w, it), s)
osw = lambda s, w=700: ImageFont.truetype(ff("oswald", w), s)
mont = lambda s, w=500: ImageFont.truetype(ff("montserrat", w), s)
inter = lambda s, n="Regular": ImageFont.truetype(f"{FI}Inter-{n}.otf", s)
LOGO = Image.open(f"{R}/brand/logo_lrh_blanco.png").convert("RGBA")
LOGO = LOGO.crop(LOGO.getbbox())

def develop(path, W, H, focus=(0.5, 0.5)):
    """Revelado natural (sin IA): recorte, limpieza suave de JPEG, ampliación Lanczos y nitidez."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB"); iw, ih = im.size; r = W / H
    if iw / ih > r: cw = int(ih * r); x = int((iw - cw) * focus[0]); im = im.crop((x, 0, x + cw, ih))
    else: ch = int(iw / r); y = int((ih - ch) * focus[1]); im = im.crop((0, y, iw, y + ch))
    u8 = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    if im.size[0] < W: u8 = cv2.fastNlMeansDenoisingColored(u8, None, 2, 2, 7, 21)
    out = cv2.resize(u8, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    k = W / 1080
    bb = cv2.GaussianBlur(out, (0, 0), 15 * k); out = out + (out - bb) * 0.06
    bs = cv2.GaussianBlur(out, (0, 0), 0.8 * k); out = out + (out - bs) * 0.40
    return Image.fromarray(cv2.cvtColor(out.clip(0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))

def grad(W, H, start, strength, top=0.0, toph=300, ex=1.0, col=GREEN):
    a = np.zeros(H, np.float32); y = np.arange(H, dtype=np.float32)
    m = y > start; a[m] = strength * ((y[m] - start) / (H - start)) ** ex
    if top: t = y < toph; a[t] = np.maximum(a[t], top * (1 - y[t] / toph))
    arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = col; arr[..., 3] = (255 * a.clip(0, 1))[:, None]
    return Image.fromarray(arr, "RGBA")

class C:
    """Lienzo con unidades de diseño (1080 de ancho) y factor de escala K."""
    def __init__(s, im, K): s.im = im.convert("RGBA"); s.K = K; s.W = im.size[0]; s.d = ImageDraw.Draw(s.im)
    def over(s, ov): s.im.alpha_composite(ov); s.d = ImageDraw.Draw(s.im)
    def tw(s, t, f, sp=0): return sum(s.d.textlength(c, font=f) for c in t) + sp * s.K * (len(t) - 1) if sp else s.d.textlength(t, font=f)
    def text(s, y, t, f, fill=WHITE, sp=0, cx=None, x=None):
        K = s.K; w = s.tw(t, f, sp); x0 = x * K if x is not None else (cx * K if cx is not None else s.W / 2) - w / 2
        if not sp: s.d.text((x0, y * K), t, font=f, fill=fill); return
        for c in t: s.d.text((x0, y * K), c, font=f, fill=fill); x0 += s.d.textlength(c, font=f) + sp * K
    def lines(s, y, ts, f, fill=WHITE, lh=60, **kw):
        for t in ts: s.text(y, t, f, fill, **kw); y += lh
        return y
    def wrap(s, t, f, maxw):
        out, line = [], ""
        for w in t.split():
            n = (line + " " + w).strip()
            if s.d.textlength(n, font=f) <= maxw * s.K: line = n
            else: out.append(line); line = w
        out.append(line); return out
    def pill(s, y, t, f, fill=GREEN, color=GOLD, sp=5, padx=30, h=60, cx=None):
        K = s.K; w = s.tw(t, f, sp) + 2 * padx * K; c = (cx * K if cx else s.W / 2)
        s.d.rounded_rectangle([c - w / 2, (y - 14) * K, c + w / 2, (y - 14 + h) * K], h * K / 2, fill=(*fill, 238))
        s.text(y, t, f, color, sp, cx=cx)
    def logo(s, y, h=62, cx=None, tint=None):
        K = s.K; lg = LOGO.resize((int(LOGO.width * h * K / LOGO.height), int(h * K)), Image.LANCZOS)
        if tint: lg = Image.merge("RGBA", (*[Image.new("L", lg.size, v) for v in tint], lg.split()[3]))
        s.im.alpha_composite(lg, (int((cx * K if cx else s.W / 2) - lg.width / 2), int(y * K))); s.d = ImageDraw.Draw(s.im)
    def rule(s, y, w=70, fill=GOLD, th=2, cx=None):
        K = s.K; c = cx * K if cx else s.W / 2; s.d.line([(c - w * K / 2, y * K), (c + w * K / 2, y * K)], fill=fill, width=int(th * K))
    def save(s, name, q=93):
        p = f"{OUT}/{name}.jpg"; s.im.convert("RGB").save(p, quality=q, subsampling=0, optimize=True); return p

K = 2; FW, FH = 1080 * K, 1350 * K; SW, SH = 1080, 1920
P = lambda pid, n: f"{R}/src/{pid}/p{n}.jpg"

# ───────────────────────── FEED: carrusel de propiedad ─────────────────────────
def cover(name, src, hook, title, detail, focus=(0.5, 0.5), tsize=88, tsp=12, start=700, st=0.9):
    c = C(develop(src, FW, FH, focus), K)
    c.over(grad(FW, FH, start * K, st, top=0.30, toph=280 * K, ex=0.95, col=(10, 14, 13)))
    c.logo(46, 64)
    c.lines(1010 - 58 * (len(hook) - 1), hook, corm(50 * K, 500, True), (255, 255, 255, 245), 58)
    c.text(1092, "FOR RENT", inter(17 * K, "Medium"), (255, 255, 255, 235), 6)
    c.text(1122, title, corm(tsize * K, 400), WHITE, tsp)
    c.text(1246, detail, inter(16 * K), (255, 255, 255, 230), 4)
    return c.save(name)

def clean(name, src, focus=(0.5, 0.5)):
    return C(develop(src, FW, FH, focus), K).save(name)

def ficha(name, src, proyecto, zona, precio, feats, focus=(0.5, 0.5)):
    c = C(develop(src, FW, FH, focus), K)
    c.over(Image.new("RGBA", (FW, FH), (*LUXD, 226)))
    two = len(proyecto) > 1; b = 100 if two else 150
    c.logo(b, 110 if two else 120)
    c.text(b + (180 if two else 200), "DISPONIBLE  ·  LARGO PLAZO", inter(18 * K, "Medium"), PIEDRA, 7)
    y = c.lines(b + (232 if two else 260), proyecto, corm(84 * K, 500, True), WHITE, 90)
    c.text(y + 18, zona, inter(19 * K, "Medium"), (255, 255, 255, 225), 7)
    c.rule(y + 78, 70, PIEDRA, 1.5)
    c.text(y + (96 if two else 118), precio, corm(150 * K, 500), WHITE)
    c.text(y + (276 if two else 300), "AL MES", inter(19 * K, "Medium"), PIEDRA, 9)
    y2 = c.lines(y + (346 if two else 380), feats, inter(29 * K, "Light"), WHITE, 54)
    assert y2 < 1150, (name, y2)
    c.pill(1178, f"WHATSAPP  {WA}", inter(22 * K, "Medium"), fill=WHITE, color=LUXD, sp=5, padx=44, h=72)
    return c.save(name)

# ───────────────────────── FEED: educativo (foto + texto) ─────────────────────────
def edu(name, src, i, n, draw, focus=(0.5, 0.5), start=560):
    c = C(develop(src, FW, FH, focus), K)
    c.over(grad(FW, FH, start * K, 0.97, top=0.45, toph=300 * K, ex=0.9))
    c.logo(44, 56); c.text(64, f"{i}/{n}", inter(22 * K, "Medium"), (255, 255, 255, 200), x=988)
    draw(c); return c.save(name)

def paso(num, titulo, sub):
    def f(c):
        c.text(940, num, play(64 * K, False, 600), GOLD)
        y = c.lines(1040, c.wrap(titulo, play(58 * K, True), 860), play(58 * K, True), WHITE, 74)
        c.lines(y + 22, c.wrap(sub, inter(32 * K, "Light"), 800), inter(32 * K, "Light"), (255, 255, 255, 235), 46)
    return f

# ───────────────────────── HISTORIAS LRH ─────────────────────────
def story(name, src, draw, focus=(0.5, 0.5), start=560, strength=1.0, ex=0.75):
    c = C(develop(src, SW, SH, focus), 1)
    c.over(grad(SW, SH, start, strength, top=0.5, toph=420, ex=ex))
    c.logo(250, 70); draw(c); return c.save("h_" + name, 95)

# ───────────────────────── HISTORIAS MACIEL (Estilo Jason) ─────────────────────────
def jason(name, kicker, head, body=None, quote=None, ask=None, src=None, focus=(0.5, 0.5), hs=132):
    if src:
        c = C(develop(src, SW, SH, focus), 1); c.over(grad(SW, SH, 220, 1.0, top=0.6, toph=560, ex=0.42, col=INKJ))
    else:
        c = C(Image.new("RGB", (SW, SH), INKJ), 1)
    X = 96; y = 400 if not src else 740
    c.text(y, kicker, mont(23, 600), AMBAR, 7, x=X); y += 62
    for ln in head:
        col = AMBAR if ln.startswith("*") else CREMA; c.text(y, ln.lstrip("*"), osw(hs, 700), col, x=X); y += int(hs * 1.13)
    y += 46; c.d.line([(X, y), (SW - X, y)], fill=CREMA, width=2); y += 44
    if quote:
        for ln in quote: c.text(y, ln, play(52, True, 400), CREMA, x=X); y += 68
        y += 22
    if body:
        for ln in body: c.text(y, ln, mont(34, 500), (216, 210, 202), x=X); y += 52
        y += 26
    if ask:
        for ln in ask: c.text(y, ln, osw(58, 700), AMBAR, x=X); y += 70
    c.text(1640, "MACIEL CARTY  ·  LUXURY RENT HOUSE", mont(19, 600), (130, 124, 122), 5, x=X)
    assert y < 1620, (name, y)
    return c.save("m_" + name, 95)

def build():
    made = []
    A = made.append
    # ── F1 · Villa San Juan Lake (1039)
    A(cover("f1_1039_01", P(1039, 1), ["¿Y si tu piscina", "te esperara en casa?"], "SAN JUAN LAKE", "DOWNTOWN PUNTA CANA   -   3 HABITACIONES   -   3.5 BAÑOS   -   PISCINA", focus=(0.5, 0.5), tsize=84))
    for k, n in enumerate([3, 2, 5, 6, 8], 2): A(clean(f"f1_1039_{k:02d}", P(1039, n)))
    A(ficha("f1_1039_07", P(1039, 1), ["Villa en San Juan Lake"], "DOWNTOWN PUNTA CANA", "US$2,875",
            ["3 habitaciones  ·  3.5 baños", "Piscina  ·  Desayunador", "Habitación de servicio  ·  3 parqueos", "Acepta mascotas"]))
    # ── F3 · Esto o aquello (1036 vs 1030)
    c = C(Image.new("RGB", (FW, FH), LUXD), K)
    top = develop(P(1036, 4), FW, 390 * K, (0.5, 0.62)).convert("RGBA"); top.alpha_composite(grad(FW, 390 * K, 190 * K, 0.88, col=(10, 14, 13)))
    bot = develop(P(1030, 1), FW, 620 * K, (0.5, 0.45)).convert("RGBA"); bot.alpha_composite(grad(FW, 620 * K, 380 * K, 0.9, col=(10, 14, 13)))
    c.im.paste(top, (0, 250 * K)); c.im.paste(bot, (0, 730 * K)); c.d = ImageDraw.Draw(c.im)
    c.logo(40, 54); c.text(128, "¿Tú eres team…?", corm(74 * K, 500, True), WHITE)
    c.text(548, "A", corm(60 * K, 600), GOLD, x=70); c.text(552, "Villa con piscina", corm(54 * K, 500, True), WHITE, x=150)
    c.text(1238, "B", corm(60 * K, 600), GOLD, x=70); c.text(1242, "Apartamento frente al golf", corm(54 * K, 500, True), WHITE, x=150)
    c.pill(668, "COMENTA  A  O  B", inter(22 * K, "Medium"), fill=WHITE, color=LUXD, sp=6, padx=46, h=64)
    A(c.save("f3_team"))
    # ── F4 · Sabana Equestrian (1036)
    A(cover("f4_1036_01", P(1036, 1), ["Techos altos, piedra natural", "y madera cálida."], "SABANA", "VISTA CANA   -   3 HABITACIONES   -   5 BAÑOS   -   PISCINA Y GAZEBO", tsize=104, tsp=22))
    for k, n in enumerate([4, 3, 16, 8, 6, 17], 2): A(clean(f"f4_1036_{k:02d}", P(1036, n)))
    A(ficha("f4_1036_08", P(1036, 4), ["Sabana Equestrian", "& Residences"], "VISTA CANA  ·  PUNTA CANA", "US$3,480",
            ["3 habitaciones + habitación de servicio", "5 baños  ·  Family room / Studio", "Piscina y gazebo  ·  Línea blanca incluida", "Acepta mascotas"]))
    # ── F5 · Educativo: antes de firmar
    def e1(c):
        c.pill(842, "GUÁRDALO PARA CUANDO TE TOQUE", inter(22 * K, "Medium"))
        c.text(912, "5 cosas que revisar", play(84 * K, False, 600), WHITE)
        c.text(1014, "antes de firmar", play(84 * K, False, 600), WHITE)
        c.text(1116, "un alquiler.", play(84 * K, True, 600), GOLD)
        c.text(1262, "DESLIZA  →", inter(24 * K, "Medium"), (255, 255, 255, 220), 6)
    A(edu("f5_edu_01", P(1044, 9), 1, 7, e1, start=500))
    pasos = [("01", "Mírala antes de pagar.", "En persona o por videollamada en vivo. Las fotos no lo dicen todo.", P(1038, 3)),
             ("02", "Pregunta qué incluye el precio.", "Mantenimiento, agua, luz, gas, internet. Que no haya sorpresas.", P(1044, 2)),
             ("03", "Todo por escrito.", "Depósito, duración del contrato y condiciones de salida.", P(1036, 3)),
             ("04", "Recibe con fotos.", "Revisa el estado y el inventario el día de la entrega.", P(1038, 5)),
             ("05", "Paga siempre con recibo.", "Y a nombre de quien corresponde.", P(1044, 8))]
    for k, (n, t, s_, src) in enumerate(pasos, 2): A(edu(f"f5_edu_{k:02d}", src, k, 7, paso(n, t, s_)))
    def e7(c):
        c.text(760, "¿Cuál se te pasó", play(80 * K, False, 600), WHITE)
        c.text(860, "la última vez?", play(80 * K, True, 600), GOLD)
        c.lines(1000, ["Cuéntanos en los comentarios y envíaselo", "a quien anda buscando dónde mudarse."], inter(36 * K, "Light"), WHITE, 52)
        c.pill(1180, "SÍGUENOS  ·  @LUXURYRENTHOUSERD", inter(24 * K, "Medium"))
    A(edu("f5_edu_07", P(1044, 6), 7, 7, e7, start=440))
    # ── F6 · Cana Pearl (1030)
    A(cover("f6_1030_01", P(1030, 4), ["Imagina vivir rodeado", "de un campo de golf."], "CANA PEARL", "CANA BAY   -   2 HABITACIONES   -   2 BAÑOS   -   AMUEBLADO", focus=(0.62, 0.5), start=560, st=0.97))
    for k, (n, fx) in enumerate([(3, 0.35), (8, 0.45), (10, 0.3), (9, 0.5), (1, 0.42)], 2): A(clean(f"f6_1030_{k:02d}", P(1030, n), (fx, 0.5)))
    A(ficha("f6_1030_07", P(1030, 1), ["Cana Pearl"], "CANA BAY  ·  BÁVARO", "US$1,800",
            ["2 habitaciones  ·  2 baños  ·  Amueblado", "Balcón con vista a la piscina", "Membresía del Club de Playa", "Campo de golf  ·  Gimnasio  ·  Spa"], focus=(0.42, 0.5)))

    # ── HISTORIAS LRH
    PF = lambda s, it=False, w=600: play(s, it, w)
    L = lambda s: inter(s, "Light"); M = lambda s: inter(s, "Medium")
    def teaser(tag, nombre, zona, precio, det):
        def f(c):
            c.pill(1010, tag, M(26))
            c.text(1090, nombre, play(84, True, 500), WHITE)
            c.text(1206, zona, M(26), (255, 255, 255, 225), 6)
            c.text(1262, precio, PF(150), GOLD)
            c.text(1446, "AL MES  ·  LARGO PLAZO", M(28), WHITE, 6)
            c.rule(1510, 120)
            c.lines(1540, det, L(36), WHITE, 52)
        return f
    A(story("j12_1_villa", P(1039, 1), teaser("NUEVA EN EL FEED", "Villa San Juan Lake", "DOWNTOWN PUNTA CANA", "US$2,875", ["3 habitaciones · 3.5 baños · Piscina", "Mira todas las fotos en nuestro perfil"]), start=520))
    def h(c):
        c.pill(1040, "NOS PASA A TODOS", M(26))
        c.lines(1120, ["“Solo voy a ver", "el apartamento.”"], PF(88, True), WHITE, 104)
        c.lines(1370, ["Diez minutos después:", "decidiendo dónde va el sofá."], L(42), WHITE, 60)
        c.text(1530, "¿A quién más le ha pasado?", M(38), GOLD)
    A(story("j12_2_humor", P(1044, 3), h, start=520))
    def h(c):
        c.pill(1000, "TIP PARA INQUILINOS", M(26))
        c.lines(1080, ["Antes de decir que sí,", "pregunta esto:"], PF(76), WHITE, 92)
        c.lines(1300, ["“¿El mantenimiento", "está incluido?”"], PF(76, True), GOLD, 92)
        c.lines(1520, ["Un precio sin esa respuesta", "es un precio a medias."], L(40), WHITE, 56)
    A(story("v13_1_tip", P(1044, 2), h, start=480))
    def h(c):
        c.pill(980, "CUÉNTANOS TU CASO", M(26))
        c.lines(1060, ["“Me enseñaron", "un apartamento en fotos…"], PF(72, True), WHITE, 90)
        c.lines(1262, ["y cuando llegué", "era otro.”"], PF(72, True), GOLD, 90)
        c.lines(1480, ["¿Qué habrías hecho tú?"], M(42), WHITE, 56)
        c.pill(1580, "RESPÓNDENOS AQUÍ ABAJO", M(26), fill=WHITE, color=GREEN)
    A(story("v13_2_chisme", P(1038, 8), h, focus=(0.35, 0.5), start=480))
    # sábado: esto o aquello
    c = C(Image.new("RGB", (SW, SH), GREEN), 1)
    c.im.paste(develop(P(1044, 4), SW, 940, (0.5, 0.55)), (0, 0)); c.im.paste(develop(P(1036, 16), SW, 940, (0.5, 0.35)), (0, 980)); c.d = ImageDraw.Draw(c.im)
    ov = Image.new("RGBA", (SW, SH)); od = ImageDraw.Draw(ov)
    od.rectangle([0, 0, SW, 400], fill=(*GREEN, 165)); od.rectangle([0, 770, SW, 940], fill=(*GREEN, 175)); od.rectangle([0, 1560, SW, SH], fill=(*GREEN, 190))
    c.over(ov); c.logo(180, 64)
    c.text(280, "Sábado: ¿tú eres team…?", PF(64, True), WHITE)
    c.text(812, "1", PF(60), GOLD, x=120); c.text(814, "Piscina todo el día", play(56, True), WHITE, x=190)
    c.text(1592, "2", PF(60), GOLD, x=120); c.text(1594, "Cocinar en casa con la música alta", play(50, True), WHITE, x=190)
    c.d.rounded_rectangle([(SW - 520) / 2, 934, (SW + 520) / 2, 1026], 46, fill=WHITE); c.text(952, "Respóndenos con 1 o 2", M(36), GREEN)
    A(c.save("h_s14_1_team", 95))
    def h(c):
        c.pill(1120, "SÁBADO EN PUNTA CANA", M(26))
        c.lines(1200, ["Hay planes que", "no necesitan salir de casa."], PF(74, True), WHITE, 92)
        c.lines(1430, ["¿Con quién compartirías esta piscina?", "Mándale esta historia."], L(40), WHITE, 58)
    A(story("s14_2_piscina", P(1036, 4), h, focus=(0.5, 0.5), start=620))
    def h(c):
        c.pill(960, "PARA PROPIETARIOS", M(26))
        c.lines(1040, ["Tú descansas", "el domingo."], PF(88), WHITE, 104)
        c.lines(1270, ["Tu propiedad puede", "seguir trabajando."], PF(72, True), GOLD, 90)
        c.lines(1480, ["La alquilamos a largo plazo", "y la administramos por ti."], L(40), WHITE, 56)
        c.pill(1620, f"ESCRÍBENOS {WA}", M(26), fill=WHITE, color=GREEN)
    A(story("d15_1_propietarios", P(1030, 3), h, focus=(0.4, 0.5), start=460))
    A(story("l16_1_sabana", P(1036, 1), teaser("NUEVA EN EL FEED", "Sabana Equestrian", "VISTA CANA · PUNTA CANA", "US$3,480", ["3 habitaciones · 5 baños · Piscina y gazebo", "Mira todas las fotos en nuestro perfil"]), start=520))
    def h(c):
        c.pill(880, "MITO", M(26), fill=(120, 40, 40), color=WHITE)
        c.lines(960, ["“Para alquilar hay que", "ir a verlo sí o sí.”"], PF(68, True), WHITE, 84)
        c.pill(1190, "REALIDAD", M(26))
        c.lines(1270, ["Te enviamos el video completo", "por WhatsApp antes de que vengas.", "Así llegas a ver solo lo que te gustó."], L(40), WHITE, 56)
        c.text(1500, "¿Cuál quieres ver primero?", M(38), GOLD)
        c.pill(1600, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    A(story("l16_2_mito", P(1038, 2), h, start=440))
    def h(c):
        c.pill(1040, "NUEVO EN EL FEED", M(26))
        c.lines(1120, ["5 cosas que revisar", "antes de firmar"], PF(80), WHITE, 96)
        c.text(1318, "un alquiler.", PF(80, True), GOLD)
        c.lines(1470, ["Está en nuestro perfil.", "Guárdalo: un día te va a servir."], L(40), WHITE, 56)
    A(story("m17_1_edu", P(1036, 3), h, start=500))
    def h(c):
        c.pill(960, "BUSCANDO APARTAMENTO", M(26))
        c.lines(1040, ["“Que tenga piscina,", "gimnasio y parqueo,", "que esté cerca de todo…"], PF(66, True), WHITE, 84)
        c.text(1310, "y que sea barato.”", PF(66, True), GOLD)
        c.lines(1450, ["Dinos tu presupuesto real", "y te decimos qué hay."], L(42), WHITE, 58)
        c.pill(1620, "RESPÓNDENOS AQUÍ ABAJO", M(26), fill=WHITE, color=GREEN)
    A(story("m17_2_humor", P(1044, 5), h, start=460))
    A(story("x18_1_canapearl", P(1030, 4), teaser("NUEVA EN EL FEED", "Cana Pearl", "CANA BAY · BÁVARO", "US$1,800", ["2 habitaciones · 2 baños · Amueblado", "Mira todas las fotos en nuestro perfil"]), focus=(0.6, 0.5), start=520))
    def h(c):
        c.pill(1000, "LARGO PLAZO · BÁVARO Y PUNTA CANA", M(26))
        c.lines(1080, ["¿Te mudas", "pronto?"], PF(100), WHITE, 116)
        c.lines(1340, ["Dinos zona, habitaciones", "y presupuesto."], PF(60, True), GOLD, 78)
        c.lines(1520, ["Te enviamos las opciones disponibles", "con video y precio."], L(38), WHITE, 54)
        c.pill(1650, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    A(story("x18_2_cta", P(1044, 7), h, start=440))

    # ── HISTORIAS MACIEL
    A(jason("j12_villa", "RECIÉN PUBLICADA", ["VILLA CON", "PISCINA EN", "*US$2,875"], body=["San Juan Lake, Downtown Punta Cana.", "3 habitaciones, 3.5 baños y 3 parqueos."],
            ask=["ESCRÍBEME Y TE", "MANDO EL VIDEO"], src=P(1039, 1), focus=(0.5, 0.3), hs=120))
    A(jason("v13_tip", "CONSEJO DE AGENTE", ["LA PREGUNTA", "QUE NADIE HACE", "*ANTES DE FIRMAR"], quote=["“¿El mantenimiento está", "incluido en el precio?”"],
            body=["Si no te lo dicen claro, pregúntalo dos", "veces. Un precio a medias sale caro."], ask=["¿TÚ LO PREGUNTASTE?"], hs=118))
    A(jason("s14_team", "SÁBADO", ["¿VILLA CON", "PISCINA O", "*APARTAMENTO", "*CON GOLF?"], quote=["Yo ya elegí. Y no te voy", "a decir cuál."], ask=["RESPÓNDEME CON", "TU FAVORITA"], hs=124))
    A(jason("l16_sabana", "PARA LOS QUE AMAN LOS CABALLOS", ["SABANA", "EQUESTRIAN", "*US$3,480"], body=["Vista Cana. 3 habitaciones, 5 baños,", "piscina, gazebo y línea blanca incluida."],
            ask=["¿TE LA ENSEÑO?"], src=P(1036, 1), focus=(0.5, 0.3), hs=120))
    A(jason("x18_canapearl", "AMUEBLADO Y LISTO", ["CANA PEARL,", "FRENTE AL GOLF", "*US$1,800"], body=["Cana Bay. 2 habitaciones, 2 baños y", "membresía del Club de Playa."],
            ask=["ESCRÍBEME: " + WA], src=P(1030, 4), focus=(0.62, 0.3), hs=112))
    return made

if __name__ == "__main__":
    m = build(); print(len(m)); [print(os.path.basename(x), os.path.getsize(x) // 1024, "KB") for x in m]
