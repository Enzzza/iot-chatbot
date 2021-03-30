from time import sleep
import serial
import sys

ser = serial.Serial('/dev/ttyACM0', 9600)
def Sensor(): 
    msg  = ser.readline()
    split = msg.split(",")
    
    if(len(split) == 2):
        i=0
	
        while i < (len(split)):
            split[i].replace("\\r\\n","")
            i=i+1
        split[1] = split[1].rstrip('\n')
    try:
        return {"temp":split[0],"hum":split[1]}
    except:
        return "Error"


while True:
    param = Sensor()
    if param != "Error":
        if sys.argv[1] == "temp":
            print(param["temp"])
            sys.stdout.flush()
            break
        elif sys.argv[1] == "hum":
            print(param["hum"])
            sys.stdout.flush()
            break
            

    sleep(2)



