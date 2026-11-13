import asyncio, base64, hashlib, re
from pathlib import Path
VOICE_MAP={"english":"en-IN-NeerjaNeural","tamil":"ta-IN-PallaviNeural","telugu":"te-IN-ShrutiNeural","hindi":"hi-IN-SwaraNeural"}
def speech_text(text,language):
    text=str(text or '').strip()
    # Parenthetical transliterations are reading aids, not additional spoken content.
    # Parenthetical transliterations are visual reading aids; never speak them.
    text=re.sub(r'\s*\([^()]*\)','',text)
    text=re.sub(r'\bI\s*/\s*Me\b','I',text,flags=re.I)
    text=re.sub(r'\*\*|[*_#`]', '', text)
    text=re.sub(r'^(?:Irula|English|Tamil|Telugu|Hindi):\s*', '', text, flags=re.I)
    text=re.sub(r'\s+',' ',text).strip()
    return text

def generate_audio(text,language='english',output_dir=None):
    text=speech_text(text,language)
    if not text: raise ValueError('Audio text cannot be empty.')
    if language not in VOICE_MAP: raise ValueError('No configured verified voice for this language.')
    import edge_tts
    folder=Path(output_dir or Path(__file__).resolve().parents[1]/'cache'/'audio'); folder.mkdir(parents=True,exist_ok=True)
    target=folder/(hashlib.sha256((language+text).encode()).hexdigest()[:24]+'.mp3')
    if not target.exists():
        async def make(): await edge_tts.Communicate(text,VOICE_MAP[language]).save(str(target))
        try: asyncio.run(make())
        except RuntimeError:
            loop=asyncio.new_event_loop(); loop.run_until_complete(make()); loop.close()
    return target

def audio_data_uri(path):
    data=Path(path).read_bytes()
    return 'data:audio/mpeg;base64,'+base64.b64encode(data).decode('ascii')
