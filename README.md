# legorobot
ROS eneabled Lego robot using Python 2

## Requirements:
* Python 2
  * PYNPUT library for keyboard control
* PIP
* ROS
* Lego EV3 computer and motors
* Wifi dongle (USB) for EV3
* 16GB SD Card

## Setup (Using an Ubuntu laptop as ROS publisher):

### ROS (Melodic)
* Follow instructions provided here: http://wiki.ros.org/melodic/Installation/Ubuntu
* I used the 'desktop full install' option as I wanted the additonal ROS tools installed


### EV3
* I used the EV3DEV operating system isntalled on a 16gb SD card to run ROS on the EV3
* Follow instructions provided here: https://www.ev3dev.org/docs/getting-started/
* Once you have the EV3 booted with EV3DEV running on it you can SSH to the device with:

`ssh robot@IPADDRESS
Password is: maker`

### Project
* Clone the code into your `~/ros_catkin_ws/src directory` if you haven't already 
  
    `git clone https://github.com/themotleycoder/roslegorobot.git`

* then...

    `cd ~/ros_catkin_ws`

    `pip install pynput`

    `catkin_make install`



## Useful Commands:
* rosdep update
* source devel/setup.bash
* catkin_make install
