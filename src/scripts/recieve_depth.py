#! /usr/bin/python3

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import rospy
import numpy
import os

class RecieveImage_depth(object):
    def __init__(self):
        # Params
        # self.image = None
        self.depth = None
        self.br = CvBridge()

        #Node cycle rate in Hz
        self.loop_rate = rospy.Rate(1)

        #Subscribers realsense topic
        rospy.Subscriber("/camera/aligned_depth_to_color/image_raw",Image,self.callback_depth)

    def callback_depth(self, msg):
        depthPath = '/home/russapat/realsense_capture_ws/src/rs_capture/src/depth'
        rospy.loginfo('Depth Recieve..')
        self.depth = self.br.imgmsg_to_cv2(msg)
        cv_image = CvBridge().imgmsg_to_cv2(msg, desired_encoding="passthrough")
        # cv_image = cv2.applyColorMap(cv2.convertScaleAbs(cv_image, alpha=0.03), cv2.COLORMAP_JET)   #colorized

        cv_image = cv2.cvtColor(cv_image,cv2.COLOR_GRAY2BGR)
        cv2.imshow('depth_frame', cv_image)
        cv2.waitKey(1)

    
    def start(self):
        # rospy.loginfo("Timing images")
        #rospy.spin()
        while not rospy.is_shutdown():
            if self.depth is not None:
                # self.pub.publish(br.cv2_to_imgmsg(self.image))
                rospy.loginfo('show image')
                
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node('recievedepth')
    my_node_depth = RecieveImage_depth()
    my_node_depth.start()
