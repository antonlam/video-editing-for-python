@echo off
setlocal enableDelayedExpansion

if "%~1"=="" (
    echo Please drop a video file onto this script.
    pause
    exit /b
)

set "video_path=%~1"'
set "extension=%video_path:~-4%"
set "extension=%extension:.=%"

set "current_dir=%CD%"
set "ffmpeg_path=%current_dir%\tools\ffmpeg.exe"

set "watermark_path=%current_dir%\tools\watermark2.png"


for %%A in ("%video_path%") do (
    set "file_name=%%~nA"
    set "file_extension=%%~xA"
)
set "output_path=%current_dir%\%file_name%_watermark.mp4"

if /i "%extension%"=="mp4" (
    "%ffmpeg_path%" -i "%video_path%" -i %watermark_path% -filter_complex overlay=10:10 -codec:a copy %output_path%"
) else (
    if /i "%extension%"=="avi" (
       "%ffmpeg_path%" -i "%video_path%" -i %watermark_path% -filter_complex overlay=10:10 -codec:a copy %output_path%"
    ) else (
        echo This is not video type
	pause
	exit /b
    )
)

pause