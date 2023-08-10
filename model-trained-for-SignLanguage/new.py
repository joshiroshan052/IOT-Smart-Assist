import base64
import io
import json

from PIL import Image
import numpy as np
from flask import Flask, request, jsonify
import tensorflow as tf

app = Flask(__name__)

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Preprocess the image
def preprocess_image(image):
    image = image.resize((input_details[0]['shape'][2], input_details[0]['shape'][1]))
    image = np.expand_dims(image, axis=0)
    image = (image - input_details[0]['quantization'][0]) / input_details[0]['quantization'][1]
    image = image.astype(input_details[0]['dtype'])
    return image

# Perform object detection on the image
def run_inference(image):
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.json:
        return jsonify({'error': 'Image not found in the request'}), 400

    # Decode and preprocess the image
    image_data = base64.b64decode(request.json['image'])
    image = Image.open(io.BytesIO(image_data))
    preprocessed_image = preprocess_image(image)

    # Run inference
    predictions = run_inference(preprocessed_image)

    # Get the predicted label
    label = 'Label'  # Replace with your logic to get the label from predictions

    return jsonify({'label': label})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
