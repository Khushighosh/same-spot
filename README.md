\# Same Spot



A local, no-cloud tool that compares photos of the same outdoor spot taken on different evenings, using an open-weight model (Gemma 3 4B via Ollama) on a CPU-only laptop.



\## How it works

\- `run\_all.py` sends each pair of photos to Gemma 3 in both directions (forward and reversed)

\- results are saved to SQLite and rendered in `results.html`

\- a claim only counts if it survives the swap AND matches what I can see



\## Run it

1\. Install Ollama and run `ollama pull gemma3:4b`

2\. `pip install ollama pillow`

3\. Edit the `PHOTOS` list in `run\_all.py`, then `python run\_all.py`



## Findings

- Brightness and warmth: often right, but not always (it once called the 9 Sept sky more orange, which was wrong).
- Framing: after the prompt fix it notices the framing differs in every run, but understates it ("slightly different").
- Position bias: in one pair it said "more clouds in Image 1" in both directions.
- I scored 19 claims by hand: 11 correct, 5 debatable, 3 wrong.

