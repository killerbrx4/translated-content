"""Anúncios estáticos da Jolie (feed 1080x1350 e story 1080x1920), no padrão visual das edições 04–09.
Fotos = quadros dos vídeos do cliente (graduados com o LUT da Jolie). Render: Playwright/Chromium.
Uso: python3 -I src/gerar.py <pasta_quadros> <logo.png> <saida>"""
import re, sys, pathlib
from playwright.sync_api import sync_playwright

FR, LOGO, OUT = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
ROOT = pathlib.Path(__file__).resolve().parents[5]
FONTS = ROOT / "zentury/videos/07-jolie-acai/assets/fonts"
ICONS = ROOT / "zentury/videos/07-jolie-acai/assets/icons"

def ic(name):
    t = (ICONS / f"lucide-{name}.svg").read_text()
    inner = re.sub(r"<!--.*?-->", "", re.search(r"<svg[^>]*>(.*)</svg>", t, re.S).group(1), flags=re.S)
    return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'

def img(n): return (FR / f"{n}.jpg").as_uri()

CSS = f"""
@font-face {{ font-family: M; src: url('{(FONTS / 'montserrat-latin-700-normal.woff2').as_uri()}'); font-weight: 700; }}
@font-face {{ font-family: M; src: url('{(FONTS / 'montserrat-latin-900-normal.woff2').as_uri()}'); font-weight: 900; }}
:root {{ --navy:#0b1d47; --red:#e61a27; --orange:#f39a1e; --cream:#f6ece3; --acai:#5a1a6e; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width: var(--w); height: var(--h); overflow: hidden; font-family: M, sans-serif; font-weight: 900; color: #fff; background: var(--navy); }}
.ic {{ width:1em; height:1em; display:inline-block; vertical-align:-0.13em; }}
.bg {{ position:absolute; inset:0; background-size: cover; background-position: var(--pos, 50% 50%); }}
.shade {{ position:absolute; inset:0; background: linear-gradient(to bottom, rgba(11,29,71,.78) 0%, rgba(11,29,71,0) 34%, rgba(11,29,71,0) 58%, rgba(11,29,71,.85) 86%, rgba(11,29,71,.95) 100%); }}
.hl {{ position:absolute; left:64px; right:64px; top: var(--top, 70px); font-size: var(--hs, 104px); line-height:1.03; letter-spacing:-.04em; text-transform: uppercase; }}
.t {{ color:#fff; -webkit-text-stroke: 16px var(--navy); paint-order: stroke fill; }}
.pill {{ display:inline-block; padding: 0 26px 8px; border-radius: 28px; color:#fff; box-shadow: 0 12px 0 rgba(11,29,71,.85); white-space: nowrap; }}
.red {{ background: var(--red); }} .navy {{ background: var(--navy); border: 6px solid #fff; }} .purple {{ background: var(--acai); box-shadow: 0 12px 0 #2c0a37; }}
.bar {{ position:absolute; left:40px; right:40px; bottom: 40px; display:flex; align-items:center; gap: 20px; padding: 22px 24px; border-radius: 40px; background: var(--navy); border: 5px solid var(--cream); box-shadow: 0 14px 0 rgba(0,0,0,.35); }}
.bar img {{ width: 112px; height: 112px; border-radius: 24px; }}
.bar .tx {{ flex:1; }}
.bar .a {{ font-size: 40px; letter-spacing: -.02em; white-space: nowrap; }} .bar .a b {{ color: var(--orange); }}
.bar .b {{ font-size: 26px; font-weight: 700; color: var(--cream); margin-top: 6px; line-height: 1.2; }}
.cta {{ padding: 20px 26px; border-radius: 999px; background: var(--red); font-size: 32px; white-space: nowrap; box-shadow: 0 10px 0 #7d0b12; }}
.badge {{ position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; border-radius:50%; background: var(--orange); color: var(--navy); border: 8px solid #fff; box-shadow: 0 14px 0 rgba(11,29,71,.8); text-transform: uppercase; line-height: .95; transform: rotate(-9deg); }}
.chips {{ display:flex; gap: 18px; margin-top: 26px; }}
.chip {{ display:flex; align-items:center; gap:14px; padding: 14px 26px 14px 14px; border-radius: 999px; background: var(--cream); color: var(--navy); font-size: 40px; box-shadow: 0 10px 0 rgba(11,29,71,.7); text-transform: none; letter-spacing: -.01em; }}
.chip i {{ display:flex; align-items:center; justify-content:center; width: 58px; height: 58px; border-radius: 50%; color:#fff; font-style: normal; font-size: 34px; }}
"""

def bar(sub="Sorvetes · Açaí · Cafés · Crepes", cta="Como chegar"):
    return f"""<div class="bar"><img src="{LOGO.as_uri()}" alt=""><div class="tx"><div class="a">{ic('map-pin')} CLN 407 · <b>Asa Norte</b></div>
    <div class="b">{sub}</div></div><div class="cta">{cta} ›</div></div>"""

def page(w, h, body, extra=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}body{{--w:{w}px;--h:{h}px}}{extra}</style></head><body>{body}</body></html>"

