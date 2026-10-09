"""Mix final: narração (frases nos tempos de timings.json) + trilha sintetizada com ducking sob a voz + SFX discretos. Saída -14 LUFS."""
import json, os, subprocess, wave
NOVOICE = os.environ.get("NOVOICE") == "1"  # NOVOICE=1: só trilha + SFX (sem narração, sem ducking)
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
TJ = json.load(open(HERE / "timings.json"))
L = {l["id"]: l for l in TJ["lines"]}
SR = 48000; T = TJ["total"] + 0.3; N = int(SR * T)
voice = np.zeros(N, np.float32); music = np.zeros((N, 2), np.float32); sfx = np.zeros((N, 2), np.float32)
rng = np.random.default_rng(3)


def readwav(p):
    with wave.open(str(p)) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    x = np.frombuffer(raw, np.int16 if sw == 2 else np.int32).astype(np.float32) / (32768 if sw == 2 else 2**31)
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    if sr != SR: x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x).astype(np.float32)
    return x


for l in TJ["lines"]:
    x = readwav(HERE / f"assets/audio/lines/{l['id']}.wav")
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    i0 = int(l["start"] * SR); voice[i0:i0 + len(x)] += x[: N - i0]


def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)


def tone(f, dur, d=0.3, a=0.01):
    n = int(dur * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t) * env(n, a, d)).astype(np.float32)


def put(buf, sig, t, g=1.0, pan=0.0):
    i0 = int(t * SR)
    if i0 >= N or i0 < 0: return
    s = sig[: N - i0] * g
    if buf.ndim == 2:
        buf[i0:i0 + len(s), 0] += s * (1 - max(0, pan)); buf[i0:i0 + len(s), 1] += s * (1 + min(0, pan))
    else: buf[i0:i0 + len(s)] += s


# ---- trilha: drone escuro + pulso suave + arpejo discreto (90 BPM) ----
BEAT = 60 / 90; t = np.arange(N) / SR
drone = 0.10 * np.sin(2 * np.pi * 55 * t) + 0.06 * np.sin(2 * np.pi * 82.41 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.1 * t)) + 0.035 * np.sin(2 * np.pi * 164.81 * t + 1)
fade = np.minimum(1, t / 1.2) * np.minimum(1, (T - t) / 1.5)
music[:, 0] += drone * fade; music[:, 1] += drone * fade
arp = [220.0, 261.63, 329.63, 392.0, 329.63, 261.63]
k = 0; tb = 2.7
while tb < T - 1.5:
    n = int(0.45 * SR); s = (np.sin(2 * np.pi * arp[k % 6] * np.arange(n) / SR) * env(n, 0.004, 0.18)).astype(np.float32)
    put(music, s, tb, 0.05, 0.3 if k % 2 else -0.3)
    if k % 4 == 0:
        kn = int(0.35 * SR); tt = np.arange(kn) / SR
        put(music, (np.sin(2 * np.pi * (48 + 70 * np.exp(-tt * 28)) * tt) * env(kn, 0.002, 0.14)).astype(np.float32), tb, 0.28)
    tb += BEAT / 2; k += 1

# ducking: a trilha cai ~9 dB enquanto a voz fala
ve = np.abs(voice); win = int(0.12 * SR)
ve = np.convolve(ve, np.ones(win) / win, "same")
duck = 1 - 0.65 * np.clip(ve / 0.05, 0, 1)
if NOVOICE: duck[:] = 1; voice[:] = 0
music *= duck[:, None]

# ---- SFX discretos ----
def whoosh(d=0.45):
    n = int(d * SR); x = rng.standard_normal(n).astype(np.float32); x = np.convolve(x, np.ones(50) / 50, "same")
    return x * np.sin(np.pi * np.arange(n) / n) ** 2 * 3
def tick(): n = int(0.03 * SR); return (rng.standard_normal(n).astype(np.float32) * env(n, 0.001, 0.005)) * 0.6
def pop(f=600): n = int(0.1 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * (f + 800 * tt) * tt) * env(n, 0.002, 0.035)).astype(np.float32)
def thud(): n = int(0.3 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * (90 - 50 * tt) * tt) * env(n, 0.002, 0.1)).astype(np.float32)

for i in range(14): put(sfx, tick(), L["l1"]["start"] + i * 0.12, 0.25)          # contador
put(sfx, thud(), L["l2"]["start"] + 0.6, 0.5)                                       # "pessoas certas"
put(sfx, whoosh(), L["l3"]["start"] - 0.1, 0.12)                                     # celular entra
put(sfx, thud(), L["l4"]["start"] - 0.95, 0.35)                                      # vendas: 0
put(sfx, whoosh(0.5), L["l5"]["start"] - 0.1, 0.12)
for d in (1.2, 2.0, 2.6): put(sfx, pop(700), L["l6"]["start"] + d, 0.18)          # filtros
put(sfx, whoosh(0.5), L["l7"]["start"] - 0.2, 0.12)
for i in range(20): put(sfx, tick(), L["l9"]["start"] - 0.05 + i * 0.05, 0.22)     # digitação
put(sfx, pop(520), L["l9"]["end"], 0.3)                                              # clique no patrocinado
for d in (0.0, 0.7, 1.4, 2.1, 2.9): put(sfx, pop(600 + d * 120), L["l10"]["start"] + 0.9 + d * 0.8, 0.15)
put(sfx, whoosh(0.6), L["l12"]["start"] - 0.2, 0.12)
put(sfx, thud(), L["l13"]["start"] + 1.2, 0.4)
for f in (392.0, 493.88, 587.33): put(sfx, tone(f, 2.5, 1.2), L["l14"]["start"], 0.07)  # assinatura

mix = music + sfx + np.stack([voice, voice], 1)
mix = np.tanh(mix * 0.95).astype(np.float32)
NAME = "mix-sem-voz.wav" if NOVOICE else "mix.wav"
out = HERE / "assets/audio"; raw = out / "raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(raw)], input=mix.tobytes(), check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(out / NAME)], check=True)
raw.unlink(); print("mix ->", out / NAME)
