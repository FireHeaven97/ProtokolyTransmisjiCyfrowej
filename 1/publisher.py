import paho.mqtt.client as mqtt
import time
import datetime
import random
import sys

client = mqtt.Client()
client.connect("localhost",1883,60)

#minT = int(input("Wprowadz minT \n"))
#maxT = int(input("Wprowadz maxT \n"))
#t = int(input("Wprowadz czas \n"))
minT = 0
maxT = 20
stan = 0

for i in range(100):
    now = datetime.datetime.now()
    t = time.gmtime()
    date_tag = '['+now.strftime('{}.0{}.{} {}:{}:{} +2'.format(
            t.tm_mday,
            t.tm_mon,
            t.tm_year,
            t.tm_hour,
            t.tm_min,
            t.tm_sec))+']'
    czas = time.asctime(time.localtime(time.time()))
    T = round(random.uniform(minT, maxT), 2)
    client.publish("topic/test",'{date} {T:.2f} {stan}'.format(date = date_tag, T = T, stan = stan))
    time.sleep(5)

client.disconnect()
