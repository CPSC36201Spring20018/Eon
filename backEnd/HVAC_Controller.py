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
