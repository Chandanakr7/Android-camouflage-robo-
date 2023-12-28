import time                                #Import time library
import RPi.GPIO as GPIO                    #Import GPIO library                            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                   #Set GPIO pin numbering 

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
