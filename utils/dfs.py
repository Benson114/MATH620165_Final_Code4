import numpy as np
from src.operations import read_maze

maze = read_maze()

# 给定两个坐标，判断它们在迷宫上的连通性
start = (63, 44)
goal = (1, 0)

# 使用深度优先搜索算法
# 坐标的表示方法是(x, y)，x表示列，y表示行
def dfs(maze, start, goal):
    # 初始化栈
    stack = []
    stack.append(start)

    # 初始化访问标记数组
    visited = np.zeros_like(maze)

    # 开始搜索
    while len(stack) > 0:
        # 从栈中取出一个坐标
        x, y = stack.pop()

        # 如果这个坐标是终点，则搜索成功
        if (x, y) == goal:
            return True

        # 标记这个坐标已经被访问过
        visited[y, x] = 1

        # 检查上下左右四个方向的坐标
        # 如果某个方向的坐标没有被访问过，且不是墙，就把它加入栈中
        if y > 0 and visited[y-1, x] == 0 and maze[y-1, x] == 0:
            stack.append((x, y-1))
        if y < maze.shape[0] - 1 and visited[y+1, x] == 0 and maze[y+1, x] == 0:
            stack.append((x, y+1))
        if x > 0 and visited[y, x-1] == 0 and maze[y, x-1] == 0:
            stack.append((x-1, y))
        if x < maze.shape[1] - 1 and visited[y, x+1] == 0 and maze[y, x+1] == 0:
            stack.append((x+1, y))

    # 如果栈空了还没有返回，说明搜索失败
    return False

if __name__ == "__main__":
    print(dfs(maze, start, goal))