import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
read_txt_car = open("/home/russapat/obodroid_ws/src/rs_capture/text/human_walking_2d_traj_221106.txt", "r")
read_txt_rtab = open("/home/russapat/obodroid_ws/src/rs_capture/text/global_poses_maxdepth_4_5.txt", "r")
# read_txt_rtab = open("/home/russapat/obodroid_ws/src/rs_capture/text/gobal_optimize_poses.txt", "r")
save_txt_car = read_txt_car.read().split()
save_txt_rtab = read_txt_rtab.read().split()
# print(save_txt) 
# print(len(save_txt))

x = []
y = []
a = []
b = []
index = 1
index_rtab = 1

# print(int(len(save_txt)/12))
for i in range(int(len(save_txt_car)/8)):
    x.append(float(save_txt_car[index]))
    y.append(float(save_txt_car[index+1]))
    index +=8

for j in range(int(len(save_txt_rtab)/8)):
    a.append(float(save_txt_rtab[index_rtab]))
    b.append(float(save_txt_rtab[index_rtab+1]))
    index_rtab +=8

# print(x)
# print(y)
fig, myGraph = plt.subplots(1,1,figsize=(7,7))
myGraph.plot(x, y, 'r', a, b, 'b')
red_patch = mpatches.Patch(color='red', label='Cartographer')
blue_patch = mpatches.Patch(color='blue', label='RTAB-Map')
myGraph.legend(handles=[red_patch,blue_patch],loc ='upper right')
plt.xlabel('x - axis [m]')
plt.ylabel('y - axis [m]')
plt.xlim(-2,8)
plt.show()
# plt.figure(figsize=(8,8))
# plt.plot(x, y, 'r--', a, b, 'b--')

# plt.xticks(range(-15,8,2))
# plt.yticks(range(-15,8,2))

# plt.title('trajectory')
# plt.show()

