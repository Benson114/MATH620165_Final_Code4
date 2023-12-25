import numpy as np
from tqdm import tqdm
from src.MazeEnv import MazeEnv
from src.QLearningAgent import QLearningAgent
from src.operations import read_maze, draw_maze, hash

# 读取迷宫数据和起点坐标
maze, start = read_maze(), (63, 44)

# 设定智能体的状态空间大小和动作空间大小
state_space_size, action_space_size = (maze == 0).sum(), 4  # 由于智能体不会出现在墙上，所以状态空间大小为迷宫数据中0的数量

# 生成状态索引和坐标的映射
state2id, id2state = hash(maze)

# 设定智能体的训练参数
train_kwargs = {"alpha": 0.1, "gamma": 0.9, "epsilon": 0.9}

# 设定训练的总回合数和每回合的最大步数
total_episodes, max_steps = 100000, 1000


def train(goal):
    # 初始化环境和智能体
    env = MazeEnv(maze=maze, start=start, goal=goal)
    agent = QLearningAgent(
        state_space_size=state_space_size,
        action_space_size=action_space_size,
        **train_kwargs
    )

    # 开始训练
    for episode in tqdm(range(total_episodes)):
        # 重置环境
        state = env.reset()
        done = False
        steps = 0

        while not done and steps < max_steps:
            # 根据当前状态选择动作
            action = agent.choose_action(state2id[state])
            # 执行动作，观察新状态和奖励
            new_state, reward, done = env.step(action)
            # 更新Q表
            agent.update(state2id[state], action, reward, state2id[new_state])
            # 移动到新状态
            state = new_state
            # 增加步数
            steps += 1

        # 可选：减少探索率
        agent.epsilon = max(agent.epsilon * 0.99, 0.1)

    # 设定Q表的路径
    path = f"./model/{goal[0]}-{goal[1]}.pkl"

    # 保存Q表
    agent.save(path)
    print("Q-table has been saved to {}".format(path))

    return agent


def extract_path(agent, start, goal):
    # 如果起点和终点相同，直接返回起点
    if start == goal:
        return [start]

    # 如果终点位置是墙，返回False
    if maze[goal[1], goal[0]] == 1:
        return False

    # 初始化环境
    env = MazeEnv(maze=maze, start=start, goal=goal)
    state = env.reset()

    # 从起点开始移动，直到到达终点或无法移动
    path = [state]
    done = False
    while not done:
        action = np.argmax(agent.q_table[state2id[state]])  # 选择最佳动作
        new_state, _, done = env.step(action)  # 执行动作

        if done:  # 如果到达终点，返回路径
            path.append(new_state)
            return path
        elif new_state in path:  # 如果无法移动，返回False
            return False
        else:  # 否则，继续移动
            path.append(new_state)
            state = new_state

    return False  # 如果未能到达终点，返回无效路径标识


if __name__ == '__main__':
    goal = input("请输入终点坐标，用空格分隔：")
    goal = tuple(map(int, goal.split()))

    q_table_path = f"./model/{goal[0]}-{goal[1]}.pkl"

    try:
        open(q_table_path, 'rb')
    except FileNotFoundError:
        print("Q-table file not found.")
        agent = train(goal)
    else:
        print("Q-table file found.")
        agent = QLearningAgent(
            state_space_size=state_space_size,
            action_space_size=action_space_size,
            **train_kwargs
        )
        agent.load(q_table_path)

    path = extract_path(agent, start, goal)

    if not path:
        print("无法到达终点")
        # 将起点和终点标记在迷宫上，用数字2表示起点，数字3表示终点
        maze_with_path = maze.copy()
        maze_with_path[start[1], start[0]] = 2
        maze_with_path[goal[1], goal[0]] = 3

        # 保存迷宫图像
        draw_maze(maze_with_path)
    else:
        # 将路径标记在迷宫上，用数字2表示起点，数字3表示终点，数字4表示路径
        maze_with_path = maze.copy()
        for point in path:
            maze_with_path[point[1], point[0]] = 4
        maze_with_path[start[1], start[0]] = 2
        maze_with_path[goal[1], goal[0]] = 3

        # 保存迷宫图像
        draw_maze(maze_with_path)
