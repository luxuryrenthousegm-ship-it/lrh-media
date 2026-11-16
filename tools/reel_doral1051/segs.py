import subprocess, os
V="/home/claude/raw/Doral1051_video.mov"
SEG=[(93.3,3.87,1),(4.6,4.73,1),(10.4,2.7,1),(22.4,2.6,1),(30.4,1.6,1),(34.0,2.8,1),(15.6,2.0,1),(63.8,3.3,1),(46.5,2.4,1),(100.6,2.4,0.55)]
for i,(s,d,sp) in enumerate(SEG):
    out=f"seg/s{i}.mp4"; trf=f"seg/s{i}.trf"
    pre=0.6  # margen para el estabilizador
    ss=max(0,s-pre); 
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(d+2*pre),"-i",V,"-vf",f"vidstabdetect=shakiness=6:accuracy=15:result={trf}","-f","null","-"],check=True)
    vf=(f"vidstabtransform=input={trf}:smoothing=24:optzoom=1:interpol=bicubic,unsharp=5:5:0.4,"
        f"trim=start={s-ss}:duration={d},setpts=(PTS-STARTPTS)/{sp},fps=30,scale=1080:1920:flags=lanczos,setsar=1")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(d+2*pre),"-i",V,"-an","-vf",vf,"-c:v","libx264","-preset","slow","-crf","12","-pix_fmt","yuv420p",out],check=True)
    print(i, subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout.strip())
open("seg/list.txt","w").write("".join(f"file 's{i}.mp4'\n" for i in range(len(SEG))))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","seg/list.txt","-c","copy","base.mp4"],check=True)
