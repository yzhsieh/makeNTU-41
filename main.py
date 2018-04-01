import RPi.GPIO as GPIO
from threading import Thread
from app import *
from asrk import asr_model
import smbus
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP) #IR sensor
GPIO.setup(18,GPIO.OUT) #light
GPIO.setup(17,GPIO.OUT) #white
GPIO.setup(6,GPIO.OUT) #yellow
GPIO.setup(13,GPIO.OUT) #blue
GPIO.setup(19,GPIO.OUT) #green
GPIO.setup(26,GPIO.OUT) #red
address=0x04
bus=smbus.SMBus(1)
cmd={'b':0,'w':1,'s':2,'d':3,'a':4,'x':-1}
ws = None

def IR_callback(channel):
	global ws
	Status.state['detecting']=True
	if Status.step<=2:
		Status.state['detecting']=False
		return
	GPIO.output(18,True)
	time.sleep(0.5)
	Status.state["keepGoing"]=False
	if ws.take_a_shot():
		GPIO.output(18,False)
	else:
		while not Status.state["keepGoing"]:
			GPIO.output(18,False)
			GPIO.output(17,True)
			GPIO.output(6,True)
			GPIO.output(13,True)
			GPIO.output(19,True)
			GPIO.output(26,True)
			time.sleep(0.1)
			GPIO.output(18,True)
			GPIO.output(17,False)
			GPIO.output(6,False)
			GPIO.output(13,False)
			GPIO.output(19,False)
			GPIO.output(26,False)
			time.sleep(0.1)
	GPIO.output(18,False)
	GPIO.output(17,False)
	GPIO.output(6,True)
	GPIO.output(13,False)
	GPIO.output(19,False)
	GPIO.output(26,False)    
	Status.state['detecting']=False
	Status.step=0

class carThread(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		GPIO.output(18,False)
		GPIO.output(17,False)
		GPIO.output(6,False)
		GPIO.output(13,False)
		GPIO.output(19,False)
		GPIO.output(26,False)
 
		while True:
			if Status.state["setUp"]:
				GPIO.output(26,True)
				idx=0
				while Status.state["setUp"] and idx<=1:
					GPIO.output(26,False)
					time.sleep(0.3)
					GPIO.output(26,True)
					Status.motionCommand[idx]=Status.model.recognize()
					if idx==0 and Status.motionCommand[0]!=0 and Status.motionCommand[0]!=1 and Status.motionCommand[0]!=2:
						continue
					if idx==0:
						GPIO.output(19,True)
						idx+=1
					elif idx==1 and Status.motionCommand[1]!=10:
						GPIO.output(13,True)
						idx+=1
				f=open('cmd.txt','w')
				if Status.motionCommand[0]==1: #square
					n=Status.motionCommand[1]
					for k in range(0,n):
						f.write('w'+',')
					for k in range(0,n):
						f.write('s'+',')
				elif Status.motionCommand[0]==2: #spin
					n=Status.motionCommand[1]
					for i in range(0,n):
						f.write('a'+',')
					for i in range(0,n):
						f.write('d'+',')
				elif Status.motionCommand[0]==0: #stop
					f.write('b'+',')
				f.write('x')
				GPIO.output(13,False)
				GPIO.output(19,False)
				GPIO.output(26,False)
				Status.state["setUp"]=False
				f.close()
			elif Status.state["execution"]:
				f=open("cmd.txt",'r') 
				line=f.readline()
				currentline=line.split(",")
				GPIO.output(6,True)
				Status.state["manual"]=False
				Status.state["move"]=0
				GPIO.add_event_detect(23,GPIO.RISING,callback=IR_callback)
				while Status.state["execution"]:
					for key in currentline:
						while Status.state["manual"]:
							if Status.state["move"]==1: # turn left
								bus.write_byte(address,cmd['a'])
								Status.state["move"]=0
							elif Status.state["move"]==2: # turn right
								bus.write_byte(address,cmd['d'])
								Status.state["move"]=0
						while Status.state['detecting']:
							a=1
						bus.write_byte(address,cmd[key])
						Status.step+=1
						time.sleep(1.5)
						if not Status.state['execution']:
							GPIO.remove_event_detect(23)
							GPIO.output(6,False)
							f.close()
							break
				GPIO.remove_event_detect(23)
				GPIO.output(6,False)
				f.close()

Obj=carThread()

if __name__=="__main__":
	global ws
	Obj.start()
	print("OAO")
	ws = webService()
	ws.app.run(host='0.0.0.0', threaded=True)
