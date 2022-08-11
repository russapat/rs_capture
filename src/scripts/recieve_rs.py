#! /usr/bin/python3

from gc import callbacks
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
import cv2
import rospy
import time
import numpy
from message_filters import Subscriber 
import message_filters
import os

# imageQuantity = 0
# starttime = 0
class RecieveImage(object):
    def __init__(self):
        # Params
        self.image = None
        self.depth = None
        self.br = CvBridge()
        self.starttime = 0.0
        self.imageQuantity = 0
        self.imagePath = '/home/russapat/obodroid_ws/src/rs_capture/src/image'
        self.depthPath = '/home/russapat/obodroid_ws/src/rs_capture/src/depth'
        # self.msg.header = Header()
        #Node cycle rate in Hz
        self.loop_rate = rospy.Rate(1)
        self.image_sub = Subscriber('/camera/color/image_raw',Image)
        self.depth_sub = Subscriber('/camera/aligned_depth_to_color/image_raw',Image)
        self.TimeSynchronizer = message_filters.ApproximateTimeSynchronizer([self.image_sub,self.depth_sub],queue_size=10,slop=0.5)
        self.TimeSynchronizer.registerCallback(self.callback)
        # rospy.Subscriber("/camera/color/image_raw",Image,self.callback_rgb,queue_size=10)
    #     rospy.Subscriber("/camera/aligned_depth_to_color/image_raw",Image,self.callback_depth,queue_size=10)
    def callback(self, msg_img, msg_depth):
        time_get_info = msg_img.header.stamp
        rospy.loginfo('data recieve_{}')
        self.image = msg_img
        self.depth = msg_depth
        time_get_info= msg_img.header.stamp 
        msg_img = self.br.imgmsg_to_cv2(msg_img, desired_encoding="rgb8")
        msg_depth = self.br.imgmsg_to_cv2(msg_depth, desired_encoding="passthrough")
        if time_get_info - self.starttime >= 100000000.0:
        #     cv2.imwrite(os.path.join(self.imagePath,"img_{}.jpg".format(time_get_info)),msg_img)
        #     cv2.imwrite(os.path.join(self.depthPath,"depth_{}.png".format(time_get_info)),msg_depth)
            rospy.loginfo('saveImages')
        # cv2.imshow('rgb frame', rgb_image)
        # cv2.waitKey(1)
        # depthPath = '/home/russapat/obodroid_ws/src/rs_capture/src/depth'
        # imagePath = '/home/russapat/obodroid_ws/src/rs_capture/src/image'
        
        # cv2.imwrite(os.path.join(imagePath,"img_{}.jpg".format(times)),rgb_image)    #saveimage
    
    
    def start(self):
        rospy.loginfo("Timing images")
        while not rospy.is_shutdown():
            rospy.loginfo('recieve image')
            if self.image is not None:
                # self.pub.publish(br.cv2_to_imgmsg(self.image))
                rospy.loginfo('show image')
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node('recieveimage')
    my_node = RecieveImage()
    my_node.start()

    