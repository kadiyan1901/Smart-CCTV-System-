from flask import Flask, render_template, Response
import cv2
import numpy as np
import time
from datetime import datetime
import requests

app = Flask(__name__)

# Absolute paths to the YOLO configuration and weights files
config_path = "C:\\Users\\welcome\\Desktop\\NLP-main\\yolov4-tiny.cfg"
weights_path = "C:\\Users\\welcome\\Desktop\\NLP-main\\yolov4-tiny.weights"

# Load YOLO
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open("C:\\Users\\welcome\\Desktop\\NLP-main\\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Telegram bot details
TELEGRAM_BOT_TOKEN = '7732922339:AAHJsfwOnDWcs-Z5Eu1UqDbT3uq5are9izk'
CHAT_ID = '7986442227'

# Settings
COOLDOWN_PERIOD = 10  # seconds
CONFIDENCE_THRESHOLD = 0.5
HISTORY_FRAMES = 10  # Number of frames to analyze for consistency

# Initialize variables
last_alert_time = 0
detections_history = []

cap = cv2.VideoCapture(0)

def detect_person(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONFIDENCE_THRESHOLD and classes[class_id] == 'person':
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, 0.4)
    if len(indexes) > 0:
        return True, boxes, confidences, class_ids, indexes
    return False, boxes, confidences, class_ids, indexes

def send_telegram_alert(message, frame):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Alert sent successfully.")
    else:
        print("Failed to send alert.")
    
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()

    photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    files = {'photo': frame_bytes}
    data = {'chat_id': CHAT_ID}
    
    response = requests.post(photo_url, files=files, data=data)
    if response.status_code == 200:
        print("Photo sent successfully.")
    else:
        print("Failed to send photo.")

def should_send_alert():
    global last_alert_time
    current_time = time.time()
    if current_time - last_alert_time < COOLDOWN_PERIOD:
        return False
    consistent_detection = sum(detections_history[-HISTORY_FRAMES:]) > (HISTORY_FRAMES / 2)
    return consistent_detection

def generate_frames():
    global last_alert_time
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            person_detected, boxes, confidences, class_ids, indexes = detect_person(frame)
            detections_history.append(person_detected)

            if should_send_alert():
                last_alert_time = time.time()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = f"Person detected!\nTimestamp: {timestamp}\nLocation: [Your Location]"
                send_telegram_alert(message, frame)
            
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)







