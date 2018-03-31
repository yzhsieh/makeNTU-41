#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
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
    return render_template("status.html", status="Good")


if __name__ == '__main__':
    # app.run(host='0.0.0.0', threaded=True)
    app.run()
