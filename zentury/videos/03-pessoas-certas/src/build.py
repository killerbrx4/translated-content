import re, sys, pathlib
P = pathlib.Path(sys.argv[1])
A = P / "assets"

def lucide(name, cls="ic"):
    t = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", t, re.S).group(1)
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

def si(name, cls="si"):
    d = re.search(r'<path d="([^"]+)"', (A / f"icons/si-{name}.svg").read_text()).group(1)
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{d}" /></svg>'

def logo(name, cls):
    t = (A / f"zentury-{name}.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', t).group(1)
    g = re.search(r"(<g transform=.*</g>)", t, re.S).group(1)
    g = g.replace('fill="#000000"', 'fill="currentColor"')
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true">{g}</svg>'

T = (pathlib.Path(sys.argv[2])).read_text()
import json
T = T.replace("__TIMINGS__", json.dumps(json.load(open(P / "timings.json")), ensure_ascii=False))
T = re.sub(r"\{\{lucide:([a-z-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), T)
T = re.sub(r"\{\{si:([a-z-]+)(?::([a-z-]+))?\}\}", lambda m: si(m.group(1), m.group(2) or "si"), T)
T = re.sub(r"\{\{logo:([a-z]+):([a-z-]+)\}\}", lambda m: logo(m.group(1), m.group(2)), T)

TJ = json.load(open(P / "timings.json"))
TOTAL = round(TJ["total"] + 0.3, 2)
LI = {l["id"]: l for l in TJ["lines"]}
LS = round(LI["l14"]["start"] - 0.15, 3)
T = T.replace("__TOTAL__", str(TOTAL)).replace("__LOGOSTART__", str(LS)).replace("__ENDDUR__", str(round(TOTAL - LS, 3)))
T = T.replace("__CLOSESTART__", str(LI["l12"]["start"])).replace("__CLOSEDUR__", str(round(LS - LI["l12"]["start"], 3)))
def cap_html(c):
    # envolve cada palavra (com sua pontuação colada) num span, preservando <em> e os espaços originais
    return re.sub(r"(?:^|(?<=>))([^<]+)", lambda m: re.sub(r"(\S+)", r'<span class="cw">\1</span>', m.group(1)), c)
lines = TJ["lines"]; caps = []
for i, l in enumerate(lines):
    nxt = lines[i + 1]["start"] if i + 1 < len(lines) else TOTAL
    dur = round(min(nxt - 0.03, l["end"] + 0.5) - l["start"], 3)
    caps.append(f'<div class="cap clip" id="cap-{l["id"]}" data-line="{l["id"]}" data-start="{l["start"]}" data-duration="{dur}" data-track-index="9">{cap_html(l["caption"])}</div>')
T = T.replace("__CAPTIONS__", "\n        ".join(caps))
(P / "index.html").write_text(T)
print("ok", len(T.splitlines()))
