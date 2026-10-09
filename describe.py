import ollama, sys, json

resp = ollama.chat(
    model="gemma3:4b",
    messages=[{
        "role": "user",
                "content": (
            "You are logging outdoor field notes. Describe ONLY what is clearly visible. "
            "Reply as JSON with keys: summary (one plain sentence), weather_light, "
            "plants, animals, notable. Rules: never guess species; if you cannot "
            "identify something say 'unclear'; if no animals are visible say 'none visible'; "
            "keep each value under 15 words; no poetic language."
        ),
        "images": [sys.argv[1]],
    }],
    format="json",
)
note = json.loads(resp["message"]["content"])
json.dump(note, open("photo_note.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(note, indent=2, ensure_ascii=False))