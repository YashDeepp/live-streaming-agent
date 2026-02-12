from ultralytics import YOLO
model = YOLO("yolov8n.pt")
def detect(frame):
    results = model(frame, verbose=False)
    detections = []
    annotated = frame.copy()
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            detections.append(label)
    annotated = results[0].plot()
    return annotated, detections
