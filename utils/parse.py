# %%
import numpy as np
# import matplotlib.pyplot as plt
from PIL import Image

# %%
# maze.png：迷宫图像
# 读取迷宫图像
img = Image.open('maze-2.jpg')

# %%
# plt.imshow(img)

# 地图左下角的点的坐标是：(49, 438)
# plt.plot(49, 438, 'ro', ms=0.5)

# 地图右上角的点的坐标是：(569, 47)
# plt.plot(569, 47, 'ro', ms=0.5)

# 迷宫共49行，65列
# 每个格子的宽度是：(569-49)/65=8
# 每个格子的高度是：(438-47)/49=8

# %%
# 需要根据每个格子的颜色来判断是墙还是路，偏黑的是路，不黑的是墙
# 但是一个格子内包含多个像素点，导致一个格子的颜色不是纯黑或纯白
# 所以需要对每个格子内的像素点颜色进行统计，然后取平均值，并根据一个阈值来判断是墙还是路

# %%
# 定义一个49*65的数组，用来存储每个格子的像素点颜色统计值
maze_color = np.zeros((49, 65))
# 读取图像的像素点
img_array = np.array(img)
# 统计每个格子内的像素点颜色，坐标范围：x1=49, x2=569, y1=47, y2=438
for i in range(49):
    for j in range(65):
        # 每个格子内的像素点颜色统计值
        maze_color[i, j] = np.mean(img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8])
# 统计值越高，说明越偏白；统计值越低，说明越偏黑
# 统计值大于阈值（设为50）且小于等于150，说明是墙；统计值小于阈值或大于150，说明是路（起点格子是黄色的，所以还要设置一个小于等于150的条件，为了避免将起点格子判断为墙）
maze_color = np.logical_and(maze_color > 50, maze_color <= 150)
# 将布尔类型的数组转换为整型数组
maze_color = maze_color.astype(int)

# %%
# 将迷宫地图保存为txt文件
np.savetxt('maze.txt', maze_color, fmt='%d', delimiter=' ')

# %%
# 根据img_array和maze_color绘制新的迷宫图像，保存为parsed_maze.jpg
for i in range(49):
    for j in range(65):
        if maze_color[i, j] == 1:
            img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = 255
        else:
            img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = 0
# 保存图像
img = Image.fromarray(img_array)
img.save('maze.jpg')
