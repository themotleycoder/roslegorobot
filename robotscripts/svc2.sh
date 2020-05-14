echo "Setting up ROS..."
source /home/robot/ros_catkin_ws/install_isolated/setup.bash
export ROS_IP=192.168.86.236
export ROS_MASTER_URI=http://192.168.86.68:11311/

#while true
#do
/home/robot/legorobotctrl.py
#done
