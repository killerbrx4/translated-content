"""Mix: voz original das meninas (mesma EDL do vídeo) + trilha pop leve sintetizada (112 BPM) com ducking + SFX nos grafismos. Saída -14 LUFS."""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
E = json.load(open(HERE / "edl.json")); TL = json.load(open(HERE / "timeline.json"))
SR = 48000; TOTAL = TL["total"]; N = int(SR * TOTAL)
rng = np.random.default_rng(11)

with wave.open(str(HERE / "assets/audio/voice.wav")) as w:
    src = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2).mean(1) / 32768

# ---- voz: cada corte da EDL, com fade de 15 ms nas bordas ----
voice = np.zeros(N, np.float32)
for c in TL["cuts"]:
    if not c["src"]: continue
    a, b = c["src"]; b += 0.10 if c["id"] == "c5" else 0  # deixa o fim de "vontade" respirar
    seg = src[int(a * SR):int(b * SR)].copy(); f = int(0.015 * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i0 = int(c["out"] * SR); seg = seg[: N - i0]; voice[i0:i0 + len(seg)] += seg
voice = voice / (np.abs(voice).max() + 1e-9) * 0.9

def env(n, a=0.004, d=0.2): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def mixs(*s):
    o = np.zeros(max(len(x) for x in s), np.float32)
    for x in s: o[:len(x)] += x
    return o
def tone(f, dur, d=0.25, a=0.004, kind="sin"):
    n = int(dur * SR); t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) if kind == "sin" else np.sign(np.sin(2 * np.pi * f * t)) * 0.4
    return (w * env(n, a, d)).astype(np.float32)
def noise(dur, d=0.03):
    n = int(dur * SR); x = np.diff(rng.standard_normal(n + 1)).astype(np.float32); return x * env(n, 0.001, d)

drums = np.zeros((N, 2), np.float32); music = np.zeros((N, 2), np.float32); sfx = np.zeros((N, 2), np.float32)
def put(buf, sig, t, g=1.0, pan=0.0):
    i0 = int(t * SR)
    if i0 < 0 or i0 >= N: return
    s = sig[: N - i0] * g; buf[i0:i0 + len(s), 0] += s * (1 - max(0, pan)); buf[i0:i0 + len(s), 1] += s * (1 + min(0, pan))

# ---- trilha: pop solar, I–V–vi–IV em Dó, 112 BPM ----
BEAT = 60 / 112; BAR = 4 * BEAT
CH = [[261.63, 329.63, 392.0], [246.94, 293.66, 392.0], [220.0, 261.63, 329.63], [261.63, 349.23, 440.0]]
BASS = [65.41, 98.0, 110.0, 87.31]
def kick(): n = int(0.35 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (50 + 80 * np.exp(-t * 32)) * t) * env(n, 0.001, 0.12)).astype(np.float32)
def clap(): return mixs(noise(0.12, 0.035), 0.6 * noise(0.12, 0.02)) * 0.7
def pluck(f): return mixs(tone(f, 0.4, 0.16), 0.3 * tone(f * 2, 0.3, 0.08))
t = 0.0; k = 0
while t < TOTAL - 0.2:
    bar = k // 4; ch = CH[bar % 4]; beat_in_bar = k % 4
    put(drums, kick(), t, 0.55)
    if beat_in_bar in (1, 3): put(drums, clap(), t, 0.22, 0.1)
    for h in (0, 0.5): put(music, noise(0.05, 0.01) * 0.5, t + h * BEAT + BEAT / 4, 0.18, -0.4 + 0.8 * h)
    if beat_in_bar == 0: put(drums, tone(BASS[bar % 4], BAR, 0.9, 0.01), t, 0.30)
    for j, f in enumerate(ch): put(music, pluck(f), t + BEAT / 2 + j * 0.012, 0.09, (-0.3, 0, 0.3)[j])
    if beat_in_bar == 2: put(music, pluck(ch[-1] * 2), t + BEAT * 0.75, 0.05, 0.4)
    t += BEAT; k += 1
