import time                                #Import time library
import RPi.GPIO as GPIO                    #Import GPIO library                            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                   #Set GPIO pin numbering 

LM=21
GPIO.setup(LM, GPIO.IN)

IN1=19
IN2=26
IN3=16
IN4=20

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)

#set GPIO Pins
GPIO_TRIGGER = 5
GPIO_ECHO = 6
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def FORWORD():
    print('FORWORD')
    GPIO.output(IN1,False)
    GPIO.output(IN2, True)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
    time.sleep(1)
    
def BACKWORD():
    print('BACKWORD')
    GPIO.output(IN1,True)
    GPIO.output(IN2, False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)
    time.sleep(1)
    
def STOP():
    print('STOP')
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
    time.sleep(1)

def RIGHT():
    print('RIGHT')
    GPIO.output(IN1,True)
    GPIO.output(IN2, False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
    time.sleep(1)

def LEFT():
    print('LEFT')
    GPIO.output(IN1,False)
    GPIO.output(IN2, True)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)
    time.sleep(1)

a = 0
try:
    while True:
        if GPIO.input(LM) == False:
            print("Landmine detected")
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        if dist < 15:
            if a == 0:
                STOP()
                LEFT()
                a = 1
            else:
                STOP()
                RIGHT()
                a = 0
        else:
            FORWORD()
except:
    GPIO.cleanup()
