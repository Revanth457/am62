import cv2
import torch
from flask import Flask, Response

# Initialize Flask application
app = Flask(__name__)

# Load YOLOv5 model (pre-trained or custom model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # You can replace 'yolov5n' with other models like 'yolov5s', 'yolov5m'

# Open the video capture device (use 0 for the default webcam)
cap = cv2.VideoCapture(0)  # Use 0 for default camera, or provide another index if needed

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Function to generate video frames for streaming
def gen():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform YOLOv5 inference
        results = model(frame)  # Perform detection on the frame

        # Render bounding boxes and labels on the frame
        frame = results.render()[0]  # results.render() returns a list of frames with annotations

        # Convert frame to JPEG for streaming over HTTP
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_data = jpeg.tobytes()

        # Yield the JPEG frame as part of an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

# Route for streaming video
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the Flask server
if __name__ == '__main__':
    print("Server running at http://<your-ip>:5000")
    app.run(host='0.0.0.0', port=5000)
