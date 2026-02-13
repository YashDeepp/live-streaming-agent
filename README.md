# Live Video Streaming 

This project demonstrates a real-time video streaming solution with integrated AI-based object detection and searchable metadata.

The system captures video (MP4 or camera), performs object detection using YOLO (PyTorch), streams the original video via RTSP → HLS, and stores detection results in Redis for search and retrieval.

---

##  How to Run

Make sure Docker and Docker Compose are installed.

Replace the `VIDEO_SOURCE` value with actual source path/0/rtsp in capture/camera_stream.py

From the root directory of the project, simply run:

```bash
cd docker

docker compose up --build
```

This will start the following services:

- MediaMTX (RTSP + HLS streaming server)

- Capture service (video processing + AI detection)

- Backend API (FastAPI)

- Redis (metadata storage)

HLS Stream URL - `http://localhost:8888/mystream/index.m3u8`

For Video Playback - `web/index.html` (wait for 30-35 sec after opening the page)

For Search from Redis - `web/search.html` or `http://localhost:8000/search?objects=person,car`

## To close the application
```bash
docker compose down
```
