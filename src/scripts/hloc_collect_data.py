#!/usr/bin/python3

from importlib.resources import path
from tkinter import N
from tokenize import Number
from tracemalloc import start
# import rosbag
from sensor_msgs.msg import Joy, Image
import rospy
from message_filters import Subscriber
import message_filters
import os
import cv2
from cv_bridge import CvBridge, CvBridgeError



class data2rosbag():
    def __init__(self):
        self.loop_rate = rospy.Rate(10) #hz
        self.br = CvBridge()
        self.count = 0
        self.subscriber = rospy.Subscriber('/joy',Joy,self.joy_callback)
        self.homeDir = os.getenv('HOME')
        self.cameraInfo = {'RGB1': None, 'RGB2': None, 'RGB3': None}
        self.savePath = {"Camera_1_RGBPath": self.homeDir + "/Cam1", "Camera_2_RGBPath": self.homeDir + "/Cam2",
        "Camera_3_RGBPath": self.homeDir + "/Cam3" } # ---> edit folder name here
        self.subscriber_rgb = {"Camera_1_RGBSub": Subscriber('/camera1/color/image_raw',Image), "Camera_2_RBGSub": Subscriber('/camera2/color/image_raw',Image),\
            "Camera_3_RGBSub": Subscriber('/camera3/color/image_raw',Image)} 
        self.TimeSynchronizer = message_filters.ApproximateTimeSynchronizer([self.subscriber_rgb['Camera_1_RGBSub'], self.subscriber_rgb['Camera_2_RBGSub'],self.subscriber_rgb['Camera_3_RGBSub']],queue_size=10,slop=0.5)
        self.TimeSynchronizer.registerCallback(self.SnyCallback)
        # self.bag = rosbag.Bag('testbag.bag','w')
        # self.bag = rosbag.Bag('testbag2.bag','w')
        self.ButtoSstate = 0
    
    def SnyCallback(self, msgs1, msgs2, msgs3):
        # rospy.loginfo('snycallback')
        self.cameraInfo['RGB1'] = self.br.imgmsg_to_cv2(msgs1, desired_encoding='bgr8')
        self.cameraInfo['RGB2'] = self.br.imgmsg_to_cv2(msgs2, desired_encoding='bgr8')
        self.cameraInfo['RGB3'] = self.br.imgmsg_to_cv2(msgs3, desired_encoding='bgr8')

    def joy_callback(self, joy_data):
        rospy.loginfo('joy callback')
        if(joy_data.buttons[0] == 1 and self.ButtoSstate == 0): #green button
            self.ButtoSstate = 1
            cv2.imwrite(os.path.join(self.savePath['Camera_1_RGBPath'], 'rgb{}.png'.format(self.count)),self.cameraInfo['RGB1'])
            cv2.imwrite(os.path.join(self.savePath['Camera_2_RGBPath'], 'rgb{}.png'.format(self.count)),self.cameraInfo['RGB2'])
            cv2.imwrite(os.path.join(self.savePath['Camera_3_RGBPath'], 'rgb{}.png'.format(self.count)),self.cameraInfo['RGB3'])
            self.count += 1
        elif(joy_data.buttons[0] == 0 and self.ButtoSstate == 1):
            self.ButtoSstate = 0
        print(joy_data)

    def start(self):
        if not (os.path.exists(self.savePath['Camera_1_RGBPath'])) or \
            not (os.path.exists(self.savePath['Camera_2_RGBPath'])) or not (os.path.exists(self.savePath['Camera_3_RGBPath'])):

            os.mkdir(self.savePath['Camera_1_RGBPath'])
            os.mkdir(self.savePath['Camera_2_RGBPath'])
            os.mkdir(self.savePath['Camera_3_RGBPath'])
        # while not rospy.is_shutdown():
        #     rospy.loginfo('funtion start')
        #     self.loop_rate.sleep()
        # rospy.spin()

if __name__ == '__main__':
    rospy.init_node('data2rosbag')
    mynode = data2rosbag()
    mynode.start()
    rospy.spin()

