import edge_tts, asyncio


def generate_audio(text, output_file):
    tts = edge_tts.Communicate(text, "en-US-JennyNeural")
    asyncio.run(tts.save(output_file))