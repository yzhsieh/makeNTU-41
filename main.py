import RPi.GPIO as GPIO
from threading import Thread
import app
# from asr import asr_model
import smbus
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=PUD_UP) #IR sensor
GPIO.setup(18,GPIO.OUT) #light
GPIO.setup(17,GPIO.OUT) #white
GPIO.setup(6,GPIO.OUT) #yellow
GPIO.setup(13,GPIO.OUT) #blue
GPIO.setup(19,GPIO.OUT) #green
GPIO.setup(26,GPIO.OUT) #red
address=0x04
bus=smbus.SMBus(1)
cmd={'b':0,'w':1,'s':2,'d':3,'a':4,'x':-1}

class status:
    def __init__(self):
        self.state={"setUp":False,"execution":False,"keepGoing":True,"manual":False,'move':0}
        self.model=asr_model()
        self.motionCommand="90"

Status=status()

def IR_callback(channel):
    GPIO.output(18,True)
    Status.state["keepGoing"]=False
    
    if app.take_a_shot():
        GPIO.output(18,False)
        return
    else
        while !Status.state["keepGoing"]:
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


class carThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
    	GPIO.output(17,True)
        while True:
            if Status.state["setUp"]:
            	GPIO.output(26,True)
                idx=0
                while Status.state["setUp"] or idx<=1:
                    Status.motionCommand[idx]=Status.model.recognize()
                    if Status.motionCommand[0]=="9":
                    	continue
                    if idx==0:
                    	GPIO.output(19,True)
                    elif idx==1:
                    	GPIO.output(13,True)
                    idx+=1
                f.open('cmd.txt',w)
                if Status.motionCommand[0]=="0": #square
                	n=int(Status.motionCommand[1])
                	for i in range(0,4):
                		for k in range(0,n):
                			f.write('w')
                		for k in range(0,4):
                			f.write('a')
                elif Status.motionCommand[0]=="1": #spin
                	f.write('a')
                elif Status.motionCommand[0]=="2": #stop
                	f.write('b')
                GPIO.output(13,False)
            	GPIO.output(19,False)
            	GPIO.output(26,False)
                f.close()
            elif Status.state["execution"]:
                f=open("cmd.txt",'r')
                GPIO.add_event_detect(23,GPIO.RISING,callback=IR_callback)
                line=f.readline()
                currentline=line.split(",")
                GPIO.output(6,True)
                Status.state["manual"]=False
                Status.state["move"]=0
                while Status.state["execution"]:
                    for key in currentline:
                        while Status.state["manual"]:
                            if Status.state["move"]==1: # turn left
                                bus.write_byte(address,cmd[4])
                                Status.state["move"]=0
                            elif Status.state["move"]==2: # turn right
                                bus.write_byte(address,cmd[3])
                                Status.state["move"]=0
                        bus.write_byte(address,cmd[key])
                        time.sleep(1)
                GPIO.remove_event_detect(23)
                GPIO.output(6,False)
                f.close()

Obj=carThread()

if __name__=="__main__":
    Obj.start()
    app.webService()
