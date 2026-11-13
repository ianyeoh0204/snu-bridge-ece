"""Real screenshots for the poster, so that the presenter can point at the thing itself.

    .venv/bin/python tools/poster_shots.py

Writes three pictures to out/poster/shots/ (not published):
  board.png    the department's own Korean academic board, as a student finds it (one page request)
  notice.png   the same board's newest notice as this site shows it, opened
  card.png     one requirement as this site shows it, opened, with its source and Korean line
Run `python -m bridge site` first. The site's two pictures are taken from site/index.html at a phone's width, so that
the type is large enough to read on the printed poster.
"""
import functools
import http.server
import json
import pathlib
import re
import subprocess
import tempfile
import threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "poster" / "shots"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCALE = 3  # device pixels per CSS pixel: about 160 dots per inch at the printed size

# A page that shows one part of the site in a frame exactly as tall as the picture wanted, with the site's own bar hidden.
FRAME = """<!doctype html><meta charset="utf-8"><style>html, body {{ margin: 0; background: #fff; }} iframe {{ border: 0; display: block; width: {width}px; height: {height}px; }}</style>
<iframe id="f" src="index.html#{address}"></iframe>
<script>
const f = document.getElementById("f");
f.onload = () => setTimeout(() => {{
  const d = f.contentDocument, style = d.createElement("style");
  style.textContent = ".nav, #deptbar {{ display: none !important; }} * {{ scroll-behavior: auto !important; transition: none !important; }}";
  d.head.append(style);
  const part = d.getElementById("{address}");
  part.open = true;
  f.contentWindow.scrollTo(0, part.getBoundingClientRect().top + f.contentWindow.scrollY - {above});
}}, 1200);
</script>"""


def shoot(url, target, width, height):
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}", f"--force-device-scale-factor={SCALE}",
                        f"--window-size={width},{height}", "--virtual-time-budget=8000", f"--screenshot={target}", url], check=True, capture_output=True, timeout=180)
    print(target.relative_to(ROOT), target.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ece = json.loads((ROOT / "sources/ECE/config.json").read_text(encoding="utf-8"))
    notices = json.loads((ROOT / "data/ECE/notices.json").read_text(encoding="utf-8"))
    # Among the six rows the board picture shows, the notice with the most dates that print a weekday and were found
    # word for word in the Korean: its picture then shows what the date check does.
    def weekday_dates(notice):
        brief = json.loads((ROOT / "data/ECE/briefs" / f"{notice['id']}.json").read_text(encoding="utf-8"))
        return sum(1 for d in brief["dates"] if d["verified"] and re.search(r"[월화수목금토일]\s*(요일)?\s*\)", d["original_ko"]))
    newest = max(notices[:6], key=weekday_dates)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "site"))
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}/"
    try:
        for name, address, height, above in (("notice", f"notice-{newest['id']}", 782, 6), ("card", f"card-{ece['headline_cards']['masters']}", 600, 70)):
            helper = ROOT / "site" / f"_shot_{name}.html"
            helper.write_text(FRAME.format(width=600, height=height, address=address, above=above), encoding="utf-8")
            shoot(base + helper.name, OUT / f"{name}.png", 600, height)
            helper.unlink()
    finally:
        server.shutdown()
    shoot(ece["board"]["list_url"], OUT / "board.png", 1100, 1300)
