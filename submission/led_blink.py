import RPi.GPIO as IO # header file for GPIO
import time             # calling for time to provide delays in program
import sys
import timeit

#print("start"+str(timeit.default_timer()))

def run():
  IO.setmode (IO.BOARD)       # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
  IO.setup(40,IO.OUT)             # initialize digital pin40 as an output.
  IO.output(40,1)                      # turn the LED on (making the voltage level HIGH)
  time.sleep(2.5)                         # sleep for a second
  IO.cleanup()                         # turn the LED off (making all the output pins LOW)

if len(sys.argv)>1 and sys.argv[1]=="run":
  run()


#print("end"+str(timeit.default_timer()))