# drop: bateria e baixo só entram no carimbo do 10% (momento-chave); antes, só pluck + shaker
html = (HERE / "index.html").read_text()
T = json.loads(html.split("const T = ", 1)[1].split(";\n", 1)[0])
gate = (np.arange(N) / SR >= T["dez"] - 0.02).astype(np.float32)[:, None]
music += drums * gate
rn = int(0.9 * SR); rt = np.arange(rn) / SR
riser = (np.convolve(rng.standard_normal(rn), np.ones(12) / 12, "same") * (rt / 0.9) ** 3 * 0.6 + np.sin(2 * np.pi * (300 + 900 * (rt / 0.9) ** 2) * rt) * (rt / 0.9) ** 2 * 0.12).astype(np.float32)
put(music, riser, T["dez"] - 0.9, 0.5)
fade = np.minimum(1, np.arange(N) / SR / 0.3)[:, None] * np.minimum(1, (TOTAL - np.arange(N) / SR) / 0.6)[:, None]
music *= fade

# ducking sob a voz
ve = np.convolve(np.abs(voice), np.ones(int(0.1 * SR)) / int(0.1 * SR), "same")
music *= (1 - 0.7 * np.clip(ve / 0.04, 0, 1))[:, None]

# ---- SFX presos aos grafismos (mesmos gatilhos do index.html) ----
def pop(f=650): n = int(0.11 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * (f + 900 * tt) * tt) * env(n, 0.002, 0.04)).astype(np.float32)
def thump(): n = int(0.4 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * (120 - 80 * tt) * tt) * env(n, 0.002, 0.14)).astype(np.float32)
def whoosh(d=0.35):
    n = int(d * SR); x = np.convolve(rng.standard_normal(n), np.ones(40) / 40, "same").astype(np.float32); return x * np.sin(np.pi * np.arange(n) / n) ** 2 * 3
def sparkle(): return mixs(*[np.pad(tone(f, 0.5, 0.18), (int(i * 0.05 * SR), 0)) for i, f in enumerate((1318.5, 1568.0, 2093.0))])

put(sfx, pop(560), T["sul"] - 0.08, 0.35, -0.4); put(sfx, pop(700), T["norte"] - 0.08, 0.35, 0.4)
put(sfx, whoosh(0.3), T["praVoce"] - 0.15, 0.10)
put(sfx, thump(), T["dez"] + 0.03, 0.75); put(sfx, sparkle(), T["dez"] + 0.06, 0.10)
for i, k2 in enumerate(("sorv", "acai", "cafe")): put(sfx, pop(600 + i * 140), T[k2] - 0.1, 0.32, (-0.4, 0, 0.4)[i])
put(sfx, whoosh(0.3), T["sul2"] - 0.14, 0.10, -0.5); put(sfx, whoosh(0.3), T["norte2"] - 0.14, 0.10, 0.5)
put(sfx, whoosh(0.35), T["parar"] - 0.32, 0.10); put(sfx, thump(), T["parar"] + 0.1, 0.5)
put(sfx, whoosh(0.4), T["cuts"]["c6"][0] - 0.1, 0.12)
c8 = T["cuts"]["card"][0]
for f in (523.25, 659.25, 783.99, 1046.5): put(sfx, tone(f, 2.4, 0.9), c8, 0.08)
put(sfx, sparkle(), c8 + 0.05, 0.12)
if "cta" in T["cuts"]:  # V2: carimbo do selo + clique no botão
    e0 = T["cuts"]["cta"][0]
    put(sfx, whoosh(0.3), e0, 0.12); put(sfx, thump(), e0 + 0.33, 0.6)
    put(sfx, mixs(noise(0.03, 0.006) * 0.8, tone(2400, 0.03, 0.008) * 0.5), e0 + 1.3, 0.8)
    for i, f in enumerate((783.99, 1046.5, 1318.5)): put(sfx, tone(f, 1.2, 0.5), e0 + 1.36 + i * 0.07, 0.10)

mix = np.tanh((music + sfx + voice[:, None]) * 0.95).astype(np.float32)
out = HERE / "assets/audio"; raw = out / "raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(raw)], input=mix.tobytes(), check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"highpass=f=60,loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(out / "mix.wav")], check=True)
raw.unlink(); print("mix ->", out / "mix.wav")
