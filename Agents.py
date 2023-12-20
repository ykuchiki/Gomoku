import random
import math

from gamestate import State
import const as C

def random_action(state):
    """ランダムプレイ"""
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]


def mini_max(state, depth, max_depth):
    """ミニマックス法で状態価値計算"""
    # 負けは状態価値-1
    if state.is_lose():
        return -1
    # 引き分けは状態価値0
    if state.is_draw():
        return 0
    # 最大深さに達した場合
    if depth == max_depth:
        return state.evaluate()

    # 合法手の状態価値の計算
    best_score = -float("inf")
    for action in state.legal_actions():
        score = -mini_max(state.next(action), depth + 1, max_depth)
        if score > best_score:
            best_score = score

    return best_score  # 合法手の状態価値の最大値

def mini_max_action(state, max_depth=C.max_depth):
    """ミニマックス法で行動選択"""
    # 合法手の状態価値の計算
    best_action = 0
    best_score = -float("inf")
    str = ["", ""]
    for action in state.legal_actions():
        score = -mini_max(state.next(action), 0, max_depth)
        if score > best_score:
            best_action = action
            best_score = score

        # str[0] = "{}{:2d},".format(str[0], action)
        # str[1] = "{}{:2d},".format(str[1], score)
    # print("action:", str[0], "\nscore:", str[1], "\n")

    return best_action # 合法手の状態価値の最大を持つ行動を返す


def alpha_beta(state, alpha, beta, depth, max_depth):
    """アルファベータ法で状態価値計算"""
    if state.is_lose():
        return -1
    if state.is_draw():
        return 0
    if depth == max_depth:
        return state.evaluate()

    # 合法手の状態価値の計算
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -beta, -alpha, depth + 1, max_depth)
        if score > alpha:
            alpha = score

        # 現ノードのベストスコアが親ノードを超えたら探索終了
        if alpha >= beta:
            return alpha

    # 合法手の状態価値の最大値を返す
    return alpha

def alpha_beta_action(state, max_depth=C.max_depth):
    """アルファベータ法で行動選択"""
    # 合法手の状態価値の計算
    best_action = 0
    alpha = -float("inf")
    str = ["",""]
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -float("inf"), -alpha, 0, max_depth)
        if score > alpha:
            best_action = action
            alpha = score

        # str[0] = "{}{:2d},".format(str[0], action)
        # str[1] = "{}{:2d},".format(str[1], score)
    # print("action:", str[0], "\nscore:", str[1], "\n")
    return  best_action


def playout(state):
    """プレイアウト"""
    if state.is_lose():
        return -1
    if state.is_draw():
        return 0
    return playout(state.next(random_action(state)))

def mcs_action(state):
    """原始モンテカルロ探索で行動選択"""
    # 合法手ごとに10回プレイアウトした時の状態価値の合計の計算
    legal_actions = state.legal_actions()
    values = [0] * len(legal_actions)
    for i, action, in enumerate(legal_actions):
        for _ in range(100):
            values[i] += playout(state.next(action))

    return legal_actions[argmax(values)]

def argmax(collection, key=None):
    return collection.index(max(collection))

def mcts_action(state):
    """モンテカルロ木探索の行動選択"""
    # モンテカルロ木探索のノードの定義
    class Node:
        def __init__(self, state):
            self.state = state
            self.w = 0
            self.n = 0
            self.child_nodes = None

        def evaluate(self):
            if self.state.is_done():
                value = -1 if self.state.is_lose() else 0

                self.w += value
                self.n += 1
                return value

            if not self.child_nodes:
                value = playout(self.state)
                self.w += value
                self.n += 1
                if self.n == 10:
                    self.expand()
                return value
            else:
                value = -self.next_child_node().evaluate()

                self.w += value
                self.n += 1
                return value

        def expand(self):
            legal_actions = self.state.legal_actions()
            self.child_nodes = []
            for action in legal_actions:
                self.child_nodes.append(Node(self.state.next(action)))

        def next_child_node(self):
            for child_node in self.child_nodes:
                if child_node.n == 0:
                    return child_node

            t = 0
            for c in self.child_nodes:
                t += c.n
            ucb1_values = []
            for child_node in self.child_nodes:
                ucb1_values.append(-child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)

            return self.child_nodes[argmax(ucb1_values)]


    # 現在の局面のノード作成
    root_node = Node(state)
    root_node.expand()

    # 指定回数のシミュレーションを実行
    for _ in range(100):
        root_node.evaluate()

    # 試行回数の最大値を持つ行動を返す
    legal_actions = state.legal_actions()
    n_list = []
    for c in root_node.child_nodes:
        n_list.append(c.n)
    return legal_actions[argmax(n_list)]

