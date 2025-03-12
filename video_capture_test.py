import cv2

def capture_video():
    cap = cv2.VideoCapture(0)  # Use 0 for webcam, or try changing to 1, 2, etc.
    if not cap.isOpened():
        print("Error: Could not open video device")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Video Stream Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the test
capture_video()

