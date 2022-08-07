import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

LED_Red = 7
LED_Yellow= 11

GPIO.setup(LED_Red, GPIO.OUT) 
GPIO.setup(LED_Yellow, GPIO.OUT) 

while 1:
   GPIO.output(LED_Red, True)
   time.sleep(0.1)
   GPIO.output(LED_Yellow, True)
   time.sleep(0.1)
   GPIO.output(LED_Red, False)
   time.sleep(0.1)
   GPIO.output(LED_Yellow, False)
   time.sleep(0.1)
   
   