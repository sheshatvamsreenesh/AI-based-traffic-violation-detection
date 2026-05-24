from ultralytics import YOLO
import cv2
model = YOLO("yolov8n.pt")
image = cv2.imread("data/samples/traffic.jpg")
if image is None:
    raise RuntimeError("Could not read data/samples/traffic.jpg")
results = model(image)
annotated_frame = results[0].plot()
try:
    cv2.imshow("Vehicle Detection", annotated_frame)
    cv2.waitKey(0)
finally:
    cv2.destroyAllWindows()
