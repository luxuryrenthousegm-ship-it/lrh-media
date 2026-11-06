#!/usr/bin/env python3
"""Lote 2 variado: carrusel 'Adivina el precio' + 5 historias de formatos distintos."""
import os
from PIL import Image, ImageDraw
import make_images as m
from make_images import CW, CH, SW, SH, GOLD, GREEN, WHITE, play, LIGHT, MED, ctext, spaced, pill, lines, brand, photo, grad, wrap

m.OUT = OUT = f"{m.S}/contenido_lote2"; os.makedirs(OUT, exist_ok=True)
N = 7

def pista(num, txt):
    def f(d):
        pill(d, CW, 930, f"PISTA {num}")
        y = 1010
        for t in wrap(d, txt, play(56, True), 840): ctext(d, CW, y, t, play(56, True), WHITE); y += 72
        spaced(d, CW / 2, 1262, "¿YA TIENES TU NÚMERO?  →", MED(22), (255, 255, 255, 210), 5)
    return f

def carousel():
    def s1(d):
        pill(d, CW, 800, "JUEGO RÁPIDO")
        ctext(d, CW, 875, "Adivina el precio", play(92, w=600), WHITE)
        ctext(d, CW, 985, "de este apartamento", play(64, True), GOLD)
        ctext(d, CW, 1065, "en Costa Bávaro", play(64, True), GOLD)
        lines(d, CW, 1170, ["Comenta tu número antes de llegar al final.", "Sin trampa."], LIGHT(32), WHITE, 46)
    m.slide(1, N, 1, s1, start=480)
    m.slide(2, N, 3, pista(1, "Sala y comedor con aire acondicionado, listos para mudarte."), start=560)
    m.slide(3, N, 2, pista(2, "Cocina con estufa de gas, campana y nevera."), start=560)
    m.slide(4, N, 5, pista(3, "2 habitaciones y 2 baños."), start=560)
    m.slide(5, N, 4, pista(4, "Terraza para tus tardes."), start=520)
    m.slide(6, N, 8, pista(5, "Amueblado y con el mantenimiento incluido."), start=560)
    def s7(d):
        pill(d, CW, 560, "¿ACERTASTE?")
        ctext(d, CW, 640, "Doral Residences", play(72, True), WHITE)
        spaced(d, CW / 2, 740, "COSTA BÁVARO · PUNTA CANA", MED(24), (255, 255, 255, 220), 6)
        ctext(d, CW, 795, "US$1,175", play(128, w=600), GOLD)
        spaced(d, CW / 2, 955, "AL MES · LARGO PLAZO", MED(26), WHITE, 6)
        d.line([(CW / 2 - 50, 1012), (CW / 2 + 50, 1012)], fill=GOLD, width=2)
        lines(d, CW, 1036, ["94.75 m² · Piscina · Lobby · Coworking", "Vigilancia 24h · Acepta mascotas"], LIGHT(34), WHITE, 48)
        ctext(d, CW, 1150, "Comenta cuánto dijiste tú.", MED(36), WHITE)
        spaced(d, CW / 2, 1250, "WHATSAPP 849-247-2107", MED(26), GOLD, 5)
    m.slide(7, N, 7, s7, start=320, strength=1.0)

def save_story(im, name): im.convert("RGB").save(f"{OUT}/historia_{name}.jpg", quality=95, subsampling=0)

