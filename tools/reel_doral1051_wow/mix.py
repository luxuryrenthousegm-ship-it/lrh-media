import subprocess, json
A="/home/claude/lrh-media/audio/gen/"
tl=json.load(open("timeline.json")); TOT=tl["tot"]; P=tl["starts"][8]
off=18.622-P
cuts=[2.3,4.6,6.9,9.2,11.5,13.8,14.933]
inputs=["-ss",f"{off:.3f}","-t",f"{TOT:.3f}","-i",A+"doral_music_b.mp3","-i",A+"sfx_lock.mp3","-i",A+"sfx_impact.mp3"]+sum([["-i",A+"sfx_whoosh.mp3"] for _ in cuts],[])
fc=[f"[0:a]afade=t=in:d=0.3,afade=t=out:st={TOT-1.6:.3f}:d=1.6,volume=1.0[m]",
    "[1:a]adelay=700|700,volume=0.55[l]",
    f"[2:a]adelay={int((P-0.05)*1000)}|{int((P-0.05)*1000)},volume=0.7[i]"]
for k,c in enumerate(cuts):
    d=int((c-0.25)*1000); fc.append(f"[{3+k}:a]adelay={d}|{d},volume=0.28[w{k}]")
mixin="[m][l][i]"+"".join(f"[w{k}]" for k in range(len(cuts)))
fc.append(f"{mixin}amix=inputs={3+len(cuts)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=10[a]")
subprocess.run(["ffmpeg","-y","-loglevel","error"]+inputs+["-filter_complex",";".join(fc),"-map","[a]","-t",f"{TOT:.3f}","-ar","48000","-ac","2","mix.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","ov.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","libx264","-preset","slow","-b:v","14M","-maxrate","16M","-bufsize","28M","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-shortest","-movflags","+faststart","Reel_Doral1051_LRH_wow.mp4"],check=True)
print("ok",off)
