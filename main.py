#coding=utf8

#run with python 3.4
import serial  
import sys  
import binascii  
import string 
import requests
from sys import platform as _platform

def unsigned(n):
    return n & 0xFF

try:
    if _platform == "linux" or _platform == "linux2":
        ser = serial.Serial('/dev/ttyUSB0', 19200) 
    elif _platform == "win32":
        ser = serial.Serial('COM4', 19200) 
except ValueError:  
    print ('open serial failed.' )
    print (ValueError) 
    exit(1)  
  
print ('SerialIs Running...' )
i = 0
while True: 
    i += 1
    s = ser.read(15) 
    print (str(binascii.b2a_hex(s)))
    high = s[1]
    low = s[2]
    check = s[3]
    print(high)
    print( type( high ))	
    new_check = ( ~( unsigned (sum([high,low]))) + 1 )
    if unsigned(check) == unsigned(new_check) :
        print ('check ok' )
        #print ord(low)    
        result = (float(high * 256 + low) / 1000)        
        print (result)     
        if i % 30 == 0:
            postdata = '[{"Name": "bj_002","Value": "' + str(result) + '"}]'    
            payload = {"UserKey": "f1ed8c099ae54c4aaff38c2e6a4cf211","url": "http://www.lewei50.com/api/V1/gateway/UpdateSensors/02","postdata" : postdata}
            print ( payload )
            headers = {'Content-type': 'application/json'}
            r = requests.post('http://www.lewei50.com/dev/apitestResult/3', json=payload)        
            print (r.text)        
 
