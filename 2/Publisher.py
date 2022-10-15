import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost",1883,60)
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
    msg.append(normHex(hex(Starting_addres)))#dodanie adresu startowego
    if(No_of_reg<256):
        msg.append(normHex(hex(00)))
    msg.append(normHex(hex(No_of_reg)))#dodanie liczby rejestrow

    print(info)
    
    for i in info.encode('ascii'):
        LRC ^= i
    msg.append(normHex(hex(LRC))) #dodanie sumy kontrolnej LRC
    msg.append(normHex(hex(CR))) #dodanie znacznika koncowego CR
    msg.append(normHex(hex(LF))) #dodanie znacznika koncowego LF
    
    msg = ''.join(msg)
    return msg

adres =5#int(input("Wprowadź adres jednostki slave:  ")) 
fun =3#int(input("Kod funkcji: "))
Starting_addres=30#int(input("Adres startowy: "))
No_of_reg=2#int(input("Liczba rejestrów: "))

msg=makeMsg(adres , fun, Starting_addres, No_of_reg)
if(msg != 0):
    client.publish("topic/zapytanie",msg)
    print('Wysłano:',msg)
    client.disconnect()