def stories():
    # 1 Humor
    def h1(d):
        pill(d, SW, 1060, "TODO DOMINICANO LO HA ESCUCHADO")
        ctext(d, SW, 1140, "“Mientras tú vivas", play(84, True, 600), WHITE)
        ctext(d, SW, 1240, "en esta casa…”", play(84, True, 600), WHITE)
        ctext(d, SW, 1380, "Ya tú sabes cómo termina.", LIGHT(40), WHITE)
        ctext(d, SW, 1436, "¿Y tú qué estás esperando pa’ independizarte?", LIGHT(36), GOLD)
        pill(d, SW, 1560, "RESPÓNDENOS AQUÍ ABAJO", fill=WHITE, color=GREEN)
    m.OUT = OUT; m.story("1_humor", 8, h1, focus=0.35)
    # 2 Noticia / chisme
    def h2(d):
        pill(d, SW, 1080, "LO QUE TU JEFE NO TE DIJO")
        ctext(d, SW, 1160, "El lunes 9", play(116, w=600), WHITE)
        ctext(d, SW, 1290, "no se trabaja.", play(116, True, 600), GOLD)
        lines(d, SW, 1460, ["El descanso del Día de la Constitución", "se pasó para el lunes. Fin de semana largo."], LIGHT(36), WHITE, 50)
        ctext(d, SW, 1600, "¿Qué vas a hacer con tu lunes libre?", MED(38), WHITE)
    m.story("2_feriado", 4, h2)
    # 3 Esto o aquello (pantalla dividida)
    im = Image.new("RGBA", (SW, SH), (*GREEN, 255))
    src = Image.open(f"{m.SRC}/p1.jpg").convert("RGB"); iw, ih = src.size; ch = int(iw * 940 / SW)
    top = src.crop((0, ih - ch, iw, ih)).resize((SW, 940), Image.LANCZOS).convert("RGBA")  # parte baja: la piscina
    bot = photo(4, SW, 940, 0.5).convert("RGBA")
    im.paste(top, (0, 0)); im.paste(bot, (0, 980))
    ov = Image.new("RGBA", (SW, SH)); od = ImageDraw.Draw(ov)
    od.rectangle([0, 0, SW, 330], fill=(*GREEN, 150)); od.rectangle([0, 760, SW, 940], fill=(*GREEN, 170)); od.rectangle([0, 1740, SW, SH], fill=(*GREEN, 170))
    im.alpha_composite(ov); d = ImageDraw.Draw(im); brand(d, SW, 120)
    ctext(d, SW, 200, "¿Tú eres team…?", play(70, True, 600), WHITE)
    spaced(d, 120, 820, "1", play(60, w=600), GOLD, 0); d.text((190, 822), "Piscina de noche", font=play(56, True), fill=WHITE)
    spaced(d, 120, 1780, "2", play(60, w=600), GOLD, 0); d.text((190, 1782), "Terraza al sol", font=play(56, True), fill=WHITE)
    d.rounded_rectangle([(SW - 520) / 2, 934, (SW + 520) / 2, 1026], 46, fill=WHITE)
    ctext(d, SW, 952, "Respóndenos con 1 o 2", MED(36), GREEN)
    save_story(im, "3_esto_o_aquello")
    # 4 Mito vs realidad
    def h4(d):
        pill(d, SW, 900, "MITO", fill=(120, 40, 40), color=WHITE)
        lines(d, SW, 980, ["“En Punta Cana todo", "es para turistas.”"], play(68, True, 600), WHITE, 84)
        pill(d, SW, 1200, "REALIDAD")
        lines(d, SW, 1280, ["También hay apartamentos para vivir", "todo el año: amueblados y con el", "mantenimiento incluido."], LIGHT(40), WHITE, 56)
        ctext(d, SW, 1480, "Nosotros solo hacemos eso:", MED(38), GOLD)
        ctext(d, SW, 1532, "alquiler a largo plazo.", MED(38), GOLD)
    m.story("4_mito_realidad", 3, h4, focus=0.5)
    # 5 Propietarios
    def h5(d):
        pill(d, SW, 940, "PARA PROPIETARIOS")
        lines(d, SW, 1020, ["¿Tienes un apartamento", "en Punta Cana?"], play(78, w=600), WHITE, 92)
        lines(d, SW, 1230, ["Cada mes vacío", "es un mes que no vuelve."], play(64, True), GOLD, 80)
        lines(d, SW, 1420, ["Lo alquilamos a largo plazo", "y lo administramos por ti."], LIGHT(40), WHITE, 56)
        pill(d, SW, 1580, "ESCRÍBENOS 849-247-2107", fill=WHITE, color=GREEN)
    m.story("5_propietarios", 6, h5, focus=0.6)

if __name__ == "__main__":
    carousel(); stories(); print(sorted(os.listdir(OUT)))
