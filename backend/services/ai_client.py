import requests

AI_SERVICE_URL = "http://localhost:5000/process"

def send_to_ai(video_id, file_path):
    try:
        requests.post(AI_SERVICE_URL, json={
            "video_id": video_id,
            "video_path": file_path
        })
    except Exception as e:
        print("AI service error:", e)