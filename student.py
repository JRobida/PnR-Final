import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 82
    STOP_DIST = 20

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "v": ("Voltage", self.status),
                "4": ("Calibrate servo", self.calibrate),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        print('Is it safe to dance?')
        for x in range(100, 200, 25):
            if not self.clearToDance():
                print ("you can not dance")
                break
            print('Speed is set to: ' + str(x))
            set_speed(x)
            servo(30)
            self.encB(9)
            self.encR(180)
            servo(80)
            self.encL(180)
            self.encF(5)
            self.encB(5)
            servo(100)
            servo(82)
    def status(self):
        print("My power is at "+ str(volt()) + "volts")

    #Needs improvement before put in problem was STOP_DIST
    '''def clearToDance(self):
        #need to at encR and encL and encd b
        extraTurn = False
        servo(self.MIDPOINT)
        time.sleep(.1)
        dist = us_dist(15)
        print('Front distance:' + str(dist)
        if dist < self.STOP_DIST:
            self.encB(20)
        servo(self.MIDPOINT - 60)
        time.sleep(.1)
        dist = us_dist(15)
        print('Right distance:' + str(dist)
        if dist < self.STOP_DIST:
            self.encR(10)
            self.encB(5)
            extraTurn = True
        servo(self.MIDPOINT + 60)
        time.sleep(.1)
        if extraTurn:
            self.encL(10)
        print('Left distance:' + str(us_dist(15)))
        if dist < self.STOP_DIST:
            self.encL(10)
            self.encB(5)
        return True'''

    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO: If while loop fails, check for another path
        while self.isClear():
            #let's go forward just a little
            self.encF(18)
        if self.isClear() is False
            self.encB(18)

####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()