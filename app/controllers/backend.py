import serial, json
from app import app, socketio, emit
from threading import Thread, Event
from time import sleep


def open_serial(port,rate): #abre a porta serial(?)
    ser = serial.Serial(port,
                        baudrate=rate,
                        timeout=None,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)
    return ser

def take_string(n): #leitura da serial
    mystring=''
    i=0
    cond=False

    while cond!=True:
        while True:
            data=n.readline().decode('utf-8').strip('\r\n')
            if(data)=="{": #procura o caractere "{"
                mystring=data 
                break
        while(i<17):
                mystring+=n.readline().decode('utf-8').strip('\r\n')
                i=i+1
        mystring=mystring.replace(' ','', 2)
        cond=True

    return mystring

def make_json(str): #cria o dicionario atraves da string lida pela serial
    dic=(json.loads(str))
    return dic

def make_json_file(name,dict): #cria arquivo txt
    name+=".txt"
    with open(name, 'w') as outfile:
        json.dump(dict,outfile,indent=4)

def read_json_file(name): #lê um arquivo txt
    name+=".txt"
    with open(name) as json_file:
        data = json.load(json_file)
        return data

def take_json(channel): #retorna um dicionario
    ok = False
    str=take_string(channel)
    json_f=make_json(str)
    ok = True
    return json_f, ok

def print_json(port,rate,pretty): #printa o json
    if pretty==False:
        print(take_json(port,rate))
    else:
        a=take_json(port,rate)
        print(json.dumps(a,indent=4))    

thread = Thread()
thread_stop_event = Event()

def sendValues():
    global channel
    print("Taking values")
    while not thread_stop_event.isSet():
        k,x=take_json(channel)
        if x:
            print(k)
            socketio.emit('atualiza',k)
        else:
            socketio.sleep(1)

channel = open_serial("/dev/ttyACM0",9600)