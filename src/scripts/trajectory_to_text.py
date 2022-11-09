#!/usr/bin/env python3  

from time import time
import rospy
import tf2_ros

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(1)
    # time = rospy.Time()
    text = open("/home/russapat/obodroid_ws/src/rs_capture/text/static_human_2d_traj_221106.txt", "a+")

    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('map', 'trajectory_0', rospy.Time())

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        # time = tfBuffer.stamp 
        time = str(trans.header.stamp.secs)
        print(time)
        
        pose = [str(trans.transform.translation.x), str(trans.transform.translation.y), str(trans.transform.translation.z),
        str(trans.transform.rotation.x), str(trans.transform.rotation.y), str(trans.transform.rotation.z), str(trans.transform.rotation.z)]

        # text.write("("+" "+pose[0]+" "+pose[1]+" "+pose[2]+" "+")"+" "+"("+" "+pose[3]+" "+pose[4]+" "+pose[5]+" "+pose[6]+" "+")"+" "+time+"\n")
        # print("("+" "+pose[0]+" "+pose[1]+" "+pose[2]+" "+")"+" "+"("+" "+pose[3]+" "+pose[4]+" "+pose[5]+" "+pose[6]+" "+")"+" "+time+"\n")

        text.write(time+" "+pose[0]+" "+pose[1]+" "+pose[2]+" "+pose[3]+" "+pose[4]+" "+pose[5]+" "+pose[6]+"\n")
        print(time+" "+pose[0]+" "+pose[1]+" "+pose[2]+" "+pose[3]+" "+pose[4]+" "+pose[5]+" "+pose[6]+"\n")

        rate.sleep()