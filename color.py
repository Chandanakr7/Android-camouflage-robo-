import cv2   
import numpy as np
import os
import time                                #Import time library
import RPi.GPIO as GPIO                    #Import GPIO library  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                   #Set GPIO pin numbering 

LM=21
GPIO.setup(LM, GPIO.IN)

IN1=24
IN2=23
IN3=22
IN4=27

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)

cap=cv2.VideoCapture(0)
while True:
        if GPIO.input(LM) == False:
            print("Landmine detected")
        _, img = cap.read()
            
        #converting frame(img i.e BGR) to HSV (hue-saturation-value)

        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        #definig the range of red color
        red_lower=np.array([136,87,111],np.uint8)
        red_upper=np.array([180,255,255],np.uint8)

        #defining the Range of Green color
        green_lower=np.array([45,100,50],np.uint8)
        green_upper=np.array([75,255,255],np.uint8)

        #defining the Range of yellow color
        yellow_lower=np.array([22,60,200],np.uint8)
        yellow_upper=np.array([60,255,255],np.uint8)

        #defining the Range of blue color
        blue_lower=np.array([110,50,50],np.uint8)
        blue_upper=np.array([130,255,255],np.uint8)

        #finding the range of red,blue and yellow color in the image
        red=cv2.inRange(hsv, red_lower, red_upper)
        blue=cv2.inRange(hsv,blue_lower,blue_upper)
        green=cv2.inRange(hsv,green_lower,green_upper)
        yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)

        #Morphological transformation, Dilation  	
        kernal = np.ones((5 ,5), "uint8")

        red=cv2.dilate(red, kernal)
        res=cv2.bitwise_and(img, img, mask = red)

        blue=cv2.dilate(blue,kernal)
        res1=cv2.bitwise_and(img, img, mask = blue)

        green=cv2.dilate(green,kernal)
        res2=cv2.bitwise_and(img, img, mask = green)  

        yellow=cv2.dilate(yellow,kernal)
        res3=cv2.bitwise_and(img, img, mask = yellow)    


        #Tracking the Red Color
        (contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>1900):
                        
                        x,y,w,h = cv2.boundingRect(contour)	
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                        cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
                        print ('change to RED')
                        GPIO.output(IN1, True)
                        GPIO.output(IN2, False)
                        GPIO.output(IN3, False)
                        time.sleep(1)
                        break
                        
        (contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>1900):
                        x,y,w,h = cv2.boundingRect(contour)	
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        cv2.putText(img,"BLUE color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))
                        print ('change to BLUE')
                        GPIO.output(IN1, False)
                        GPIO.output(IN2, False)
                        GPIO.output(IN3, True)
                        time.sleep(1)
                        break


        (contours,hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>1900):
                        x,y,w,h = cv2.boundingRect(contour)	
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                        cv2.putText(img,"green  color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))
                        print ('change to GREEN')
                        GPIO.output(IN1, False)
                        GPIO.output(IN2, True)
                        GPIO.output(IN3, False)
                        time.sleep(1)
                        break

                        
        cv2.imshow("Color Tracking",img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
                GPIO.output(IN1, False)
                GPIO.output(IN2, False)
                GPIO.output(IN3, False)
                cap.release()
                cv2.destroyAllWindows()
                break  
          

    
