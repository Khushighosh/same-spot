from faster_whisper import WhisperModel
import sys, json

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(sys.argv[1], vad_filter=True)
out = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]
json.dump(out, open("transcript.json", "w"), ensure_ascii=False, indent=2)
print(f"{len(out)} segments, language: {info.language}")