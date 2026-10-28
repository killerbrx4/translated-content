"""Troca '59,90' por '159,90' na legenda queimada (quadros 446–476), reaproveitando os pixels originais do texto."""
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, dst, n0, n1 = sys.argv[1], sys.argv[2], 446, 476
W, H = 480, 854
SPLIT, SH = 304, 4          # coluna entre "APENAS" e "59,90"; meio avanço do "1" (8 px)
Y0, Y1, X0, X1 = 560, 600, 100, 380

def frames():
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()

# máscara estática do texto (união dos quadros)
allf = list(frames())
core = np.zeros((H, W), np.uint8)
for f in allf[n0:n1 + 1]:
    r = f[Y0:Y1, X0:X1]
    core[Y0:Y1, X0:X1] |= (r.min(axis=2) > 200).astype(np.uint8)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
txt = cv2.dilate(core, k, iterations=1)                       # letra + borda suave
shadow = np.roll(np.roll(cv2.dilate(core, k, iterations=2), 2, 0), 1, 1)
hole = cv2.dilate(txt | shadow, k, iterations=1)             # o que some e é reconstruído
alpha = cv2.GaussianBlur((txt | shadow).astype(np.float32), (0, 0), 1.0)
alpha = np.clip(alpha * 1.6, 0, 1)

# glifo "1" (Montserrat Bold) no tamanho dos dígitos originais: altura 572–587
S = 8
f = ImageFont.truetype("/root/.local/share/fonts/Montserrat-900.ttf", 400)
g = Image.new("L", (400, 500), 0); ImageDraw.Draw(g).text((20, 0), "1", font=f, fill=255)
g = g.crop(g.getbbox())
dig_h = 14; scale = dig_h * S / g.height
g = g.resize((max(1, round(g.width * scale)), dig_h * S), Image.LANCZOS)
pad = 6 * S
big = Image.new("L", (g.width + 2 * pad, g.height + 2 * pad), 0); big.paste(g, (pad, pad))
one_a = cv2.GaussianBlur(np.array(big.resize((big.width // S, big.height // S), Image.LANCZOS)).astype(np.float32) / 255, (0, 0), 0.45)
one_a = np.clip(one_a * 1.2, 0, 1)
one_sh = np.roll(np.roll(np.array(big.filter(ImageFilter.GaussianBlur(1.1 * S)).resize((big.width // S, big.height // S), Image.LANCZOS)).astype(np.float32) / 255, 1, 0), 1, 1)
gap = 2                                    # espaço entre o "1" e o "5", igual ao dos outros dígitos
five_x = 308 + SH
one_w = g.width / S
ox = int(round(five_x - gap - one_w)) - 6; oy = 571 - 6

def fix(fr):
    out = cv2.inpaint(fr, hole * 255, 5, cv2.INPAINT_TELEA).astype(np.float32)
    src_f = fr.astype(np.float32)
    for lo, hi, dx in ((0, SPLIT, -SH), (SPLIT, W, SH)):
        a = np.zeros((H, W), np.float32); a[:, lo:hi] = alpha[:, lo:hi]
        a = np.roll(a, dx, 1); s = np.roll(src_f, dx, 1)
        out = out * (1 - a[..., None]) + s * a[..., None]
    h, w = one_a.shape
    reg = out[oy:oy + h, ox:ox + w]
    reg *= (1 - np.array([0.25, 0.4, 0.5]) * np.clip(one_sh * 1.6, 0, 1)[..., None])                     # sombra suave como a do texto
    reg[:] = reg * (1 - one_a[..., None]) + np.array([232, 238, 245], np.float32) * one_a[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p",
                        "-c:a", "copy", "-movflags", "+faststart", "-shortest", dst], stdin=subprocess.PIPE)
for i, fr in enumerate(allf):
    if n0 <= i <= n1: fr = fix(fr)
    enc.stdin.write(fr.tobytes())
    if i in (446, 460, 476): cv2.imwrite(dst.rsplit("/", 1)[0] + f"/chk{i}.png", fr)
enc.stdin.close(); enc.wait(); print("ok", len(allf))
