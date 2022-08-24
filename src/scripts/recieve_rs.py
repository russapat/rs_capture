#! /usr/bin/python3

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
import cv2
import rospy
from message_filters import Subscriber 
import message_filters
import os

# starttime = 0
class RecieveImage(object):
    def __init__(self):
        # Params
        self.image = None
        self.depth = None
        
        self.br = CvBridge()
        self.imagePath = '/home/russapat/obodroid_ws/src/rs_capture/src/image'
        self.depthPath = '/home/russapat/obodroid_ws/src/rs_capture/src/depth'
        self.imageQuantity = 0
        # self.msg.header = Header()
        #Node cycle rate in Hz
        self.loop_rate = rospy.Rate(1)
        self.image_sub = Subscriber('/camera/color/image_raw',Image)
        self.depth_sub = Subscriber('/camera/aligned_depth_to_color/image_raw',Image)
        self.TimeSynchronizer = message_filters.ApproximateTimeSynchronizer([self.image_sub,self.depth_sub],queue_size=10,slop=0.5)
        self.TimeSynchronizer.registerCallback(self.callback)
        self.timer = rospy.Timer(rospy.Duration(1), self.timer_callback)   #Change frequency here
        
   
    def callback(self, msg_img, msg_depth):
        # rospy.loginfo('data recieve')
        self.image = self.br.imgmsg_to_cv2(msg_img, desired_encoding="bgr8")
        self.depth = self.br.imgmsg_to_cv2(msg_depth, desired_encoding="passthrough")
        
    def timer_callback(self, event):
        rospy.loginfo('callback access')
        get_timer = rospy.Time.now()
        self.imageQuantity += 1
        try:
            if self.image.any() is not None and self.depth.any() is not None:
                cv2.imwrite(os.path.join(self.imagePath,"img_{}.jpg".format(get_timer)),self.image)
                rospy.loginfo('Save Images')
                cv2.imwrite(os.path.join(self.depthPath,"depth_{}.png".format(get_timer)),self.depth)
                rospy.loginfo('Save Depth Images')
            # cv2.imshow(''rgb frame', rgb_image)
        except:
            print("waiting images")
        # cv2.waitKey(1)
    
    def start(self):
        rospy.loginfo("Timing images")
        while not rospy.is_shutdown():
            rospy.loginfo('recieve image')
            if self.image is not None:
                # self.pub.publish(br.cv2_to_imgmsg(self.image))
                rospy.loginfo('show image')
            self.loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node('recieve_rs')
    my_node = RecieveImage()
    my_node.start()

    