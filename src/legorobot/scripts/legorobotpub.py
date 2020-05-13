#!/usr/bin/env python
# # license removed for brevity

import rospy
import roslib
from pynput.keyboard import Key, Listener
from std_msgs.msg import String
import sys, select, termios, tty

# globals
current_msg = "stop"

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

# define key press event callback
def on_press(key):
    global pub
    global current_msg
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if (k == 'w'):
        current_msg = "forward"
    elif (k == 's'):
        current_msg = "backward"
    elif (k == 'a'):
        current_msg = "left"    
    elif (k == 'd'):
        current_msg = "right"    
    # else:           
    #     current_msg = "stop"

    pub.publish(current_msg)    

# define key release event callback
def on_release(key):
    global pub
    global current_msg
    current_msg = "stop"
    pub.publish(current_msg)
    # stop on PAUSE
    if key == Key.pause:
        print("quit on PAUSE")
        return False


if __name__ == "__main__":
    # setup ros publisher
    pub = rospy.Publisher('ev3/active_mode', String, queue_size=10) # name of topic: /ctrl_cmd
    rospy.init_node('keyboard_input', anonymous=True) # name of node: /keyboard_input
    rate = rospy.Rate(10) # publish messages at 10Hz

    # setup keyboard listener
    listener = Listener(on_press=on_press, on_release=on_release, suppress=False)
    listener.start()

    # MAIN LOOP
    # endlessly react on keyboard events and send appropriate messages
    while listener.running and not rospy.is_shutdown():
        rospy.loginfo(current_msg)
        # pub.publish(current_msg)
        rate.sleep()