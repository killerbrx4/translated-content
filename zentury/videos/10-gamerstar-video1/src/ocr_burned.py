"""Acha a legenda queimada do original com OCR (RapidOCR) no vídeo ORIGINAL (não espelhado, onde a legenda é legível),
10 quadros/s, e guarda as caixas já convertidas para o vídeo espelhado 1080x1920 (sem zoom de câmera).
Conta o texto que bate com palavras da transcrição (o texto das caixas sai espelhado e não bate) ou que tem o tamanho de letra da legenda.
Uso: <python com rapidocr> -I src/ocr_burned.py <video original>   →   src/burned.json"""
import json, subprocess, sys, unicodedata, re, numpy as np
from rapidocr_onnxruntime import RapidOCR
SRC = sys.argv[1]; FPS = 10; W, H = 960, 1708; Y0 = int(H * 0.55)
norm = lambda s: re.sub(r"[^A-Z0-9 ]", "", unicodedata.normalize("NFKD", s.upper()).encode("ascii", "ignore").decode())
VOC = {norm(w) for w, _ in json.load(open("src/words.json"))} | {"40", "70", "50", "60", "TI", "4070", "5060"}
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
ocr = RapidOCR(); out = []
for k, f in enumerate(fr):
    res, _ = ocr(np.ascontiguousarray(f[Y0:]))
    boxes = []
    for pts, txt, conf in res or []:
        toks = [t for t in norm(txt).split() if t]
        xs = [p[0] for p in pts]; ys = [p[1] + Y0 for p in pts]
        voc = toks and sum(t in VOC for t in toks) >= max(1, len(toks) // 2 + len(toks) % 2)
        big = (max(ys) - min(ys)) >= 58 and min(ys) > 1180  # letra no tamanho da legenda (texto das caixas é menor)
        if conf < 0.6 or not (voc or (big and conf >= 0.75)): continue
        # espelha x e passa para 1080x1920
        boxes.append([round(1080 - max(xs) * 1080 / W), round(1080 - min(xs) * 1080 / W), round(min(ys) * 1920 / H), round(max(ys) * 1920 / H), txt])
    out.append(boxes)
    if k % 50 == 0: print(k, boxes, flush=True)
json.dump({"fps": FPS, "frames": out}, open("src/burned.json", "w"), ensure_ascii=False)
print("ok", len(out))
