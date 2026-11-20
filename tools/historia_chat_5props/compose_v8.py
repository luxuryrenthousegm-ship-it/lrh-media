import subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
TOT=15.0; N=int(TOT*FPS)
FI="/home/claude/fonts/fontsource-instrument-serif/files"; FM="/home/claude/fonts/fontsource-manrope/files"
ser=lambda s,it=False: ImageFont.truetype(f"{FI}/instrument-serif-latin-400-{'italic' if it else 'normal'}.woff",s)
man=lambda w,s: ImageFont.truetype(f"{FM}/manrope-latin-{w}-normal.woff",s)
VERDE=(52,59,52); VERDE2=(42,48,42); CREMA=(236,232,225); PIEDRA=(156,152,147); BL=(255,255,255); INK=(28,30,28)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def eio(x): x=min(max(x,0),1); return x*x*(3-2*x)

# --- Maciel plate
m=Image.open('maciel.png').convert('RGB').crop((0,290,1080,1640))
m=m.resize((round(1080*1920/1350),1920),Image.LANCZOS)
MAC=m.crop((185,0,185+1080,1920))
MAC_BG=Image.blend(MAC.filter(ImageFilter.GaussianBlur(14)),Image.new('RGB',(W,H),(14,17,14)),0.80)
# avatar
av=Image.open('maciel.png').convert('RGB').crop((300,470,780,950)).resize((64,64),Image.LANCZOS)
mask=Image.new('L',(64,64),0); ImageDraw.Draw(mask).ellipse([0,0,63,63],fill=255)
AV=Image.new('RGBA',(64,64)); AV.paste(av,(0,0),mask)
LOGO=Image.open('/home/claude/lrh-media/brand/logo_lrh_blanco.png').convert('RGBA')
LOGO=LOGO.resize((round(LOGO.width*90/LOGO.height),90),Image.LANCZOS)

# --- cards
PROPS=[('ae/p1051_1.jpg','Doral Residences','Villas Bávaro · 2 hab · Amueblado','US$1,150','MANTENIMIENTO E INTERNET INCLUIDOS','1051'),
       ('ae/p1038_1.jpg','Doral Residences','Villas Bávaro · 2 hab · 94.75 m² · Amueblado','US$1,175','94.75 M² · AMUEBLADO','1038'),
       ('ae/p1044_2c.jpg','Vista Cana','Punta Cana · 1 hab · 110 m² · Amueblado','US$1,195','110 M² · AMUEBLADO','1044'),
       ('ae/p1041_2.jpg','Panorama Park & Garden','Vista Cana · 1 hab · Sin amueblar','US$800','1 HAB · 2 PARQUEOS','1041'),
       ('ae/p1039_0.jpg','Villa San Juan Lake','Downtown Punta Cana · 3 hab · Sin amueblar','US$2,875','VILLA · 3 HABITACIONES','1039')]
