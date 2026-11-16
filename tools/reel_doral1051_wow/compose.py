import subprocess, numpy as np, sys, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
cfg=json.load(open("cfg.json")); BEAT=cfg["beat"]; LEAD=cfg.get("lead",0.0)
SH=[4,4,4,4,4,4,2,2,8]; END_B=cfg.get("end_beats",6)
FI="/home/claude/fonts/fontsource-instrument-serif/files"; FM="/home/claude/fonts/fontsource-manrope/files"
ser=lambda s,it=False: ImageFont.truetype(f"{FI}/instrument-serif-latin-400-{'italic' if it else 'normal'}.woff",s)
man=lambda w,s: ImageFont.truetype(f"{FM}/manrope-latin-{w}-normal.woff",s)
VERDE=(42,48,42); CREMA=(236,232,225); PIEDRA=(176,172,166); BL=(255,255,255)
LOGO=Image.open("/home/claude/lrh-media/brand/logo_lrh_blanco.png").convert('RGBA')
def logo(h): s=h/LOGO.height; return LOGO.resize((round(LOGO.width*s),h),Image.LANCZOS)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def eio(x): x=min(max(x,0),1); return x*x*(3-2*x)
def load(i):
    p=subprocess.run(["ffmpeg","-loglevel","error","-i",f"seg/s{i}.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    n=len(p)//(W*H*3); return [np.frombuffer(p[k*W*H*3:(k+1)*W*H*3],np.uint8).reshape(H,W,3) for k in range(n)]
shots=[load(i) for i in range(9)]
# timeline
frames=[]; starts=[]; t=0
for i,b in enumerate(SH):
    n=round(b*BEAT*FPS); starts.append(len(frames))
    src=shots[i]
    for k in range(n): frames.append((i,src[min(k,len(src)-1)]))
END0=len(frames); last=shots[8][-1]
for k in range(round(END_B*BEAT*FPS)): frames.append((9,last))
N=len(frames); TOT=N/FPS
json.dump({"tot":TOT,"starts":[s/FPS for s in starts],"end":END0/FPS},open("timeline.json","w"))
# grade + grain
def grade(a,n):
    a=a.astype(np.float32)/255; l=a.mean(2,keepdims=True); a=l+(a-l)*0.94
    a=a*np.array([1.015,1.0,0.972]); a=0.5+(a-0.5)*1.05; a=np.clip(a,0,1)**1.02
    y,x=VIG; a=a*(1-0.18*np.clip(((x)**2+(y)**2)-0.35,0,1)[...,None])
    g=np.random.default_rng(n).normal(0,0.011,(H//2,W//2,1)); g=np.repeat(np.repeat(g,2,0),2,1)
    return (np.clip(a+g,0,1)*255).astype(np.uint8)
yy,xx=np.mgrid[0:H,0:W]; VIG=(((yy-H/2)/(H*0.62)),((xx-W/2)/(W*0.8)))
# whip transition: 8 frames around cut
WT=4
def blurx(a,k):
    if k<2: return a
    c=np.cumsum(np.pad(a.astype(np.float32),((0,0),(k,k),(0,0)),mode='edge'),1)
    return ((c[:,2*k:]-c[:,:-2*k])/(2*k))[:, :W].astype(np.uint8)
def whip(A,B,p,dir=1):
    s=eio(p); off=int(s*W)*dir; k=int(60*math.sin(math.pi*p))+1
    out=np.zeros_like(A)
    if dir>0:
        out[:, :W-off]=A[:, off:] if off<W else 0
        out[:, W-off:]=B[:, :off] if off>0 else out[:, W-off:]
    return blurx(out,k)
# text helpers
def spaced_w(d,txt,f,sp): return sum(d.textlength(c,font=f) for c in txt)+sp*(len(txt)-1)
def spaced(d,x,y,txt,f,fill,sp,a):
    for c in txt: d.text((x,y),c,font=f,fill=fill+(int(a),)); x+=d.textlength(c,font=f)+sp
def rise(layer,y,txt,f,fill,tin,dl,sp=None,dur=0.55,h=None):
    """texto que sube desde una máscara"""
    p=ease((tin-dl)/dur)
    if p<=0: return
    d=ImageDraw.Draw(layer)
    tw=spaced_w(d,txt,f,sp) if sp is not None else d.textlength(txt,font=f)
    asc,desc=f.getmetrics(); hh=asc+desc
    tmp=Image.new('RGBA',(int(tw)+20,hh+20)); td=ImageDraw.Draw(tmp)
    if sp is not None: spaced(td,10,10,txt,f,fill,sp,255)
    else: td.text((10,10),txt,font=f,fill=fill+(255,))
    dy=int((1-p)*hh*0.9)
    crop=Image.new('RGBA',tmp.size); crop.paste(tmp,(0,dy))
    if p<1: crop.putalpha(crop.getchannel('A').point(lambda v:int(v*min(1,p*1.6))))
    layer.alpha_composite(crop,(int((W-tw)/2-10),int(y-10)))
def band(a,y0=780,y1=1560):
    ov=np.zeros((H,W,4),np.uint8); ov[...,:3]=VERDE
    yy=np.arange(H); k=np.clip((yy-y0)/260,0,1)*np.clip((y1-yy)/220,0,1)
    ov[...,3]=(170*k*a)[:,None].astype(np.uint8); return Image.fromarray(ov,'RGBA')
BANDS={}
def getband(a):
    k=round(a,2)
    if k not in BANDS: BANDS[k]=band(k)
    return BANDS[k]
def env(t,a,b,fo=0.3): return 0 if t<a or t>b else min(1,ease((t-a)/0.35),ease((b-t)/fo))
st=[s/FPS for s in starts]; END=END0/FPS
LG=logo(110)
def counter(v):
    return "US$" + f"{int(v):,}"
enc=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","slow","-crf","14","-pix_fmt","yuv420p","ov.mp4"],stdin=subprocess.PIPE)
blurred=None
for n,(i,fr) in enumerate(frames):
    t=n/FPS
    a=fr
    # whip at cuts (except into price shot, which uses a flash/zoom)
    for ci in range(1,9):
        c=starts[ci]
        if ci in (7,8): continue
        if c-WT<=n<c+WT:
            A=frames[min(n,c-1)][1] if n<c else frames[c-1][1]
            B=frames[c][1] if n<c else frames[n][1]
            p=(n-(c-WT))/(2*WT); a=whip(frames[c-1][1] if n<c else frames[c-1][1], frames[c][1] if n<c else frames[n][1], p)
    if i==9:
        if blurred is None: blurred=np.asarray(Image.fromarray(grade(last,0)).filter(ImageFilter.GaussianBlur(22)))
        img=Image.fromarray(blurred).convert('RGBA'); img.alpha_composite(Image.new('RGBA',(W,H),VERDE+(190,)))
    else:
        g=grade(a,n)
        if i==8:  # precio: zoom lento + oscurecer progresivo
            tin=t-st[8]; img=Image.fromarray(g).filter(ImageFilter.GaussianBlur(7*ease(tin/0.6))).convert('RGBA')
            img.alpha_composite(Image.new('RGBA',(W,H),VERDE+(int(140*ease(tin/0.8)),)))
        else:
            img=Image.fromarray(g).convert('RGBA')
    # flash blanco al entrar al precio
    if abs(t-st[8])<0.12:
        img.alpha_composite(Image.new('RGBA',(W,H),(255,255,255,int(150*(1-abs(t-st[8])/0.12)))))
    L=Image.new('RGBA',(W,H))
    # bandas de legibilidad
    ba=max(env(t,0.25,st[1]-0.05),env(t,st[2]+0.1,st[3]-0.05),env(t,st[4]+0.1,st[5]-0.05),env(t,st[5]+0.1,st[6]-0.05),env(t,st[6]+0.05,st[8]-0.05))
    if ba>0: img.alpha_composite(getband(ba))
    def T(a0,a1): return t>=a0 and t<a1
    if T(0.2,st[1]): 
        rise(L,1120,"Tu próximo hogar",ser(118,True),BL,t,0.25)
        rise(L,1270,"COSTA BÁVARO  ·  PUNTA CANA",man(600,28),CREMA,t,0.65,sp=7)
    if T(st[2],st[3]):
        tin=t-st[2]; rise(L,1150,"2 habitaciones · 2 baños",ser(96,True),BL,tin,0.1); rise(L,1280,"AMUEBLADO  ·  73 M²  ·  PARQUEO",man(600,28),CREMA,tin,0.4,sp=6)
    if T(st[4],st[5]):
        tin=t-st[4]; rise(L,1150,"Todo incluido",ser(104,True),BL,tin,0.1); rise(L,1280,"MANTENIMIENTO  +  INTERNET",man(600,30),CREMA,tin,0.4,sp=7)
    if T(st[5],st[6]):
        tin=t-st[5]; rise(L,1150,"Para descansar de verdad",ser(92,True),BL,tin,0.1); rise(L,1280,"PISCINA  ·  SEGURIDAD 24 H",man(600,28),CREMA,tin,0.4,sp=7)
    if T(st[6],st[8]):
        tin=t-st[6]; rise(L,1150,"Te mudas en 36 horas",ser(96,True),BL,tin,0.05); rise(L,1280,"CONTRATO DE US$100",man(600,28),CREMA,tin,0.3,sp=7)
    if T(st[8],END):
        tin=t-st[8]; d=ImageDraw.Draw(L)
        p=ease(tin/0.35)
        if p>0:
            f=man(700,27); txt="EN RENTA  ·  LARGO PLAZO"; tw=spaced_w(d,txt,f,6)
            d.rounded_rectangle([W/2-tw/2-34,640,W/2+tw/2+34,710],35,fill=BL+(int(255*p),)); spaced(d,W/2-tw/2,659,txt,f,VERDE,6,255*p)
        v=1150*ease((tin-0.15)/1.6); 
        if tin>0.15:
            f=ser(250); s=counter(v); d.text(((W-d.textlength(counter(1150),font=f))/2,760),s,font=f,fill=BL+(255,))
        rise(L,1050,"AL MES  ·  TODO INCLUIDO",man(600,32),CREMA,tin,1.5,sp=9)
        rise(L,1120,"Doral Residences, Costa Bávaro",ser(58,True),BL,tin,1.8)
    if t>=END:
        tin=t-END; d=ImageDraw.Draw(L)
        a=ease(tin/0.5)
        if a>0: lg=LG.copy(); lg.putalpha(lg.getchannel('A').point(lambda v:int(v*a))); L.alpha_composite(lg,(W//2-lg.width//2,430))
        rise(L,600,"US$1,150 al mes",ser(120),BL,tin,0.1)
        rise(L,760,"EN RENTA  ·  LARGO PLAZO  ·  BÁVARO",man(600,27),CREMA,tin,0.35,sp=5)
        p=ease((tin-0.6)/0.45)
        if p>0:
            f=man(700,30); cta="ESCRÍBENOS POR DM"; tw=spaced_w(d,cta,f,6)
            d.rounded_rectangle([W/2-tw/2-56,880,W/2+tw/2+56,982],51,outline=BL+(int(255*p),),width=3); spaced(d,W/2-tw/2,911,cta,f,BL,6,255*p)
        rise(L,1080,"Maciel Carty",ser(76,True),BL,tin,0.9)
        rise(L,1180,"LUXURY RENT HOUSE",man(600,24),PIEDRA,tin,1.05,sp=8)
    img.alpha_composite(L); out=img.convert('RGB')
    if t<0.25: out=Image.blend(Image.new('RGB',(W,H)),out,ease(t/0.25))
    if t>TOT-0.4: out=Image.blend(out,Image.new('RGB',(W,H),VERDE),ease((t-(TOT-0.4))/0.4))
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); print("frames",N,"tot",TOT)
