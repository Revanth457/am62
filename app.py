import cv2
from flask import Flask, Response

# Initialize Flask application
app = Flask(__name__)

# OpenCV webcam capture
video_capture = cv2.VideoCapture(0)  # 0 is usually the default webcam

def generate_frames():
    while True:
        # Capture frame-by-frame from the webcam
        success, frame = video_capture.read()  # Read a frame
        if not success:
            break
        else:
            # Convert frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as part of multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    # Serve the video stream to the browser
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the Flask app on all available interfaces (0.0.0.0)
    app.run(host='192.168.1.46', port=5000, debug=True)
