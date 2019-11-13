import RPi.GPIO as IO # header file for GPIO
import time             # calling for time to provide delays in program
import sys
import timeit

#print("start"+str(timeit.default_timer()))

def run():
  IO.setmode (IO.BOARD)       # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
  IO.setup(37,IO.OUT)             # init digital pin37 as an output.
  IO.output(37,1)                      # turn the LED on (making the voltage level HIGH)
  time.sleep(3.5)                         # sleep for a second
  IO.cleanup()                         # turn the LED off (making all the output pins LOW)

def next_page():
  IO.setmode (IO.BOARD)       # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
  IO.setup(40,IO.OUT)             # EN | initialize digital pin40 as an output.
  IO.setup(38,IO.OUT)             # DIR | 1->NEXT, 0->PREV | initialize digital pin39 as an output.
  IO.output(38,1)
  IO.output(40,1)
  time.sleep(0.5)
  IO.output(40,0)
  IO.cleanup()

def prev_page():
  IO.setmode (IO.BOARD)       # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
  IO.setup(40,IO.OUT)             # EN | initialize digital pin40 as an output.
  IO.setup(38,IO.OUT)             # DIR | 1->NEXT, 0->PREV | initialize digital pin39 as an output.
  IO.output(38,0)
  IO.output(40,1)
  time.sleep(0.5)
  IO.output(40,0)
  IO.cleanup()

if len(sys.argv)>1:
    if sys.argv[1]=="next":
        #run()
        next_page()
    elif sys.argv[1] == "prev":
        #run()
        prev_page()
    elif sys.argv[1] == "wait":
        run()

#print("end"+str(timeit.default_timer()))
