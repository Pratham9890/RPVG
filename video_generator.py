import subprocess, random


def generate_video(background_video: str, title: str):

    start = random.randint(0, 480)
    
    cmd = [
        "ffmpeg",

        "-ss", str(start),

        "-i", background_video,
        
        "-i", f"screenshots/{title}.png",
        "-i", f"audios/{title}.mp3",

        "-filter_complex",
        f"[0:v][1:v]overlay=(W-w)/2:(H-h)/8,ass=subtitles/{title}.ass[v]",

        "-map", "[v]",
        "-map", "2:a",

        "-c:v", "h264_nvenc",
        "-preset", "p5",

        "-c:a", "copy",

        "-shortest",

        "-y",

        f"output/{title}.mp4"
    ]
    subprocess.run(cmd,check=True)

