"""Jolie · gerador de vídeos a partir de um roteiro (EDL) — index.html + timeline.json.
Uso: python3 -I src/build.py . [edl.json]
Cada EDL define: blocos (groups) com planos e fala, cutaways, transições (xfade), sobreposições (overlays),
logo pequeno (bug), encerramento (end) e "minimal": true para a versão só com legenda.
Falas e palavras-chave ficam em src/falas.json (texto revisado + início real de cada fala)."""
import json, re, sys, difflib, unicodedata, pathlib

P = pathlib.Path(sys.argv[1]); A = P / "assets"
E = json.load(open(P / (sys.argv[2] if len(sys.argv) > 2 else "edl.json")))
F = json.load(open(P / "src/falas.json"))
ASR = json.load(open(P / "src/asr-falas.json"))
LINES = F["lines"]; KEYS = set(F["keys"])
MIN = E.get("minimal", False)
norm = lambda s: re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())

# ---- linha do tempo ----
t = 0.0; groups = {}; clips = []
for g in E["groups"]:
    g = dict(g, out=round(t, 3)); gd = 0.0
    for k, (src, ms, d, z) in enumerate(g["clips"]):
        clips.append({"id": f"{g['id']}{k}", "src": src, "ms": ms, "d": d, "z": [1, 1] if MIN else z, "out": round(t + gd, 3), "g": g["id"]})
        gd += d
    g["d"] = round(gd, 3); groups[g["id"]] = g; t += gd
TOTAL = round(t, 3)
# transição suave na troca de bloco: o plano anterior continua por baixo por XD s e o novo entra em fade
XF = {} if MIN else E.get("xfade", {}); XD = XF.get("dur", 0); XAT = set(XF.get("at", []))
for c in clips: c["fade"] = 0.0; c["dd"] = c["d"]
for i, c in enumerate(clips):
    if i and c["id"] == f"{c['g']}0" and c["g"] in XAT:
        c["fade"] = XD; clips[i - 1]["dd"] = round(clips[i - 1]["d"] + XD, 3)
cuts = []
for i, cw in enumerate(E.get("cutaways", [])):
    c = dict(id=f"x{i}", src=cw["clip"][0], ms=cw["clip"][1], d=cw["clip"][2], z=[1, 1] if MIN else cw["clip"][3],
             out=round(groups[cw["at"][0]]["out"] + cw["at"][1], 3), fade=0.0 if MIN else cw.get("fade", 0.0), fout=0.0)
    c["dd"] = c["d"]; end = round(c["out"] + c["d"], 3)
    nxt = next((g for g in groups.values() if g["id"] in XAT and abs(end - g["out"]) < 1e-3), None)
    if nxt:  # cutaway termina na troca de bloco: ele mesmo sai em fade por cima do bloco novo (que entra já visível)
        c["dd"] = round(c["d"] + XD, 3); c["fout"] = XD
        next(k for k in clips if k["id"] == f"{nxt['id']}0")["fade"] = 0.0
    cuts.append(c)

# ---- palavras de cada fala: texto revisado + tempos do Whisper (alinhados por sequência) ----
def line_words(li):
    L = LINES[li]; asr = ASR[f"A_{L['file']}.wav"]["words"]
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

def at(spec):
    """gatilho: {"w": [linha, "palavra"]} | {"g": ["BLOCO", desloc]} | {"end": desloc} | número; + "d" opcional"""
    if isinstance(spec, (int, float)): return float(spec)
    d = spec.get("d", 0.0)
    if "w" in spec: return round(trig[f"{spec['w'][0]}:{norm(spec['w'][1])}"] + d, 3)
    if "g" in spec:
        g = groups[spec["g"][0]]; off = spec["g"][1]
        return round((g["out"] + g["d"] + off if off < 0 else g["out"] + off) + d, 3)
    if "end" in spec: return round(groups["END"]["out"] + spec["end"] + d, 3)
    raise ValueError(spec)

# ---- mídia ----
def media(c, track):
    common = f'id="{c["id"]}" class="shot clip" data-start="{c["out"]}" data-duration="{c["dd"]}" data-track-index="{track}"'
    if c["src"].startswith("img:"):
        return f'<img {common} src="{c["src"][4:]}" alt="" />'
    path = f"assets/footage/{c['src']}.mp4" if "/" in c["src"] else f"assets/footage/n/{c['src']}.mp4"
    return f'<video {common} src="{path}" muted playsinline data-media-start="{c["ms"]}"></video>'
vids = [media(c, i % 2) for i, c in enumerate(clips)] + [media(c, 2) for c in cuts]

def lucide(name, cls="ic"):
    tx = (A / f"icons/lucide-{name}.svg").read_text()
    inner = re.sub(r"<!--.*?-->", "", re.search(r"<svg[^>]*>(.*)</svg>", tx, re.S).group(1), flags=re.S).strip()
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

# ---- sobreposições (gancho e etiquetas; nenhuma na versão mínima) ----
ovs_html, ovs = [], []
for o in ([] if MIN else E.get("overlays", [])):
    if o["style"] == "hook":
        hid = ' style="opacity:0"' if at(o["in"]) > 0.05 else ""
        h = f'<div class="hook" id="{o["id"]}"{hid}><div class="a">{o["a"]}</div><div class="b">{o["b"]}</div></div>'
    else:
        k = f'<div class="k">{o["k"]}</div>' if o.get("k") else ""
        h = f'<div class="tag" id="{o["id"]}"><div class="in">{k}<div class="t">{o["t"]}</div></div></div>'
    ovs_html.append(h)
    ovs.append([o["id"], at(o["in"]), at(o["out"]), o["style"], at(o["flash"]) if o.get("flash") else None])
END = E["end"]
T = {"total": TOTAL, "g": {k: [v["out"], v["d"]] for k, v in groups.items()}, "words": words, "min": MIN,
     "clips": [[c["id"], c["out"], c["dd"], c["z"], c["fade"], c.get("fout", 0.0)] for c in clips + cuts],
     "ov": ovs, "bug": None if MIN or not E.get("bug") else [at(E["bug"]), at({"end": -0.15})]}
tpl = (P / "src/template.html").read_text()
tpl = re.sub(r"\{\{lucide:([a-z0-9-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), tpl)
html = (tpl.replace("__T__", json.dumps(T, ensure_ascii=False)).replace("__TOTAL__", str(TOTAL)).replace("__TITLE__", E.get("title", "Jolie"))
        .replace("__VIDEOS__", "\n      ".join(vids)).replace("__CAPTIONS__", "\n      ".join(caps))
        .replace("__OVERLAYS__", "\n      ".join(ovs_html))
        .replace("__FIN_K__", END["k"]).replace("__FIN_C__", END["c"]).replace("__FIN_A__", END["a"]))
html = re.sub(r"\{\{lucide:([a-z0-9-]+)(?::([a-z-]+))?\}\}", lambda m: lucide(m.group(1), m.group(2) or "ic"), html)
(P / "index.html").write_text(html)
json.dump({"name": E.get("name", "main"), "total": TOTAL, "min": MIN, "music": E.get("music", "soft"),
           "groups": [{k: g[k] for k in ("id", "out", "d")} | ({"voice": g["voice"]} if "voice" in g else {}) | ({"amb": g["amb"]} if "amb" in g else {}) for g in groups.values()],
           "clips": [{k: c[k] for k in ("id", "src", "ms", "d", "out")} for c in clips],
           "T": {"ov": ovs}}, open(P / "timeline.json", "w"), indent=1)
print("ok", E.get("name", "main"), "total", TOTAL)
