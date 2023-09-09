import subprocess
import math
import os

ffmpeg = os.path.join(os.getcwd(), "tools", "ffmpeg.exe")
ffplay = os.path.join(os.getcwd(), "tools", "ffplay.exe")
ffprobe = os.path.join(os.getcwd(), "tools", "ffprobe.exe")

def runErrorCheck(cmd):
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print('FFmpeg output:', result.stdout)
    except subprocess.CalledProcessError as e:
        print('FFmpeg error:', e.stderr)
    #print(cmd)
        
def srt2ass(srtPath, assPath):
    cmd = [ffmpeg,
           "-i", srtPath,
           assPath]
    runErrorCheck(cmd)

def main(name):
    videoPath = os.path.join(os.getcwd(), f"{name}.mp4")
    srtPath = os.path.join(os.getcwd(), f"{name}.srt")
    assPath = os.path.join(os.getcwd(), f"{name}.ass")
    outputPath = os.path.join(os.getcwd(), f"{name}_sub.mp4")

    if not os.path.exists(assPath):
        srt2ass(srtPath, assPath)
        
    cmd = [ffmpeg,
           "-i", videoPath,
           "-vf", f"ass={name}.ass",
           outputPath]
    runErrorCheck(cmd)


name = input("Input name without file type: ")

main(name)
