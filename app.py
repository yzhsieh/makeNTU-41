#!/usr/bin/env python
from PIL import Image
from importlib import import_module
import os
import io
import time
import requests
from shutil import copyfile
from flask import Flask, render_template, Response, request, abort, send_file
# import camera driver
if os.environ.get('CAMERA'):
	Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
	from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera
import face_recognition
from asrk import asr_model

class status:
	def __init__(self):
		self.state={"setUp":False,"execution":False,"keepGoing":True,"manual":False,'move':0,'detecting':False}
		self.model=asr_model()
		self.motionCommand=[9,0]
		self.step = 0
Status=status()

TEMP = None
class webService():

	def __init__(self):
		print("initialize web service")
		if(os.path.isfile("./show.jpg")):
			print("[init] delete show.jpg")
			os.remove("./show.jpg")
		flag = 0
		self.app = Flask(__name__)
		self.app.add_url_rule('/', 'index', self.index)
		self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)
		self.app.add_url_rule('/shot_and_video_feed', 'shot_and_video_feed', self.shot_and_video_feed)
		self.app.add_url_rule('/test', 'test', self.test, methods=['GET', 'POST'])
		self.app.add_url_rule('/status', 'status', self.status, methods=['GET', 'POST'])
		self.app.add_url_rule('/yohao', 'yohao', self.yohao, methods=['GET', 'POST'])
		self.app.add_url_rule('/shot', 'shot', self.shot)
		self.app.add_url_rule('/show.jpg', 'show', self.show)

	def index(self):
		"""Video streaming home page."""
		return render_template('index.html')

	def show(self):
		return send_file("./show.jpg")


	def shot(self, camera = Camera()):
		frame = camera.get_frame()
		image = Image.open(io.BytesIO(frame))
		image.save('test.jpg')
		print("image saved")
		abort(400)

	def gen(self, camera):
		global flag
		"""Video streaming generator function."""
		while True:
			time.sleep(0.1)
			frame = camera.get_frame()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	def shot_and_gen(self, camera=Camera(), path=None):
		global flag
		"""Video streaming generator function."""
		frame = camera.get_frame()
		image = Image.open(io.BytesIO(frame))
		# image.thumbnail((1000,250))
		if TEMP:
			image.save(TEMP + ".jpg")
		else:
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

	def shot_and_video_feed(self, path=None):
		return Response(self.shot_and_gen(Camera(), path),
					mimetype='multipart/x-mixed-replace; boundary=frame')


	def test(self):
		if request.method == "GET":
			print(">>>>>>>>>>>>in GET method")
			return render_template('test.html')
		else:
			print(">>>>>>>>>>>>in POST method")
			return render_template('test.html', btn=request.form['type'])



	def status(self, shot=0):
		if request.method == "GET":
			print(">>>>>>>>>>>>in GET method")	
			return render_template("status.html", status="Good", shot=shot)
		else:
			print(">>>>>>>>>>>>in POST method")
			if "cmd" in request.form:
				print(request.form["cmd"])
				Status.state[request.form["cmd"]] = True
			if "turnRight" in request.form:
				Status.state['move'] = 1
				Status.state['manual'] = True
			elif "turnLeft" in request.form:
				Status.state['move'] = 2
				Status.state['manual'] = True
			elif "keepGoing" in request.form:
				Status.state["manual"] = False
				Status.state["keepGoing"] = True
			elif "stopExec" in request.form:
				print("[Button pressed] : stopExec")
				Status.state["execution"] = False

			# if Status.state["detecting"]:
				# while not os.path.isfile("./show.jpg"):
					# print("wait")
					# time.sleep(0.1)
				# copyfile('./show.jpg', './show2.jpg')
				# os.remove('./show.jpg')
				# return render_template("status.html", status="setting", show=1)
			if Status.state["setUp"] == True:
				return render_template("status.html", status="setting", shot=0, show=0)
			return render_template("status.html", status="Good", shot=1, show=0)

	def yohao(self):
		global TEMP
		if request.method == "GET":
			return render_template("yohao.html", status="Good", shot=0)
		else:
			text = request.form['text']
			print(">>>>>>>>>>>>" + text)
			TEMP = text
			return render_template("yohao.html", status="Good", shot=1)

	def take_a_shot(self):
		try:
			camera = Camera()
			frame = camera.get_frame()
		except picamera.exc.PiCameraMMALError:
			# self.shot_and_video_feed()
			self.status()
			print("re render and save")
		except PiCameraMMALError:
			# self.shot_and_video_feed()
			self.status()
			print("re render and save")
		else:
			print("direct get picture and save")
			image = Image.open(io.BytesIO(frame))
			image.save('test.jpg')

		rst = face_recognition.family_or_not()
		print(rst)
		return rst
	''' end of class definition'''
			
if __name__ == '__main__':
	WS = webService()
	WS.app.run(host='0.0.0.0', threaded=True)
	#app.run()
