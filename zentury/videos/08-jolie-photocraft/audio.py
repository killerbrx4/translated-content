"""Mix do desafio PhotoCraft × Jolie: falas originais de dois vídeos (timeline.json → voice) + trilha tropical leve sintetizada
(marimba, shaker, conga, baixo redondo; 100 BPM; Fmaj7–Em7–Dm7–Cmaj7) com ducking forte + SFX suaves. -14 LUFS."""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
TL = json.load(open(HERE / "timeline.json")); T = TL["T"]
SR = 48000; TOTAL = TL["total"]; N = int(SR * TOTAL)
rng = np.random.default_rng(21)

def readwav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2).mean(1) / 32768
SRC = {k: readwav(HERE / f"assets/audio/voice-{k}.wav") for k in ("tour", "acai")}
voice = np.zeros(N, np.float32)
for f, a, b, s in TL["voice"]:
    seg = SRC[f][int(a * SR):int(b * SR)].copy(); seg /= (np.abs(seg).max() + 1e-9); fd = int(0.015 * SR)
    seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd)
    i0 = int(s * SR); seg = seg[: N - i0]; voice[i0:i0 + len(seg)] += seg * 0.9

def env(n, a=0.003, d=0.2): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def mixs(*s):
    o = np.zeros(max(len(x) for x in s), np.float32)
    for x in s: o[:len(x)] += x
    return o
def sine(f, dur, d, a=0.003, ph=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t + ph) * env(n, a, d)).astype(np.float32)
def noise(dur, d=0.03, hp=True):
    n = int(dur * SR); x = rng.standard_normal(n + 1).astype(np.float32); x = np.diff(x) if hp else x[:n]; return x * env(n, 0.002, d)

music = np.zeros((N, 2), np.float32); sfx = np.zeros((N, 2), np.float32)
def put(buf, sig, t, g=1.0, pan=0.0):
    i0 = int(t * SR)
    if i0 < 0 or i0 >= N: return
    s = sig[: N - i0] * g; buf[i0:i0 + len(s), 0] += s * (1 - max(0, pan)); buf[i0:i0 + len(s), 1] += s * (1 + min(0, pan))

# timbres
def marimba(f):   # madeira: fundamental + 4º harmônico curto
    return mixs(sine(f, 0.6, 0.22), 0.35 * sine(f * 4.0, 0.15, 0.03), 0.12 * sine(f * 9.8, 0.05, 0.01))
def conga(f=210): n = int(0.25 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (f + 60 * np.exp(-t * 40)) * t) * env(n, 0.001, 0.07)).astype(np.float32)
def shaker(): return noise(0.07, 0.018) * 0.5
def bass(f, dur): return mixs(sine(f, dur, 0.45, 0.01), 0.25 * sine(f * 2, dur, 0.2, 0.01))
def pad(fs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + i) + 0.4 * np.sin(2 * np.pi * f * 1.004 * t) for i, f in enumerate(fs)) / len(fs)
    return (s * np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.4)).astype(np.float32)

BPM = 100; BEAT = 60 / BPM; BAR = 4 * BEAT
CH = [[174.61, 220.0, 261.63, 329.63], [164.81, 196.0, 246.94, 293.66], [146.83, 174.61, 220.0, 261.63], [130.81, 164.81, 196.0, 246.94]]
BS = [87.31, 82.41, 73.42, 65.41]
# padrão de marimba (semicolcheias, sincopado, estilo tropical/bossa)
PAT = [(0, 3), (0.75, 2), (1.5, 1), (2.0, 2), (2.75, 3), (3.25, 1), (3.5, 0)]
t0 = 0.0; bar = 0
while t0 < TOTAL - 0.1:
    ch = CH[bar % 4]
    put(music, pad(ch, BAR + 0.3), t0, 0.05)
    put(music, bass(BS[bar % 4], BEAT * 1.4), t0, 0.22); put(music, bass(BS[bar % 4] * 1.5, BEAT * 0.9), t0 + 2.5 * BEAT, 0.15)
    for b, i in PAT: put(music, marimba(ch[i] * 2), t0 + b * BEAT, 0.07, (-0.35, 0.35)[int(b * 4) % 2])
    for k in range(16): put(music, shaker(), t0 + k * BEAT / 4, 0.10 if k % 2 else 0.05, 0.3)
    for b, f in ((1.0, 210), (1.75, 260), (3.0, 210), (3.5, 180)): put(music, conga(f), t0 + b * BEAT, 0.16, -0.25)
    t0 += BAR; bar += 1
fade = (np.minimum(1, np.arange(N) / SR / 0.6) * np.minimum(1, (TOTAL - np.arange(N) / SR) / 1.0))[:, None]
music *= fade
# ducking forte ("de leve"): música bem baixa sob a voz, sobe nas cenas sem fala
ve = np.convolve(np.abs(voice), np.ones(int(0.12 * SR)) / int(0.12 * SR), "same")
music *= (1 - 0.78 * np.clip(ve / 0.04, 0, 1))[:, None]

# SFX suaves
def plop(f=520): n = int(0.14 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (f * (1 + 1.2 * np.exp(-t * 30))) * t) * env(n, 0.002, 0.05)).astype(np.float32)
def whoosh(d=0.35):
    n = int(d * SR); x = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same").astype(np.float32); return x * np.sin(np.pi * np.arange(n) / n) ** 2 * 2.5
def chime(): return mixs(*[np.pad(marimba(f), (int(i * 0.06 * SR), 0)) for i, f in enumerate((1046.5, 1318.5, 1568.0, 2093.0))])
s0, m = T["stage"][0], T["montar"]
put(sfx, whoosh(0.4), s0 - 0.3, 0.12); put(sfx, conga(150), s0, 0.55); put(sfx, plop(520), s0 + 0.3, 0.3)   # palco + açaí puro
put(sfx, whoosh(0.35), m - 0.2, 0.12); put(sfx, chime(), m + 0.12, 0.14)                                       # vira o açaí montado
put(sfx, plop(760), T["jeito"] - 0.06, 0.25)
for i in range(3): put(sfx, plop(700 + 120 * i), T["tres"] - 0.05 + i * 0.3, 0.3, (-0.3, 0, 0.3)[i])
p0 = T["poster"][0]; put(sfx, whoosh(0.4), p0 + 0.15, 0.12); put(sfx, conga(130), p0 + 0.74, 0.6); put(sfx, chime(), p0 + 0.78, 0.12)
e0 = T["cta"][0]
put(sfx, conga(150), e0 + 0.4, 0.5); put(sfx, mixs(noise(0.03, 0.006) * 0.8, sine(2400, 0.03, 0.008) * 0.5), e0 + 1.35, 0.7)
put(sfx, chime(), e0 + 1.41, 0.10)

mix = np.tanh((music + sfx + voice[:, None]) * 0.95).astype(np.float32)
out = HERE / "assets/audio"; raw = out / "raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(raw)], input=mix.tobytes(), check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"highpass=f=60,loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(out / "mix.wav")], check=True)
raw.unlink(); print("mix ->", out / "mix.wav")
