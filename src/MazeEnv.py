class MazeEnv:
    # 初始化迷宫环境
    def __init__(self, maze, start, goal):
        self.maze = maze  # 迷宫数据
        self.start = start  # 起点坐标
        self.goal = goal  # 终点坐标
        self.state = start  # 当前状态

    # 根据当前状态和动作，返回下一个状态和奖励
    def step(self, action):
        x, y = self.state
        # 根据动作计算新位置
        if action == 0:  # 向上移动一格，y轴坐标减1
            y -= 1
        elif action == 1:  # 向下移动一格，y轴坐标加1
            y += 1
        elif action == 2:  # 向左移动一格，x轴坐标减1
            x -= 1
        elif action == 3:  # 向右移动一格，x轴坐标加1
            x += 1

        # 检查新位置是否有效（不是墙也不是出界）
        if 0 <= x < self.maze.shape[1] and 0 <= y < self.maze.shape[0] and self.maze[y, x] == 0:
            self.state = (x, y)
            reward = 100 if self.state == self.goal else -1
        else:
            reward = -10  # 撞墙或出界的负奖励

        # 判断是否到达终点
        done = self.state == self.goal
        return self.state, reward, done

    # 重置迷宫环境
    def reset(self):
        self.state = self.start
        return self.state
