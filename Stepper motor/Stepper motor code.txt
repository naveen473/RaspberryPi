import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
motor_pin1=11
motor_pin2=13
GPIO.setup(motor_pin1,GPIO.OUT)
GPIO.setup(motor_pin2,GPIO.OUT)
while(1):
      GPIO.output(motor_pin1,GPIO.HIGH)
      GPIO.output(motor_pin2,GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(motor_pin1,GPIO.LOW)
      GPIO.output(motor_pin2,GPIO.HIGH)
      time.sleep(0.1)