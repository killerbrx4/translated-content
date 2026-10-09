"""Trilha + SFX 100% sintetizados (100 BPM, drop em 4,8 s), sincronizados com os estados do BRIEF. Saída: assets/audio/mix.wav a -14 LUFS."""
import json, subprocess
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
SR, T, BPM = 48000, 22.4, 100
BEAT = 60 / BPM
N = int(SR * T)
mix = np.zeros((N, 2), np.float32)
rng = np.random.default_rng(7)


def add(sig, t, gain=1.0, pan=0.0):
    i0 = int(t * SR)
    if i0 >= N: return
    s = sig[: N - i0] * gain
    mix[i0:i0 + len(s), 0] += s * (1 - max(0, pan))
    mix[i0:i0 + len(s), 1] += s * (1 + min(0, pan))


def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def tone(f, dur, d=0.2, a=0.005, kind="sin"):
    n = int(dur * SR); t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) if kind == "sin" else (2 * ((f * t) % 1) - 1) * 0.5
    return (w * env(n, a, d)).astype(np.float32)


def noise(dur, d=0.05, hp=True):
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float32)
    if hp: x = np.diff(x, prepend=0)
    return x * env(n, 0.001, d)


def mixs(*sigs):
    n = max(len(x) for x in sigs); o = np.zeros(n, np.float32)
    for x in sigs: o[:len(x)] += x
    return o


def key():  # tecla mecânica suave
    return mixs(0.5 * noise(0.04, 0.008), 0.35 * tone(1800 + rng.uniform(-150, 150), 0.03, 0.01))


def click(): return mixs(0.6 * noise(0.03, 0.006), 0.5 * tone(2400, 0.03, 0.008))
def pop(f=520): n = int(0.12 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (f + 900 * t) * t) * env(n, 0.002, 0.04)).astype(np.float32)
def thump(): n = int(0.35 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (110 - 70 * t) * t) * env(n, 0.002, 0.12)).astype(np.float32)


def whoosh(dur=0.45):
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float32)
    k = np.ones(40) / 40; x = np.convolve(x, k, "same")
    w = np.sin(np.pi * np.arange(n) / n) ** 2
    return x * w * 3


def bell(f, d=0.9):
    return mixs(0.6 * tone(f, d * 2, d), 0.25 * tone(f * 2.01, d * 1.5, d * 0.6), 0.12 * tone(f * 3.0, d, d * 0.3))


def kick(): n = int(0.4 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * env(n, 0.001, 0.16)).astype(np.float32)
def hat(): return noise(0.06, 0.012) * 0.5


def pad(freqs, dur, gain=0.08):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + i) + 0.3 * np.sin(2 * np.pi * f * 1.003 * t) for i, f in enumerate(freqs))  # mesmo n
    a = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.6)
    return (s * a * gain / len(freqs)).astype(np.float32)


# ---- música ----
C = [130.81, 196.0, 246.94, 293.66]   # Cmaj9 (C G B D)
A = [110.0, 164.81, 220.0, 261.63]   # Am7
F = [87.31, 130.81, 174.61, 220.0]   # Fmaj7
G = [98.0, 146.83, 196.0, 246.94]    # G6
add(pad(C, 4.9, 0.10), 0.0)                       # intro só pad
prog = [C, A, F, G]
for b in range(2, 9):                            # compassos 3..9 (4,8 s → 21,6 s)
    t0 = b * 4 * BEAT
    add(pad(prog[b % 4], 4 * BEAT + 0.5, 0.11), t0)
    add(tone(prog[b % 4][0] / 2, 4 * BEAT, 0.5, 0.01, "saw") * 0.35, t0)   # baixo
    for k in range(4):
        tb = t0 + k * BEAT
        if k in (0, 2): add(kick(), tb, 0.9)
        add(hat(), tb + BEAT / 2, 0.35, 0.3)
        if b < 8 and k == 3: add(hat(), tb + BEAT * 0.75, 0.2, -0.3)
add(pad(C, 2.4, 0.12), 21.6)                      # acorde final

# ---- efeitos (mesmos tempos do index.html) ----
for i, c in enumerate("Sua empresa é ótima."):
    if c != " ": add(key(), 0.25 + i * 0.052, 0.55, rng.uniform(-0.2, 0.2))
for i, c in enumerate("Mas ninguém te encontra."):
    if c != " ": add(key(), 1.5 + i * 0.035, 0.45, rng.uniform(-0.2, 0.2))
add(whoosh(0.18), 2.1, 0.12)  # marca-texto
add(key(), 2.55, 0.6)
add(pop(600), 2.6, 0.35)
add(click(), 2.95, 0.35); add(click(), 3.2, 0.35)
add(thump(), 3.55, 0.9)
add(whoosh(0.55), 3.5, 0.25)
add(bell(880, 0.6), 3.95, 0.18)
add(whoosh(0.4), 4.75, 0.2)
add(pop(480), 5.3, 0.4)
for i, t in enumerate([6.0, 8.4, 10.8, 13.2]):     # checks: sobem de tom
    add(bell([784, 880, 988, 1175][i], 0.35), t, 0.22)
    add(click(), t, 0.3)
for t in [7.2, 9.6, 12.0]:                        # arrastes
    add(click(), t - 0.08, 0.35)
    add(whoosh(0.45), t + 0.02, 0.18)
    add(click(), t + 0.54, 0.4); add(thump(), t + 0.54, 0.25)
add(whoosh(0.6), 13.72, 0.25)
add(whoosh(0.35), 14.38, 0.22)
for t in [14.7, 15.3, 15.9]:
    add(click(), t, 0.45); add(pop(700), t, 0.15)
add(bell(523.25, 1.0), 16.85, 0.3); add(bell(659.25, 1.0), 16.85, 0.18)
add(pop(520), 19.4, 0.35)
add(click(), 20.4, 0.55)
for f in [523.25, 659.25, 783.99, 1046.5]:
    add(bell(f, 1.2), 20.45, 0.14)

# fade final
f0 = int(21.3 * SR); mix[f0:] *= np.linspace(1, 0, N - f0)[:, None] ** 1.5
mix = np.tanh(mix * 0.9)

FF = "ffmpeg"
out = HERE / "assets/audio"; out.mkdir(parents=True, exist_ok=True)
raw = out / "raw.wav"
subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(raw)], input=mix.astype(np.float32).tobytes(), check=True)
m = subprocess.run([FF, "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run([FF, "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(out / "mix.wav")], check=True)
raw.unlink()
print("mix ->", out / "mix.wav")
