import random

import const as C


class State:
    def __init__(self, pieces=None, enemy_pieces=None):
        # 石の配置
        self.pieces = pieces if pieces is not None else [0] * C.NUM_LINE**2
        self.enemy_pieces = enemy_pieces if enemy_pieces is not None else [0] * C.NUM_LINE**2

        # 石の数の取得
    def piece_count(self, pieces):
        count = 0
        for i in pieces:
            if i == 1:
                count += 1
        return count

    def is_consecutive_five(self, line):
        """ 一列内に5つ連続する駒があるかチェックするヘルパー関数 """
        count = 0
        for piece in line:
            if piece == 1:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
        return False

    def is_lose(self):
        """負けかどうか"""
        n = C.NUM_LINE

        # 横方向のチェック
        for row in range(n):
            if self.is_consecutive_five(self.enemy_pieces[row*n:(row+1)*n]):
                return True

        # 縦方向のチェック
        for col in range(n):
            if self.is_consecutive_five(self.enemy_pieces[col:n**2:n]):
                return True

        # 斜め方向のチェック
        for d in range(n - 4):
            # 左上から右下へ
            if self.is_consecutive_five([self.enemy_pieces[i*n + i] for i in range(d, n)]):
                return True
            # 右上から左下へ
            if self.is_consecutive_five([self.enemy_pieces[i*n + (n - 1 - i)] for i in range(d, n)]):
                return True

        return False

    def is_draw(self):
        """引き分けかどうか"""
        return self.piece_count(self.pieces) + self.piece_count(self.enemy_pieces) == C.NUM_LINE**2

    def is_done(self):
        """ゲーム終了か"""
        return self.is_lose() or self.is_draw()

    def next(self, action):
        """次の状態を取得"""
        pieces = self.pieces.copy()
        enemy_pieces = self.enemy_pieces.copy()
        if self.is_first_player():
            pieces[action] = 1  # 現在のプレイヤーが先手（人間）の場合
        else:
            enemy_pieces[action] = 1  # 現在のプレイヤーが後手（AI）の場合
        return State(pieces, enemy_pieces)

    def legal_actions(self):
        """合法手のリスト取得"""
        actions = []
        for i in range(C.NUM_LINE**2):
            if self.pieces[i] == 0 and self.enemy_pieces[i] == 0:
                actions.append(i)
        return actions

    def is_first_player(self):
        """先手かどうか"""
        return self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)

    def __str__(self):
        """文字列表示"""
        #ox = (C.YOUR_COLOR, C.COM_COLOR) if self.is_first_player() else (C.COM_COLOR, C.YOUR_COLOR)
        ox = ("o", "x") if self.is_first_player() else ("x", "o")
        str = ""
        for i in range(C.NUM_LINE**2):
            if self.pieces[i] == 1:
                str += ox[0]
            elif self.enemy_pieces[i] == 1:
                str += ox[1]
            else:
                str += "-"
            if i % 15 == 14:
                str += "\n"
        return str

    def evaluate(self):
        """現在の状態の評価"""
        score = 0
        n = C.NUM_LINE

        # 駒の並びの評価
        def evaluate_line(line):
            count = 0
            max_count = 0
            for piece in line:
                if piece == 1:
                    count += 1
                    max_count = max(max_count, count)
                else:
                    count = 0
            return max_count

        # 横方向
        for row in range(n):
            score += evaluate_line(self.pieces[row * n:(row + 1) * n])

        # 縦方向
        for col in range(n):
            score += evaluate_line(self.pieces[col:n ** 2:n])

        # 斜め方向
        for d in range(n - 4):
            # 左上から右下へ
            score += evaluate_line([self.pieces[i * n + i] for i in range(d, n)])
            # 右上から左下へ
            score += evaluate_line([self.pieces[i * n + (n - 1 - i)] for i in range(d, n)])

        return score