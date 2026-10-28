"""V5 "O Duelo": base da V4 + impactos graves no duelo das caixas e whoosh nas transições (wipes). Gancho via env HOOK=A|B.
V4 (profissional): trilha contínua e discreta, sem drop/riser/impactos; só um "swish" suave quando cada etiqueta entra.
Base: audio.py. Mix: voz isolada (Demucs, mesma EDL do vídeo) + trilha eletrônica "gamer" sintetizada (124 BPM, Lá menor) com ducking + SFX nos grafismos.
A música de fundo do original é descartada (direitos de terceiros + saltos nos cortes). Saída -14 LUFS."""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
TL = json.load(open(HERE / "timeline.json")); T = TL["T"]
SR = 48000; TOTAL = TL["total"]; N = int(SR * TOTAL)
CUT = {c["id"]: c for c in TL["cuts"]}
rng = np.random.default_rng(7)

with wave.open(str(HERE / "assets/audio/voice.wav")) as w:
    src = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2).mean(1) / 32768

# ---- voz: cada corte da EDL, com fade de 12 ms nas bordas ----
voice = np.zeros(N, np.float32)
for c in TL["cuts"]:
    if not c["src"]: continue
    a, b = c["src"]
    seg = src[int(a * SR):int(b * SR)].copy(); f = int(0.012 * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i0 = int(c["out"] * SR); seg = seg[: N - i0]; voice[i0:i0 + len(seg)] += seg
voice = voice / (np.abs(voice).max() + 1e-9) * 0.92

def env(n, a=0.004, d=0.2): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def mixs(*s):
    o = np.zeros(max(len(x) for x in s), np.float32)
    for x in s: o[:len(x)] += x
    return o
def tone(f, dur, d=0.25, a=0.004):
    n = int(dur * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t) * env(n, a, d)).astype(np.float32)
def saw(f, dur, d=0.3, a=0.005, det=0.004):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(2 * ((t * f * (1 + k * det)) % 1) - 1 for k in (-1, 0, 1)) / 3
    x = np.convolve(x, np.ones(6) / 6, "same")  # filtro passa-baixa simples
    return (x * env(n, a, d)).astype(np.float32)
def noise(dur, d=0.03, hp=True):
    n = int(dur * SR); x = rng.standard_normal(n + 1).astype(np.float32); x = np.diff(x) if hp else x[:n]; return x * env(n, 0.001, d)

drums = np.zeros((N, 2), np.float32); music = np.zeros((N, 2), np.float32); sfx = np.zeros((N, 2), np.float32)
def put(buf, sig, t, g=1.0, pan=0.0):
    i0 = int(t * SR)
    if i0 < 0 or i0 >= N: return
    s = sig[: N - i0] * g; buf[i0:i0 + len(s), 0] += s * (1 - max(0, pan)); buf[i0:i0 + len(s), 1] += s * (1 + min(0, pan))

# ---- trilha: Am – F – C – G, 124 BPM; arpejo desde o início, bateria + baixo entram no "atenção!" ----
BEAT = 60 / 124; BAR = 4 * BEAT
CH = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
BASS = [55.0, 43.65, 65.41, 49.0]
def kick(): n = int(0.32 * SR); t = np.arange(n) / SR; return (np.tanh(2.2 * np.sin(2 * np.pi * (45 + 110 * np.exp(-t * 38)) * t)) * env(n, 0.001, 0.11)).astype(np.float32)
def snare(): return mixs(noise(0.18, 0.05) * 0.8, tone(190, 0.12, 0.05) * 0.5)
drop = T["atencao"] - 0.02
t = 0.0; k = 0
while t < TOTAL - 0.1:
    bar = k // 4; ch = CH[bar % 4]; bb = k % 4
    put(drums, kick(), t, 0.6)
    if bb in (1, 3): put(drums, snare(), t, 0.26, 0.05)
    for h in range(4): put(drums, noise(0.04, 0.008), t + h * BEAT / 4, 0.10 if h % 2 else 0.05, 0.35)
    # baixo pulsando em colcheias (side-chain: entra depois do bumbo)
    put(drums, saw(BASS[bar % 4] * 2, BEAT * 0.45, 0.12), t + 0.5 * BEAT, 0.20)
    # arpejo 1/16
    for s16 in range(4):
        f = ch[(k * 4 + s16) % 3] * (2 if (k + s16) % 8 > 5 else 1)
        put(music, saw(f * 2, BEAT / 4, 0.07, 0.002), t + s16 * BEAT / 4, 0.07, (-0.35, 0.35)[s16 % 2])
    if bb == 0:
        for j, f in enumerate(ch): put(music, saw(f, BAR, 1.6, 0.25, 0.006), t, 0.045, (-0.4, 0, 0.4)[j])
    t += BEAT; k += 1
