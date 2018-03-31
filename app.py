#!/usr/bin/env python
from PIL import Image
from importlib import import_module
import os
import io
import time
import requests
from flask import Flask, render_template, Response, request
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

class webService():

    def __init__(self):
        flag = 0
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)
        self.app.add_url_rule('/shot_and_video_feed', 'shot_and_video_feed', self.shot_and_video_feed)
        self.app.add_url_rule('/test', 'test', self.test, methods=['GET', 'POST'])
        self.app.add_url_rule('/status', 'status', self.status, methods=['GET', 'POST'])

    def index(self):
        """Video streaming home page."""
        return render_template('index.html')


    def gen(self, camera):
        global flag
        """Video streaming generator function."""
        while True:
            time.sleep(0.05)
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def shot_and_gen(self, camera):
        global flag
        """Video streaming generator function."""
        frame = camera.get_frame()
        image = Image.open(io.BytesIO(frame))
        # image.thumbnail((1000,250))
        image.save('test.jpg')

        while True:
            time.sleep(0.05)
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video_feed(self):
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def shot_and_video_feed(self):
        return Response(self.shot_and_gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


    def test(self):
        if request.method == "GET":
            print(">>>>>>>>>>>>in GET method")
            return render_template('test.html')
        else:
            print(">>>>>>>>>>>>in POST method")
            return render_template('test.html', btn=request.form['type'])



    def status(self):
        if request.method == "GET":
            print(">>>>>>>>>>>>in GET method")    
            return render_template("status.html", status="Good", shot=0)
        else:
            print(">>>>>>>>>>>>in POST method")
            print(request.form)
            return render_template("status.html", status="Good", shot=1)

    ''' end of class definition'''
def take_a_shot():
    print("let's take a shot")
    r = requests.post(url = '0.0.0.0:5000/shot_and_video_feed', data = [])

if __name__ == '__main__':
    WS = webService()
    WS.app.run(host='0.0.0.0', threaded=True)
    #app.run()
