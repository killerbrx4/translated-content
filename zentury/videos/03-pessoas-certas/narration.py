"""Gera a narração frase a frase (Kokoro pt-BR local) e grava timings.json com início/fim de cada frase."""
import json, subprocess, sys, wave
from pathlib import Path
HERE = Path(__file__).parent
VOICE, SPEED = "pm_alex", 1.26
# (id, texto falado, legenda, pausa depois em s)
LINES = [
    ("l1", "Sua empresa não precisa de mais seguidores.", "Sua empresa não precisa de <em>mais seguidores</em>.", 0.2),
    ("l2", "Ela precisa chegar às pessoas certas.", "Ela precisa chegar às <em>pessoas certas</em>.", 0.3),
    ("l3", "Dá pra ter milhares de seguidores e não vender nada.", "Dá pra ter milhares de seguidores e <em>não vender nada</em>.", 0.15),
    ("l4", "Muita gente vê, curte, e vai embora.", "Muita gente vê, curte… e <em>vai embora</em>.", 0.3),
    ("l5", "No Meta Éds, seu anúncio aparece no Instagram e no Facebook,", "No <em>Meta Ads</em>, seu anúncio aparece no Instagram e no Facebook,", 0.1),
    ("l6", "para quem tem o perfil do seu cliente: região, idade, e interesses.", "para quem tem o <em>perfil do seu cliente</em>: região, idade e interesses.", 0.3),
    ("l7", "No Gúgol Éds é diferente.", "No <em>Google Ads</em> é diferente.", 0.15),
    ("l8", "Você aparece para quem já está procurando.", "Você aparece para quem <em>já está procurando</em>.", 0.25),
    ("l9", "Uma pessoa pesquisa: dentista em Campinas. E o seu anúncio aparece como patrocinado.", "Uma pessoa pesquisa “dentista em Campinas”, e o seu anúncio aparece como <em>patrocinado</em>.", 0.3),
    ("l10", "Daí começa o caminho: anúncio, clique, contato, atendimento e venda.", "Daí começa o caminho: anúncio, clique, contato, atendimento e <em>venda</em>.", 0.2),
    ("l11", "O resultado depende da oferta, do orçamento, da página e do atendimento.", "O resultado depende da oferta, do orçamento, da página e do <em>atendimento</em>.", 0.35),
    ("l12", "Não é sobre todo mundo te ver.", "Não é sobre <em>todo mundo</em> te ver.", 0.15),
    ("l13", "É sobre quem compra te encontrar.", "É sobre <em>quem compra</em> te encontrar.", 0.4),
    ("l14", "Siga a Zentchúri e entenda o próximo passo.", "Siga a <em>ZENTURY</em> e entenda o próximo passo.", 0.0),
]
out = HERE / "assets/audio/lines"; out.mkdir(parents=True, exist_ok=True)
t, timings = 0.25, []
for lid, spoken, cap, gap in LINES:
    wav = out / f"{lid}.wav"
    if not wav.exists():
        r = subprocess.run(["npx", "--yes", "hyperframes@0.8.139", "tts", spoken, "-v", VOICE, "-l", "pt-br", "-s", str(SPEED), "-o", str(wav), "--json"], capture_output=True, text=True)
        if not wav.exists(): sys.exit(f"TTS falhou em {lid}: {r.stdout[-300:]} {r.stderr[-300:]}")
    with wave.open(str(wav)) as w: dur = w.getnframes() / w.getframerate()
    timings.append({"id": lid, "start": round(t, 3), "end": round(t + dur, 3), "caption": cap})
    t += dur + gap
json.dump({"total": round(t + 0.2, 3), "lines": timings}, open(HERE / "timings.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps([(x["id"], x["start"], x["end"]) for x in timings]), "total", round(t, 2))
