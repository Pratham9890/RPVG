import os

import stable_whisper


def generate_subtitles(audio_file, title):
    model = stable_whisper.load_model("small")
    result = model.transcribe(audio_file)
    # make dir subtitles if not exist
    os.makedirs("subtitles", exist_ok=True)

    result.to_ass(f"subtitles/{title}.ass")  # type: ignore
    ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 810
PlayResY: 1440
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Proxima Nova Extrabold,50,&H00ff00,&Hffffff,&H0,&H0,0,0,0,0,100,100,0,0,1,1,0,2,10,10,180,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    text = ""
    with open(f"subtitles/{title}.ass", "r") as f:
        text = f.read()
        start = text.find("Dialogue:")
    with open(f"subtitles/{title}.ass", "w") as f:
        f.write(ASS_HEADER + text[start:])

