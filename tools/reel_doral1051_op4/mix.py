import subprocess, json
A="/home/claude/lrh-media/audio/gen/"; tl=json.load(open("timeline.json")); TOT=tl["tot"]; P=tl["starts"][6]
off=max(0,18.622-P)
fc=[f"[0:a]afade=t=in:d=0.4,afade=t=out:st={TOT-1.6:.3f}:d=1.6[m]","[1:a]adelay=500|500,volume=0.45[l]",
    f"[m][l]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=10[a]"]
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{off:.3f}","-t",f"{TOT:.3f}","-i",A+"doral_music_b.mp3","-i",A+"sfx_lock.mp3","-filter_complex",";".join(fc),"-map","[a]","-t",f"{TOT:.3f}","-ar","48000","-ac","2","mix.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","ov.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","libx264","-preset","slow","-b:v","14M","-maxrate","16M","-bufsize","28M","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-shortest","-movflags","+faststart","Reel_Doral1051_PrecioPrimero.mp4"],check=True)
print("ok",off)
