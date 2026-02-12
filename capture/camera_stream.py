import cv2
import subprocess
import time
import json
import redis
import base64
from object_detection import detect

RTSP_URL = "rtsp://mediamtx:8554/mystream"
VIDEO_SOURCE = "ssb-ssb-rupaidiha-camera-1-1743155228233.stream.mp4"


r = redis.Redis(host="redis", port=6379)

def encode_image(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")

def start_stream():
    print("Starting AI stream...")

    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        raise RuntimeError("Could not open video source")
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Could not read first frame")
    height, width, _ = frame.shape
    fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ffmpeg = subprocess.Popen([
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-f", "rtsp",
        RTSP_URL
    ], stdin=subprocess.PIPE)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        if frame_count % 10 == 0:
            annotated, detections = detect(frame)
            if detections:
                data = {
                    "timestamp": time.time(),
                    "objects": list(set(detections)),
                }
                r.rpush("detections", json.dumps(data))
                r.ltrim("detections", -500, -1)
        ffmpeg.stdin.write(frame.tobytes())
        frame_count += 1
        time.sleep(1 / fps)

if __name__ == "__main__":
    while True:
        try:
            start_stream()
        except Exception as e:
            print("Stream crashed, restarting:", e)
            time.sleep(2)
