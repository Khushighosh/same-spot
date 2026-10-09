import ollama, json, io, time, sqlite3, html
from PIL import Image

# EDIT: photos in time order, with the real time each was taken
PHOTOS = [("p1.jpg", "4 PM"), ("p2.jpg", "5 PM"), ("p3.jpg", "EDIT TIME")]

def small(path, max_side=896):
    img = Image.open(path).convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()

def compare(a, b, la, lb):
        prompt = (
        f"These are two photos of the same outdoor spot. Image 1 was taken at {la}. "
        f"Image 2 was taken at {lb}. First, say whether the camera angle or foreground "
        "differs. Then compare sun brightness, sky colour, and cloud type and amount. "
        "Reply as JSON with keys: framing_differs (string), changes (list, max 4, each "
        "saying WHAT changed and WHERE), uncertain (list). Rules: describe only what is "
        "clearly visible; do not mention shadows unless you can see one; if unsure, put "
        "it in uncertain; each item under 15 words."
    )
    start = time.time()
    resp = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt, "images": [small(a), small(b)]}],
        format="json",
    )
    try:
        res = json.loads(resp["message"]["content"])
    except Exception:
        res = {"changes": [], "unchanged": [], "uncertain": ["model returned invalid JSON"]}
    return res, time.time() - start

db = sqlite3.connect("fieldnotes.db")
db.execute("""CREATE TABLE IF NOT EXISTS comparisons (
    id INTEGER PRIMARY KEY, first TEXT, second TEXT, direction TEXT,
    result TEXT, seconds REAL, created TEXT DEFAULT CURRENT_TIMESTAMP)""")

results = {}
for (a, la), (b, lb) in zip(PHOTOS, PHOTOS[1:]):
    results[(a, la, b, lb)] = {}
    for direction, (x, lx, y, ly) in [("forward", (a, la, b, lb)), ("reverse", (b, lb, a, la))]:
        print(f"{direction}: {x} -> {y} ...", flush=True)
        res, secs = compare(x, y, lx, ly)
        db.execute("INSERT INTO comparisons (first, second, direction, result, seconds) VALUES (?,?,?,?,?)",
                   (x, y, direction, json.dumps(res), secs))
        db.commit()
        results[(a, la, b, lb)][direction] = (res, secs)

def items(res, key):
    return "".join(f"<li>{html.escape(str(i))}</li>" for i in res.get(key, []))

page = ["<html><head><meta charset='utf-8'><title>Same Spot</title><style>"
        "body{font-family:sans-serif;max-width:1000px;margin:2em auto;padding:0 1em}"
        "img{max-width:48%}.cols{display:flex;gap:2em}.cols div{flex:1}"
        "</style></head><body><h1>Same Spot</h1>"]
for (a, la, b, lb), runs in results.items():
    page.append(f"<h2>{html.escape(la)} to {html.escape(lb)}</h2>")
    page.append(f"<img src='{a}'> <img src='{b}'><div class='cols'>")
    for direction in ("forward", "reverse"):
        res, secs = runs[direction]
        page.append(f"<div><h3>{direction} ({secs:.0f}s)</h3><b>Changes</b><ul>{items(res,'changes')}</ul>"
                    f"<b>Unchanged</b><ul>{items(res,'unchanged')}</ul>"
                    f"<b>Uncertain</b><ul>{items(res,'uncertain')}</ul></div>")
    page.append("</div>")
page.append("</body></html>")
open("results.html", "w", encoding="utf-8").write("\n".join(page))
print("Done. Opening results.html")