import tkinter as tk
from tkinter import messagebox as tkm
import random

import const as C
from gamestate import State
import Agents


class GomoEnv:
    def __init__(self, master, mode):
        self.master = master
        self.player = C.YOU
        self.mode = mode
        self.canvas = None
        self.board = None  # 盤面上の石を管理する二次元リスト
        self.color = {
            C.YOU: C.YOUR_COLOR,
            C.COM: C.COM_COLOR
        }

        # ウィジェットの作成
        self.createWidgets()

        # イベントの設定
        self.setEvents()

        # 五目並べのゲームの初期化
        self.initGomoEnv()

    def createWidgets(self):
        """ウィジェットの作成と配置"""
        # キャンパスの作成
        self.canvas = tk.Canvas(
            self.master,
            bg=C.BOARD_COLOR,
            width=C.CANVAS_SIZE,
            height=C.CANVAS_SIZE,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        # キャンバスを更新する
        self.canvas.update()

    def setEvents(self):
        """イベントの設定"""
        # キャンバス上のマウスクリックイベントを受け付ける
        self.canvas.bind("<ButtonPress>", self.click)

    def initGomoEnv(self):
        """ゲームの初期化"""
        # 盤面上の石を管理する二次元リストの作成
        self.board = [[None] * C.NUM_LINE for _ in range(C.NUM_LINE)]

        # 線と線の間隔(px)を計算
        self.interval = C.CANVAS_SIZE // (C.NUM_LINE + 1)

        # 交点描画位置の左上オフセット
        self.offset_x = self.interval
        self.offset_y = self.interval

        # 縦線を描画
        for x in range(C.NUM_LINE):
            # 線の開始と終了の座標を計算
            xs = x * self.interval + self.offset_x
            ys = self.offset_y
            xe = xs
            ye = (C.NUM_LINE - 1) * self.interval + self.offset_y

            # 線を描画
            self.canvas.create_line(
                xs, ys,
                xe, ye
            )

        # 横線を描画
        for y in range(C.NUM_LINE):
            xs = self.offset_x
            ys = y * self.interval + self.offset_y
            xe = (C.NUM_LINE - 1) * self.interval + self.offset_x
            ye = ys

            self.canvas.create_line(
                xs, ys,
                xe, ye
            )

    def drawDisk(self, x, y, color):
        """(x, y)の交点に色がcolorの石を置く"""
        # 交点中心座標の計算
        center_x = x * self.interval + self.offset_x
        center_y = y * self.interval + self.offset_y

        # 中心座標から円の開始座標と終了座標の計算
        xs = center_x - (self.interval * 0.8) // 2
        ys = center_y - (self.interval * 0.8) // 2
        xe = center_x + (self.interval * 0.8) // 2
        ye = center_y + (self.interval * 0.8) // 2

        # 円の描画
        tag_name = "disk_" + str(x) + "_" + str(y)
        self.canvas.create_oval(
            xs, ys,
            xe, ye,
            fill=color
        )

        return tag_name

    def getIntersection(self, x, y):
        """キャンバス上の座標を交点の位置に変換"""
        ix = (x - self.offset_x + self.interval // 2) // self.interval
        iy = (y - self.offset_y + self.interval // 2) // self.interval

        return ix, iy

    def count(self, x, y, color):
        """配置チェック"""
        # チェックする方向をリストに格納
        count_dir = [
            (1, 0),  # 右
            (1, 1),  # 右下
            (0, 1),  # 上
            (-1, 1)  # 左下
        ]

        max_ = 0  # 石の並び数の最大値

        # count_dirの方向に対しての石の並びチェック
        for i, j in count_dir:
            # 石の並びを1に初期化
            count_num = 1

            # (x, y)から現在の方向に対して1交点ずつ遠ざけながら石が連続しているかどうか
            for s in range(1, C.NUM_LINE):
                xi = x + i * s
                yj = y + j * s

                # 盤面の外は無視
                if xi < 0 or xi >= C.NUM_LINE or yj < 0 or yj >= C.NUM_LINE:
                    break

                # 異なる石が置かれている時は無視
                if self.board[yj][xi] != color:
                    break

                count_num += 1

            # 反対方向も同様にチェック
            for s in range(-1, -C.NUM_LINE, -1):
                xi = x + i * s
                yj = y + j * s

                if xi < 0 or xi >= C.NUM_LINE or yj < 0 or yj >= C.NUM_LINE:
                    break

                # 異なる石が置かれている時は無視
                if self.board[yj][xi] != color:
                    break

                count_num += 1

            if max_ < count_num:
                max_ = count_num

        return max_

    def check_win(self, x, y, color):
        if self.count(x, y, color) >= 5:
            return True
        return False

    def switchPlayer(self):
        self.player = C.COM if self.player == C.YOU else C.YOU

    def click(self, event):
        # 自分のターンじゃない時は何もしない
        if self.player != C.YOU:
            return

        x, y = self.getIntersection(event.x, event.y)
        index = y * C.NUM_LINE + x

        # 盤面外の位置がクリックされたら何もしない
        if x < 0 or x >= C.NUM_LINE or y < 0 or y >= C.NUM_LINE or self.board[y][x] is not None:
            return

        self.lastStone = (x, y)
        self.board[y][x] = self.color[self.player]
        self.drawDisk(x, y, self.color[self.player])
        self.master.update_idletasks()

        # ゲーム状態の更新
        state = State([1 if x == C.YOUR_COLOR else 0 for row in self.board for x in row],
                      [1 if x == C.COM_COLOR else 0 for row in self.board for x in row])

        if self.check_win(x, y, self.color[self.player]):
            self.master.after(100, self.showResult())
            return

        self.switchPlayer()

        # AIのターン
        # モードに応じてAIの行動を選択
        if self.mode == "Random":
            action = Agents.random_action(state)
        elif self.mode == "MiniMax":
            action = Agents.mini_max_action(state)
        elif self.mode == "AlphaBeta":
            action = Agents.alpha_beta_action(state)
        elif self.mode == "MCTS":
            action = Agents.mcts_action(state)
        elif self.mode == "test_com":
            x, y = self.com1()
            if x is not None and y is not None:
                action = y * C.NUM_LINE + x
            else:
                action = None

        ax, ay = action % C.NUM_LINE, action // C.NUM_LINE
        self.board[ay][ax] = self.color[self.player]
        self.drawDisk(ax, ay, self.color[self.player])
        self.master.update_idletasks()

        if self.check_win(ax, ay, self.color[self.player]):
            self.master.after(100, self.showResult())
            return

        self.switchPlayer()

    def showResult(self):
        """ゲームの終了時の結果を表示"""
        # 勝利者はその時に石をおいた人
        winner = self.player

        # 結果をメッセージボックスで表示
        if winner == C.YOU:
            tkm.showinfo("結果", "あなたの勝ちです！！！")
        else:
            tkm.showinfo("結果", "あなたの負けです...")

        # 勝利メッセージ表示後、タイトル画面に戻る
        self.returnToTitle()

    def returnToTitle(self):
        """タイトル画面に戻る"""
        # 現在のゲーム画面のウィジェットをクリア
        self.canvas.destroy()

        from Title import TitleScreen
        # タイトル画面を表示
        TitleScreen(self.master)

    def com1(self):
        """COMを石を置かせる"""
        # 相手が石をおいた時に石が最大で交差する座標を取得
        max_list = []
        max_ = 0
        for y in range(C.NUM_LINE):
            for x in range(C.NUM_LINE):
                if not self.board[y][x]:
                    # (x, y)座標に相手が置いた石を置いた場合に石が連続する数を取得
                    count_num = self.count(x, y, self.color[C.YOU])
                    if count_num == max_:
                        max_list.append((x, y))
                    elif count_num > max_:
                        max_list = []
                        max_list.append((x, y))
                        max_ = count_num

        # 連続する石が最大になる交点から一つランダムに選択
        if max_list:
            choice = random.randrange(len(max_list))
            x, y = max_list[choice]
            return x, y
        return None