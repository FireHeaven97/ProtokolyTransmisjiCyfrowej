import paho.mqtt.client as mqtt
import random
def normHex(hstr):
    if len(hstr) == 3:
        hstr=hstr[0:1]+hstr[-1]
        return hstr.upper()
    else:
        hstr = hstr[2:]
        return hstr.upper()
def wyswietl(msg):
    LRC=0
    wiad=[]
    adres=msg[1:3]
    i=int(adres,16)
    adres=str(i)
    print('Adres slave: '+adres)

    
    funkcja=msg[3:5]
    i=int(funkcja,16)
    funkcja=str(i)
    print('Kod Funkcji: '+funkcja)

    SA=msg[5:9]
    i=int(SA,16)
    SA=str(i)
    print('Żądany adres startowy: '+SA)

    NoR=msg[9:13]
    i=int(NoR,16)
    NoR=str(i)
    print('Żądana ilość rejestów: '+NoR)

    sumaLRC=SA+NoR

    #Sprawdzenie LRC
    for i in sumaLRC.encode('ascii'):
        LRC ^= i
        
    przyslane_LRC=msg[13:15]
    i=int(przyslane_LRC,16)
    print("-------------------")
    if(i != LRC):
        print("Błąd LRC się nie zgadza")
        msg2=[':',];
        msg2.append(normHex(hex(adres))) #dodanie adresu
        msg2.append(normHex(hex(83)))#dodanie kodu funkcji
        msg2.append(normHex(hex(NoR)))#dodanie liczbry rej
        msg2.append(normHex(hex(LRC)))#dodanie kodu funkcji
        msg2 = ''.join(msg2)
        client.publish("topic/odpowiedz",msg2)
        print("-------------------")
    #else:
    dane2.randint(0,256)
    print("-------------------")
    #msg2.append(normHex(hex(adres))) #dodanie adresu
    #msg2.append(normHex(hex(funkcja)))#dodanie kodu funkcji
    Number_of_bits=NoR*2    
    #msg2.append(normHex(hex(Number_of_bits)))#dodanie liczby bitow
    dane=[]


    for i in range(Number_of_bits):
        dane[i]=randint(0,256)

    print(dane)
            
            

    client.publish("topic/test",msg2)
    
def on_connect(client, userdata, flags, rc):
        print("Connected with result code"+str(rc))
        client.subscribe("topic/zapytanie")

def on_message(client, userdata, msg):
        msg = msg.payload.decode()
        wyswietl(msg)
        
client = mqtt.Client()
client.connect("localhost",1883,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