CW,PH=470,470
HD=0
def card(img,t,sub,price,tag,code):
    ch=HD+PH+170
    c=Image.new('RGBA',(CW,ch),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([0,0,CW-1,ch-1],26,fill=(250,249,247,255))
    xo=None
    if '@' in img: img,xo=img.split('@'); xo=int(xo)
    ph=Image.open(img).convert('RGB'); r=max(CW/ph.width,PH/ph.height)
    ph=ph.resize((round(ph.width*r),round(ph.height*r)),Image.LANCZOS)
    x0=(ph.width-CW)//2 if xo is None else xo; y0=(ph.height-PH)//2; ph=ph.crop((x0,y0,x0+CW,y0+PH))
    phr=ph.convert('RGBA'); g=np.zeros((PH,CW,4),np.uint8); yy=np.arange(PH); k=np.clip((yy-PH*0.62)/(PH*0.38),0,1)*0.75
    g[...,3]=(255*k)[:,None].astype(np.uint8); phr.alpha_composite(Image.fromarray(g,'RGBA'))
    dp=ImageDraw.Draw(phr); ft=man(700,17); xx=24
    for tc in tag: dp.text((xx,PH-44),tc,font=ft,fill=(255,255,255,255)); xx+=dp.textlength(tc,font=ft)+3
    c.paste(phr.convert('RGB'),(0,HD))
    d.text((24,HD+PH+16),t,font=ser(42),fill=INK+(255,))
    d.text((24,HD+PH+64),sub,font=man(500,21),fill=(95,95,90,255))
    d.text((24,HD+PH+100),price,font=ser(46),fill=VERDE+(255,))
    pw=d.textlength(price,font=ser(46)); d.text((24+pw+8,HD+PH+116),"/mes",font=man(500,21),fill=(95,95,90,255))
    cd=f"Cód. {code}"; fc=man(600,20); cw_=d.textlength(cd,font=fc)
    d.text((CW-24-cw_,HD+PH+120),cd,font=fc,fill=(110,110,106,255))
    # rounded mask
    mk=Image.new('L',c.size,0); ImageDraw.Draw(mk).rounded_rectangle([0,0,CW-1,ch-1],26,fill=255)
    c.putalpha(Image.fromarray(np.minimum(np.array(c.getchannel('A')),np.array(mk))))
    return c
CARDS=[card(*p) for p in PROPS]; CH=CARDS[0].height; GAP=30

# --- chat
CHAT=[(2.7,'c',"¿Tienen algo en Bávaro o Punta Cana?"),
      (4.0,'m',"¡Sí! Tengo varias con entrega inmediata."),
      (5.8,'c',"¿Desde cuánto?"),
      (7.0,'m',"Amueblados desde US$1,150 al mes. Entras con 1 mes de depósito + 1 mes de renta."),
      (9.2,'c',"¿Me das más detalles?"),
      (10.4,'m',"¡Claro! Escríbeme y te envío todos los detalles.")]
BF=man(500,31)
def bubble(kind,txt):
    dd=ImageDraw.Draw(Image.new('RGB',(1,1))); maxw=395 if kind=='m' else 400; lines=[]; cur=''
    for w_ in txt.split(' '):
        tst=(cur+' '+w_).strip()
        if dd.textlength(tst,font=BF)<=maxw: cur=tst
        else: lines.append(cur); cur=w_
    lines.append(cur)
    tw=max(dd.textlength(l,font=BF) for l in lines); bw=int(tw)+56; bh=28+44*len(lines)
    b=Image.new('RGBA',(bw,bh)); d=ImageDraw.Draw(b)
    fill=(255,255,255,245) if kind=='c' else VERDE+(250,)
    d.rounded_rectangle([0,0,bw-1,bh-1],30,fill=fill)
    if kind=='m': d.rounded_rectangle([0,0,bw-1,bh-1],30,outline=(200,196,190,140),width=2)
    for i,l in enumerate(lines): d.text((28,13+44*i),l,font=BF,fill=(INK if kind=='c' else BL)+(255,))
    return b
BUBS=[(t,k,bubble(k,s)) for t,k,s in CHAT]

def spaced(d,x,y,txt,f,fill,sp):
    for ch in txt: d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+sp
def sw(d,txt,f,sp): return sum(d.textlength(c,font=f) for c in txt)+sp*(len(txt)-1)

grain_rng=np.random.default_rng(3)
def grain(img,n):
    a=np.asarray(img).astype(np.float32)
    g=np.random.default_rng(n).normal(0,3.2,(H//2,W//2,1)); g=np.repeat(np.repeat(g,2,0),2,1)
    return Image.fromarray(np.clip(a+g,0,255).astype(np.uint8))

S2,S3=2.4,12.8
enc=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-preset","slow","-crf","14","-pix_fmt","yuv420p","ov8.mp4"],stdin=subprocess.PIPE)
for n in range(N):
    t=n/FPS
    if t<S2+0.6:
        # scene 1: portrait push-in
        z=1+0.05*(t/(S2+0.6)); w2,h2=int(W/z),int(H/z)
        img=MAC.crop(((W-w2)//2,(H-h2)//3,(W-w2)//2+w2,(H-h2)//3+h2)).resize((W,H),Image.LANCZOS).convert('RGBA')
        ov=np.zeros((H,W,4),np.uint8); y=np.arange(H); k=np.clip((y-820)/420,0,1)*0.88
        ov[...,3]=(255*k)[:,None].astype(np.uint8); ov[...,:3]=8; img.alpha_composite(Image.fromarray(ov,'RGBA'))
        L=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(L)
        a=ease((t-0.15)/0.5)*(1-ease((t-S2)/0.5))
        A=int(255*a)
        if A>0:
            f=man(600,22); tx="MACIEL CARTY  ·  LUXURY RENT HOUSE"; spaced(d,(W-sw(d,tx,f,6))/2,1020,tx,f,CREMA+(A,),6)
            for i,l in enumerate(["¿Buscas renta de 6 a 12 meses","en Bávaro–Punta Cana?"]):
                ff=ser(78,True); d.text(((W-d.textlength(l,font=ff))/2,1080+i*92),l,font=ff,fill=BL+(A,))
        img.alpha_composite(L)
        if t>S2:
            # crossfade into scene 2 background
            bg=MAC_BG.convert('RGBA'); img=Image.blend(img,bg,ease((t-S2)/0.6))
    if t>=S2+0.6 or (S2<=t):
        if t>=S2+0.6: img=MAC_BG.convert('RGBA')
        if t>=S2:
            L=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(L)
            a=ease((t-S2)/0.6)*(1-ease((t-S3)/0.5)); A=int(255*a)
            if A>0:
                f=man(600,20); spaced(d,60,296,"LUXURY RENT HOUSE",f,CREMA+(A,),6)
                d.text((60,350),"Listas para",font=ser(88),fill=BL+(A,)); d.text((60,438),"mudarte",font=ser(88),fill=BL+(A,))
                d.text((60,560),"Amueblados desde US$1,150",font=ser(46,True),fill=CREMA+(A,))
                d.text((60,614),"con entrega inmediata",font=ser(46,True),fill=CREMA+(A,))
                d.line([(60,694),(150,694)],fill=CREMA+(int(A*.8),),width=2)
            # cards column scrolling
            if A>0:
                v=(900+(len(CARDS)-1)*(CH+GAP)-660)/(S3-S2-0.4)
                y0=900-v*(t-S2)-260
                for i,cd in enumerate(CARDS):
                    yy=int(y0+i*(CH+GAP)+260)
                    if -CH<yy<H:
                        c2=cd.copy()
                        if A<255: c2.putalpha(c2.getchannel('A').point(lambda v:int(v*a)))
                        L.alpha_composite(c2,(W-CW-40,yy))
            # chat bubbles (left)
            vis=[b for b in BUBS if t>=b[0]]
            def stack(lst): return sum(b.height+22 for _,_,b in lst)
            off=0.0
            for j in range(len(BUBS)):
                tb=BUBS[j][0]
                if t>=tb:
                    need=max(0,730+stack(BUBS[:j+1])-22-1230); prev=max(0,730+stack(BUBS[:j])-22-1230) if j else 0
                    off=prev+(need-prev)*eio((t-tb)/0.45)
            CL=Image.new('RGBA',(W,H)); L0=L; L=CL
            y=730-off
            for (tb,k,b) in vis:
                p=ease((t-tb)/0.35)
                bb=b.copy(); bb.putalpha(bb.getchannel('A').point(lambda v:int(v*p*a)))
                bb=bb.resize((max(1,int(b.width*(0.85+0.15*p))),max(1,int(b.height*(0.85+0.15*p)))),Image.LANCZOS)
                x=60 if k=='c' else 112
                if k=='m':
                    ap=AV.resize((48,48),Image.LANCZOS); ap.putalpha(ap.getchannel('A').point(lambda v:int(v*p*a)))
                    L.alpha_composite(ap,(60,int(y+(1-p)*20+b.height-50)))
                L.alpha_composite(bb,(x,int(y+(1-p)*20)))
                y+=b.height+22
            mk=np.ones((H,W),np.float32); yy_=np.arange(H); fade=np.clip((yy_-715)/110,0,1)**1.5; mk*=fade[:,None]
            CL.putalpha(Image.fromarray((np.array(CL.getchannel('A')).astype(np.float32)*mk).astype(np.uint8)))
            L=L0; L.alpha_composite(CL)
            img.alpha_composite(L)
    if t>=S3:
        e=ease((t-S3)/0.6)
        end=Image.new('RGBA',(W,H),VERDE2+(255,)); d=ImageDraw.Draw(end)
        big=Image.new('L',(220,220),0); ImageDraw.Draw(big).ellipse([0,0,219,219],fill=255)
        avb=Image.open('maciel.png').convert('RGB').crop((260,420,820,980)).resize((220,220),Image.LANCZOS)
        end.paste(avb,((W-220)//2,330),big)
        d.ellipse([(W-220)//2-6,324,(W+220)//2+5,555],outline=CREMA+(160,),width=2)
        f=man(600,22); tx="RENTA A LARGO PLAZO  ·  BÁVARO  ·  PUNTA CANA"; spaced(d,(W-sw(d,tx,f,5))/2,620,tx,f,CREMA+(255,),5)
        for i,l in enumerate(["Escríbeme y te envío","todos los detalles."]):
            ff=ser(84,i==1); d.text(((W-d.textlength(l,font=ff))/2,680+i*96),l,font=ff,fill=BL+(255,))
        f2=man(600,22); tx2="ESCRÍBEME POR INSTAGRAM"; spaced(d,(W-sw(d,tx2,f2,6))/2,920,tx2,f2,CREMA+(255,),6)
        hh="@maciel.luxuryrh"; fh=ser(64,True); d.text(((W-d.textlength(hh,font=fh))/2,958),hh,font=fh,fill=BL+(255,))
        end.alpha_composite(LOGO,((W-LOGO.width)//2,1100))
        img=Image.blend(img,end,e)
    out=grain(img.convert('RGB'),n)
    if t<0.25: out=Image.blend(Image.new('RGB',(W,H)),out,ease(t/0.25))
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); print("ok",N)
