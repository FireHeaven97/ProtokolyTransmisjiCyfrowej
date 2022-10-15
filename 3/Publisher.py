import paho.mqtt.client as mqtt
import time
import threading

client = mqtt.Client()
client.connect("localhost",1883,60)

def SUB() :
        def wyswietl(msg):
            LRC=0
            adres=msg[1:3]
            i=int(adres,16)
            adres=str(i)
            print('Adres slave: '+adres)

            
            funkcja=msg[3:5]
            i=int(funkcja,16)
            funkcja=str(i)
             
            print('Kod Funkcji: '+funkcja)
            if int(funkcja) == 83:
                    NoR=msg[5:7]
                    i=int(NoR,16)
                    NoR=str(i)
                    print('Liczba Rejestrów: '+NoR)
                    
            else:
                    LB=msg[5:7]
                    i=int(LB,16)
                    LB=str(i)
                    print('Liczba Przysłanych Bajtów: '+LB)


       
   
        def on_connect(client, userdata, flags, rc):
               # print("Connected with result code"+str(rc))
                client.subscribe("topic/odpowiedz")

        def on_message(client, userdata, msg):
                msg = msg.payload.decode()
                print('\n Odpowiedź:',msg)
                wyswietl(msg)

        client = mqtt.Client()
        client.connect("localhost",1883,60)
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_forever()
                 

                

def PUB():
        
        def normHex(hstr):
            if len(hstr) == 3:
                hstr=hstr[0:1]+hstr[-1]
                return hstr.upper()
            else:
                hstr = hstr[2:]
                return hstr.upper()

        def makeMsg(adres , fun, Starting_addres, No_of_reg):
            LRC=0
            CR=13
            LF=10
            info=[]
            SA=str(Starting_addres)
            NOR=str(No_of_reg)
            info=SA+NOR
     
            if(adres<1 or adres>247):
                print('Błędny adres jednostki slave')
                return 0
            if(fun<1 or fun>17):
                print('Błędny kod funkcji')
                return 0


                
            msg=[':',];
            msg.append(normHex(hex(adres))) #dodanie adresu
            msg.append(normHex(hex(fun)))#dodanie kodu funkcji
            if(Starting_addres<256):
                msg.append(normHex(hex(00)))
            elif Starting_addres>256 and Starting_addres<=4095:
                msg.append('0')
            #elif Starting_addres>999 and Starting_addres<9999:
                
            msg.append(normHex(hex(Starting_addres)))#dodanie adresu startowego
            if(No_of_reg<256):
                msg.append(normHex(hex(00)))
            elif No_of_reg>256 and No_of_reg<=4095:
                msg.append('0')
              
            msg.append(normHex(hex(No_of_reg)))#dodanie liczby rejestrow
           
            for i in info.encode('ascii'):
                LRC ^= i
            msg.append(normHex(hex(LRC))) #dodanie sumy kontrolnej LRC
            msg.append(normHex(hex(CR))) #dodanie znacznika koncowego CR
            msg.append(normHex(hex(LF))) #dodanie znacznika koncowego LF
            
            msg = ''.join(msg)
            return msg

        adres =int(input("Wprowadź adres jednostki slave:  ")) 
        fun =int(input("Kod funkcji: "))
        Starting_addres=int(input("Adres startowy: "))
        No_of_reg=int(input("Liczba rejestrów: "))

        msg=makeMsg(adres , fun, Starting_addres, No_of_reg)
        if(msg != 0):
            time.sleep(0.1)
            client.publish("topic/zapytanie",msg)
            print('\n Wysłano:',msg)
            client.disconnect()
            
t = threading.Thread(target = SUB)
t.start()
PUB()
t.join()
