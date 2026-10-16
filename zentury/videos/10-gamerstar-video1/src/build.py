"""Gera index.html a partir de edl.json + src/words.json + src/template.html.
Uso: python3 -I src/build.py ."""
import json, re, sys, pathlib

P = pathlib.Path(sys.argv[1])
A = P / "assets"
E = json.load(open(P / "edl.json"))
WORDS = json.load(open(P / "src/words.json"))  # [texto, início na fonte]
KEYS = set(E["keys"])

# ---- linha do tempo de saída ----
t = 0.0; cuts = {}
for c in E["cuts"]:
    d = c["dur"] if "img" in c else round(c["src"][1] - c["src"][0], 3)
    cuts[c["id"]] = dict(c, out=round(t, 3), d=d); t += d
TOTAL = round(t, 3)

def out(i):
    """tempo de saída da palavra i (a partir do corte que a contém)"""
    for c in cuts.values():
        if "w" in c and c["w"][0] <= i <= c["w"][1]:
            return round(c["out"] + max(0.0, min(WORDS[i][1], c["src"][1] - 0.05) - c["src"][0]), 3)
    raise KeyError(i)

def hidden(cut, src_t):
    return any(cut == n[0] and n[1] <= src_t <= n[2] for n in E["nocap"])

# ---- vídeos (um <video> por corte, alternando trilhas) ----
vids = []
for i, c in enumerate(cuts.values()):
    if "img" in c:
        vids.append(f'<img id="{c["id"]}" class="shot clip" src="{c["img"]}" alt="" data-start="{c["out"]}" data-duration="{c["d"]}" data-track-index="{i % 2}" />')
    else:
        vids.append(f'<video id="{c["id"]}" class="shot clip" src="assets/footage/gamerstar.mp4" muted playsinline data-start="{c["out"]}" data-duration="{c["d"]}" data-media-start="{c["src"][0]}" data-track-index="{i % 2}"></video>')

# ---- legendas: blocos de até 3 palavras / 17 letras dentro da placa ----
caps, words = [], []
for c in cuts.values():
    if "w" not in c: continue
    ids = [i for i in range(c["w"][0], c["w"][1] + 1) if not hidden(c["id"], WORDS[i][1])]
    chunks, cur = [], []
    for i in ids:
        txt = " ".join(WORDS[j][0] for j in cur + [i])
        if cur and (len(cur) == 3 or len(txt) > 17 or WORDS[cur[-1]][0][-1] in ",.?!"):
            chunks.append(cur); cur = []
        cur.append(i)
    if cur: chunks.append(cur)
    for k, ch in enumerate(chunks):
        s = out(ch[0]) - 0.05
        e = out(chunks[k + 1][0]) - 0.05 if k + 1 < len(chunks) else c["out"] + c["d"]
        for n in E["nocap"]:  # o bloco some quando começa o trecho sem legenda (cartão de tela cheia)
            if n[0] == c["id"] and n[1] > c["src"][0]:
                e = min(e, c["out"] + n[1] - c["src"][0])
        spans = []
        for i in ch:
            k_ = WORDS[i][0] in KEYS
            spans.append(f'<span id="w{i}" class="cw{" k" if k_ else ""}">{WORDS[i][0]}</span>')
            words.append({"id": f"w{i}", "t": out(i), "k": k_})
        caps.append(f'<div class="cap clip" id="cap{len(caps)}" data-start="{round(max(0, s), 3)}" data-duration="{round(e - max(0, s), 3)}" data-track-index="9">{" ".join(spans)}</div>')

def lucide(name, cls="ic"):
    tx = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.sub(r"<!--.*?-->", "", re.search(r"<svg[^>]*>(.*)</svg>", tx, re.S).group(1), flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

# gatilhos dos grafismos: todos presos a palavras ditas (índice em src/words.json)
TRIG = {"g4070": 2, "g5060": 4, "serie50": 11, "melhor": 15, "serie40": 19, "q40": 20,
        "rtx4070": 22, "s40": 28, "rtx5060": 32, "s50": 37, "atencao": 40,
        "geracao": 43, "suficiente": 47, "comparar": 58,
        "testes": 66, "memoria": 69, "recursos": 71, "jogo": 76,
        "nova": 91, "auto": 94, "superar": 98,
        "voce": 105, "optG": 117, "optD": 121, "conta": 124}
T = {"total": TOTAL, "cuts": {k: [v["out"], v["d"], v["zoom"]] for k, v in cuts.items()}, "words": words}
T.update({k: out(i) for k, i in TRIG.items()})
T["card"] = cuts["c2"]["out"] + (8.50 - cuts["c2"]["src"][0])

tpl = (P / "src/template.html").read_text()
tpl = re.sub(r"\{\{lucide:([a-z0-9-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), tpl)
html = (tpl.replace("__T__", json.dumps(T, ensure_ascii=False))
        .replace("__TOTAL__", str(TOTAL))
        .replace("__VIDEOS__", "\n        ".join(vids))
        .replace("__CAPTIONS__", "\n      ".join(caps)))
(P / "index.html").write_text(html)
json.dump({"total": TOTAL, "cuts": [{"id": k, "out": v["out"], "d": v["d"], "src": v.get("src")} for k, v in cuts.items()], "T": {k: v for k, v in T.items() if k not in ("words", "cuts")}},
          open(P / "timeline.json", "w"), indent=1)
print("ok total", TOTAL)
