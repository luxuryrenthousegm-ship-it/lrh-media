import subprocess
from concurrent.futures import ThreadPoolExecutor
V="/home/claude/raw/Doral1051_video.mov"
# (inicio fuente, duración fuente, duración salida)
S=[(2.2,2.2,3.6),(60.0,2.0,3.0),(23.6,2.0,3.0),(35.2,2.0,3.0),(96.6,2.0,3.0),(47.4,1.8,3.0),(15.0,2.0,4.6)]
def run(i):
    s,d,od=S[i]; sp=d/od; pre=0.6; ss=max(0,s-pre); trf=f"seg/s{i}.trf"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(d+2*pre),"-i",V,"-vf",f"vidstabdetect=shakiness=6:accuracy=15:result={trf}","-f","null","-"],check=True)
    slow=",minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if sp<0.9 else ""
    vf=(f"vidstabtransform=input={trf}:smoothing=30:optzoom=1:interpol=bicubic,unsharp=5:5:0.35,"
        f"trim=start={s-ss}:duration={d},setpts=(PTS-STARTPTS)/{sp}{slow},fps=30,scale=1080:1920:flags=lanczos,setsar=1,trim=duration={od}")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(d+2*pre),"-i",V,"-an","-vf",vf,"-c:v","libx264","-preset","slow","-crf","12","-pix_fmt","yuv420p",f"seg/s{i}.mp4"],check=True)
    return i
with ThreadPoolExecutor(4) as ex: print(list(ex.map(run,range(len(S)))))
