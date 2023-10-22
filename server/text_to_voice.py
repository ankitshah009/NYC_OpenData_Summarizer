import asyncio
from msspeech import MSSpeech


async def generate_audio(translated_text, language):
    language = language.lower() + "-" + language.upper()
    mss = MSSpeech()
    print("Geting voices...")
    voices = await mss.get_voices_list()
    print("searching Russian voice...")
    for voice in voices:
        if voice["Locale"] == language:
            await mss.set_voice(voice["Name"])

    print("*" * 10)
    filename = "audio.mp3"
    print("waiting...")
    await mss.set_rate(10)
    await mss.set_pitch(0)
    await mss.set_volume(1.0)
    await mss.synthesize(translated_text.strip(), filename)
    print("*"*10)
    print("SUCCESS! OK!")
    print("*"*10)
    print("playing...")
