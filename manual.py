import time                                #Import time library
import RPi.GPIO as GPIO                    #Import GPIO library                            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

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

import socket
TCP_IP = '192.168.108.222'
TCP_PORT = 8084
BUFFER_SIZE = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connection address:', addr)
ck=1

def FORWORD():
    print('FORWORD')
    GPIO.output(IN1,False)
    GPIO.output(IN2, True)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
    
    
def BACKWORD():
    print('BACKWORD')
    GPIO.output(IN1,True)
    GPIO.output(IN2, False)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)
    
def STOP():
    print('STOP')
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def RIGHT():
    print('RIGHT')
    GPIO.output(IN1,True)
    GPIO.output(IN2, False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,True)
    

def LEFT():
    print('LEFT')
    GPIO.output(IN1,False)
    GPIO.output(IN2, True)
    GPIO.output(IN3,True)
    GPIO.output(IN4,False)

LM=21
GPIO.setup(LM, GPIO.IN)

while ck==1:
    data = conn.recv(BUFFER_SIZE)
    data=data.decode('UTF-8','ignore')

    print ("received data:", str(data))
    if str(data) == 'f':
        FORWORD()

    if str(data) == 'b':
        BACKWORD()

    if str(data) == 'l':
        LEFT()

    if str(data) == 'r':
        RIGHT()

    if str(data) == 's':
        STOP()

    time.sleep(1)
    if GPIO.input(LM) == False:
            print("Landmine detected")

conn.close()
GPIO.cleanup()
