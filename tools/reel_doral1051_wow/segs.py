import subprocess
V="/home/claude/raw/Doral1051_video.mov"; BEAT=60/105
S=[(2.2,2.2,4),(4.4,3.0,4),(56.8,1.8,4),(15.6,2.3,4),(22.4,2.3,4),(34.0,2.4,4),(46.5,1.2,2),(47.7,1.2,2),(96.6,2.0,8)]
for i,(s,d,b) in enumerate(S):
    if i not in (2,6,7,8): continue
    out_d=b*BEAT; sp=d/out_d; pre=0.6; ss=max(0,s-pre); trf=f"seg/s{i}.trf"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(d+2*pre),"-i",V,"-vf",f"vidstabdetect=shakiness=6:accuracy=15:result={trf}","-f","null","-"],check=True)
    slow=",minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if sp<0.8 else ""
    vf=(f"vidstabtransform=input={trf}:smoothing=26:optzoom=1:interpol=bicubic,unsharp=5:5:0.35,"
        f"trim=start={s-ss}:duration={d},setpts=(PTS-STARTPTS)/{sp}{slow},fps=30,scale=1080:1920:flags=lanczos,setsar=1,trim=duration={out_d}")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(d+2*pre),"-i",V,"-an","-vf",vf,"-c:v","libx264","-preset","slow","-crf","12","-pix_fmt","yuv420p",f"seg/s{i}.mp4"],check=True)
    print(i, round(out_d,3), subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v","-show_entries","stream=nb_read_frames","-of","csv=p=0",f"seg/s{i}.mp4"],capture_output=True,text=True).stdout.strip())
