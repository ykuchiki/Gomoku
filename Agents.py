class MiniMaxAgent:
    def __init__(self, depth):
        """
        ミニマックス法はゼロサムゲームにおいて，最適な手を見つけるアルゴリズム
        :param depth: 探索木の深さ 1だったら現在とその結果を考慮
        """
        self.depth = depth

    def choose_move(self, env):
        """ゲームの状態に基づいて次の手を選択する"""
        best_score = -float("inf")
        best_move = None
        for move in env.get_possible_actions():
            env.make_action(move)
