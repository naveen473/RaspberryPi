#!/usr/bin/python
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 11
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16
R1 = 29
R2 = 31
R3 = 32
R4 = 33
C1 = 36
C2 = 35
C3 = 38
C4 = 37
DC1 = 18
DC2= 22


'''
define pin for lcd
'''
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
inputstring = ""
hidekey=""
secretkey = "9922"
delay = 1



GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
GPIO.setup(R1, GPIO.OUT) # DB7
GPIO.setup(R2, GPIO.OUT) # DB7
GPIO.setup(R3, GPIO.OUT) # DB7
GPIO.setup(R4, GPIO.OUT) # DB7
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DC1, GPIO.OUT) # DB7
GPIO.setup(DC2, GPIO.OUT) # DB7
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line



'''
Function Name :lcd_init()
Function Description : this function is used to initialized lcd by sending the different commands
'''
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
'''
Function Name :lcd_byte(bits ,mode)
Fuction Name :the main purpose of this function to convert the byte data into bit and send to lcd port
'''
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
'''
Function Name : lcd_toggle_enable()
Function Description:basically this is used to toggle Enable pin
'''
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
'''
Function Name :lcd_string(message,line)
Function  Description :print the data on lcd 
'''
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
def readLine(line, characters):
    global inputstring
    global hidekey
    GPIO.output(line, GPIO.HIGH)
    time.sleep(0.02)
    if(GPIO.input(C1) == 1):
      inputstring = inputstring +characters[0]
      hidekey = hidekey +"*"
      lcd_string(hidekey,LCD_LINE_2)
    elif(GPIO.input(C2) == 1):
      inputstring = inputstring +characters[1]
      hidekey = hidekey +"*"
      lcd_string(hidekey,LCD_LINE_2)
    elif(GPIO.input(C3) == 1):
      inputstring = inputstring +characters[2]
      hidekey = hidekey +"*"
      lcd_string(hidekey,LCD_LINE_2)
      
    elif(GPIO.input(C4) == 1):
      if(characters[3] ==  "#"):
       if(inputstring == secretkey):
        lcd_string("valid person",LCD_LINE_2)
        time.sleep(1)
        lcd_string("gate open",LCD_LINE_2)
        GPIO.output(DC1, GPIO.HIGH)
        GPIO.output(DC2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(DC1, GPIO.LOW)
        GPIO.output(DC2, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(DC1 ,GPIO.LOW)
        GPIO.output(DC2, GPIO.LOW)
        time.sleep(1)
        lcd_string("",LCD_LINE_2)
        inputstring = ""
        hidekey= ""
       else:
        lcd_string("Unknown person",LCD_LINE_2)
        time.sleep(1)
        lcd_string("again",LCD_LINE_2)
        inputstring = ""
        hidekey= ""
      else:
       inputstring = inputstring +characters[3]
       hidekey = hidekey +"*"
       lcd_string(hidekey,LCD_LINE_2)
    GPIO.output(line, GPIO.LOW)
    time.sleep(0.02)

# Define delay between readings
delay = 5
lcd_init()
lcd_string("welcome ",LCD_LINE_1)
time.sleep(1)
lcd_string("Enter Password ",LCD_LINE_1)
time.sleep(1)
while 1:
   readLine(R1, ["7","8","9","/"])
   readLine(R2, ["4","5","6","*"])
   readLine(R3, ["1","2","3","-"])
   readLine(R4, ["C","0","=","#"])

   
   
 
 