#!/usr/bin/python3

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospy
import cv2
import os

class publish_image():
    def __init__(self):
        self.folderDirectory = {'camera1_color' : '/home/russapat/obodroid_ws/src/rs_capture/src/image',
        'camera1_depth' : '/home/russapat/obodroid_ws/src/rs_capture/src/depth',
        'camera2_color' : '/home/russapat/obodroid_ws/src/rs_capture/src/image',
        'camera2_depth' : '/home/russapat/obodroid_ws/src/rs_capture/src/depth'}                            # edit folder directory here
        self.count = 1
        self.reader = {'read_camera1_image' : None, 'read_camera1_depth' : None,
        'read_camera2_image' : None, 'read_camera2_depth' : None}                                           # image data collector
        self.publisher = {'cam1_img_publisher': rospy.Publisher('/camera1/color/image_raw', Image, queue_size=1),
        'cam1_depth_publisher': rospy.Publisher('/camera1/depth/image_raw', Image, queue_size=1),
        'cam2_img_publisher': rospy.Publisher('/camera2/color/image_raw', Image, queue_size=1),
        'cam2_depth_publisher': rospy.Publisher('/camera2/depth/image_raw', Image, queue_size=1)}           # msg publisher
        self.Message = {'cam1_img_msg': None, 'cam1_depth_msg': None,
        'cam2_img_msg': None, 'cam2_depth_msg': None}                                                       # msg collector
        
        
    def data_reader(self):
        dataFile = {'cam1_img': 'img_{}.jpg'.format(self.count), 
        'cam1_depth': 'depth_{}.png'.format(self.count),
        'cam2_img': 'img_{}.jpg'.format(self.count),
        'cam2_depth': 'depth_{}.png'.format(self.count)}                                               # file name, need to add camera number, For example cam1_img_1.png
    
        dataPath = {'cam1_img_path': os.path.join(self.folderDirectory['camera1_color'], dataFile['cam1_img']),
        'cam1_depth_paht': os.path.join(self.folderDirectory['camera1_depth'], dataFile['cam1_depth']), 
        'cam2_img_path': os.path.join(self.folderDirectory['camera2_color'], dataFile['cam2_img']),
        'cam2_depth_path': os.path.join(self.folderDirectory['camera2_depth'], dataFile['cam2_depth'])}     # join file name with foider directory

        self.reader['read_camera1_image'] = cv2.imread(dataPath['cam1_img_path'])                           # read image and collect in data collector
        self.reader['read_camera1_depth'] = cv2.imread(dataPath['cam1_depth_paht'])
        self.reader['read_camera2_image'] = cv2.imread(dataPath['cam2_img_path'])
        self.reader['read_camera2_depth'] = cv2.imread(dataPath['cam2_depth_path'])

        self.Message['cam1_img_msg'] = CvBridge().cv2_to_imgmsg(self.reader['read_camera1_image'], encoding='bgr8')      # convert cv2 image to image message 
        self.Message['cam1_depth_msg'] = CvBridge().cv2_to_imgmsg(self.reader['read_camera1_depth'], encoding='passthrough')
        self.Message['cam2_img_msg'] = CvBridge().cv2_to_imgmsg(self.reader['read_camera2_image'], encoding='bgr8')
        self.Message['cam2_depth_msg'] = CvBridge().cv2_to_imgmsg(self.reader['read_camera2_depth'], encoding='passthrough')

        self.publish_callback()                                          # time callback, change frequency here
        rate.sleep()

    def publish_callback(self, event = None):
        
        Msgs = {'cam1ColorMsg': self.Message['cam1_img_msg'], 'cam1DepthMsg': self.Message['cam1_depth_msg'],  
        'cam2ColorMsg': self.Message['cam2_img_msg'], 'cam2DepthMsg': self.Message['cam2_depth_msg']}       # collect message

        Msgs['cam1ColorMsg'].header.stamp = rospy.Time.now()                                                # add header
        Msgs['cam1DepthMsg'].header.stamp = rospy.Time.now()
        Msgs['cam2ColorMsg'].header.stamp = rospy.Time.now()
        Msgs['cam2DepthMsg'].header.stamp = rospy.Time.now()                                                
        Msgs['cam1ColorMsg'].header.frame_id = 'Camera 1 Color'
        Msgs['cam1DepthMsg'].header.frame_id = 'Camera 1 Depth'
        Msgs['cam2ColorMsg'].header.frame_id = 'Camera 2 Color'
        Msgs['cam2DepthMsg'].header.frame_id = 'Camera 2 Depth'
    
        rospy.loginfo('image publishing')                                                                   # debug message
        self.publisher['cam1_img_publisher'].publish(Msgs['cam1ColorMsg'])                                  # publish message
        self.publisher['cam1_depth_publisher'].publish(Msgs['cam1DepthMsg'])
        self.publisher['cam2_img_publisher'].publish(Msgs['cam2ColorMsg'])
        self.publisher['cam2_depth_publisher'].publish(Msgs['cam2DepthMsg'])

        self.count += 1                 # increse image number

if __name__ == '__main__':
    rospy.init_node('publish_image')    # init node
    mynode = publish_image() 
    rate = rospy.Rate(1)           
    # mynode.data_reader()
    # rospy.spin()                        #spin node to keep node alive
    while not rospy.is_shutdown():
        mynode.data_reader()
    rospy.spin()
