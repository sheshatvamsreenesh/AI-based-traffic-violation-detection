from ultralytics import YOLO
import cv2
import math

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture("traffic.mp4")

line_y = 300

# Store previous positions
prev_positions = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    current_positions = {}

    for result in results:
        boxes = result.boxes

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = int((x1 + x2) / 2)
            cy = int(y2)

            current_positions[i] = (cx, cy)

            # Draw box
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

            # Draw center
            cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)

            # Speed calculation
            if i in prev_positions:
                px, py = prev_positions[i]

                distance = math.sqrt((cx - px)**2 + (cy - py)**2)

                speed = int(distance * 2)  # scale factor

                cv2.putText(frame, f"Speed: {speed}",
                            (x1, y1-30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255,255,0), 2)

            # Violation detection
            if cy > line_y:
                cv2.putText(frame, "VIOLATION!",
                            (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0,0,255), 2)

    prev_positions = current_positions

    # Draw line
    cv2.line(frame, (0, line_y),
             (frame.shape[1], line_y),
             (255,0,0), 3)

    cv2.imshow("Smart Traffic System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()