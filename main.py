import RPi.GPIO as GPIO
from threading import Thread
import smbus
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=PUD_UP)
GPIO.setup(18,GPIO.OUT)
address=0x04
bus=smbus.SMBus(1)
cmd={'b':0,'w':1,'s':2,'d':3,'a':4,'x':-1}
class status:
    def __init__(self):
        self.setUp=False
        self.execution=False
        self.motionCommand="00"

Status=status()

class carThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        while True:
            if Status.setUp:
                while Status.setUp:

            elif Status.execution:
                f=open("cmd.txt",'r')
                GPIO.add_event_detect(23,GPIO.RISING,callback=IR_callback)
                line=f.readline()
                currentline=line.split(",")
                while True:
                    for key in currentline:
                        while(Status.CAMERA):
                            a=1
                        bus.write_byte(address,cmd[key])
                        time.sleep(1)

Obj=carThread()
Obj.start()

if __name__=="__main__":
    webService()
