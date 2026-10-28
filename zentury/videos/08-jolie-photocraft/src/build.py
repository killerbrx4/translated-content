"""Desafio PhotoCraft × Jolie: monta o index.html a partir da EDL abaixo (dois vídeos de origem, já graduados com o LUT
feito no PhotoCraft) e grava timeline.json para o audio.py. Uso: python3 -I src/build.py ."""
import json, re, sys, pathlib

P = pathlib.Path(sys.argv[1]); A = P / "assets"

# trechos de vídeo: (id, arquivo, origem_ini, origem_fim, saída_ini, zoom)
V = [
    ("v1", "tour", 2.95, 4.75, 0.00, [1.16, 1.04]),   # espiada: "Você gosta de sorvete?"
    ("v2", "tour", 13.20, 13.67, 1.80, [1.10, 1.14]),  # vitrine de sabores  (B-roll sob "Então é porque você ainda não viu…")
    ("v3", "tour", 23.30, 23.77, 2.27, [1.06, 1.12]),  # bola no copo
    ("v4", "tour", 29.50, 29.96, 2.74, [1.08, 1.12]),  # coberturas
    ("v5", "acai", 9.22, 12.62, 6.60, [1.04, 1.16]),   # "Escolha o seu açaí e seus três acompanhamentos"
    ("v6", "acai", 14.35, 16.42, 10.00, [1.04, 1.08]), # "Então vem montar o seu na Jolie!"
]
# falas (áudio original): (arquivo, origem_ini, origem_fim, saída_ini)
VOICE = [("tour", 2.95, 4.75, 0.00), ("acai", 3.55, 5.32, 1.80), ("acai", 5.85, 8.62, 3.75), ("acai", 9.22, 12.62, 6.60), ("acai", 14.40, 16.42, 10.05)]
STAGE = (3.20, 6.60)          # palco roxo com os adesivos do PhotoCraft
POSTER = (12.07, 14.67)       # pôster do PhotoCraft
CTA = (14.67, 17.57)
TOTAL = CTA[1]

def o(vi, t):  # tempo de origem → saída, pelo índice da fala
    f, a, b, s = VOICE[vi]; return round(s + (t - a), 3)

PH = [  # frases da legenda: (fala, [(palavra, t_origem, chave?)], y)
    (0, [("Você", 3.50), ("gosta", 3.66), ("de", 3.92), ("sorvete?", 4.06, 1)], None),
    (1, [("Então", 3.62), ("é", 3.72), ("porque", 3.86), ("você", 4.18), ("ainda", 4.36), ("não", 4.52), ("viu", 4.68), ("nosso", 4.92), ("açaí.", 5.02, 1)], 1530),
    (2, [("E", 5.92), ("o", 6.02), ("melhor", 6.24), ("é", 6.62), ("que", 6.76), ("você", 7.14)], 1530),
    (2, [("pode", 7.40), ("montar", 7.66, 1), ("do", 7.92), ("seu", 8.06), ("jeito.", 8.32, 1)], 1530),
    (3, [("Escolha", 9.28), ("o", 9.62), ("seu", 9.74), ("açaí", 9.94, 1)], 1300),
    (3, [("e", 10.96), ("seus", 11.22), ("três", 11.42, 1), ("acompanhamentos.", 11.78)], 1300),
    (4, [("Então", 14.52), ("vem", 14.82), ("montar", 15.10), ("o", 15.36), ("seu", 15.52), ("na", 15.72), ("Jolie!", 15.88, 1)], 1250),
]
caps, words = [], []
for i, (vi, ws, y) in enumerate(PH):
    s = o(vi, ws[0][1]) - 0.06
    nxt = [o(PH[i + 1][0], PH[i + 1][1][0][1]) - 0.08] if i + 1 < len(PH) else []
    e = min([o(vi, VOICE[vi][2])] + nxt)
    spans = []
    for j, w in enumerate(ws):
        wid = f"w{i}_{j}"; k = len(w) > 2
        cls = "cw k" + (" acai" if "aça" in w[0].lower() else "") if k else "cw"
        spans.append(f'<span id="{wid}" class="{cls}">{w[0]}</span>'); words.append({"id": wid, "t": o(vi, w[1]), "k": k})
    if y is None: continue  # 1ª frase vira o título do topo
    caps.append(f'<div class="cap clip" id="cap{i}" style="top:{y}px" data-start="{round(s, 3)}" data-duration="{round(e - s, 3)}" data-track-index="9">{" ".join(spans)}</div>')

vids = []
for n, (vid, f, a, b, s, z) in enumerate(V):
    vids.append(f'<video id="{vid}" class="shot clip" src="assets/footage/{f}.mp4" muted playsinline data-start="{s}" data-duration="{round(b - a, 3)}" data-media-start="{a}" data-track-index="{n % 2}"></video>')

W = {w["id"]: w["t"] for w in words}
T = {"total": TOTAL, "shots": {v[0]: [v[4], round(v[3] - v[2], 3), v[5]] for v in V}, "words": words,
     "stage": STAGE, "poster": POSTER, "cta": CTA,
     "sorvete": W["w0_3"], "acai": W["w1_8"], "montar": W["w3_1"], "jeito": W["w3_4"], "acai2": W["w4_3"], "tres": W["w5_2"], "acomp": W["w5_3"], "vem": W["w6_1"], "jolie": W["w6_6"]}

def lucide(name, cls="ic"):
    tx = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.sub(r"<!--.*?-->", "", re.search(r"<svg[^>]*>(.*)</svg>", tx, re.S).group(1), flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

tpl = (P / "src/template.html").read_text()
tpl = re.sub(r"\{\{lucide:([a-z-]+)\}\}", lambda m: lucide(m.group(1)), tpl)
html = (tpl.replace("__T__", json.dumps(T, ensure_ascii=False)).replace("__TOTAL__", str(TOTAL))
        .replace("__VIDEOS__", "\n        ".join(vids)).replace("__CAPTIONS__", "\n      ".join(caps)))
(P / "index.html").write_text(html)
json.dump({"total": TOTAL, "voice": VOICE, "T": {k: v for k, v in T.items() if k != "words"}}, open(P / "timeline.json", "w"), indent=1)
print("ok total", TOTAL)