tt = np.arange(N) / SR
music += drums * 0.45  # V4: groove leve e constante, sem drop
# fim: tudo some no último compasso do cartão final
fade = np.minimum(1, tt / 0.15)[:, None] * np.clip((TOTAL - tt) / 0.9, 0, 1)[:, None]
music *= fade

# ducking sob a voz
ve = np.convolve(np.abs(voice), np.ones(int(0.12 * SR)) / int(0.12 * SR), "same")
music *= 0.8 * (1 - 0.8 * np.clip(ve / 0.035, 0, 1))[:, None]

# ---- SFX presos aos grafismos (mesmos gatilhos do index.html) ----
def blip(f=900): n = int(0.09 * SR); x = np.arange(n) / SR; return (np.sign(np.sin(2 * np.pi * (f + 1500 * x) * x)) * 0.35 * env(n, 0.001, 0.03)).astype(np.float32)
def impact(): n = int(0.7 * SR); x = np.arange(n) / SR; return mixs((np.sin(2 * np.pi * (90 - 50 * x) * x) * env(n, 0.002, 0.22)).astype(np.float32), noise(0.4, 0.09) * 0.35)
def whoosh(d=0.32):
    n = int(d * SR); x = np.convolve(rng.standard_normal(n), np.ones(30) / 30, "same").astype(np.float32); return x * np.sin(np.pi * np.arange(n) / n) ** 2 * 3
def glitch(d=0.18):
    n = int(d * SR); x = np.repeat(rng.standard_normal(n // 240 + 1), 240)[:n].astype(np.float32); return x * 0.4 * (rng.random(n) > 0.3) * env(n, 0.001, d / 2)
def tick(): return mixs(noise(0.03, 0.005) * 0.8, tone(2600, 0.04, 0.01) * 0.6)

def swish(d=0.28):
    n = int(d * SR); x = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same").astype(np.float32); return x * np.sin(np.pi * np.arange(n) / n) ** 2 * 1.6
for j, key in enumerate(("g4070", "g5060", "rtx4070", "rtx5060", "geracao", "comparar", "testes", "memoria", "recursos", "jogo", "nova", "optG", "optD", "conta")):
    put(sfx, swish(), T[key] - 0.2, 0.06, (-0.3, 0.3)[j % 2])
put(sfx, swish(0.4), T["card"] - 0.2, 0.08); put(sfx, tone(880, 0.6, 0.25), T["serie40"] - 0.05, 0.035)
put(sfx, tone(660, 0.5, 0.2), T["atencao"] - 0.2, 0.04)
import os
HOOK = os.environ.get("HOOK", "A")
def hit():
    n = int(0.9 * SR); x = np.arange(n) / SR
    return mixs((np.sin(2 * np.pi * (70 - 30 * x) * x) * env(n, 0.003, 0.32)).astype(np.float32), noise(0.5, 0.12) * 0.12)
if HOOK == "A":
    put(sfx, hit(), 0.0, 0.5); put(sfx, swish(0.5), 0.0, 0.10)
    put(sfx, hit(), T["g4070"] - 0.08, 0.35); put(sfx, hit(), T["g5060"] - 0.08, 0.35)
for tw in (CUT["c2"]["out"], CUT["c3"]["out"], CUT["end"]["out"]):
    put(sfx, swish(0.35), tw - 0.25, 0.10)
put(sfx, hit(), CUT["end"]["out"], 0.3)
e0 = CUT["end"]["out"]
put(sfx, swish(0.4), e0 - 0.15, 0.08)
for i, f in enumerate((659.25, 880.0, 1318.5)): put(sfx, tone(f, 1.0, 0.4), e0 + 0.5 + i * 0.07, 0.05)

mix = np.tanh((music + sfx + voice[:, None]) * 0.95).astype(np.float32)
out = HERE / "assets/audio"; raw = out / "raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(raw)], input=mix.tobytes(), check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"highpass=f=40,loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(out / "mix-v5.wav")], check=True)
raw.unlink(); print("mix ->", out / "mix-v5.wav")
