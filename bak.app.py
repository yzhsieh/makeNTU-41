#!/usr/bin/env python
from PIL import Image
from importlib import import_module
import os
import io
import time
from flask import Flask, render_template, Response, request
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera


flag = 0


app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    global flag
    """Video streaming generator function."""
    while True:
        time.sleep(0.05)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def shot_and_gen(camera):
    global flag
    """Video streaming generator function."""
    frame = camera.get_frame()
    image = Image.open(io.BytesIO(frame))
    image.save('test.jpg')

    while True:
        time.sleep(0.05)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shot_and_video_feed')
def shot_and_video_feed():
    return Response(shot_and_gen(Camera()),
                mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        print(">>>>>>>>>>>>in GET method")
        return render_template('test.html')
    else:
        print(">>>>>>>>>>>>in POST method")
        return render_template('test.html', btn=request.form['type'])



@app.route('/status', methods=['GET', 'POST'])
def status():
    if request.method == "GET":
        print(">>>>>>>>>>>>in GET method")    
        return render_template("status.html", status="Good", shot=0)
    else:
        print(">>>>>>>>>>>>in POST method")
        return render_template("status.html", status="Good", shot=1)



if __name__ == '__main__':
     app.run(host='0.0.0.0', threaded=True)
    #app.run()
