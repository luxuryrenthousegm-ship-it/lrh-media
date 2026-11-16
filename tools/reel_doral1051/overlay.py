import subprocess, numpy as np, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0,"/home/claude/scripts"); from music_lounge import music
W,H,FPS=1080,1920,30
FI="/home/claude/fonts/fontsource-instrument-serif/files"; FM="/home/claude/fonts/fontsource-manrope/files"
ser=lambda s,it=False: ImageFont.truetype(f"{FI}/instrument-serif-latin-400-{'italic' if it else 'normal'}.woff",s)
man=lambda w,s: ImageFont.truetype(f"{FM}/manrope-latin-{w}-normal.woff",s)
VERDE=(42,48,42); CREMA=(236,232,225); PIEDRA=(170,166,160); BL=(255,255,255)
LOGO=Image.open("/home/claude/lrh-media/brand/logo_lrh_blanco.png").convert('RGBA')
def logo(h): s=h/LOGO.height; return LOGO.resize((round(LOGO.width*s),h),Image.LANCZOS)
LG=logo(100)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def env(t,a,b,fi=0.4,fo=0.35):
    if t<a or t>b: return 0
    return min(ease((t-a)/fi), ease((b-t)/fo))
def spaced(d,y,txt,f,fill,sp,a):
    ws=[d.textlength(c,font=f) for c in txt]; x=(W-sum(ws)-sp*(len(txt)-1))/2
    for c,w in zip(txt,ws): d.text((x,y),c,font=f,fill=fill+(int(a),)); x+=w+sp
def ctext(d,y,txt,f,fill,a): d.text(((W-d.textlength(txt,font=f))/2,y),txt,font=f,fill=fill+(int(a),))
def band(a):
    ov=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(ov)
    for y in range(820,1700):
        k=min(1,(y-820)/300)*(1 if y<1500 else max(0,1-(y-1500)/200)); d.line([(0,y),(W,y)],fill=VERDE+(int(165*k*a),))
    return ov
