# Test if the files are accessible
try:
    with open("C:\\Users\\welcome\\Desktop\\NLP-main\\yolov4-tiny.cfg", "r") as f:
        print("yolov4-tiny.cfg is accessible")
    with open("C:\\Users\\welcome\\Desktop\\NLP-main\\yolov4-tiny.weights", "r") as f:
        print("yolov4-tiny.weights is accessible")
    with open("C:\\Users\\welcome\\Desktop\\NLP-main\\coco.names", "r") as f:
        print("coco.names is accessible")
except Exception as e:
    print(f"Error accessing files: {e}")


