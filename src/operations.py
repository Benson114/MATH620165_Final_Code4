import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 迷宫数据储存在maze.txt中
# 每个迷宫格子用数字表示：0=路，1=墙
# 迷宫格子之间的分隔符是空格
# 迷宫共49行，65列
# 设定左上角为原点(0,0)，x轴向右，y轴向下
# 超出迷宫范围的格子，设定为墙

def read_maze():
    maze = []
    with open('./res/maze.txt', 'r') as f:
        for line in f.readlines():
            maze.append(line.strip().split(' '))
    maze = np.array(maze).astype(int)
    return maze

def draw_maze(maze):
    # 读取迷宫图像
    img = Image.open('./res/maze-2.jpg')
    img_array = np.array(img)

    # 将迷宫数据转换为图像数据
    for i in range(49):
        for j in range(65):
            if maze[i, j] == 1:
                # 墙用白色表示
                img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = 255
            elif maze[i, j] == 0:
                # 路用黑色表示
                img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = 0
            elif maze[i, j] == 2:
                # 起点用黄色表示
                img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = [255, 255, 0]
            elif maze[i, j] == 3:
                # 终点用红色表示
                img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = [255, 0, 0]
            elif maze[i, j] == 4:
                # 路径用绿色表示
                img_array[47+i*8:47+(i+1)*8, 49+j*8:49+(j+1)*8] = [0, 255, 0]
    img = Image.fromarray(img_array)

    # 保存图像
    img.save('./result.jpg')

    # 显示图像
    plt.imshow(img)
    plt.show()

def hash(maze):
    state2id = {}
    id2state = {}

    idx = 0
    for i in range(65):
        for j in range(49):
            if maze[j, i] == 0:
                state2id[(i, j)] = idx
                id2state[idx] = (i, j)
                idx += 1
    # state2id：坐标到状态索引的映射
    # id2state：状态索引到坐标的映射
    return state2id, id2state