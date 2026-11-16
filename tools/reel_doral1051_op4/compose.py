import subprocess, numpy as np, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
DUR=[3.6,3.0,3.0,3.0,3.0,3.0,4.6]
FI="/home/claude/fonts/fontsource-instrument-serif/files"; FM="/home/claude/fonts/fontsource-manrope/files"
ser=lambda s,it=False: ImageFont.truetype(f"{FI}/instrument-serif-latin-400-{'italic' if it else 'normal'}.woff",s)
man=lambda w,s: ImageFont.truetype(f"{FM}/manrope-latin-{w}-normal.woff",s)
VERDE=(42,48,42); CREMA=(236,232,225); PIEDRA=(176,172,166); BL=(255,255,255)
LOGO=Image.open("/home/claude/lrh-media/brand/logo_lrh_blanco.png").convert('RGBA')
s_=110/LOGO.height; LG=LOGO.resize((round(LOGO.width*s_),110),Image.LANCZOS)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def load(i):
    p=subprocess.run(["ffmpeg","-loglevel","error","-i",f"seg/s{i}.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    n=len(p)//(W*H*3); return [np.frombuffer(p[k*W*H*3:(k+1)*W*H*3],np.uint8).reshape(H,W,3) for k in range(n)]
shots=[load(i) for i in range(7)]
starts=[0];
for d in DUR: starts.append(starts[-1]+d)
N=round(starts[-1]*FPS); TOT=N/FPS; END=starts[6]
json.dump({"tot":TOT,"starts":starts},open("timeline.json","w"))
yy,xx=np.mgrid[0:H,0:W]; VIG=np.clip((((yy-H/2)/(H*0.62))**2+((xx-W/2)/(W*0.8))**2)-0.35,0,1)
def grade(a,n):
    a=a.astype(np.float32)/255; l=a.mean(2,keepdims=True); a=l+(a-l)*0.94
    a=a*np.array([1.015,1.0,0.972]); a=0.5+(a-0.5)*1.05; a=np.clip(a,0,1)**1.02
    a=a*(1-0.18*VIG)[...,None]
    g=np.random.default_rng(n).normal(0,0.010,(H//2,W//2,1)); g=np.repeat(np.repeat(g,2,0),2,1)
    return (np.clip(a+g,0,1)*255).astype(np.uint8)
def frame_at(t):
    i=max(k for k in range(7) if starts[k]<=t+1e-6); k=int((t-starts[i])*FPS); s=shots[i]; return i,s[min(k,len(s)-1)]
def spaced_w(d,txt,f,sp): return sum(d.textlength(c,font=f) for c in txt)+sp*(len(txt)-1)
def spaced(d,x,y,txt,f,fill,sp,a):
    for c in txt: d.text((x,y),c,font=f,fill=fill+(int(a),)); x+=d.textlength(c,font=f)+sp
def rise(layer,x,y,txt,f,fill,tin,dl,sp=None,dur=0.55,center=True,alpha=1.0):
    p=ease((tin-dl)/dur)
    if p<=0: return
    d=ImageDraw.Draw(layer); tw=spaced_w(d,txt,f,sp) if sp is not None else d.textlength(txt,font=f)
    asc,desc=f.getmetrics(); hh=asc+desc
    tmp=Image.new('RGBA',(int(tw)+20,hh+20)); td=ImageDraw.Draw(tmp)
    if sp is not None: spaced(td,10,10,txt,f,fill,sp,255)
    else: td.text((10,10),txt,font=f,fill=fill+(255,))
    crop=Image.new('RGBA',tmp.size); crop.paste(tmp,(0,int((1-p)*hh*0.9)))
    crop.putalpha(crop.getchannel('A').point(lambda v:int(v*min(1,p*1.6)*alpha)))
    layer.alpha_composite(crop,(int((W-tw)/2-10) if center else int(x-10),int(y-10)))
def grad(y0,y1,amax,fin=260,fout=220):
    ov=np.zeros((H,W,4),np.uint8); ov[...,:3]=VERDE; y=np.arange(H)
    k=np.clip((y-y0)/fin,0,1)*np.clip((y1-y)/fout,0,1); ov[...,3]=(amax*k)[:,None].astype(np.uint8); return Image.fromarray(ov,'RGBA')
G_OPEN=grad(560,1380,175); G_LIST=grad(820,1700,200,fin=300,fout=200); G_TOP=grad(-200,520,120,fin=1,fout=260)
ROOMS=["Sala","Cocina","Habitación","Comedor","Baño"]
ITEMS=["Mantenimiento incluido","Internet incluido","Amueblado  ·  2 hab  ·  2 baños","Piscina y seguridad 24 h","Te mudas en 36 horas"]
blurred=None
enc=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","slow","-crf","14","-pix_fmt","yuv420p","ov.mp4"],stdin=subprocess.PIPE)
XF=0.25
for n in range(N):
    t=n/FPS; i,fr=frame_at(t)
    if i==6:
        if blurred is None:
            b=Image.fromarray(grade(shots[6][0],0)).filter(ImageFilter.GaussianBlur(24)).convert('RGBA'); b.alpha_composite(Image.new('RGBA',(W,H),VERDE+(185,))); blurred=b
        tin=t-END; sharp=Image.fromarray(grade(fr,n)).convert('RGBA')
        img=Image.blend(sharp,blurred,ease(tin/0.7))
    else:
        img=Image.fromarray(grade(fr,n)).convert('RGBA')
        tin=t-starts[i]
        if i>0 and tin<XF:  # disolvencia limpia
            k=int(round((t-starts[i-1])*FPS)); prev=shots[i-1][min(k,len(shots[i-1])-1)]
            img=Image.blend(Image.fromarray(grade(prev,n)).convert('RGBA'),img,ease(tin/XF))
    L=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(L)
    if t<starts[1]:
        a=ease((t-0.15)/0.5)
        if a>0: g=G_OPEN.copy(); g.putalpha(g.getchannel('A').point(lambda v:int(v*a))); img.alpha_composite(g)
        out_a=1-ease((t-(starts[1]-0.35))/0.35)
        rise(L,0,770,"US$1,150",ser(210),BL,t,0.25,alpha=out_a)
        rise(L,0,1010,"al mes, todo incluido",ser(70,True),BL,t,0.55,alpha=out_a)
        rise(L,0,1130,"EN RENTA  ·  LARGO PLAZO",man(600,28),CREMA,t,0.85,sp=7,alpha=out_a)
        rise(L,0,1200,"DORAL RESIDENCES  ·  COSTA BÁVARO",man(500,24),PIEDRA,t,1.05,sp=6,alpha=out_a)
    elif i<6:
        r=i-1; tin=t-starts[i]
        img.alpha_composite(G_LIST); img.alpha_composite(G_TOP)
        # etiqueta editorial arriba
        rise(L,90,250,f"0{r+1}",man(600,24),CREMA,tin,0.15,sp=4,center=False)
        a=ease((tin-0.15)/0.5); d.line([(90,292),(90+int(70*a),292)],fill=CREMA+(int(220*a),),width=2)
        rise(L,90,305,ROOMS[r],ser(64),BL,tin,0.25,center=False)
        # precio fijo + lista acumulada
        rise(L,90,1010,"US$1,150 al mes",ser(76),BL,t-starts[1],0.1,center=False)
        d.line([(90,1112),(990,1112)],fill=BL+(90,),width=1)
        for j in range(r+1):
            dl=0.2 if j==r else -5; alpha=1.0 if j==r else 0.78
            y=1145+j*82
            rise(L,140,y,ITEMS[j],man(600,41),BL,tin,dl,center=False,alpha=alpha)
            pa=ease((tin-dl)/0.4)*alpha
            if pa>0: d.ellipse([92,y+19,110,y+37],outline=CREMA+(int(255*pa),),width=2); d.ellipse([98,y+25,104,y+31],fill=CREMA+(int(255*pa),))
    else:
        tin=t-END
        a=ease((tin-0.3)/0.5)
        if a>0: lg=LG.copy(); lg.putalpha(lg.getchannel('A').point(lambda v:int(v*a))); L.alpha_composite(lg,(W//2-lg.width//2,430))
        rise(L,0,600,"US$1,150 al mes",ser(120),BL,tin,0.4)
        rise(L,0,760,"EN RENTA  ·  LARGO PLAZO  ·  BÁVARO",man(600,27),CREMA,tin,0.65,sp=5)
        p=ease((tin-0.9)/0.45)
        if p>0:
            f=man(700,30); cta="ESCRÍBENOS POR DM"; tw=spaced_w(d,cta,f,6)
            d.rounded_rectangle([W/2-tw/2-56,880,W/2+tw/2+56,982],51,outline=BL+(int(255*p),),width=3); spaced(d,W/2-tw/2,911,cta,f,BL,6,255*p)
        rise(L,0,1080,"Maciel Carty",ser(76,True),BL,tin,1.2)
        rise(L,0,1180,"LUXURY RENT HOUSE",man(600,24),PIEDRA,tin,1.35,sp=8)
    img.alpha_composite(L); out=img.convert('RGB')
    if t<0.2: out=Image.blend(Image.new('RGB',(W,H)),out,ease(t/0.2))
    if t>TOT-0.4: out=Image.blend(out,Image.new('RGB',(W,H),VERDE),ease((t-(TOT-0.4))/0.4))
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); print("frames",N,"tot",TOT)
