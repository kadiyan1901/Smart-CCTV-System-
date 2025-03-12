#time based monitoring system and taking updates from the telegram bot 
import cv2
import numpy as np
import requests
import time

# Absolute paths to the YOLO configuration and weights files
config_path = "C:/Users/welcome/Desktop/NLP-main/yolov4-tiny.cfg"
weights_path = "C:/Users/welcome/Desktop/NLP-main/yolov4-tiny.weights"

# Load YOLO
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open("C:/Users/welcome/Desktop/NLP-main/coco.names", "r") as f:
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

def detect_person(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Initialization
    class_ids = []
    confidences = []
    boxes = []

    # For each detection from each output layer, get the confidence, class id, bounding box params
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONFIDENCE_THRESHOLD and classes[class_id] == 'person':
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply non-max suppression to remove multiple boxes for the same object
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
    
    # Encode frame as JPEG and send as photo
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

def capture_video():
    global last_alert_time
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            person_detected, boxes, confidences, class_ids, indexes = detect_person(frame)
            detections_history.append(person_detected)

            if should_send_alert():
                last_alert_time = time.time()
                send_telegram_alert("Person detected!", frame)
            
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def should_send_alert():
    global last_alert_time

    # Check cooldown period
    current_time = time.time()
    if current_time - last_alert_time < COOLDOWN_PERIOD:
        return False

    # Check if majority of recent frames detect a person
    consistent_detection = sum(detections_history[-HISTORY_FRAMES:]) > (HISTORY_FRAMES / 2)
    return consistent_detection

if __name__ == "__main__":
    capture_video()





































