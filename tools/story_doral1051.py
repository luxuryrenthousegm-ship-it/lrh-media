import sys, subprocess, wave, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.path.insert(0,"/home/claude/scripts")
from music_lounge import music
SRC="/home/claude/dl/lrh-media/src/1051"; BR="/home/claude/lrh-media/brand"; OUT="/home/claude/vid"
FI="/home/claude/fonts/fontsource-instrument-serif/files"; FM="/home/claude/fonts/fontsource-manrope/files"
ser=lambda s,it=False: ImageFont.truetype(f"{FI}/instrument-serif-latin-400-{'italic' if it else 'normal'}.woff",s)
man=lambda w,s: ImageFont.truetype(f"{FM}/manrope-latin-{w}-normal.woff",s)
W,H,FPS=1080,1920,30
VERDE=(42,48,42); CREMA=(236,232,225); PIEDRA=(164,160,156); BL=(255,255,255)
def grade(im):
    im=ImageEnhance.Color(im).enhance(0.9)
    a=np.asarray(im).astype(np.float32)/255
    a=a*np.array([1.02,1.0,0.965])           # leve calidez
    a=0.5+(a-0.5)*0.96; a=a**1.04             # contraste suave, sin look HDR
    a=np.clip(a,0,1); return Image.fromarray((a*255).astype(np.uint8))
def base(p,fx=0.5):
    im=grade(Image.open(f"{SRC}/{p}.jpg").convert('RGB'))
    s=max(W*1.12/im.width,H*1.12/im.height)*1.6
    return im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
def kb(b,t,z0=1.0,z1=1.07,px=0.0,fx=0.5):
    z=z0+(z1-z0)*t; cw=b.width/1.12/z*(W*1.12/b.width*b.width/W) if False else None
    # ventana visible
    sc=b.height/(H*1.12)            # px base por px salida a z=1 con margen
    vw,vh=W*sc*1.12/ (1.12*z), H*sc*1.12/(1.12*z)
    cx=b.width*fx+px*b.width*0.03*(t-0.5); cy=b.height/2
    cx=min(max(cx,vw/2),b.width-vw/2)
    return b.transform((W,H),Image.EXTENT,(cx-vw/2,cy-vh/2,cx+vw/2,cy+vh/2),Image.BICUBIC)
VIG=None
def vignette():
    y,x=np.mgrid[0:H,0:W]; r=np.sqrt(((x-W/2)/(W*0.75))**2+((y-H/2)/(H*0.7))**2)
    return np.clip(1-0.22*np.clip(r-0.55,0,1)/0.45,0,1)[...,None]
