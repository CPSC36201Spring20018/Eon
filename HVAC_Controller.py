import RPi.GPIO as gpio
import tempRead
import time
from datetime import datetime

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

def ChangeTemp(requested, current):
    print('current tempurature: {0} \ncurrent requested: {1}'.format(current,requested))
    user_input = input('Would you like to change the temp?(y/n)')
    if user_input == 'y':
        return int(input('What temp in f? '))
    elif user_input == 'n':
        return requested

def ACOn():
    gpio.setup(21,gpio.OUT)
    print('AC on')
    gpio.output(21,gpio.HIGH)
    return True

def ACOff():
    gpio.setup(21,gpio.OUT)
    print('AC off')
    gpio.output(21,gpio.LOW)
    return False

def HeatOn():
    gpio.setup(18,gpio.OUT)
    print('Heat on')
    gpio.output(18,gpio.HIGH)
    return True

def HeatOff():
    gpio.setup(18,gpio.OUT)
    print('Heat off')
    gpio.output(18,gpio.LOW)
    return False


AC = False
Heat = False
threshold = 3
requested_temp = 0 #0 is the predefined off state
og_time = datetime.time(datetime.now())


while True:
    temp = tempRead.read_temp()
    temp_f = temp[1]
    current_time = datetime.time(datetime.now())
    if int(current_time.minute) == int(og_time.minute) + 1:
        requested_temp = ChangeTemp(requested_temp, temp_f)
        og_time = datetime.time(datetime.now())
    if AC == True and (temp_f <= requested_temp or requested_temp == 0):
        AC = ACOff()
    if Heat == True and (temp_f >= requested_temp or requested_temp == 0):
        Heat = HeatOff()
    if AC == False and temp_f > requested_temp + threshold and requested_temp != 0:
        AC = ACOn()
    if Heat == False and temp_f < requested_temp - threshold and requested_temp != 0:
        Heat = HeatOn()
