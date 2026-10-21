"""Mix: falas do celular (limpas, sincronizadas) + som ambiente da câmera nos planos de preparo (baixo, dá textura)
+ trilha pop leve sintetizada (100 BPM, Ré maior) com ducking + SFX discretos nas etiquetas. Saída -14 LUFS."""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
TL = json.load(open(HERE / "timeline.json")); T = TL["T"]
SR = 48000; TOTAL = TL["total"]; N = int(SR * TOTAL)
rng = np.random.default_rng(5)

def read(path, ss=0.0, d=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss), "-i", str(path)] + (["-t", str(d)] if d else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()
def fades(x, a=0.012, b=0.03):
    fa, fb = int(a * SR), int(b * SR); x[:fa] *= np.linspace(0, 1, fa); x[-fb:] *= np.linspace(1, 0, fb); return x
def place(buf, x, t, g=1.0):
    i0 = int(round(t * SR)); x = x[: max(0, N - i0)]; buf[i0:i0 + len(x)] += x * g

voice = np.zeros(N, np.float32); amb = np.zeros(N, np.float32)
for g in TL["groups"]:
    if "voice" in g:
        f, vs = g["voice"]
        place(voice, fades(read(HERE / f"assets/audio/clean/{f}.wav", vs, g["d"])), g["out"])
    if "amb" in g:
        for c in TL["clips"]:
            if c["id"].startswith(g["id"]) and c["id"][len(g["id"]):].isdigit() and not c["src"].startswith("img:"):
                place(amb, fades(read(HERE / f"assets/footage/n/{c['src']}.mp4", c["ms"], c["d"]), 0.04, 0.06), c["out"], g["amb"])
voice = voice / (np.abs(voice).max() + 1e-9) * 0.9
amb = np.convolve(amb, [0.5, 0.5], "same")  # tira um pouco do chiado

def env(n, a=0.004, d=0.2): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def tone(f, dur, d=0.25, a=0.004):
    n = int(dur * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t) * env(n, a, d)).astype(np.float32)
def noise(dur, d=0.03):
    n = int(dur * SR); return (np.diff(rng.standard_normal(n + 1)) * env(n, 0.001, d)).astype(np.float32)
def pluck(f): return tone(f, 0.45, 0.18) + 0.35 * tone(2 * f, 0.3, 0.08) + 0.12 * tone(3 * f, 0.2, 0.05)

music = np.zeros((N, 2), np.float32)
def put(sig, t, g=1.0, pan=0.0):
    i0 = int(t * SR)
    if 0 <= i0 < N:
        s = sig[: N - i0] * g; music[i0:i0 + len(s), 0] += s * (1 - max(0, pan)); music[i0:i0 + len(s), 1] += s * (1 + min(0, pan))
BEAT = 60 / 100; BAR = 4 * BEAT
CH = [[293.66, 369.99, 440.0], [220.0, 277.18, 329.63], [246.94, 293.66, 369.99], [196.0, 246.94, 293.66]]  # D A Bm G
BASS = [73.42, 55.0, 61.74, 49.0]
def kick(): n = int(0.3 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (48 + 70 * np.exp(-t * 30)) * t) * env(n, 0.001, 0.11)).astype(np.float32)
t = 0.0; k = 0
while t < TOTAL - 0.2:
    bar = k // 4; ch = CH[bar % 4]; bb = k % 4
    put(kick(), t, 0.45)
    if bb in (1, 3): put(noise(0.12, 0.03) * 0.7, t, 0.18, 0.1)
    for h in (0.25, 0.75): put(noise(0.04, 0.008), t + h * BEAT, 0.10, 0.35 if h > 0.5 else -0.35)
    if bb == 0: put(tone(BASS[bar % 4], BAR * 0.95, 1.2, 0.02), t, 0.28)
    for j, f in enumerate(ch): put(pluck(f), t + BEAT / 2 + j * 0.015, 0.06, (-0.3, 0, 0.3)[j])
    if bb == 2: put(pluck(ch[-1] * 2), t + BEAT * 0.75, 0.035, 0.4)
    t += BEAT; k += 1
tt = np.arange(N) / SR
music *= (np.minimum(1, tt / 0.25) * np.clip((TOTAL - tt) / 1.2, 0, 1))[:, None]
ve = np.convolve(np.abs(voice), np.ones(int(0.12 * SR)) / int(0.12 * SR), "same")
music *= (0.85 * (1 - 0.72 * np.clip(ve / 0.035, 0, 1)))[:, None]

def swish(d=0.3):
    n = int(d * SR); x = np.convolve(rng.standard_normal(n), np.ones(50) / 50, "same").astype(np.float32); return x * np.sin(np.pi * np.arange(n) / n) ** 2 * 1.6
for key in ("tapioca", "frango", "cuscuz", "ama"): put(swish(), T[key] - 0.2, 0.06)
END = next(g["out"] for g in TL["groups"] if g["id"] == "END")
put(swish(0.45), END - 0.2, 0.08)
for i, f in enumerate((587.33, 739.99, 880.0, 1174.66)): put(tone(f, 1.2, 0.45), END + 0.15 + i * 0.07, 0.05)

mix = np.tanh(music + (voice + amb)[:, None] * 0.95).astype(np.float32)
out = HERE / "assets/audio"; raw = out / "raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(raw)], input=mix.tobytes(), check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(out / "mix.wav")], check=True)
raw.unlink(); print("mix ->", out / "mix.wav")
