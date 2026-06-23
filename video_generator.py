from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip


def generate_video(back_img: str, post_img: str, audio_file: str, out_file: str):

    background = VideoFileClip(back_img)
    back_height = background.h
    back_width = background.w
    # get the aspect ratio then crop the largest possible to get 9:16 aspect ratio
    aspect_ratio = back_width / back_height

    w1, w2, h1, h2 = 0, back_width, 0, back_height

    # Crop any video to 9:16 aspect ratio (shorts/reel format)
    if aspect_ratio > 9 / 16:
        new_width = int(back_height * 9 / 16)
        w1 = int((back_width - new_width) / 2)
        w2 = w1 + new_width
    else:
        new_height = int(back_width * 16 / 9)
        h1 = int((back_height - new_height) / 2)
        h2 = h1 + new_height

    cropped = background.cropped(
        x1=w1,
        x2=w2,
        y1=h1,
        y2=h2,
    )
    print("Video duration:", background.duration)

    audio = AudioFileClip(audio_file)

    # Post overlay
    post_overlay = ImageClip(post_img).with_duration(audio.duration)
    post_overlay = post_overlay.with_position(
        (((w2 - w1) - post_overlay.w) / 2, (h2 - h1) / 16), relative=False
    )
    print("Audio duration:", audio.duration)

    # Trimmed video to match audio duration
    trimed_vid = cropped.subclipped(0, audio.duration)
    trimed_vid = trimed_vid.with_audio(audio)
    trimed_vid = trimed_vid.with_fps(30)
    composite = CompositeVideoClip([trimed_vid, post_overlay])
    composite.write_videofile(out_file, codec="h264_nvenc", preset="fast", threads=4)

    background.close()
    audio.close()
    post_overlay.close()
    trimed_vid.close()
    composite.close()
