import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import make_stories as m
R = [m.STORIES["s1_humor"][0], m.STORIES["s1_humor"][1]] + m.STORIES["s4_tour"] + m.STORIES["s5_precio"]
R = [dict(s) for s in R]; R[-1]["dur"] = 5.5
# render with original music, then also a silent version for Instagram audio
m.render("reel_1038", R)
src = os.path.join(m.OUT, "reel_1038.mp4"); dst = os.path.join(m.OUT, "reel_1038_silent.mp4")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,"-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest",dst],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","9","-i",src,"-frames:v","1","-q:v","2",os.path.join(m.OUT,"reel_1038_cover.jpg")],check=True)
print("done")
