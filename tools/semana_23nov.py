#!/usr/bin/env python3
"""Semana 23-30 nov 2026: feed 4:5 (2160x2700) e historias 1080x1920 para @luxuryrenthouserd (Estilo Oppenheim)
y @maciel.luxuryrh (Estilo Jason). Reutiliza el motor de semana_12nov.py. Solo fotos reales de AlterEstate.
Propiedades: 1038 (Doral Residences, Costa Bávaro) y 1044 (Vista Cana). Datos tomados de cada ficha (data/alterestate_fichas.json).
Sin etiquetas de audiencia y sin la palabra "barato" (reglas del README)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import semana_12nov as b
from semana_12nov import (C, develop, grad, play, corm, inter, osw, mont, P, SW, SH, FW, FH, K,
                          GREEN, GOLD, WHITE, LUXD, PIEDRA, INKJ, AMBAR, CREMA, WA, ImageDraw, Image)

b.OUT = f"{b.R}/media/semana_1123"; os.makedirs(b.OUT, exist_ok=True)
PF = lambda s, it=False, w=600: play(s, it, w)
L = lambda s: inter(s, "Light"); M = lambda s: inter(s, "Medium")
ESP = (255, 255, 255, 235)

# ───────── datos de fichas (copiados tal cual de AlterEstate) ─────────
D1038 = dict(nombre="DORAL RESIDENCES", zona="COSTA BÁVARO", precio="US$1,175",
             det="COSTA BÁVARO   -   2 HABITACIONES   -   2 BAÑOS   -   AMUEBLADO",
             feats=["2 habitaciones  ·  2 baños  ·  Amueblado", "Terraza privada  ·  Walking clóset", "Piscina  ·  Coworking  ·  1 parqueo", "Mantenimiento incluido  ·  Acepta mascotas"])
D1044 = dict(nombre="VENTURA GOLF", zona="VISTA CANA  ·  PUNTA CANA", precio="US$1,195",
             det="PUNTA CANA   -   1 HABITACIÓN   -   1.5 BAÑOS   -   AMUEBLADO",
             feats=["1 habitación  ·  1.5 baños  ·  Amueblado", "Terraza  ·  110 m²  ·  1 parqueo", "Golf  ·  Casa club  ·  Gimnasio", "Mantenimiento incluido  ·  Acepta mascotas"])

def paso2(num, es, en, sub):
    """Paso educativo bilingüe: número, título en español, línea en inglés y apoyo corto."""
    def f(c):
        c.text(900, num, play(64 * K, False, 600), GOLD)
        y = c.lines(1000, c.wrap(es, play(58 * K, True), 880), play(58 * K, True), WHITE, 72)
        y = c.lines(y + 24, c.wrap(en, inter(26 * K, "Medium"), 880), inter(26 * K, "Medium"), PIEDRA, 38)
        c.lines(y + 24, c.wrap(sub, inter(31 * K, "Light"), 820), inter(31 * K, "Light"), ESP, 44)
    return f

def card(name, src, draw, focus=(0.5, 0.5), dark=228):
    c = C(develop(src, FW, FH, focus), K); c.over(Image.new("RGBA", (FW, FH), (*LUXD, dark))); draw(c); return c.save(name)

def build():
    made = []; A = made.append

    # ═════════════ FEED @luxuryrenthouserd ═════════════
    # L23 · Carrusel 1038
    A(b.cover("f_l23_1038_01", P(1038, 3), ["Llegar y que todo esté listo.", "Move-in ready."], D1038["nombre"], D1038["det"], tsize=80, tsp=10))
    for k, n in enumerate([8, 2, 5, 7, 6, 4], 2): A(b.clean(f"f_l23_1038_{k:02d}", P(1038, n)))
    A(b.ficha("f_l23_1038_08", P(1038, 8), ["Doral Residences"], "COSTA BÁVARO", D1038["precio"], D1038["feats"]))

    # M24 · Educativo bilingüe: por qué unas propiedades se alquilan rápido
    def e1(c):
        c.pill(812, "GUÁRDALO  ·  SAVE IT", inter(22 * K, "Medium"))
        c.lines(884, ["¿Por qué unas propiedades", "se alquilan en días…"], play(74 * K, False, 600), WHITE, 92)
        c.text(1070, "y otras en meses?", play(74 * K, True, 600), GOLD)
        c.text(1180, "Why some homes rent in days, and others take months.", inter(24 * K, "Medium"), PIEDRA)
        c.text(1262, "DESLIZA  →", inter(24 * K, "Medium"), (255, 255, 255, 220), 6)
    A(b.edu("f_m24_edu_01", P(1044, 3), 1, 7, e1, start=480))
    pasos = [("01", "Fotos reales y con buena luz.", "Real photos, good light.", "Lo primero que se decide es si vale la pena venir a verla.", P(1044, 9)),
             ("02", "Un precio claro.", "Clear pricing.", "Qué incluye y qué no: mantenimiento, servicios, depósito.", P(1038, 3)),
             ("03", "Lista para mudarse.", "Move-in ready.", "Todo funcionando el día de la visita. Los detalles venden.", P(1038, 2)),
             ("04", "Responder rápido.", "Fast replies.", "Quien está buscando casa no espera tres días por un mensaje.", P(1044, 6)),
             ("05", "Inquilino evaluado y contrato claro.", "Screened tenants, clear contracts.", "Así el alquiler dura y todos duermen tranquilos.", P(1038, 8))]
    for k, (n, es, en, s_, src) in enumerate(pasos, 2): A(b.edu(f"f_m24_edu_{k:02d}", src, k, 7, paso2(n, es, en, s_), start=470))
    def e7(c):
        c.lines(720, ["Eso es lo que hacemos", "todos los días."], play(76 * K, False, 600), WHITE, 92)
        c.text(912, "That's our everyday job.", play(56 * K, True, 500), GOLD)
        c.lines(1020, ["¿Cuál de las cinco crees que pesa más?", "Te leemos en los comentarios."], inter(34 * K, "Light"), WHITE, 50)
        c.pill(1180, f"WHATSAPP  {WA}", inter(22 * K, "Medium"), fill=WHITE, color=LUXD, sp=5, padx=44, h=72)
    A(b.edu("f_m24_edu_07", P(1044, 11), 7, 7, e7, start=400))

    # X25 · Esto o aquello bilingüe
    c = C(Image.new("RGB", (FW, FH), LUXD), K)
    top = develop(P(1038, 4), FW, 560 * K, (0.5, 0.55)).convert("RGBA"); top.alpha_composite(grad(FW, 560 * K, 300 * K, 0.88, col=(10, 14, 13)))
    bot = develop(P(1044, 4), FW, 560 * K, (0.5, 0.6)).convert("RGBA"); bot.alpha_composite(grad(FW, 560 * K, 300 * K, 0.9, col=(10, 14, 13)))
    c.im.paste(top, (0, 230 * K)); c.im.paste(bot, (0, 790 * K)); c.d = ImageDraw.Draw(c.im)
    c.logo(30, 50); c.text(94, "¿Tú eres team…?  ·  Team A or B?", corm(54 * K, 500, True), WHITE)
    c.text(682, "A", corm(60 * K, 600), GOLD, x=70); c.text(686, "Café en la terraza", corm(52 * K, 500, True), WHITE, x=150)
    c.text(742, "COFFEE ON THE TERRACE", inter(18 * K, "Medium"), PIEDRA, 5, x=152)
    c.text(1240, "B", corm(60 * K, 600), GOLD, x=70); c.text(1244, "Piscina después del trabajo", corm(52 * K, 500, True), WHITE, x=150)
    c.text(1300, "POOL AFTER WORK", inter(18 * K, "Medium"), PIEDRA, 5, x=152)
    c.pill(180, "COMENTA  A  O  B  ·  COMMENT A OR B", inter(19 * K, "Medium"), fill=WHITE, color=LUXD, sp=4, padx=40, h=58)
    A(c.save("f_x25_team"))

    # V27 · Carrusel 1044
    A(b.cover("f_v27_1044_01", P(1044, 4), ["Piscina, palmas y cielo abierto.", "Your new everyday view."], D1044["nombre"], D1044["det"], focus=(0.5, 0.5), tsize=96, tsp=18))
    for k, n in enumerate([3, 1, 2, 6, 9, 5], 2): A(b.clean(f"f_v27_1044_{k:02d}", P(1044, n)))
    A(b.ficha("f_v27_1044_08", P(1044, 3), ["Ventura Golf"], "VISTA CANA  ·  PUNTA CANA", D1044["precio"], D1044["feats"]))

    # S28 · Humor (deja mensaje): "solo voy a ver uno"
    def hum(c):
        c.logo(110, 96)
        c.text(300, "SÁBADO  ·  SATURDAY", inter(20 * K, "Medium"), PIEDRA, 8)
        c.lines(390, ["“Solo voy a ver", "un apartamento.”"], corm(104 * K, 500, True), WHITE, 116)
        c.text(650, "“I'm just going to look at one.”", corm(50 * K, 400, True), PIEDRA)
        c.rule(760, 80, PIEDRA, 1.5)
        c.lines(810, ["Siete apartamentos después:", "ya sabes dónde va el sofá,", "qué cuarto es la oficina"], inter(38 * K, "Light"), WHITE, 56)
        c.text(978, "y quién se queda con el balcón.", inter(38 * K, "Light"), GOLD)
        c.lines(1070, ["Etiqueta a quien te acompaña a ver casas.", "Tag your house-hunting partner."], inter(28 * K, "Medium"), ESP, 44)
        c.pill(1200, "@LUXURYRENTHOUSERD", inter(22 * K, "Medium"), fill=WHITE, color=LUXD, sp=5, padx=44, h=68)
    A(card("f_s28_humor", P(1044, 3), hum, dark=222))

    # D29 · Confianza: así trabajamos (carrusel)
    def t1(c):
        c.pill(820, "ASÍ TRABAJAMOS  ·  HOW WE WORK", inter(22 * K, "Medium"))
        c.lines(890, ["Mudarse en Punta Cana", "sin perder fines de semana"], play(70 * K, False, 600), WHITE, 88)
        c.text(1070, "viendo lo que no es.", play(70 * K, True, 600), GOLD)
        c.text(1190, "Moving to Punta Cana, minus the wasted weekends.", inter(24 * K, "Medium"), PIEDRA)
        c.text(1262, "DESLIZA  →", inter(24 * K, "Medium"), (255, 255, 255, 220), 6)
    A(b.edu("f_d29_team_01", P(1038, 1), 1, 6, t1, start=470))
    st = [("01", "Nos dices qué buscas.", "Tell us what you need.", "Zona, habitaciones, presupuesto y fecha de mudanza.", P(1044, 8)),
          ("02", "Te enviamos video real.", "We send you real video.", "De cada opción disponible, antes de que salgas de casa.", P(1038, 3)),
          ("03", "Visitas solo lo que te gustó.", "Visit only what you liked.", "Contrato claro y entrega con inventario y fotos.", P(1044, 9)),
          ("04", "Y seguimos ahí.", "And we stay close.", "Administramos la propiedad durante todo el alquiler.", P(1038, 5))]
    for k, (n, es, en, s_, src) in enumerate(st, 2): A(b.edu(f"f_d29_team_{k:02d}", src, k, 6, paso2(n, es, en, s_), start=470))
    def t6(c):
        c.lines(740, ["¿Qué es lo que más", "te preocupa al mudarte?"], play(72 * K, False, 600), WHITE, 90)
        c.text(930, "What worries you most about moving?", play(46 * K, True, 500), GOLD)
        c.lines(1030, ["Cuéntanos en los comentarios.", "Te respondemos sin rodeos."], inter(34 * K, "Light"), WHITE, 50)
        c.pill(1180, f"WHATSAPP  {WA}", inter(22 * K, "Medium"), fill=WHITE, color=LUXD, sp=5, padx=44, h=72)
    A(b.edu("f_d29_team_06", P(1044, 7), 6, 6, t6, start=420))

    # L30 · Cyber Monday
    def cy(c):
        c.pill(700, "CYBER MONDAY", inter(22 * K, "Medium"))
        c.lines(770, ["Lo único que vale la pena", "“agregar al carrito”"], play(70 * K, False, 600), WHITE, 88)
        c.text(950, "es una casa donde quieras quedarte.", play(56 * K, True, 500), GOLD)
        c.lines(1050, ["The best thing to add to cart:", "a home you actually want to stay in."], inter(28 * K, "Medium"), PIEDRA, 42)
        c.pill(1180, f"WHATSAPP  {WA}", inter(22 * K, "Medium"), fill=WHITE, color=LUXD, sp=5, padx=44, h=72)
    c = C(develop(P(1044, 9), FW, FH, (0.5, 0.5)), K); c.over(grad(FW, FH, 380 * K, 0.97, top=0.45, toph=300 * K, ex=0.8)); c.logo(44, 60); cy(c)
    A(c.save("f_l30_cyber"))

    # ═════════════ HISTORIAS @luxuryrenthouserd ═════════════
    def teaser(tag, nombre, zona, precio, det):
        def f(c):
            c.pill(1010, tag, M(26)); c.text(1090, nombre, play(80, True, 500), WHITE)
            c.text(1200, zona, M(26), (255, 255, 255, 225), 6); c.text(1256, precio, PF(150), GOLD)
            c.text(1440, "AL MES  ·  LARGO PLAZO", M(28), WHITE, 6); c.rule(1504, 120); c.lines(1534, det, L(36), WHITE, 52)
        return f
    def poll(name, title, a, b_, srcA, srcB, fa=(0.5, 0.5), fb=(0.5, 0.5)):
        c = C(Image.new("RGB", (SW, SH), GREEN), 1)
        c.im.paste(develop(srcA, SW, 940, fa), (0, 0)); c.im.paste(develop(srcB, SW, 940, fb), (0, 980)); c.d = ImageDraw.Draw(c.im)
        ov = Image.new("RGBA", (SW, SH)); od = ImageDraw.Draw(ov)
        od.rectangle([0, 0, SW, 400], fill=(*GREEN, 165)); od.rectangle([0, 770, SW, 940], fill=(*GREEN, 175)); od.rectangle([0, 1560, SW, SH], fill=(*GREEN, 190))
        c.over(ov); c.logo(180, 64); c.text(280, title, PF(58, True), WHITE)
        c.text(812, "1", PF(60), GOLD, x=110); c.text(814, a, play(52, True), WHITE, x=180)
        c.text(1592, "2", PF(60), GOLD, x=110); c.text(1594, b_, play(52, True), WHITE, x=180)
        c.d.rounded_rectangle([(SW - 520) / 2, 934, (SW + 520) / 2, 1026], 46, fill=WHITE); c.text(952, "Respóndenos con 1 o 2", M(36), GREEN)
        return c.save("h_" + name, 95)

    A(b.story("l23_1_doral", P(1038, 3), teaser("NUEVA EN EL FEED", "Doral Residences", "COSTA BÁVARO", D1038["precio"], ["2 habitaciones · 2 baños · Terraza privada", "Mira todas las fotos en nuestro perfil"]), start=520))
    A(poll("l23_2_poll", "Lunes: ¿cómo te mudas tú?", "Amueblado, llegar y listo", "Vacío, a mi gusto", P(1038, 8), P(1038, 4), fb=(0.5, 0.6)))
    def h(c):
        c.pill(1000, "DATO DEL DÍA", M(26))
        c.lines(1080, ["Una propiedad", "con fotos reales"], PF(84), WHITE, 100)
        c.lines(1290, ["recibe visitas", "que sí vienen a firmar."], PF(66, True), GOLD, 82)
        c.lines(1500, ["Hoy en el feed: 5 cosas que hacen", "que un alquiler se mueva rápido."], L(38), WHITE, 54)
    A(b.story("m24_1_dato", P(1044, 9), h, start=460))
    def h(c):
        c.pill(980, "PREGUNTA SERIA", M(26))
        c.lines(1060, ["¿Qué pesa más", "al elegir dónde vivir?"], PF(78), WHITE, 94)
        c.lines(1290, ["Ubicación, espacio", "o amenidades."], PF(64, True), GOLD, 80)
        c.text(1490, "Respóndenos con una palabra.", M(38), WHITE)
        c.pill(1600, "RESPÓNDENOS AQUÍ ABAJO", M(26), fill=WHITE, color=GREEN)
    A(b.story("m24_2_pregunta", P(1044, 6), h, start=460))
    A(poll("x25_1_team", "¿Team terraza o team piscina?", "Café en la terraza", "Piscina después del trabajo", P(1038, 4), P(1044, 4), fa=(0.5, 0.55), fb=(0.5, 0.6)))
    def h(c):
        c.pill(1000, "NOS PASA A TODOS", M(26))
        c.lines(1080, ["“Ese apartamento", "lo vi en un video…"], PF(78, True), WHITE, 96)
        c.lines(1290, ["y ya le puse", "nombre al balcón.”"], PF(78, True), GOLD, 96)
        c.text(1520, "¿A quién más le ha pasado?", M(38), WHITE)
    A(b.story("x25_2_humor", P(1044, 6), h, start=480))
    def h(c):
        c.pill(1010, "HAPPY THANKSGIVING", M(26))
        c.lines(1090, ["Gracias a cada familia", "que eligió Punta Cana"], PF(70), WHITE, 86)
        c.text(1270, "como hogar.", PF(70, True), GOLD)
        c.lines(1420, ["Thank you to every family", "that made Punta Cana home."], L(38), WHITE, 54)
    A(b.story("j26_1_thanks", P(1044, 4), h, focus=(0.5, 0.5), start=520))
    def h(c):
        c.pill(1000, "ACCIÓN DE GRACIAS", M(26))
        c.lines(1080, ["¿Por qué das", "gracias este año?"], PF(86), WHITE, 102)
        c.lines(1320, ["Una palabra basta.", "One word is enough."], PF(60, True), GOLD, 76)
        c.pill(1560, "RESPÓNDENOS AQUÍ ABAJO", M(26), fill=WHITE, color=GREEN)
    A(b.story("j26_2_pregunta", P(1044, 8), h, start=520))
    A(b.story("v27_1_vistacana", P(1044, 4), teaser("NUEVA EN EL FEED", "Ventura Golf", "VISTA CANA · PUNTA CANA", D1044["precio"], ["1 habitación · 1.5 baños · Mantenimiento incluido", "Mira todas las fotos en nuestro perfil"]), start=520))
    def h(c):
        c.pill(980, "BLACK FRIDAY", M(26))
        c.lines(1060, ["Hoy todo el mundo", "anda buscando ofertas."], PF(76), WHITE, 92)
        c.lines(1270, ["Nosotros te ahorramos", "algo mejor: tiempo."], PF(66, True), GOLD, 82)
        c.lines(1480, ["Te mandamos el video completo", "antes de que vengas a verlo."], L(38), WHITE, 54)
        c.pill(1620, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    A(b.story("v27_2_blackfriday", P(1044, 1), h, start=450))
    A(poll("s28_1_team", "Sábado: ¿tú eres team…?", "Cocinar en casa", "Salir a comer fuera", P(1038, 2), P(1044, 9)))
    def h(c):
        c.pill(980, "CUÉNTANOS TU CASO", M(26))
        c.lines(1060, ["“Me mudé por la piscina…"], PF(70, True), WHITE, 90)
        c.lines(1170, ["y ahora la uso", "todos los días.”"], PF(70, True), GOLD, 88)
        c.lines(1420, ["¿Qué te hizo decir “esta es”", "en tu última mudanza?"], M(40), WHITE, 56)
        c.pill(1580, "RESPÓNDENOS AQUÍ ABAJO", M(26), fill=WHITE, color=GREEN)
    A(b.story("s28_2_chisme", P(1038, 1), h, start=480))
    def h(c):
        c.pill(980, "¿TE MUDAS EN ENERO?", M(26))
        c.lines(1060, ["El último domingo", "de noviembre"], PF(84), WHITE, 100)
        c.lines(1290, ["es buen día para", "empezar a buscar."], PF(66, True), GOLD, 82)
        c.lines(1500, ["Dinos zona, habitaciones y presupuesto.", "Te mandamos opciones con video."], L(38), WHITE, 54)
        c.pill(1640, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    A(b.story("d29_1_enero", P(1038, 5), h, start=450))
    def h(c):
        c.pill(960, "DOMINGO DE NÚMEROS", M(26))
        c.lines(1040, ["Una propiedad vacía", "también tiene gastos."], PF(76), WHITE, 92)
        c.lines(1260, ["Una bien alquilada", "trabaja mientras descansas."], PF(62, True), GOLD, 80)
        c.lines(1470, ["La alquilamos a largo plazo", "y la administramos por ti."], L(40), WHITE, 56)
        c.pill(1620, f"ESCRÍBENOS {WA}", M(26), fill=WHITE, color=GREEN)
    A(b.story("d29_2_gastos", P(1038, 7), h, start=440))
    def h(c):
        c.pill(1000, "CYBER MONDAY", M(26))
        c.lines(1080, ["Hoy se compra", "de todo en línea."], PF(84), WHITE, 100)
        c.lines(1290, ["Tu próxima casa", "también se ve primero en video."], PF(58, True), GOLD, 76)
        c.lines(1480, ["Escríbenos y te mandamos", "las opciones disponibles."], L(40), WHITE, 56)
        c.pill(1620, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    A(b.story("l30_1_cyber", P(1044, 3), h, start=470))
    def h(c):
        c.pill(1000, "MAÑANA ES DICIEMBRE", M(26))
        c.lines(1080, ["¿Dónde quieres", "recibir el 2027?"], PF(88), WHITE, 104)
        c.lines(1320, ["Todavía hay tiempo", "para mudarte con calma."], PF(60, True), GOLD, 78)
        c.pill(1560, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    A(b.story("l30_2_diciembre", P(1038, 1), h, start=520))

    # ═════════════ HISTORIAS @maciel.luxuryrh (Estilo Jason) ═════════════
    A(b.jason("l23_doral", "RECIÉN PUBLICADO", ["DORAL", "RESIDENCES", "*US$1,175"],
              body=["Costa Bávaro. 2 habitaciones, 2 baños,", "terraza privada y mantenimiento incluido."],
              ask=["¿TE MANDO EL VIDEO?"], src=P(1038, 3), focus=(0.5, 0.3), hs=124))
    A(b.jason("x25_consejo", "CONSEJO DE AGENTE", ["FOTOS BONITAS", "NO ES LO MISMO", "*QUE FOTOS REALES"],
              quote=["Pide siempre un video de la", "propiedad tal como está hoy."],
              body=["Yo se lo mando a todo el que me", "escribe, antes de la visita."], ask=["¿TE HA PASADO?"], hs=110))
    A(b.jason("v27_viernes", "BLACK FRIDAY, VERSIÓN AGENTE", ["LA MEJOR", "OFERTA ES", "*TU TIEMPO"],
              quote=["Ver tres apartamentos buenos", "vale más que ver diez al azar."],
              body=["Dime qué buscas y te filtro", "las opciones con video."], ask=["ESCRÍBEME: " + WA], hs=124))
    A(b.jason("d29_domingo", "PREGUNTA DE DOMINGO", ["¿BÁVARO", "O VISTA", "*CANA?"],
              quote=["Dos zonas, dos estilos de vida.", "Las dos tienen lo suyo."],
              body=["Cuéntame cuál va contigo y te", "enseño lo que hay disponible."], ask=["RESPÓNDEME AQUÍ"], hs=124))
    return made

if __name__ == "__main__":
    m = build(); print(len(m)); [print(os.path.basename(x), os.path.getsize(x) // 1024, "KB") for x in m]
