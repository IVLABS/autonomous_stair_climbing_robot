#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import sys, select, tty

moveBindings = {
        'w':(-1,0),     # Move Straight w , 
        'a':(-1,-1),    # + Turn Left   a . 
        'd':(-1,1),     # + Turn Right  d m
           }

speed = .2
turn = 3


def callback(keyr):
    print('ireached')
    read = keyr.data
    print(read)
    x = 0
    key = 0
    th = 0
    status = 0
    count = 0
    acc = 0.2
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    if read > -1 :

        if read == 3 :
            key = 'w'
            print(key)
        elif read == 1 :
            key = 'd'
            print(key)
        elif read == 0 :
            key = 'a'
            print(key)
        if key in moveBindings.keys():
            x = moveBindings[key][0]
            th = moveBindings[key][1]
            count = 0
        elif key == ' ' or key == 'k' :
            x = 0
            th = 0
            control_speed = 0
            control_turn = 0
        else:
            count = count + 1
            if count > 4:
                x = 0
                th = 0
            if (key == '\x03'):
                exit()

        target_speed = speed * x
        target_turn = turn * th

        if target_speed > control_speed:
            control_speed = min( target_speed, control_speed + 0.1 )

        elif target_speed < control_speed:
            control_speed = max( target_speed, control_speed - 0.1 )
        else:
            control_speed = target_speed

        if target_turn > control_turn:
            control_turn = min( target_turn, control_turn + 0.5 )
        elif target_turn < control_turn:
            control_turn = max( target_turn, control_turn - 0.5 )
        else:
            control_turn = target_turn

        twist = Twist()
        twist.linear.x = 3*control_speed; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1*control_turn
        pub.publish(twist)
        print(twist)


if __name__=="__main__":

    rospy.init_node('turtlebot_teleop')
    pub = rospy.Publisher('~cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/in_put', Int32 , callback)
    print('Completed Initializations')
    rospy.spin()
