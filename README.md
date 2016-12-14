# PnR-Final
The final project for my Programming and Robotics class
Hey future Jake, welcome back to your 11th grade PnR Final Project. You are probably doing fantastic right now
in college. As you look back on your project, there should be two folders, pigo.py and student.py. Pigo.py was Mr. A's
parent class that he provided for us. We want to dive into the student.py class.

def handler: this method gives you options to drive forward, rotate, dance or calibrate your speed and servo(head).

def turnR: this method is a little weird. If you can remember, we had trouble turning right, it just go in circles. So we
decided to turn the robot 360 - degrees. You by now have figured out how to turn right.

def dance: This is fun!. The robot is moves back and forth and the servo swings side to side. Remember to check out that
video Mr. A put on youtube.

def nav: this is your main method. Instead of driving and scanning, our robot inches forward then scans. With in the method
there is a back up method. If the robot sees an object 15 centimeters away it will back up to give more room.

With in the def nav is a commented out section. This is the orginal method we used. It would turn left or right by
forty-five degrees.

def recheck: is an method that rechecks the robots position. If the robot moves forward three times, it will stop and recheck
to make sure it is on the best path possible.

def kenny: this method was made by kenny and Mr. A, this method makes for a more accurate turn.

def status: gives you the voltage of your robot.

