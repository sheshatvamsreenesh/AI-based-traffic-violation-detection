from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
import uuid
from datetime import datetime
import cv2
from ultralytics import YOLO
from reportlab.pdfgen import canvas

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "data/uploads"
OUTPUT_FOLDER = "data/outputs"
DB_NAME = "traffic.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------- YOLO MODEL ----------------
model = YOLO("yolov8n.pt")
CLASS_NAMES = model.names

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        violation TEXT,
        amount INTEGER,
        status TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def seed_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users (username,password,role) VALUES ('user','123','user')")
    cursor.execute("INSERT OR IGNORE INTO users (username,password,role) VALUES ('police','123','police')")

    conn.commit()
    conn.close()

init_db()
seed_users()

# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "role": user[0],
            "username": username
        })

    return jsonify({"status": "fail"})

# ---------------- YOLO PROCESSING ----------------
def run_yolo_detection(video_path):
    cap = cv2.VideoCapture(video_path)

    output_image_path = os.path.join(OUTPUT_FOLDER, "result.jpg")

    violations = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        red_light = False

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = CLASS_NAMES[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if label == "person":
                color = (255, 0, 0)
            elif label in ["car", "motorcycle", "bus", "truck"]:
                color = (0, 255, 0)
            elif label == "traffic light":
                red_light = True
                color = (0, 0, 255)
            else:
                color = (200, 200, 200)

            # draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # limit spam
        if red_light and frame_id % 30 == 0:
            violations.append({
                "type": "Signal Jump",
                "fine": 1000,
                "frame": frame_id
            })

        frame_id += 1

    # save LAST frame as output image (for frontend)
    cv2.imwrite(output_image_path, frame)

    cap.release()

    return violations, output_image_path

# ---------------- VIDEO UPLOAD ----------------
@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['file']
    username = request.form.get("username", "user")

    filename = str(uuid.uuid4()) + ".mp4"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    violations, output_image = run_yolo_detection(path)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for v in violations:
        cursor.execute("""
            INSERT INTO challans (username, violation, amount, status, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            v["type"],
            v["fine"],
            "unpaid",
            str(datetime.now())
        ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "violations": violations,
        "output": output_image   # ✅ matches frontend
    })

# ---------------- USER CHALLANS ----------------
@app.route('/challans/<username>')
def get_challans(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT violation, amount, status, date
        FROM challans
        WHERE username=?
    """, (username,))

    data = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "violation": r[0],
            "amount": r[1],
            "status": r[2],
            "date": r[3]
        }
        for r in data
    ])

# ---------------- PAY ----------------
@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    username = data['username']
    violation = data['violation']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE challans
        SET status='paid'
        WHERE username=? AND violation=?
    """, (username, violation))

    conn.commit()
    conn.close()

    return jsonify({"status": "paid"})

# ---------------- INVOICE ----------------
@app.route('/invoice/<username>')
def invoice(username):
    file_path = os.path.join(OUTPUT_FOLDER, f"{username}_invoice.pdf")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT violation, amount, status
        FROM challans
        WHERE username=?
    """, (username,))

    data = cursor.fetchall()
    conn.close()

    pdf = canvas.Canvas(file_path)
    pdf.drawString(100, 800, f"Traffic Invoice - {username}")

    y = 750
    for d in data:
        pdf.drawString(100, y, f"{d[0]} | ₹{d[1]} | {d[2]}")
        y -= 30

    pdf.save()

    return send_file(file_path, as_attachment=True)

# ---------------- POLICE ----------------
@app.route('/police/violations')
def police_dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM challans")
    data = cursor.fetchall()

    conn.close()

    return jsonify(data)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