def finish(im,n):
    global VIG
    if VIG is None: VIG=vignette()
    a=np.asarray(im).astype(np.float32)*VIG
    g=np.random.default_rng(n).normal(0,3.2,(H//2,W//2,1)); g=np.repeat(np.repeat(g,2,0),2,1)
    return Image.fromarray(np.clip(a+g,0,255).astype(np.uint8))
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def spaced(d,y,txt,f,fill,sp,a=255):
    ws=[d.textlength(c,font=f) for c in txt]; x=(W-sum(ws)-sp*(len(txt)-1))/2
    for c,w in zip(txt,ws): d.text((x,y),c,font=f,fill=fill+(a,)); x+=w+sp
def ctext(d,y,txt,f,fill,a=255): d.text(((W-d.textlength(txt,font=f))/2,y),txt,font=f,fill=fill+(a,))
def grad(y0,y1,a0,a1,col=VERDE):
    ov=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(ov)
    for y in range(y0,y1): d.line([(0,y),(W,y)],fill=col+(int(a0+(a1-a0)*(y-y0)/(y1-y0)),))
    return ov
LOGO=Image.open(f"{BR}/logo_lrh_blanco.png").convert('RGBA')
def logo(h): s=h/LOGO.height; return LOGO.resize((round(LOGO.width*s),h),Image.LANCZOS)
BEAT=0.6
SEG=[("p7",6,"hook",0.5),("p1",4,"SALA AMUEBLADA",0.4),("p2",4,"COMEDOR",0.55),("p3",4,"2 HABITACIONES",0.5),("p5",4,"2 BAÑOS",0.45),("p7",8,"end",0.45)]
def render(ver):
    bases={}
    for p,_,_,fx in SEG: bases.setdefault(p,base(p))
    endbg=None
    TOT=sum(b for _,b,_,_ in SEG)*BEAT; N=int(TOT*FPS)
    top=grad(0,420,150,0); low=grad(1150,1920,0,215); lowend=grad(0,1920,175,175)
    enc=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-c:v","libx264","-preset","slow","-crf","16","-pix_fmt","yuv420p",f"{OUT}/v_{ver}.mp4"],stdin=subprocess.PIPE)
    lg=logo(66); lgb=logo(96)
    for n in range(N):
        t=n/FPS; acc=0
        for i,(p,b,lab,fx) in enumerate(SEG):
            d0=acc*BEAT; d1=(acc+b)*BEAT
            if t<d1 or i==len(SEG)-1: break
            acc+=b
        lt=(t-d0)/(d1-d0)
        if lab=="end":
            if endbg is None: endbg=kb(bases["p7"],0.0,1.07,1.07,fx=0.45).filter(ImageFilter.GaussianBlur(14))
            fr=endbg.copy().convert('RGBA'); fr.alpha_composite(lowend)
        else:
            fr=kb(bases[p],lt,1.0,1.07,px=(1 if i%2 else -1),fx=fx).convert('RGBA'); fr.alpha_composite(top); fr.alpha_composite(low)
        # corte con micro-fundido de 0.2 s
        d=ImageDraw.Draw(fr); tin=t-d0
        if ver=="lrh": fr.alpha_composite(lg,(W//2-lg.width//2,270))
        if lab=="hook":
            a=int(255*ease(tin/0.5)); dy=int(30*(1-ease(tin/0.5)))
            ctext(d,1180+dy,"¿Cuánto crees",ser(104,True),BL,a); ctext(d,1300+dy,"que cuesta vivir aquí?",ser(104,True),BL,a)
            a2=int(255*ease((tin-1.0)/0.5)); spaced(d,1460,"DORAL RESIDENCES  ·  COSTA BÁVARO",man(500,24),CREMA,5,a2)
        elif lab=="end":
            def L(y,txt,f,col,delay,sp=None):
                a=int(255*ease((tin-delay)/0.45)); dy=int(24*(1-ease((tin-delay)/0.45)))
                if a<=0: return
                (spaced(d,y+dy,txt,f,col,sp,a) if sp else ctext(d,y+dy,txt,f,col,a))
            if ver=="lrh": L(400,"","",BL,0) ; fr.alpha_composite(lgb,(W//2-lgb.width//2,330))
            L(520,"EN RENTA  ·  LARGO PLAZO",man(600,28),CREMA,0.0,6)
            L(640,"US$1,150",ser(250),BL,0.15)
            L(930,"AL MES  ·  TODO INCLUIDO",man(500,30),CREMA,0.45,8)
            d.line([(W/2-70,1010),(W/2+70,1010)],fill=PIEDRA+(int(255*ease((tin-0.6)/0.4)),),width=2)
            L(1050,"Mantenimiento e internet incluidos",ser(54,True),BL,0.7)
            L(1140,"2 HAB  ·  2 BAÑOS  ·  AMUEBLADO  ·  73 M²",man(500,25),CREMA,0.9,3)
            L(1190,"Doral Residences  ·  Costa Bávaro",man(500,25),PIEDRA,1.0,2)
            cta="ESCRÍBEME POR DM" if ver=="mac" else "ESCRÍBENOS AL 849-247-2107"
            a=int(255*ease((tin-1.4)/0.45))
            if a>0:
                f=man(600,27); tw=sum(d.textlength(c,font=f) for c in cta)+5*(len(cta)-1)
                d.rounded_rectangle([W/2-tw/2-46,1300,W/2+tw/2+46,1392],46,outline=BL+(a,),width=2); spaced(d,1329,cta,f,BL,5,a)
            if ver=="mac": L(1560,"MACIEL CARTY  ·  LUXURY RENT HOUSE",man(600,20),PIEDRA,1.6,5)
        else:
            a=int(255*ease((tin-0.25)/0.45)); spaced(d,1440,lab,man(600,30),BL,9,a)
            if ver=="mac" and False: pass
        img=fr.convert('RGB')
        if tin<0.18 and n>0: img=Image.blend(prev,img,tin/0.18)
        if t>TOT-0.5: img=Image.blend(img,Image.new('RGB',(W,H),VERDE),ease((t-(TOT-0.5))/0.5)*0.0)
        img=finish(img,n); prev=img
        enc.stdin.write(img.tobytes())
    enc.stdin.close(); enc.wait(); return TOT
def audio(TOT):
    music(f"{OUT}/m.wav",TOT+0.5,bpm=100)
    SR=44100; w=wave.open(f"{OUT}/m.wav"); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32)/32767
    tr=sum(b for _,b,_,_ in SEG[:-1])*BEAT; i=int(tr*SR)
    # boom suave en la revelación del precio
    L=int(1.4*SR); tt=np.arange(L)/SR; boom=np.sin(2*np.pi*(42+30*np.exp(-tt*6))*tt)*np.exp(-tt*3.2)*0.45
    e=min(L,len(a)-i); a[i:i+e]+=boom[:e,None]
    # pequeño silencio antes de la revelación
    g=int(0.25*SR); a[i-g:i]*=np.linspace(1,0.15,g)[:,None]
    a=np.tanh(a*1.1)*0.9
    w2=wave.open(f"{OUT}/m2.wav","wb"); w2.setnchannels(2); w2.setsampwidth(2); w2.setframerate(SR); w2.writeframes((a*32767).astype(np.int16).tobytes()); w2.close()
for ver in sys.argv[1:]:
    TOT=render(ver); audio(TOT)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{OUT}/v_{ver}.mp4","-i",f"{OUT}/m2.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",f"{OUT}/Historia_Doral1051_{ver}.mp4"],check=True)
    print(ver,TOT)
