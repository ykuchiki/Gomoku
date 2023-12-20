import random

import const as C
from gamestate import State
from Agents import random_action, mini_max_action, alpha_beta_action, mcs_action, mcts_action


def first_player_point(ended_state):
    """先手プレイヤーのポイント"""
    if ended_state.is_lose():
        return 0 if ended_state.is_first_player() else 1
    return 0.5

def play(next_actions):
    """1ゲームの実行"""
    # 状態の生成
    state = State()

    # ゲーム終了までのループ
    while True:
        # ゲーム終了時
        if state.is_done():
            break
        # 行動の取得
        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)

        # 次の状態の取得
        state = state.next(action)

    return first_player_point(state)

def evaluate_algorithm_of(label, next_actions):
    """任意のアルゴリズムの評価"""
    # 複数回の対戦を繰り返す
    total_point = 0
    for i in range(C.EP_GAME_COUNT):
        if i % 2 == 0:
            total_point += play(next_actions)
        else:
            total_point += 1 - play(list(reversed(next_actions)))

        # 出力
        print("\rEvaluate {}/{}".format(i + 1, C.EP_GAME_COUNT), end="")
    print("")

    # 平均ポイントの計算
    average_point = total_point /C.EP_GAME_COUNT
    print(label.format(average_point))


# VSランダム
#next_action = (mcts_action, random_action)
#evaluate_algorithm_of("VS_Random {:.3f}", next_action)

# アルファベータ法
#next_action = (mcts_action, alpha_beta_action)
#evaluate_algorithm_of("VS_AlphaBeta {:.3f}", next_action)