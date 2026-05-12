from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
import uuid
from datetime import datetime
import cv2
from ultralytics import YOLO
from reportlab.pdfgen import canvas

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "data/uploads"
OUTPUT_FOLDER = "data/outputs"
DB_NAME = "traffic.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")
CLASS_NAMES = model.names

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
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

    cursor.execute("SELECT * FROM users")
    if not cursor.fetchall():
        cursor.execute("INSERT INTO users VALUES (NULL,'police1','1234','police')")
        cursor.execute("INSERT INTO users VALUES (NULL,'user1','1234','user')")

    conn.commit()
    conn.close()

init_db()
seed_users()

# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (data['username'], data['password'])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "role": user[0],
            "username": data['username']
        })

    return jsonify({"status": "fail"})

# ---------------- YOLO ----------------
def run_yolo(video_path):
    cap = cv2.VideoCapture(video_path)

    output_path = os.path.join(OUTPUT_FOLDER, "result.avi")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

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
                person = True
            elif label == "traffic light":
                red_light = True

            if label == "traffic light":
                red_light = True
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)

            cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
            cv2.putText(frame, label, (x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if red_light:
            violations.append({
                "type": "Signal Jump",
                "fine": 1000
            })

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()

    return violations, output_path

# ---------------- UPLOAD ----------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    username = request.form.get("username", "user1")

    filename = str(uuid.uuid4()) + ".mp4"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    violations, output = run_yolo(path)

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
        "violations": violations
    })

# ---------------- GET CHALLANS ----------------
@app.route('/challans/<username>')
def get_challans(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT violation, amount, status, date
    FROM challans WHERE username=?
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

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE challans SET status='paid'
    WHERE username=? AND violation=?
    """, (data['username'], data['violation']))

    conn.commit()
    conn.close()

    return jsonify({"status": "paid"})

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
