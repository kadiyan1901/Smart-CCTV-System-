#loading the pre trained model 
import tensorflow as tf
import numpy as np

# Step 1: Load the Pre-Trained Model
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=True)

# Step 2: Convert the Model to TensorFlow Lite Format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the converted model to a file
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
#   


