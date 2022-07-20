#!/usr/bin/python3

import cv2 
import pyrealsense2 as rs 
import numpy as np
from cv_bridge import CvBridge
import time
import os
 
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
imagePath = '/home/russapat/realsense_capture_ws/src/rs_capture/src/image'
imageQuantity = 0
imageLimit = 10
# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
found_rgb = False

for s in device.sensors: # s = [stereo Module, RGB Camera]
    # print(s.get_info(rs.camera_info.name))
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

cap = cv2.VideoCapture(0)
bridge = CvBridge()


starttime = 0
try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        colorizer = rs.colorizer()
        
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Aligning process
        align = rs.align(rs.stream.color)
        frames = align.process(frames)
        aligned_depth_frame = frames.get_depth_frame()
        
        depth = np.asanyarray(aligned_depth_frame.get_data())
        # Apply color on depth image
        colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())
        
        color_colormap_dim = color_image.shape                                                  # contain matrix size of color image
        depth_colormap_dim = colorized_depth.shape                                              # contain matrix size of depth image
        
        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((color_image, colorized_depth))                                  # depth_colormap is not align
        else:
            images = np.hstack((color_image, colorized_depth))                                  # depth_colormap is not align
        
            
        # print(images.shape)
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)
        # cv2.imshow('depth', depth)
        # cv2.waitKey(1)
        # # save image 
        currenttime = time.time()
        if currenttime - starttime >= 1 and imageQuantity < imageLimit:
            # y = ("img_{}.jpg".format(imageQuantity))
            cv2.imwrite(os.path.join(imagePath,"img_{}.jpg".format(imageQuantity)),color_image)
            imageQuantity = imageQuantity+1 
            starttime = currenttime
            print(currenttime)
            print(imageQuantity)
            
        
finally:

    # Stop streaming
    pipeline.stop()