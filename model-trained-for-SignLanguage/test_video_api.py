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

    # Get the webcam feed
    camera = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the webcam
        ret, frame = camera.read()

        # Print the status of the camera
        print(camera.isOpened())

        # Preprocess the frame
        processed_frame = preprocess_frame(frame)

        # Run inference on the preprocessed frame
        input_data = np.expand_dims(processed_frame, axis=0)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Process the output_data as needed (get predictions, convert to text, etc.)
        predictions = process_output_data(output_data)

        # Display the predictions on the frame
        for prediction in predictions:
            x, y, w, h = prediction[0:4]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, prediction[5], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

        # Display the frame
        cv2.imshow('Object Detection', frame)

        # Quit if the user presses ESC
        if cv2.waitKey(1) == 27:
            break

        # Release the webcam
        camera.release()
        cv2.destroyAllWindows()
        return jsonify({'alphabet': predictions})
        # Release the webcam
    camera.release()
    cv2.destroyAllWindows()
    return jsonify({'alphabet': predictions})
def preprocess_frame(frame):
    # Placeholder function for preprocessing the frames
    # Modify this function according to your preprocessing requirements

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the frame to the desired size
    resized_frame = cv2.resize(gray_frame, (224, 224))

    # Normalize the frame
    normalized_frame = resized_frame / 255.0

    return normalized_frame
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
