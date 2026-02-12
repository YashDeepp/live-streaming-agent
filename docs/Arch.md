## 1 Technology

### 1.1 Video Processing

- OpenCV for video frame capture
- FFmpeg for encoding and RTSP publishing
- H.264 (yuv420p) for browser compatibility

Reason:
FFmpeg provides stable, industry-standard encoding and RTSP publishing. OpenCV allows flexible frame processing for AI integration.

---

### 1.2 Streaming Protocol

- RTSP for ingestion
- HLS for browser playback

Reason:
RTSP is widely used for camera ingestion.
HLS is universally supported in modern browsers and suitable for scalable delivery.

---

### 1.3 Streaming Server

- MediaMTX (open-source RTSP/HLS server)

Reason:
MediaMTX supports RTSP ingest and automatic HLS generation, making it ideal for a lightweight streaming backend.

---

### 1.4 AI Framework

- YOLOv8 (Ultralytics)
- PyTorch backend

---

### 1.5 Metadata Storage

- Redis
---

### 1.6 Backend API

- FastAPI

---

## 2 Detailed Component Design

### 2.1 Capture & AI Service

Responsibilities:
- Read frames from video/source
- Run detection every 10 frames
- Store metadata in Redis
- Stream original frames to RTSP

Detection frequency optimization:
Detection runs every 10 frames to reduce CPU usage while maintaining adequate detection coverage.

---

### 2.2 Streaming Pipeline

The capture service sends raw frames to FFmpeg.
FFmpeg encodes frames using:

- H.264
- yuv420p pixel format
- ultrafast preset
- zerolatency tuning

FFmpeg publishes the stream via RTSP to MediaMTX.

MediaMTX converts RTSP stream into HLS segments for browser playback.

---

### 2.3 AI Inference

YOLOv8 nano coco model is used for detection.

Performance optimizations:
- Detection every 10 frames

Detection results include:
- Timestamp
- Object labels
- Annotated snapshot - removed due to increased fetching and search time have (attached working snap)
---