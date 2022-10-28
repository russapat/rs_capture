#!/usr/bin/python3

import time
import rospy
import os
import subprocess


timenow = time.perf_counter()

# if timenow >= 2600:
#     print(timenow)
# else: 
#     print(timenow)
#     print(1)
# rospy.Time()
# gettime = 
while(True):
    rospy.loginfo(rospy.Time.now)
    rospy.loginfo('timer callback')