BANDS={}
def grade(img,n):
    a=np.asarray(img).astype(np.float32)/255
    l=a.mean(2,keepdims=True); a=l+(a-l)*0.93          # saturación suave
    a=a*np.array([1.015,1.0,0.975]); a=0.5+(a-0.5)*1.04
    a=np.clip(a,0,1)**1.02
    g=np.random.default_rng(n).normal(0,0.010,(H//2,W//2,1)); g=np.repeat(np.repeat(g,2,0),2,1)
    return Image.fromarray((np.clip(a+g,0,1)*255).astype(np.uint8))
END=26.03; TOT=30.4
dec=subprocess.Popen(["ffmpeg","-loglevel","error","-i","base.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","slow","-crf","14","-pix_fmt","yuv420p","ov.mp4"],stdin=subprocess.PIPE)
n=0; endbg=None
while True:
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    t=n/FPS; fr=grade(Image.frombytes("RGB",(W,H),buf),n).convert('RGBA')
    if t>=END:
        k=ease((t-END)/0.5)
        blur=fr.filter(ImageFilter.GaussianBlur(18*k)); fr=Image.blend(fr,blur,1.0)
        fr.alpha_composite(Image.new('RGBA',(W,H),VERDE+(int(185*k),)))
    else:
        ba=max(env(t,0.4,3.75),env(t,4.2,8.45),env(t,18.35,26.03,0.35,0.01))
        if ba>0:
            key=round(ba,2)
            if key not in BANDS: BANDS[key]=band(key)
            fr.alpha_composite(BANDS[key])
    d=ImageDraw.Draw(fr)
    a=255*env(t,0.5,3.7); 
    if a: ctext(d,1170,"Doral Residences",ser(100,True),BL,a); spaced(d,1305,"COSTA BÁVARO  ·  PUNTA CANA",man(500,26),CREMA,6,a)
    a=255*env(t,4.3,8.4)
    if a: spaced(d,1300,"2 HABITACIONES  ·  2 BAÑOS  ·  AMUEBLADO",man(600,27),BL,4,a)
    a=255*env(t,18.4,23.5)
    if a:
        f=man(600,25); txt="EN RENTA  ·  LARGO PLAZO"; tw=sum(d.textlength(c,font=f) for c in txt)+5*(len(txt)-1)
        d.rounded_rectangle([W/2-tw/2-30,1000,W/2+tw/2+30,1064],32,fill=BL+(int(a),)); spaced(d,1018,txt,f,VERDE,5,a)
        ctext(d,1085,"US$1,150",ser(200),BL,a); spaced(d,1305,"AL MES",man(500,28),CREMA,10,a)
        spaced(d,1355,"MANTENIMIENTO E INTERNET INCLUIDOS",man(500,24),CREMA,4,a)
    a=255*env(t,23.75,26.0,0.35,0.2)
    if a: ctext(d,1140,"Te mudas en 36 horas",ser(84,True),BL,a); spaced(d,1260,"CONTRATO DE US$100  ·  SOLO LARGO PLAZO",man(500,24),CREMA,4,a)
    if t>=END:
        tin=t-END
        def L(y,txt,f,col,dl,sp=None):
            a=255*ease((tin-dl)/0.45)
            if a<=0: return
            dy=int(22*(1-ease((tin-dl)/0.45)))
            (spaced(d,y+dy,txt,f,col,sp,a) if sp else ctext(d,y+dy,txt,f,col,a))
        a=ease((tin-0.1)/0.5)
        if a>0: lg=LG.copy(); lg.putalpha(lg.getchannel('A').point(lambda v:int(v*a))); fr.alpha_composite(lg,(W//2-lg.width//2,330))
        L(500,"EN RENTA  ·  LARGO PLAZO",man(600,28),CREMA,0.2,6)
        L(600,"US$1,150",ser(240),BL,0.35)
        L(880,"AL MES  ·  TODO INCLUIDO",man(500,30),CREMA,0.6,8)
        L(950,"Mantenimiento e internet incluidos",ser(54,True),BL,0.8)
        L(1045,"2 HAB  ·  2 BAÑOS  ·  AMUEBLADO  ·  73 M²",man(500,25),CREMA,1.0,3)
        L(1095,"Doral Residences  ·  Costa Bávaro",man(500,25),PIEDRA,1.1,2)
        a=255*ease((tin-1.4)/0.45)
        if a>0:
            f=man(600,28); cta="ESCRÍBENOS POR DM"; tw=sum(d.textlength(c,font=f) for c in cta)+5*(len(cta)-1)
            d.rounded_rectangle([W/2-tw/2-50,1200,W/2+tw/2+50,1296],48,outline=BL+(int(a),),width=2); spaced(d,1230,cta,f,BL,5,a)
    img=fr.convert('RGB')
    if t<0.35: img=Image.blend(Image.new('RGB',(W,H)),img,ease(t/0.35))
    enc.stdin.write(img.tobytes()); n+=1
enc.stdin.close(); enc.wait()
# ---- audio
music("mus.wav",TOT+0.5,bpm=96)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/lrh-media/audio/doral1051_vo_es.mp3","-af","atempo=1.06,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,adelay=250|250,apad","-t",str(TOT),"-ar","44100","-ac","2","vo.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","vo.wav","-i","mus.wav","-filter_complex",
 f"[1:a]volume=0.30,afade=t=out:st={TOT-1.5}:d=1.5[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[md][0:a]amix=inputs=2:normalize=0:weights=1 1.6,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
 "-map","[a]","-t",str(TOT),"-ar","48000","mix.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","ov.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","libx264","-preset","slow","-b:v","12M","-maxrate","14M","-bufsize","24M","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","Reel_Doral1051_ES.mp4"],check=True)
print("ok")
