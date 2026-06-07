import edge_tts


async def generate_audio(text, output_file):
    tts = edge_tts.Communicate(text, "en-US-JennyNeural")
    await tts.save(output_file)