from flask import Flask, render_template, Response
import cv2
import torch
from detect import detect  # Import your YOLOv7 detection function

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Open the webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Run YOLOv7 detection
            detect()

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in a format Flask can stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera')
def start_camera():
    global camera
    if not camera.isOpened():
        camera.open(0)
    return "Camera started"

@app.route('/stop_camera')
def stop_camera():
    global camera
    if camera.isOpened():
        camera.release()
    return "Camera stopped"

if __name__ == '__main__':
    app.run(debug=True)
