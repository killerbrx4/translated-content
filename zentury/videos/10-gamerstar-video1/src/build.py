"""Gera index.html a partir de edl.json + src/words.json + um template.
Uso: python3 -I src/build.py . [src/template.html]   (V4 "profissional": src/template-v4.html)"""
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

# ---- legenda queimada do original (OCR, já espelhada para o vídeo virado): src/burned.json ----
BUR = json.load(open(P / "src/burned.json"))
JUNK = re.compile(r"AJI|ITAM|MROF|AMRO|CEEO|EEOB|ELOB|BCE|OBC")  # INFORMÁTICA da camisa e GEFORCE RTX das caixas, lidos ao contrário
def burned(a, b):
    """caixas da legenda antiga entre os tempos de fonte a e b"""
    bx = []
    for f in range(max(0, int(a * BUR["fps"])), min(len(BUR["frames"]), int(b * BUR["fps"]) + 1)):
        for x0, x1, y0, y1, txt in BUR["frames"][f]:
            if JUNK.search(txt) or abs((x0 + x1) / 2 - 540) > 260 or y1 > 1760 or y0 < 1250: continue
            bx.append((x0, x1, y0, y1))
    return bx
OY = 0.83 * 1920  # origem do zoom da câmera (#cam)
def zoomed(b, z):
    return (540 + (b[0] - 540) * z, 540 + (b[1] - 540) * z, OY + (b[2] - OY) * z, OY + (b[3] - OY) * z)

# ---- legendas: blocos de até 3 palavras / 15 letras numa etiqueta compacta que cobre a legenda antiga daquele trecho ----
caps, words = [], []
for c in cuts.values():
    if "w" not in c or not E.get("captions", True): continue  # V3: usa a legenda queimada do original
    ids = [i for i in range(c["w"][0], c["w"][1] + 1) if not hidden(c["id"], WORDS[i][1])]
    chunks, cur = [], []
    for i in ids:
        txt = " ".join(WORDS[j][0] for j in cur + [i])
        if cur and (len(cur) == 3 or len(txt) > 15 or WORDS[cur[-1]][0][-1] in ",.?!"):
            chunks.append(cur); cur = []
        cur.append(i)
    if cur: chunks.append(cur)
    for k, ch in enumerate(chunks):
        s = c["out"] if k == 0 else out(ch[0]) - 0.05  # o 1º bloco já cobre desde o início do corte
        e = out(chunks[k + 1][0]) - 0.05 if k + 1 < len(chunks) else c["out"] + c["d"]
        for n in E["nocap"]:  # o bloco some quando começa o trecho sem legenda (cartão de tela cheia)
            if n[0] == c["id"] and n[1] > c["src"][0]:
                e = min(e, c["out"] + n[1] - c["src"][0])
        s = round(max(0, s), 3); e = round(e, 3)
        a, b = c["src"][0] + s - c["out"], c["src"][0] + e - c["out"]
        z0, z1 = c["zoom"]; zs = [z0 + (z1 - z0) * (t - c["out"]) / c["d"] for t in (s, e)]
        bx = [zoomed(q, z) for q in burned(a - 0.1, b + 0.1) for z in zs]
        # a etiqueta é uma peça só: centrada na legenda antiga e no mínimo do tamanho dela
        st = "left:540px;top:1572px"
        if bx:
            X0, X1 = min(q[0] for q in bx) - 22, max(q[1] for q in bx) + 22
            Y0, Y1 = min(q[2] for q in bx) - 16, max(q[3] for q in bx) + 16
            st = f"left:{round((X0 + X1) / 2)}px;top:{round((Y0 + Y1) / 2)}px;min-width:{round(X1 - X0)}px;min-height:{round(Y1 - Y0)}px"
        spans = []
        for i in ch:
            k_ = WORDS[i][0] in KEYS
            spans.append(f'<span id="w{i}" class="cw{" k" if k_ else ""}">{WORDS[i][0]}</span>')
            words.append({"id": f"w{i}", "t": out(i), "k": k_})
        caps.append(f'<div class="cap clip" id="cap{len(caps)}" style="{st}" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="9">{" ".join(spans)}</div>')

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
def wend(i):
    """fim da palavra i = início da próxima no mesmo corte, ou o fim do corte"""
    for c in cuts.values():
        if "w" in c and c["w"][0] <= i <= c["w"][1]:
            return out(i + 1) if i + 1 <= c["w"][1] else round(c["out"] + c["d"], 3)
T.update({"e_" + k: wend(i) for k, i in {"ti": 5, "s40": 29, "s50": 38, "atencao": 40, "suficiente": 47,
          "testes": 68, "memoria": 69, "recursos": 72, "jogo": 76, "anterior": 103, "optG": 117, "optD": 123, "conta": 127}.items()})

tpl = (P / (sys.argv[2] if len(sys.argv) > 2 else "src/template.html")).read_text()
tpl = re.sub(r"\{\{lucide:([a-z0-9-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), tpl)
html = (tpl.replace("__T__", json.dumps(T, ensure_ascii=False))
        .replace("__TOTAL__", str(TOTAL))
        .replace("__VIDEOS__", "\n        ".join(vids))
        .replace("__CAPTIONS__", "\n      ".join(caps)))
(P / "index.html").write_text(html)
json.dump({"total": TOTAL, "cuts": [{"id": k, "out": v["out"], "d": v["d"], "src": v.get("src")} for k, v in cuts.items()], "T": {k: v for k, v in T.items() if k not in ("words", "cuts")}},
          open(P / "timeline.json", "w"), indent=1)
print("ok total", TOTAL)
