import tensorflow as tf

# Path to the saved model directory
saved_model_dir = r'C:\Users\welcome\Desktop\NLP-main\tensorflow-yolov4-tflite\checkpoints\yolov4-tiny-416'
output_path = 'yolov4-tiny.tflite'

# Convert the model to TensorFlow Lite with Select Ops
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # Use TensorFlow Lite built-in ops.
    tf.lite.OpsSet.SELECT_TF_OPS  # Enable TensorFlow Select ops.
]
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open(output_path, 'wb') as f:
    f.write(tflite_model)

print("Model conversion to TensorFlow Lite completed with Select Ops!")