# ---- 5 conceitos (cada um em feed e story) ----
def sorvete(w, h):
    s = h > 1500
    return page(w, h, f"""<div class="bg" style="background-image:url('{img('menta')}');--pos:50% {'55%' if s else '52%'}"></div><div class="shade"></div>
      <div class="hl" style="--top:{150 if s else 70}px"><span class="t">Você monta</span><br><span class="pill red">seu sorvete!</span></div>
      <div class="badge" style="right:46px; top:{760 if s else 470}px; width:300px; height:300px; font-size:50px">Pague<br><span style="font-size:72px">pelo</span><br>peso</div>
      {bar("Self-service de sorvete · pague pelo peso")}""")

def acai(w, h):
    s = h > 1500
    chips = "".join(f'<div class="chip"><i style="background:{c}">{n}</i>{l}</div>' for n, l, c in ((1, "Banana", "#e0a800"), (2, "Morango", "#e2263a"), (3, "Uva", "#7cb342")))
    return page(w, h, f"""<div class="bg" style="background-image:url('{img('acai')}');--pos:50% {'60%' if s else '66%'}"></div><div class="shade"></div>
      <div class="hl" style="--top:{150 if s else 70}px"><span class="t">Açaí</span> <span class="pill purple">do seu jeito</span>
        <div style="font-size:46px;margin-top:30px;letter-spacing:-.02em"><span class="pill" style="background:var(--orange);color:var(--navy);box-shadow:0 10px 0 rgba(11,29,71,.8)">+ 3 acompanhamentos</span></div>
        <div class="chips">{chips}</div></div>
      {bar("Açaí · Sorvetes · Cafés · Crepes")}""")

def passos(w, h):
    s = h > 1500
    P = [("copos", "Pegue seu copo"), ("vitrine", "Escolha o sabor"), ("menta2", "Sirva-se"), ("coberturas", "Coberturas"), ("balanca", "Pague pelo peso"), ("comendo", "É só curtir!")]
    ch = 300 if not s else 500
    cells = "".join(f"""<div style="position:relative;height:{ch}px;border-radius:30px;overflow:hidden;border:5px solid #fff;box-shadow:0 10px 0 rgba(0,0,0,.35)">
        <div class="bg" style="background-image:url('{img(n)}');--pos:50% 50%"></div>
        <div style="position:absolute;left:0;right:0;bottom:0;padding:44px 16px 14px;background:linear-gradient(to top,rgba(11,29,71,.95),rgba(11,29,71,0));font-size:{34 if not s else 38}px;letter-spacing:-.02em;text-transform:uppercase">{l}</div>
        <div style="position:absolute;left:14px;top:14px;width:70px;height:70px;border-radius:50%;background:var(--red);border:5px solid #fff;display:flex;align-items:center;justify-content:center;font-size:40px">{i + 1}</div></div>"""
                    for i, (n, l) in enumerate(P))
    return page(w, h, f"""<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 35%,#16337a,#0b1d47 70%)"></div>
      <div class="hl" style="--top:{120 if s else 54}px;--hs:{96 if s else 84}px"><span class="t">Como funciona</span><br><span class="pill red">na Jolie?</span></div>
      <div style="position:absolute;left:40px;right:40px;top:{420 if s else 290}px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px">{cells}</div>
      {bar("Self-service · pague pelo peso")}""")

def desconto(w, h):
    s = h > 1500
    return page(w, h, f"""<div class="bg" style="background-image:url('{img('meninas')}');--pos:50% 30%"></div><div class="shade"></div>
      <div class="hl" style="--top:{150 if s else 70}px;--hs:{96 if s else 92}px"><span class="t">Mora na</span><br><span class="pill navy">Asa Sul</span> <span class="t">ou</span><br><span class="pill red">Asa Norte?</span></div>
      <div class="badge" style="right:40px; top:{820 if s else 560}px; width:320px; height:320px; background:var(--cream); color:var(--navy); border-color:var(--red); font-size:120px; letter-spacing:-.05em">10%<span style="font-size:36px;color:var(--red);letter-spacing:0;margin-top:8px">de desconto</span></div>
      {bar("Sorvetes · Açaí · Cafés · Crepes")}""")

def fachada(w, h):
    s = h > 1500
    return page(w, h, f"""<div class="bg" style="background-image:url('{img('mesa_loja')}');--pos:50% 40%"></div><div class="shade"></div>
      <div class="hl" style="--top:{150 if s else 70}px"><span class="t">Coisa boa</span><br><span class="t">perto de</span> <span class="pill red">você.</span></div>
      {bar("Sorvetes · Picolés · Açaí · Cafés · Crepes")}""")

C = {"01-monte-seu-sorvete": sorvete, "02-acai-do-seu-jeito": acai, "03-como-funciona": passos, "04-asa-sul-ou-norte-10": desconto, "05-coisa-boa-perto": fachada}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--allow-file-access-from-files"])
    for name, fn in C.items():
        for tag, (w, h) in (("feed", (1080, 1350)), ("story", (1080, 1920))):
            pg = b.new_page(viewport={"width": w, "height": h})
            f = OUT / f"_{name}-{tag}.html"; f.write_text(fn(w, h))
            pg.goto(f.as_uri()); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / f"jolie-{name}-{tag}.png")); pg.close(); f.unlink()
            print("ok", name, tag)
    b.close()
