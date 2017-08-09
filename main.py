import serial  
import sys  
import binascii  
import string 
import requests

def unsigned(n):
    return n & 0xFF

try:  
    ser = serial.Serial('/dev/ttyUSB0', 19200)  
except Exception, e:  
    print 'open serial failed.'  
    exit(1)  
  
print 'SerialIs Running...' 
i = 0
while True: 
    i += 1
    s = ser.read(15) 
    print str(binascii.b2a_hex(s))
    high = s[1]
    low = s[2]
    check = s[3]
    new_check = ( ~( unsigned (sum([ord(high),ord(low)]))) + 1 )
    if unsigned(ord(check)) == unsigned(new_check) :
        print 'check ok'
        #print ord(low)	
        result = (float(ord(high) * 256 + ord(low)) / 1000)		
        print result 	
        if i % 10 == 0:
            postdata = '[{"Name": "bj_001","Value": "' + str(result) + '"}]'	
            payload = {"UserKey": "f1ed8c099ae54c4aaff38c2e6a4cf211","url": "http://www.lewei50.com/api/V1/gateway/UpdateSensors/02","postdata" : postdata}
            print payload
            headers = {'Content-type': 'application/json'}
            r = requests.post('http://www.lewei50.com/dev/apitestResult/3', json=payload)		
            print r.text		
 
