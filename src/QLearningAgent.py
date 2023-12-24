import pickle
import numpy as np


class QLearningAgent:
    # 初始化Q表
    def __init__(self, state_space_size, action_space_size, alpha, gamma, epsilon):
        self.q_table = np.zeros((state_space_size, action_space_size))  # Q表
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.action_space_size = action_space_size  # 动作空间大小

    # 通过当前坐标计算在Q表中的状态索引

    # 根据当前状态选择动作
    def choose_action(self, state):
        # 以epsilon的概率进行探索，否则利用Q表
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.randint(self.action_space_size)  # 探索
        else:
            action = np.argmax(self.q_table[state])  # 利用
        return action

    # 更新Q表
    def update(self, state, action, reward, next_state):
        old_value = self.q_table[state][action]  # 旧值
        next_max = np.max(self.q_table[next_state])  # 下一状态的最大值
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)  # 新值
        self.q_table[state][action] = new_value  # 更新Q表

    # 保存Q表
    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.q_table, f)
            f.close()

    # 加载Q表
    def load(self, path):
        try:
            open(path, 'rb')
        except FileNotFoundError:
            print("Q-table file not found.")
            return

        with open(path, 'rb') as f:
            self.q_table = pickle.load(f)
            f.close()
