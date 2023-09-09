import subprocess
import math
import os

ffmpeg = os.path.join(os.getcwd(), "tools", "ffmpeg.exe")
ffprobe = os.path.join(os.getcwd(), "tools", "ffprobe.exe")

def runErrorCheck(cmd):
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print('FFmpeg output:', result.stdout)
    except subprocess.CalledProcessError as e:
        print('FFmpeg error:', e.stderr)
    #print(cmd)
        
def get_audio_duration(file_path):
    ffprobe_cmd = [ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
    result = subprocess.check_output(ffprobe_cmd).decode('utf-8').strip()
    duration = float(result)
    return duration

def convertTime(time):
    hrs = (time - ( time % 3600))/3600
    sec_mins_hrs = (time - hrs*3600)
    mins = (sec_mins_hrs - (sec_mins_hrs % 60) )/60
    sec = sec_mins_hrs - mins*60
    return '{}:{:02.0f}:{:02.0f}'.format(int(hrs), int(mins), int(sec))

def timeCal(time):
    if len(time.split(",")) == 3:
        hrs, mins, sec = time.split(",")
    else:
        hrs = 0
        mins, sec = time.split(",")

    return int(hrs) * 60 * 60 + int(mins) * 60 + int(sec)

def split_video(name, timeArray, duration):
    result = []
    
    result.append(0)
    for item in timeArray:
        result.append(timeCal(item))
    result.append(duration)
    inputFile = os.path.join(os.getcwd(), f"{name}.mp4")
    for i in range(len(result)-1):
        output_file = os.path.join(os.getcwd(), f"{name}_{i + 1}.mp4")

        cmd = [ffmpeg,
               '-i', inputFile,
               '-ss', convertTime(result[i]),
               '-to', convertTime(result[i+1]),
               '-c', 'copy',
               output_file
        ]
        runErrorCheck(cmd)

def main():
    timeArray = []
    name = input("Input file name without datatype; ")
    duration = get_audio_duration(os.path.join(os.getcwd(), f"{name}.mp4"))
    print(f"Duration: {convertTime(duration)}")

    word = input("Input time u want to split (HH,MM,SS) and type \'end\' when complete spliting:")
    while word != "end":
        timeArray.append(word)
        word = input("Input time u want to split (HH,MM,SS) and type \'end\' when complete spliting:")

    split_video(name, timeArray, duration)


main()
