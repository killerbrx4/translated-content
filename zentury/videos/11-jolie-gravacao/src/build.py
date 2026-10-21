"""Jolie · vídeo de venda "Não é só sorvete" — gera index.html + timeline.json a partir de edl.json.
Uso: python3 -I src/build.py ."""
import json, re, sys, difflib, unicodedata, pathlib

P = pathlib.Path(sys.argv[1]); A = P / "assets"
E = json.load(open(P / "edl.json"))
ASR = json.load(open(P / "src/asr-falas.json"))
KEYS = set(E["keys"])
norm = lambda s: re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())

# ---- linha do tempo ----
t = 0.0; groups = {}; clips = []
for g in E["groups"]:
    g = dict(g, out=round(t, 3)); gd = 0.0
    for k, (src, ms, d, z) in enumerate(g["clips"]):
        clips.append({"id": f"{g['id']}{k}", "src": src, "ms": ms, "d": d, "z": z, "out": round(t + gd, 3), "g": g["id"]})
        gd += d
    g["d"] = round(gd, 3); groups[g["id"]] = g; t += gd
TOTAL = round(t, 3)
# transição suave na troca de bloco: o plano anterior continua por baixo por XD s e o novo entra em fade
XF = E.get("xfade", {}); XD = XF.get("dur", 0); XAT = set(XF.get("at", []))
for i, c in enumerate(clips):
    c["fade"] = 0.0; c["dd"] = c["d"]
for i, c in enumerate(clips):
    if i and c["id"] == f"{c['g']}0" and c["g"] in XAT:
        c["fade"] = XD; clips[i - 1]["dd"] = round(clips[i - 1]["d"] + XD, 3)
cuts = [dict(id=f"x{i}", src=c["clip"][0], ms=c["clip"][1], d=c["clip"][2], z=c["clip"][3],
             out=round(groups[c["at"][0]]["out"] + c["at"][1], 3)) for i, c in enumerate(E["cutaways"])]
for c in cuts:  # cutaway que termina junto com o bloco também segura por baixo da transição
    end = round(c["out"] + c["d"], 3); c["fade"] = E["cutaways"][int(c["id"][1:])].get("fade", 0.0)
    c["dd"] = c["d"]; c["fout"] = 0.0
    nxt = next((g for g in groups.values() if g["id"] in XAT and abs(end - g["out"]) < 1e-3), None)
    if nxt:  # cutaway termina na troca de bloco: ele mesmo sai em fade por cima do bloco novo (que entra já visível)
        c["dd"] = round(c["d"] + XD, 3); c["fout"] = XD
        next(k for k in clips if k["id"] == f"{nxt['id']}0")["fade"] = 0.0

# ---- palavras de cada fala: texto revisado + tempos do Whisper (alinhados por sequência) ----
def line_words(li):
    L = E["lines"][li]; asr = ASR[f"A_{L['file']}.wav"]["words"]
    toks = L["text"].split(); sm = difflib.SequenceMatcher(None, [norm(w) for w in toks], [norm(w[0]) for w in asr])
    tm = [None] * len(toks)
    for b in sm.get_matching_blocks():
        for k in range(b.size): tm[b.a + k] = asr[b.b + k][1]
    tm[0] = L["start"]
    for i in range(len(toks)):  # palavras sem par: interpolação entre vizinhas
        if tm[i] is None:
            j = next((j for j in range(i + 1, len(toks)) if tm[j] is not None), None)
            prev = tm[i - 1]; nxt = tm[j] if j is not None else prev + 0.3 * (len(toks) - i)
            tm[i] = prev + (nxt - prev) / ((j or len(toks)) - i + 1)
    return list(zip(toks, tm))

caps, words, trig = [], [], {}
for g in groups.values():
    if "voice" not in g: continue
    vs = g["voice"][1]; wl = line_words(g["line"])
    o = lambda ta: round(g["out"] + ta - vs, 3)
    chunks, cur = [], []
    for i, (w, ta) in enumerate(wl):
        if cur and (len(cur) == 3 or len(" ".join(x[0] for x in cur + [(w, 0)])) > 18 or cur[-1][0][-1] in ",.?!"):
            chunks.append(cur); cur = []
        cur.append((w, ta, i))
    chunks.append(cur)
    for k, ch in enumerate(chunks):
        s = o(ch[0][1]) - 0.05
        e = o(chunks[k + 1][0][1]) - 0.05 if k + 1 < len(chunks) else min(o(ch[-1][1]) + 1.1, g["out"] + g["d"] - 0.05)
        spans = []
        for w, ta, i in ch:
            wid = f"w{g['line']}_{i}"; key = w in KEYS
            spans.append(f'<span id="{wid}" class="cw{" k" if key else ""}">{w}</span>')
            words.append({"id": wid, "t": o(ta), "k": key})
            trig.setdefault(f"{g['line']}:{norm(w)}", o(ta))
        caps.append(f'<div class="cap clip" id="cap{len(caps)}" data-start="{round(max(0, s), 3)}" data-duration="{round(e - max(0, s), 3)}" data-track-index="9">{" ".join(spans)}</div>')

# ---- mídia ----
def media(c, track):
    common = f'id="{c["id"]}" class="shot clip" data-start="{c["out"]}" data-duration="{c["dd"]}" data-track-index="{track}"'
    if c["src"].startswith("img:"):
        return f'<img {common} src="{c["src"][4:]}" alt="" />'
    return f'<video {common} src="assets/footage/n/{c["src"]}.mp4" muted playsinline data-media-start="{c["ms"]}"></video>'
vids = [media(c, i % 2) for i, c in enumerate(clips)] + [media(c, 2) for c in cuts]

def lucide(name, cls="ic"):
    tx = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.sub(r"<!--.*?-->", "", re.search(r"<svg[^>]*>(.*)</svg>", tx, re.S).group(1), flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

G = {k: [v["out"], v["d"]] for k, v in groups.items()}
T = {"total": TOTAL, "g": G, "words": words,
     "clips": [[c["id"], c["out"], c["dd"], c["z"], c["fade"], c.get("fout", 0.0)] for c in clips + cuts],
     "tapioca": trig["3:tapioca"], "frango": trig["4:frango"], "cuscuz": trig["5:cuscuz"], "ama": trig["6:quem"],
     "sorvete": trig["0:sorvete"], "mostrar": trig["0:mostrar"]}
tpl = (P / "src/template.html").read_text()
tpl = re.sub(r"\{\{lucide:([a-z0-9-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), tpl)
html = (tpl.replace("__T__", json.dumps(T, ensure_ascii=False)).replace("__TOTAL__", str(TOTAL))
        .replace("__VIDEOS__", "\n        ".join(vids)).replace("__CAPTIONS__", "\n      ".join(caps)))
(P / "index.html").write_text(html)
json.dump({"total": TOTAL, "groups": [{k: g[k] for k in ("id", "out", "d") } | ({"voice": g["voice"]} if "voice" in g else {}) | ({"amb": g["amb"]} if "amb" in g else {}) for g in groups.values()],
           "clips": [{k: c[k] for k in ("id", "src", "ms", "d", "out")} for c in clips],
           "T": {k: v for k, v in T.items() if k not in ("words", "clips", "g")}}, open(P / "timeline.json", "w"), indent=1)
print("ok total", TOTAL)
