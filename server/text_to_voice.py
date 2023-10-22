import asyncio
from msspeech import MSSpeech


async def main():
	mss = MSSpeech()
	print("Geting voices...")
	voices = await mss.get_voices_list()
	print("searching Russian voice...")
	for voice in voices:
		if voice["Locale"] == "fr-FR":
			print("es voice found:", voice["FriendlyName"])
			await mss.set_voice(voice["Name"])


	print("*" * 10)
	filename = "audio.mp3"
	# with open("s.txt", encoding="UTF8") as f: text:str = f.read()
	#text = "Или написать текст здесь"
	#text = "¡Hola! ¿Cómo estás? Si necesitas ayuda con algo específico, no dudes en preguntar"
	text = "Le petit chat est très mignon. Il a des yeux verts et un pelage doux et soyeux. Il aime jouer avec des balles et des souris en peluche. Il est très affectueux et ronronne souvent. Il dort beaucoup, surtout l’après-midi. Il est très heureux quand il reçoit des caresses et des câlins."
	print("waiting...")
	await mss.set_rate(10)
	await mss.set_pitch(0)
	await mss.set_volume(1.0)
	await mss.synthesize(text.strip(), filename)
	print("*"*10)
	print("SUCCESS! OK!")
	print("*"*10)

if __name__ == "__main__":
	asyncio.run(main())
