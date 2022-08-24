## rs_capture
 create folder in home directory. By defualt --> cam1, cam2, cam3 
 To edit folder name, you can check in line 25,26 in hloc_collect_data.py

# Run realsense multicamera
check in github Obdvslam file name multiple_align_realsense.launch

~~~
roslaunch multiple_camera_process
~~~

#Run joy node 
~~~
rosrun joy joy_node
~~~

#Run hloc collect
~~~
rosrun rs_capture hloc_collect_data.py
~~~
