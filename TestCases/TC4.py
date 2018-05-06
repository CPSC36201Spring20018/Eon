import sys
sys.path.append('../')
import controller
import time

c = controller.Controller()
while True:
    c.setCurrentTemperature()
    print('Current Temperature: {}'.format(c.getCurrentTemperature()))
    if not c.isVacation:
        c.setRequestedTemperature(int(input('What would you like to set the temperature to?')))
    else:
        print("Vacation mode is active Requested Temperature set to: {}".format(c.getRequestedTemperature()))
    if not c.isAC() and (c.getCurrentTemperature() + c.threshold > c.getRequestedTemperature()):
        if c.isHeat():
            c.deactivateHeat()
        c.activateAC()
    if not c.isHeat() and (c.getCurrentTemperature() - c.threshold < c.getRequestedTemperature()):
        if c.isAC():
            c.deactivateAC()
        c.activateHeat()
    while True and (not c.isDisable or c.isVacation):
        print('Requested Temperature: {}'.format(c.getRequestedTemperature()))
        if c.isVacation:
            print("Vacation mode active assume working as intended")
            break
        if c.getRequestedTemperature() == c.getCurrentTemperature():
            if c.isAC():
                c.deactivateAC()
            if c.isHeat():
                c.deactivateHeat()
            break
        if c.isAC():
            c.setRequestedTemperature(c.getRequestedTemperature()+1)
        elif c.isHeat():
            c.setRequestedTemperature(c.getRequestedTemperature()-1)
        time.sleep(1)
    answer = input("continue?(y/n)")
    if answer == 'n':
        break
    if c.isVacation:
        vacation = input("Vacation mode is on, disable it?(y/n)")
    else:
        vacation = input("Vacation mode is off, enable it?(y/n)")
    if vacation == 'y':
        c.setVacation()
print("pass")
