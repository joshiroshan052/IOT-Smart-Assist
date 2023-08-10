from flask import Flask, request, jsonify
import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)
interpreter = tf.lite.Interpreter(model_path='model.tflite')  # Load your TFLite model
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.route('/process_frames', methods=['POST'])
def process_frames():
    if 'frames' not in request.files:
        return jsonify({'error': 'No frames found'})

    frames_file = request.files['frames']
    frames_array = np.fromfile(frames_file, np.uint8)  # Convert frames file to numpy array
    frames = cv2.imdecode(frames_array, cv2.IMREAD_COLOR)  # Decode the frames array as images

    # Preprocess frames as needed (resize, normalize, etc.)
    preprocessed_frames = preprocess_frames(frames)

    # Run inference on the preprocessed frames
    input_data = np.expand_dims(preprocessed_frames, axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Process the output_data as needed (get predictions, convert to text, etc.)
    predictions = process_output_data(output_data)

    return jsonify({'alphabet': predictions})

def preprocess_frames(frames):
    # Placeholder function for preprocessing the frames
    # Modify this function according to your preprocessing requirements
    processed_frames = frames  # Replace with actual preprocessing steps
    return processed_frames

def process_output_data(output_data):
    # Placeholder function for processing the output data
    # Modify this function according to your post-processing requirements
    predictions = output_data  # Replace with actual post-processing steps
    return predictions

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
