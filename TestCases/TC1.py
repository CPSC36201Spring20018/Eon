import sys
sys.path.append('../')
import controller
import time

c = controller.Controller()

c.setCurrentTemperature()
f = c.getForecast(c.getLocation())
for i in range(1,4):
    print(f[i].text)
    print(f[i].date)
    print(f[i].high)
c.setRequestedTemperature(c.getCurrentTemperature() + c.threshold + 1)
print('Current Temperature: {}'.format(c.getCurrentTemperature()))
if not c.isHeat() and (c.getCurrentTemperature() - c.threshold < c.getRequestedTemperature()):
    if c.isAC():
        c.deactivateAC()
    c.activateHeat()
while True and not c.isDisable:
    print('Requested Temperature: {}'.format(c.getRequestedTemperature()))
    if (c.getCurrentTemperature() >= c.getRequestedTemperature()) and c.isHeat():
        c.deactivateHeat()
        break
    c.setRequestedTemperature(c.getRequestedTemperature()-1)
    time.sleep(1)
c.setRequestedTemperature(c.getCurrentTemperature() - c.threshold - 1)
if not c.isAC() and (c.getCurrentTemperature() + c.threshold > c.getRequestedTemperature()):
    if c.isHeat():
        c.deactivateHeat()
    c.activateAC()
while True and not c.isDisable:
    print('Requested Temperature: {}'.format(c.getRequestedTemperature()))
    if (c.getCurrentTemperature() <= c.getRequestedTemperature()) and c.isAC:
        c.deactivateAC()
        break
    c.setRequestedTemperature(c.getRequestedTemperature() + 1)
    time.sleep(1)
c.Disable()
c.setRequestedTemperature(c.getCurrentTemperature() + c.threshold + 1)
print('Current Temperature: {}'.format(c.getCurrentTemperature()))
if not c.isHeat() and (c.getCurrentTemperature() - c.threshold < c.getRequestedTemperature()):
    if c.isAC():
        c.deactivateAC()
    c.activateHeat()
while True and not c.isDisable:
    print('Requested Temperature: {}'.format(c.getRequestedTemperature()))
    if (c.getCurrentTemperature() >= c.getRequestedTemperature()) and c.isHeat():
        c.deactivateHeat()
        break
    c.setRequestedTemperature(c.getRequestedTemperature()-1)
    time.sleep(1)
c.setRequestedTemperature(c.getCurrentTemperature() - c.threshold - 1)
if not c.isAC() and (c.getCurrentTemperature() + c.threshold > c.getRequestedTemperature()):
    if c.isHeat():
        c.deactivateHeat()
    c.activateAC()
while True and not c.isDisable:
    print('Requested Temperature: {}'.format(c.getRequestedTemperature()))
    if (c.getCurrentTemperature() <= c.getRequestedTemperature()) and c.isAC():
        c.deactivateAC()
        break
    c.setRequestedTemperature(c.getRequestedTemperature() + 1)
    time.sleep(1)
c.Enable()
print("Pass")
