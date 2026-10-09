import sys, json, cv2, mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
video, model, out = sys.argv[1:4]
opts = vision.HandLandmarkerOptions(base_options=mpp.BaseOptions(model_asset_path=model),
    running_mode=vision.RunningMode.VIDEO, num_hands=2, min_hand_detection_confidence=0.4, min_tracking_confidence=0.4)
lm = vision.HandLandmarker.create_from_options(opts)
cap = cv2.VideoCapture(video); fps = cap.get(cv2.CAP_PROP_FPS); i = 0; res = []
while True:
    ok, fr = cap.read()
    if not ok: break
    if i % 2 == 0:  # 15 Hz
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
        r = lm.detect_for_video(img, int(i * 1000 / fps))
        hands = []
        for h, hd in zip(r.hand_landmarks, r.handedness):
            # palm center = mean of wrist(0), index MCP(5), pinky MCP(17), middle MCP(9)
            pts = [h[k] for k in (0, 5, 9, 17)]
            cx = sum(p.x for p in pts) / 4 * 1080; cy = sum(p.y for p in pts) / 4 * 1920
            # palm facing up/open heuristic: fingertips spread, tip of middle above? store tips too
            tips = [(round(h[k].x * 1080), round(h[k].y * 1920)) for k in (4, 8, 12, 16, 20)]
            hands.append({"side": hd[0].category_name, "cx": round(cx), "cy": round(cy), "tips": tips})
        res.append({"t": round(i / fps, 3), "hands": hands})
    i += 1
json.dump(res, open(out, "w"))
print("frames", len(res))
