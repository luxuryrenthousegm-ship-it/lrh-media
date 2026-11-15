#!/usr/bin/env python3
"""Relleno 20-22 nov 2026: 2 historias @luxuryrenthouserd (domingo 22) y 2 historias @maciel.luxuryrh (viernes 20 y domingo 22).
Reutiliza el motor de semana_12nov.py. Solo fotos reales de AlterEstate."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import semana_12nov as b
from semana_12nov import C, develop, play, inter, P, SW, SH, GREEN, GOLD, WHITE, WA, ImageDraw, Image

b.OUT = f"{b.R}/media/semana_1120"; os.makedirs(b.OUT, exist_ok=True)
PF = lambda s, it=False, w=600: play(s, it, w)
L = lambda s: inter(s, "Light"); M = lambda s: inter(s, "Medium")

def build():
    made = []
    # ── LRH domingo 22, 1:00 p. m. · esto o aquello (villa 1039 vs Doral 1038)
    c = C(Image.new("RGB", (SW, SH), GREEN), 1)
    c.im.paste(develop(P(1039, 1), SW, 940, (0.5, 0.5)), (0, 0)); c.im.paste(develop(P(1038, 3), SW, 940, (0.5, 0.5)), (0, 980)); c.d = ImageDraw.Draw(c.im)
    ov = Image.new("RGBA", (SW, SH)); od = ImageDraw.Draw(ov)
    od.rectangle([0, 0, SW, 400], fill=(*GREEN, 165)); od.rectangle([0, 770, SW, 940], fill=(*GREEN, 175)); od.rectangle([0, 1560, SW, SH], fill=(*GREEN, 190))
    c.over(ov); c.logo(180, 64)
    c.text(280, "Domingo: ¿dónde te mudarías?", PF(60, True), WHITE)
    c.text(812, "1", PF(60), GOLD, x=120); c.text(814, "Villa con piscina propia", play(56, True), WHITE, x=190)
    c.text(1592, "2", PF(60), GOLD, x=120); c.text(1594, "Apartamento amueblado en Bávaro", play(50, True), WHITE, x=190)
    c.d.rounded_rectangle([(SW - 520) / 2, 934, (SW + 520) / 2, 1026], 46, fill=WHITE); c.text(952, "Respóndenos con 1 o 2", M(36), GREEN)
    made.append(c.save("h_d22_1_team", 95))

    # ── LRH domingo 22, 6:00 p. m. · mudanza de enero
    def h(c):
        c.pill(980, "¿TE MUDAS EN ENERO?", M(26))
        c.lines(1060, ["Diciembre es para", "buscar con calma."], PF(84), WHITE, 100)
        c.lines(1290, ["No a última hora", "con las maletas hechas."], PF(64, True), GOLD, 82)
        c.lines(1500, ["Dinos zona, habitaciones y presupuesto.", "Te mandamos opciones con video."], L(38), WHITE, 54)
        c.pill(1640, f"WHATSAPP {WA}", M(26), fill=WHITE, color=GREEN)
    made.append(b.story("d22_2_enero", P(1044, 4), h, focus=(0.5, 0.55), start=440))

    # ── MACIEL viernes 20 · Ventura Golf (1044)
    made.append(b.jason("v20_ventura", "LISTO PARA MUDARTE", ["AMUEBLADO", "EN VISTA CANA", "*US$1,195"],
                        body=["Ventura Golf, Vista Cana. 1 habitación,", "terraza y mantenimiento incluido."],
                        ask=["¿TE MANDO EL VIDEO?"], src=P(1044, 3), focus=(0.5, 0.35), hs=124))
    # ── MACIEL domingo 22 · tip para propietarios
    made.append(b.jason("d22_propietarios", "PARA PROPIETARIOS", ["UN APARTAMENTO", "VACÍO TAMBIÉN", "*TE CUESTA"],
                        quote=["Mantenimiento, luz, agua…", "corren aunque nadie viva ahí."],
                        body=["Nosotros lo alquilamos a largo plazo", "y lo administramos por ti."],
                        ask=["ESCRÍBEME: " + WA], hs=116))
    return made

if __name__ == "__main__":
    for x in build(): print(os.path.basename(x), os.path.getsize(x) // 1024, "KB")
