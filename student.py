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
    #reducing left motor b/c left is too strong
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

    def status(self):
        print("My power is at "+ str(volt()) + "volts")




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

    def nav(self):
        print("Piggy nav")
        #### WRITE YOUR FINAL PROJECT HERE
        # TODO: If while loop fails, check for another path
        # TODO: Replace choosePath with  a method that's smarter
        while self.isClear():
            # let's go forward just a little
            self.recheck()
            self.encF(26)
        # Turn head to center
        servo(self.MIDPOINT)
        time.sleep(.1)
        # if there is an object that is less than 3 cm away back up and rescan
        if us_dist(15) < 3:
            self.encB(9)

        '''# Left or Right previous version worked
        answer = self.choosePath()
        # If there is an object to the left go right
        # TODO: Replace '45'  with  a variable to make a better turn
        if answer == "left":
            self.turnL(45)
            # Make more accurate, if there is an object right got left
            # TODO: Replace '45'  with  a variable to make a better turn
        elif answer == "right":
            self.turnR(45)
            '''
        answer = self.kenny()
        #a postive ruen is right
        if answer > 0:
            self.turnR(answer)
            #negative
        else:
            #let'ds remove the negative with abs()
            self.turnL(abs(answer))

        self.nav()



    def kenny(self):
        # Activate our scanner!
        self.wideScan()
        # count will keep track of contigeous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        # YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 30
        # YOU DECIDE: what increment do you have your wideScan set to?
        INC = 2

        ##########################
        ######### BUILD THE OPTIONS
        # loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                # YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    # set the counter up again for next time
                    count = 0
                    # add this option to the list
                    option.append(x - 8)

        ####################################
        ############## PICK FROM THE OPTIONS - experimental

        # The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        # the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH @  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            input("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            input("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption



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


    def setSpeed(self, left, right):
        print("Left speed: " + str(left))
        print("Right speed: " + str(right))
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)


    def dance(self):
        print("Piggy dance")
        #Starting dance method
        servo(30)
        self.encB(9)
        self.encR(180)
        servo(80)
        self.encL(180)
        self.encF(5)
        self.encB(5)
        servo(100)
        time.sleep(.01)
        servo(82)



    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        #for the head of the robot
        response = input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                #turns the robots head
                response = input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    #turns head right 1 degree
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
                #calibrating speed method
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                # Robot will go foward more to better determine speed
                self.encF(19)
                response = input("Reduce left, reduce right or done? (l/r/d): ")
                if response == 'l':
                    # Reduces every 5 instead of ten
                    self.LEFT_SPEED -= 5
                elif response == 'r':
                    # Redueces every 5 instead of ten
                    self.RIGHT_SPEED -= 5
                elif response == 'm':
                    self.encF(19)
                else:
                    break


    # Needs improvement before put in problem was STOP_DIST
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




#################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()