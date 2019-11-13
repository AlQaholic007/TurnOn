from smbus2 import SMBus
import time
import requests

addr = 0x1c

bus = SMBus(2)

ip = 'http://10.141.158.131:5000'

while(True):
  b = bus.read_byte_data(addr,3);
  if b==0:
      continue
  elif b==2:
      r = requests.get(ip+"/next")
      print "Next Pressed, 5 second timer starts"
      time.sleep(4)
  elif b==1:
      r = requests.get(ip+"/last")
      print "Prev Pressed, 5 second timer starts"
      time.sleep(4)
  else:
      print "oops something is wrong"
  time.sleep(1)

bus.close()
