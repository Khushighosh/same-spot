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



\## Findings

\## Findings

\- It reliably picks up overall brightness and warmth: when I flipped the photo order, its claims flipped with it.

\- It missed that the camera framing differed (it said "skyline remains consistent" while the foreground changed completely), and \[new run: did it now report framing\_differs correctly? yes/no].

\- In my first prompt it invented shadows in silhouette scenes; after I removed shadows from the prompt, \[new run: still invented anything? what?].

\- It trusts the labels you give it: a placeholder "EDIT TIME" ended up in its output as if it were a real time.

\- About 60-65 seconds per comparison on a CPU-only laptop (Intel i7, no GPU), all local, nothing leaves the machine.

