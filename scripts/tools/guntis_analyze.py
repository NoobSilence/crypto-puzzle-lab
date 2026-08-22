import subprocess,os

VIDEO_FILE="guntis_video.webm"
TIMESTAMPS=["00:15:26","00:17:28"]
OUTPUT_DIR="guntis_frames"

os.makedirs(OUTPUT_DIR,exist_ok=True)

if not os.path.exists(VIDEO_FILE):
    print("ERROR: video file not found: " + VIDEO_FILE)
    print("Please rename the downloaded file to: " + VIDEO_FILE)
else:
    print("Video found: " + VIDEO_FILE)
    print("")
    print("Extracting frames...")
    for ts in TIMESTAMPS:
        outname=ts.replace(":","").replace(" ","")
        output=OUTPUT_DIR + "/frame_" + outname + ".png"
        cmd=["ffmpeg","-ss",ts,"-i",VIDEO_FILE,"-vframes","1","-y",output]
        result=subprocess.run(cmd,capture_output=True)
        if result.returncode==0 and os.path.exists(output):
            print("  OK " + ts + " -> " + output)
        else:
            print("  FAILED " + ts)
    print("")
    print("Frames saved in: " + os.path.abspath(OUTPUT_DIR))
    print("Now open this folder and view the frames!")