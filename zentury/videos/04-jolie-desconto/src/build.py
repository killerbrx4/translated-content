"""Gera index.html a partir de edl.json + src/template.html.
Uso: python3 -I src/build.py <pasta-do-projeto>"""
import json, math, re, sys, pathlib

P = pathlib.Path(sys.argv[1])
A = P / "assets"
E = json.load(open(P / "edl.json"))

# ---- linha do tempo de saída ----
t = 0.0; cuts = {}
for c in E["cuts"]:
    d = c["dur"] if "img" in c else round(c["src"][1] - c["src"][0], 3)
    cuts[c["id"]] = dict(c, out=round(t, 3), d=d); t += d
TOTAL = round(t, 3)

def out(src_t, cut):
    c = cuts[cut]; return round(c["out"] + (src_t - c["src"][0]), 3)

# ---- vídeos (um <video> por corte, alternando trilhas) ----
vids = []
for i, c in enumerate(cuts.values()):
    if "img" in c:
        vids.append(f'<img id="{c["id"]}" class="shot clip" src="{c["img"]}" alt="" data-start="{c["out"]}" data-duration="{c["d"]}" data-track-index="{i % 2}" />')
    else:
        vids.append(f'<video id="{c["id"]}" class="shot clip" src="assets/footage/jolie.mp4" muted playsinline data-start="{c["out"]}" data-duration="{c["d"]}" data-media-start="{c["src"][0]}" data-track-index="{i % 2}"></video>')

# ---- legendas: uma frase por clip, palavras com tempo próprio ----
caps, words = [], []
for i, ph in enumerate(E["phrases"]):
    s = out(ph["words"][0][1], ph["cut"]) - 0.06
    e = min(out(ph["end"], ph["cut"]), cuts[ph["cut"]]["out"] + cuts[ph["cut"]]["d"])
    spans = []
    for j, w in enumerate(ph["words"]):
        wid = f"w{i}_{j}"; cls = "cw k" if len(w) > 2 else "cw"
        spans.append(f'<span id="{wid}" class="{cls}">{w[0]}</span>')
        words.append({"id": wid, "t": out(w[1], ph["cut"]), "k": len(w) > 2})
    caps.append(f'<div class="cap clip" id="cap{i}" style="top:{ph["y"]}px" data-start="{round(max(0, s), 3)}" data-duration="{round(e - max(0, s), 3)}" data-track-index="9">{" ".join(spans)}</div>')

# ---- selo 10% (borda ondulada como o selo do logo, desenhada aqui, não é o logo) ----
def scallop(r, amp, n, cx=260, cy=260):
    pts = []
    for k in range(361):
        a = math.radians(k); rr = r + amp * math.cos(n * a)
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"

def lucide(name, cls="ic"):
    tx = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.sub(r"<!--.*?-->", "", re.search(r"<svg[^>]*>(.*)</svg>", tx, re.S).group(1), flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

W = {w["id"]: w["t"] for w in words}
def wt(phrase, word):  # tempo de saída da palavra j da frase i
    return W[f"w{phrase}_{word}"]

T = {
    "total": TOTAL, "cuts": {k: [v["out"], v["d"], v["zoom"]] for k, v in cuts.items()}, "words": words,
    # gatilhos dos grafismos (todos presos a palavras ditas)
    "sul": wt(0, 4), "norte": wt(0, 8), "praVoce": wt(1, 4),
    "dez": wt(2, 4), "aprov": wt(3, 2),
    "sorv": wt(4, 1), "acai": wt(4, 3), "cafe": wt(5, 4),
    "sul2": wt(6, 3), "norte2": wt(7, 3),
    "parar": wt(8, 5), "vontade": wt(9, 3),
}
tpl = (P / "src/template.html").read_text()
tpl = re.sub(r"\{\{lucide:([a-z-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), tpl)
html = (tpl.replace("__T__", json.dumps(T, ensure_ascii=False))
        .replace("__TOTAL__", str(TOTAL))
        .replace("__VIDEOS__", "\n        ".join(vids))
        .replace("__CAPTIONS__", "\n      ".join(caps))
        .replace("__SEAL_OUT__", scallop(236, 14, 18))
        .replace("__SEAL_IN__", scallop(196, 0, 1)))
(P / "index.html").write_text(html)
json.dump({"total": TOTAL, "cuts": [{"id": k, "out": v["out"], "d": v["d"], "src": v.get("src")} for k, v in cuts.items()]},
          open(P / "timeline.json", "w"), indent=1)
print("ok total", TOTAL)
