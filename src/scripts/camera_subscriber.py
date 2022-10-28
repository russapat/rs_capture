#!/usr/bin/python3

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
from message_filters  import Subscriber
import message_filters
import cv2
import rospy
import os

class recieve_multi_realsense(object):
    def __init__(self):
        self.br = CvBridge() 
        self.loop_rate = rospy.Rate(1)  
        self.homeDir = os.getenv('HOME')
        self.CameraInfo = {"Camera_1_RGB": None, "Camera_1_Depth": None, "Camera_2_RGB": None, "Camera_2_Depth": None, 
        "Camera_3_RGB": None, "Camera_3_Depth": None}
        self.ImagePath = {"Camera_1_RGBPath": self.homeDir + "/ImageLeftCam1", "Camera_1_DepthPath": self.homeDir + "/DepthLeftCam1", 
        "Camera_2_RGBPath": self.homeDir + "/ImageFrontCam2", "Camera_2_DepthPath": self.homeDir + "/DepthFrontCam2", 
        "Camera_3_RGBPath": self.homeDir + "/ImageRightCam3", "Camera_3_DepthPath": self.homeDir + "/DepthRightCam3"}

        # use 2 camera
        self.ImageSubscriber = {"Camera_1_RGB_Sub": Subscriber('/camera1/color/image_raw',Image), "Camera_1_Depth_Sub": Subscriber('/camera1/aligned_depth_to_color/image_raw',Image), 
        "Camera_2_RGB_Sub": Subscriber('/camera2/color/image_raw',Image), "Camera_2_Depth_Sub": Subscriber('/camera2/aligned_depth_to_color/image_raw',Image)}

        # #use 3 camera
        # self.ImageSubscriber = {"Camera_1_RGB_Sub": Subscriber('/camera1/color/image_raw',Image), "Camera_1_Depth_Sub": Subscriber('/camera1/aligned_depth_to_color/image_raw',Image), 
        # "Camera_2_RGB_Sub": Subscriber('/camera2/color/image_raw',Image), "Camera_2_Depth_Sub": Subscriber('/camera2/aligned_depth_to_color/image_raw',Image), 
        # "Camera_3_RGB_Sub": Subscriber('/camera3/color/image_raw',Image), "Camera_3_Depth_Sub": Subscriber('/camera3/aligned_depth_to_color/image_raw',Image)}

        #use 2 camera
        self.TimeSynchronizer = message_filters.ApproximateTimeSynchronizer([self.ImageSubscriber["Camera_1_RGB_Sub"], self.ImageSubscriber["Camera_1_Depth_Sub"], 
        self.ImageSubscriber["Camera_2_RGB_Sub"], self.ImageSubscriber["Camera_2_Depth_Sub"]],queue_size=10,slop=0.5)

        # # use 3 cammera
        # self.TimeSynchronizer = message_filters.ApproximateTimeSynchronizer([self.ImageSubscriber["Camera_1_RGB_Sub"], self.ImageSubscriber["Camera_1_Depth_Sub"], 
        # self.ImageSubscriber["Camera_2_RGB_Sub"], self.ImageSubscriber["Camera_2_Depth_Sub"], 
        # self.ImageSubscriber["Camera_3_RGB_Sub"], self.ImageSubscriber["Camera_3_Depth_Sub"]],queue_size=10,slop=0.5)
        
        self.TimeSynchronizer.registerCallback(self.callback)
        self.timer = rospy.Timer(rospy.Duration(1), self.timer_callback)   #Change frequency here 
        self.count = 1

    def callback(self, msgs_img1, msgs_depth1, msgs_img2, msgs_depth2): # , msgs_img3, msgs_depth3
        
        # self.image = self.br.imgmsg_to_cv2(msgs_img, desired_encoding="bgr8")
        # self.depth = self.br.imgmsg_to_cv2(msgs_depth, desired_encoding="passthrough")
        # rospy.loginfo('encoding')
        self.CameraInfo['Camera_1_RGB'] = self.br.imgmsg_to_cv2(msgs_img1, desired_encoding="bgr8")
        self.CameraInfo['Camera_1_Depth'] = self.br.imgmsg_to_cv2(msgs_depth1, desired_encoding="mono16")
        self.CameraInfo['Camera_2_RGB'] = self.br.imgmsg_to_cv2(msgs_img2, desired_encoding="bgr8")
        self.CameraInfo['Camera_2_Depth'] = self.br.imgmsg_to_cv2(msgs_depth2, desired_encoding="mono16")

        # self.CameraInfo['Camera_3_RGB'] = self.br.imgmsg_to_cv2(msgs_img3, desired_encoding="bgr8")
        # self.CameraInfo['Camera_3_Depth'] = self.br.imgmsg_to_cv2(msgs_depth3, desired_encoding="passthrough")

    def timer_callback(self, event = None):
        # rospy.loginfo(*event)
        rospy.loginfo('timer callback')
        # get_time = rospy.Time.now()
        try:
            if self.CameraInfo['Camera_1_RGB'].all() is not None and self.CameraInfo['Camera_1_Depth'].all() is not None:
                cv2.imwrite(os.path.join(self.ImagePath['Camera_1_RGBPath'],"cam1_img_{}.png".format(self.count)),self.CameraInfo['Camera_1_RGB'])
                cv2.imwrite(os.path.join(self.ImagePath['Camera_2_RGBPath'],"cam2_img{}.png".format(self.count)),self.CameraInfo['Camera_2_RGB'])
                # cv2.imwrite(os.path.join(self.ImagePath['Camera_3_RGBPath'],"{}.png".format(get_time)),self.CameraInfo['Camera_3_RGB'])
                rospy.loginfo('Save Color Images')
                cv2.imwrite(os.path.join(self.ImagePath['Camera_1_DepthPath'],"cam1_depth{}.png".format(self.count)),self.CameraInfo['Camera_1_Depth'])
                cv2.imwrite(os.path.join(self.ImagePath['Camera_2_DepthPath'],"cam2_depth{}.png".format(self.count)),self.CameraInfo['Camera_2_Depth'])
                # cv2.imwrite(os.path.join(self.ImagePath['Camera_3_DepthPath'],"{}.png".format(get_time)),self.CameraInfo['Camera_3_Depth'])
                rospy.loginfo('Save Depth Images')
                self.count += 1
            # cv2.imshow(''rgb frame', rgb_image)
        except:
            print("waiting images")

    def start(self):
        rospy.loginfo("start")
        if not os.path.exists(self.ImagePath["Camera_1_RGBPath"]):
            rospy.loginfo('Creating new folder')
            os.mkdir(self.ImagePath["Camera_1_RGBPath"])
            os.mkdir(self.ImagePath["Camera_2_RGBPath"])
            # os.mkdir(self.ImagePath["Camera_3_RGBPath"])
            os.mkdir(self.ImagePath["Camera_1_DepthPath"])
            os.mkdir(self.ImagePath["Camera_2_DepthPath"])
            # os.mkdir(self.ImagePath["Camera_3_DepthPath"])
        while not rospy.is_shutdown():
            rospy.loginfo('recieve image')
            if self.CameraInfo['Camera_3_RGB'] is not None:
                # self.pub.publish(br.cv2_to_imgmsg(self.image))
                rospy.loginfo('show image')
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node('recieve_rs')
    my_node = recieve_multi_realsense()
    my_node.start()