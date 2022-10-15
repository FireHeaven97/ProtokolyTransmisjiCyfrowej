import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from matplotlib import style
import datetime
import os
import threading
xs=[]
ys=[]
style.use('fivethirtyeight')
fig=plt.figure()
fig.autofmt_xdate()
ax1 = fig.add_subplot(1,1,1)
ax1.tick_params(axis='x', labelrotation=90)
repeat= 5



def Client() :    
    def on_connect(client, userdata, flags, rc):
            print("Connected with result code"+str(rc))
            client.subscribe("topic/test")

    def on_message(client, userdata, msg):
            T = msg.payload.decode()
            len1= len(T)-2       
            time = (T.split(' ')[1])
            last_y = float(T.split(' ')[3])
            xs.append(time)
            ys.append(last_y)
            print(T)
            
    client = mqtt.Client()
    client.connect("localhost",1883,60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    
def plotter() :
    def animate (i):
        if len(xs)>repeat:
            xs_temp=xs[repeat]
            ys_temp=ys[repeat]
            xs.clear()
            ys.clear()
            xs.append(xs_temp)
            ys.append(ys_temp)
        ax1.clear()
        ax1.plot(xs,ys)
    ani=animation.FuncAnimation(fig,animate,interval=1000, blit=False)
    plt.show()
        
t = threading.Thread(target = Client)
t.start()
plotter()
t.join()
