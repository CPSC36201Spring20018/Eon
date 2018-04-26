import os
import glob
import time
from datetime import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

while True:
    temp = read_temp()
    temp = temp[1]
    i = 'am'
    t = datetime.time(datetime.now())
    t_h = str(t)[:2]
    if int(t_h) > 12:
        i = 'pm' 
    t_h = int(t_h) % 12
    t = str(t_h) + str(t)[2:5]
    print("At {0}{2} it was {1}F".format(t, temp, i))
    time.sleep(60)
