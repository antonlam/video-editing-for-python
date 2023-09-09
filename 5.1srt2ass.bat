@echo off
setlocal enableDelayedExpansion

if "%~1"=="" (
    echo Please drop a video file onto this script.
    pause
    exit /b
)

set "video_path=%~1"
set "extension=%video_path:~-4%"
set "extension=%extension:.=%"

set "current_dir=%CD%"
set "ffmpeg_path=%current_dir%\tools\ffmpeg.exe"

echo %ffmpeg_path%
if not exist "%ffmpeg_path%" (
    echo Input file not found.
    pause
    exit /b
)

for %%A in ("%video_path%") do (
    set "file_name=%%~nA"
    set "file_extension=%%~xA"
)
set "output_file=%current_dir%\%file_name%.ass"

if /i "%extension%"=="srt" (
    "%ffmpeg_path%" -i "%video_path%" "%output_file%"
) else (
        echo This is not srt type
	pause
	exit /b
)

pause