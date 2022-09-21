#! /usr/bin/python3

from sensor_msgs.msg import Image
from std_msgs.msg import std_msgs
from cv_bridge import CvBridge, CvBridgeError
import rospy
import cv2
import os
import message_filters

class img2msgs():
    def __init__(self):
        self.imgPathFolder =  '/home/russapat/obodroid_ws/src/rs_capture/src/image'
        self.depthPathFolder = '/home/russapat/obodroid_ws/src/rs_capture/src/depth'
        self.count = 1
        self.readImg = None
        self.readDepth = None
        self.imgPublisher = rospy.Publisher('/camera1/color/image_raw', Image, queue_size=1)
        self.depthPublisher = rospy.Publisher('/camera1/depth/image_raw', Image, queue_size=1)
        self.imgMsgs = None
        self.depthMsgs = None
    def main(self):
        imgFile = 'img_{}.jpg'.format(self.count)
        depthFile = 'depth_{}.png'.format(self.count)                   #need to change png to jpg

        imgpath = os.path.join(self.imgPathFolder, imgFile)                                     #join image file directory with folder directory 
        depthPath = os.path.join(self.depthPathFolder, depthFile)                               #join depth file directory with folder directory
        self.readImg = cv2.imread(imgpath)                                                      #read image
        self.readDepth = cv2.imread(depthPath)                                                  #read depth
        self.imgMsgs = CvBridge().cv2_to_imgmsg(self.readImg, encoding='passthrough')           #covert cv2 to imgmsgs
        self.depthMsgs = CvBridge().cv2_to_imgmsg(self.readDepth, encoding='passthrough')              
        rospy.Timer(rospy.Duration(1), self.publish_callback)

    def publish_callback(self, event = None):
        imgmsg = self.imgMsgs
        imgmsg.header.stamp = rospy.Time.now()
        imgmsg.header.frame_id = 'Camera1 Color Image Number {}'.format(self.count)
        depthmsg = self.depthMsgs
        depthmsg.header.stamp = rospy.Time.now()
        depthmsg.header.frame_id = 'Camera1 Depth Image Number {}'.format(self.count)
        rospy.loginfo('pulish image')
        self.imgPublisher.publish(imgmsg)
        self.depthPublisher.publish(depthmsg)
        self.count += 1

if __name__ == '__main__':
    rospy.init_node('ims2msgs')     #init node
    mynode = img2msgs()             #run class
    mynode.main()                   #run main
    rospy.spin()                    #spin node to keep alive