echo "Setting up ROS..."
source /home/robot/ros_catkin_ws/install_isolated/setup.bash
export ROS_IP=172.17.0.1
export ROS_MASTER_URI=http://172.17.0.1:11311/

#while true
#do
/home/robot/legorobotctrl.py
#done
