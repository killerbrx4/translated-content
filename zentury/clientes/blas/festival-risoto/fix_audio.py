"""Áudio: troca 'R$ 59,90' (15,58–16,34 s da voz) pela nova gravação 'R$ 159,90' no ritmo do narrador;
'por casal' é empurrado para a pausa seguinte; a música (stem sem voz) segue intacta."""
import sys, subprocess, json, numpy as np
SR = 44100
def rd(p, ss=0, d=None, af=None):
    c = ["ffmpeg", "-v", "error", "-ss", str(ss), "-i", p] + (["-t", str(d)] if d else []) + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(c, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
voc, mus, new, out = sys.argv[1:5]
A, B, PC_END = 15.58, 16.34, 17.40          # número antigo [A,B); "por casal" [B, PC_END)
D = float(sys.argv[5]) if len(sys.argv) > 5 else 1.04
i = lambda t: int(round(t * SR))
v = rd(voc); m = rd(mus)
n = rd(new, 0.0, 1.37, f"afftdn=nf=-40,atempo={1.37 / D:.4f}")
n = n[: int(D * SR)]
def ltas(x, N=4096):
    x = x.mean(1); w = np.hanning(N); fr = [np.abs(np.fft.rfft(x[k:k + N] * w)) ** 2 for k in range(0, len(x) - N, N // 4)]
    fr = [f for f in fr if f.sum() > 1e-3 * max(g.sum() for g in fr)]   # só trechos com voz
    return np.mean(fr, 0)
def eq_match(x, ref):
    """EQ fixo que aproxima o timbre da gravação nova ao da narração (média em 1/3 de oitava, limitado a ±10 dB)."""
    N = 4096; f = np.fft.rfftfreq(N, 1 / SR); a, b = ltas(x, N), ltas(ref, N)
    g = np.ones_like(f)
    for k in range(len(f)):
        if f[k] < 60: g[k] = 1; continue
        band = (f > f[k] / 2 ** (1 / 6)) & (f < f[k] * 2 ** (1 / 6))
        g[k] = np.sqrt(b[band].sum() / (a[band].sum() + 1e-12))
    g = g / np.sqrt((g ** 2 * a).sum() / a.sum())                      # mantém o volume total
    g = np.clip(g, 10 ** (-10 / 20), 10 ** (10 / 20))
    M = len(x) + N; G = np.interp(np.fft.rfftfreq(M, 1 / SR), f, g)
    return np.stack([np.fft.irfft(np.fft.rfft(x[:, c], M) * G, M)[: len(x)] for c in range(2)], 1).astype(np.float32)
n = eq_match(n, v[i(12.0):i(15.5)])
def fade(x, a=0.008, b=0.03):
    fa, fb = int(a * SR), int(b * SR); x[:fa] *= np.linspace(0, 1, fa)[:, None]; x[-fb:] *= np.linspace(1, 0, fb)[:, None]; return x
old_num = v[i(A):i(B)]
rms = lambda x: np.sqrt((x ** 2).mean())
n = n * (rms(old_num) / rms(n[: i(D)]))     # mesmo volume da narração
pc = fade(v[i(B):i(PC_END)].copy())
nv = v.copy(); nv[i(A):i(17.68)] = 0
nv[i(A) - int(0.008 * SR):i(A)] *= np.linspace(1, 0, int(0.008 * SR))[:, None]
s = i(A); nv[s:s + len(n)] += fade(n); s += len(n); nv[s:s + len(pc)] += pc
L = min(len(nv), len(m)); mix = nv[:L] + m[:L]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", out], input=mix.astype(np.float32).tobytes(), check=True)
print("número novo", A, "→", round(A + D, 3), "| por casal", round(A + D, 3), "→", round(A + D + PC_END - B, 3))
