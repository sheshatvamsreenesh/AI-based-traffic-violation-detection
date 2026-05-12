from ultralytics import YOLO
import cv2
model = YOLO("yolov8n.pt")
image = cv2.imread("data/samples/traffic.jpg")
results = model(image)
annotated_frame = results[0].plot()
cv2.imshow("Vehicle Detection", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
