import subprocess
import math
import os
import sys

ffmpeg = os.path.join(os.getcwd(), "tools", "ffmpeg.exe")
ffplay = os.path.join(os.getcwd(), "tools", "ffplay.exe")
ffprobe = os.path.join(os.getcwd(), "tools", "ffprobe.exe")

def get_audio_duration(file_path):
    ffprobe_cmd = [ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
    result = subprocess.check_output(ffprobe_cmd).decode('utf-8').strip()
    duration = float(result)
    return duration

def srtTime(time):
    hrs = (time - ( time % 3600))/3600
    sec_mins_hrs = (time - hrs*3600)
    mins = (sec_mins_hrs - (sec_mins_hrs % 60) )/60
    sec = sec_mins_hrs - mins*60
    ms = int(time % 1 * 1000)
    return '{}:{:02.0f}:{:02.0f},{:03.0f}'.format(int(hrs), int(mins), int(sec), int(ms))

def txt_word_count(file_path):
    total_num_of_word=0
    word_count_list=[]
    
    with open(file_path,'r',encoding="utf-8") as file:
        data = file.read()
        lines = data.split()
        total_num_of_word += len(lines)
        
    for item in lines:
        word_count_list.append(len(item))

    for elem in word_count_list:
        total_num_of_word += int(elem)
    
    return word_count_list, (total_num_of_word - len(lines)), lines

def getTimeArray(audio_time, total_num_of_word, word_count_list):
    curTime = 0
    timeArray=[]
    timeArray.append("0:00:00,000")
    for elem in word_count_list:
        time = audio_time / total_num_of_word * elem
        curTime += time
        timeArray.append(srtTime(curTime))
    return timeArray

def srtCreate(timeArray, lines):
    txt=[]
    for i in range(len(timeArray)-1):
        txt.append(str(i+1)+"\n")
        try:
            txt.append(f"{timeArray[i]} --> {timeArray[i+1]}\n")
        except:
            pass
        txt.append(lines[i]+"\n\n")
    return txt

def main(name):
    fileMp3 = os.path.join(os.getcwd(),f"{name}.mp3")
    fileTxt = os.path.join(os.getcwd(),f"{name}.txt")
        
    word_count_list, total_num_of_word, lines = txt_word_count(fileTxt)
    audio_time = get_audio_duration(fileMp3)
    timeArray = getTimeArray(audio_time, total_num_of_word, word_count_list)
    result = srtCreate(timeArray, lines)
    with open(f"{name}.srt", 'w') as f:
        for line in result:
            f.write(line)
    print(f"{name}.srt has been created")

name = input("Input name without url: ")
main(name)

