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
    RIGHT_SPEED = 200
    LEFT_SPEED = 200
    #For the recheck method
    fwd_count = 0
    #Adding a more accurate turn
    turn_track = 0.0
    #uppercase will not change they are final
    TIME_PER_DEGREE = 0.01278
    TURN_MODIFIER = .5

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
                "q": ("Quit", quit),
                "s": ("Speed", self.setSpeed)
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

    #Defining the speed of the left and right motors
    def status(self):
        print("My left speed is at" + str())

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

    ##my new turn method becasue encR and encL just dont cut it
    #takes x amount of degrees and turns accordingly
    def turnR(self, deg):
        # adjust the tracker so we know how many degrees we turn
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #Do turn stuff
        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop

    def turnL(self, deg):
        #adjust the tracker so we know how many degrees we turn
        self.turn_track -= deg
        print("The exit is " + str(self.turn_track) + " degrees away.")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #Do turn stuff
        left_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)


    def setSpeed(self, left, right):
        print("Left speed: " + str(left))
        print("Right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)

    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        #### WRITE YOUR FINAL PROJECT HERE
        #TODO: If while loop fails, check for another path
        #TODO: Replace choosePath with  a method that's smarter
        while self.isClear():
            #let's go forward just a little
            self.recheck()
            self.encF(18)
        #Turn head to center
        servo(self.MIDPOINT)
        time.sleep(.1)
        # if there is an object that is less than 3 cm away back up and rescan
        if us_dist(15) < 3:
            self.encB(9)

        #Left or Right previous version worked
        answer = self.choosePath()
        #If there is an object to the left go right
        #TODO: Replace '45'  with  a variable to make a better turn
        if answer == "left":
            self.turnL(45)
            #Make more accurate, if there is an object right got left
            # TODO: Replace '45'  with  a variable to make a better turn
        elif answer == "right":
            self.turnR(45)

        self.nav()




    # If robot goes forward three times stop and look for best path
    def recheck(self):
        self.fwd_count += 1
       #start of loop
        if self.fwd_count == 3:
            self.stop()
            #Left or Right previous version worked
            answer = self.choosePath()
            #If there is an object to the left go right
            if answer == "left":
                self.turnL(45)
                #Make more accurate, if there is an object right got left
            elif answer == "right":
                self.turnR(45)
    #New calibrate method to stop robot from drifting from the right
    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':

            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                #Robot will go foward more to better determine speed
                self.encF(19)
                response = input("Reduce left, reduce right or done? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 5
                elif response == 'r':
                    self.RIGHT_SPEED -= 5
                elif response == 'm':
                    self.encF(19)
                else:
                    break








#################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()