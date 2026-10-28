"""Legendas: '159,90' fica na tela até o número terminar de ser falado e 'POR CASAL!' entra junto com a fala.
Cada legenda vira uma camada (cor + transparência) estimada por mínimos quadrados sobre vários quadros e é recolocada nos quadros novos."""
import sys, subprocess, numpy as np, cv2
src, mix, dst = sys.argv[1:4]   # src = vídeo com o preço já corrigido (fix_price.py)
W, H = 480, 854
P0, P1o, P1 = 446, 476, 498     # preço: era 446–476, passa a 446–498
C0o, C1o, C0, C1 = 482, 513, 499, 529   # "POR CASAL!": era 482–513, passa a 499–529

def frames(p):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", p, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    out = []
    while True:
        b = pr.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy())
    return out
F = frames(src)

k5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
def masks(ks):
    cnt = np.zeros((H, W), np.float32); ks = list(ks)
    for k in ks: cnt[540:620] += (F[k][540:620].min(axis=2) > 200)
    core = (cnt >= 0.8 * len(ks)).astype(np.uint8)          # só o que fica parado (texto); borda do prato e reflexos mudam
    core[:, :95] = 0; core[:, 385:] = 0                     # ignora o @ do Instagram e o lado direito
    txt = cv2.dilate(core, k5); sh = np.roll(np.roll(cv2.dilate(core, k5, iterations=2), 2, 0), 1, 1)
    region = cv2.dilate(txt | sh, k5)
    return region
def layer(ks, region):
    """I = (1-a)·B + a·t·w  (w = tom creme do texto; t = brilho) → resolve a e a·t por pixel, com B = fundo reconstruído do próprio quadro."""
    wv = np.array([232, 238, 245], np.float64) / 245
    ys, xs = np.nonzero(region); n = len(ys)
    AtA = np.zeros((n, 2, 2)); Atb = np.zeros((n, 2))
    for k in ks:
        I = F[k].astype(np.float64); B = cv2.inpaint(F[k], region * 255, 6, cv2.INPAINT_TELEA).astype(np.float64)
        Ib, Bb = I[ys, xs], B[ys, xs]
        for ch in range(3):
            row = np.zeros((n, 2)); row[:, 0] = -Bb[:, ch]; row[:, 1] = wv[ch]
            AtA += row[:, :, None] * row[:, None, :]; Atb += row * (Ib[:, ch] - Bb[:, ch])[:, None]
    AtA += np.eye(2) * 1e-3 * len(ks)
    u = np.linalg.solve(AtA, Atb[..., None])[..., 0]
    a = np.clip(u[:, 0], 0, 1); c = np.clip(u[:, 1], 0, 255 * a)[:, None] * wv
    A = np.zeros((H, W), np.float32); C = np.zeros((H, W, 3), np.float32)
    A[ys, xs] = a; C[ys, xs] = c
    return A, C
rP = masks(range(P0, P1o + 1)); rC = masks(range(C0o, C1o + 1))
AP, CP = layer(range(P0, P1o + 1), rP); AC, CC = layer(range(C0o, C1o + 1), rC)
for nm, A, C in (("P", AP, CP), ("C", AC, CC)):   # prévia das camadas sobre cinza
    g = np.full((H, W, 3), 128, np.float32); cv2.imwrite(dst.rsplit("/", 1)[0] + f"/layer{nm}.png", np.clip(g * (1 - A[..., None]) + C, 0, 255)[520:640].astype(np.uint8))

def clean(k):
    reg = np.zeros((H, W), np.uint8)
    if P0 <= k <= P1o: reg |= rP
    if C0o <= k <= C1o: reg |= rC
    return cv2.inpaint(F[k], reg * 255, 6, cv2.INPAINT_TELEA) if reg.any() else F[k]
out = []
for k in range(len(F)):
    if P0 <= k <= C1:
        fr = clean(k).astype(np.float32)
        if P0 <= k <= P1o: fr = F[k].astype(np.float32)        # quadros originais do preço ficam como estão
        if P1o < k <= P1: fr = fr * (1 - AP[..., None]) + CP
        if C0 <= k <= C1: fr = fr * (1 - AC[..., None]) + CC
        out.append(np.clip(fr, 0, 255).astype(np.uint8))
    else: out.append(F[k])
for k in (470, 480, 490, 498, 499, 505, 520, 529): cv2.imwrite(dst.rsplit("/", 1)[0] + f"/rt{k}.png", out[k])
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", dst], stdin=subprocess.PIPE)
for fr in out: enc.stdin.write(fr.tobytes())
enc.stdin.close(); enc.wait(); print("ok")
