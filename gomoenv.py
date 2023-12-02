import tkinter as tk
import tkinter.messagebox as tkm
import random
import sys

import const as C


class GomoEnv:
    def __init__(self, master, difficulty):
        self.master = master
        self.player = C.YOU
        self.difficulty = difficulty
        self.canvas = None
        self.board = None  # 盤面上の石を管理する二次元リスト
        self.color = {
            C.YOU: C.YOUR_COLOR,
            C.COM: C.COM_COLOR
        }
        self.nextDisk = None
        self.interval = None
        self.lastStone = None
        self.blinkColor = "#506396"
        self.lastStoneVisible = False
        self.blinkTimer = None

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

    def click(self, event):
        """盤面がクリックされた時"""
        # 自分のターンじゃない時は何もしない
        if self.player != C.YOU:
            return

        x, y = self.getIntersection(event.x, event.y)

        # 盤面外の位置がクリックされたら何もしない
        if x < 0 or x >= C.NUM_LINE or y < 0 or y >= C.NUM_LINE:
            return

        # その座標に石がなければ石を置く
        if not self.board[y][x]:
            self.place(x, y, self.color[self.player])

    def place(self, x, y, color):
        """石を置く&配列操作"""
        self.stopBlinking()
        # 石の描画
        self.drawDisk(x, y, color)

        # 描画した円の色を管理リストに記憶
        self.board[y][x] = color

        # UIの更新を強制
        self.master.update_idletasks()

        self.lastStone = (x, y)
        # 相手の石のみチカチカさせる
        if self.player == C.COM:
            self.lastStoneVisible = False  # 最初の点滅を白の石の色で始める
            self.blinkLastStone()

        # 5つ並んだかチェック
        if self.count(x, y, color) >= 5:
            self.showResult()
            return

        # プレイヤーは交互に変更
        self.player = C.COM if self.player == C.YOU else C.YOU

        if self.player == C.COM:
            self.master.after(1000, self.com)

        print(self.board)

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

    def com(self):
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
        choice = random.randrange(len(max_list))
        x, y = max_list[choice]

        # 石を置く
        self.place(x, y, C.COM_COLOR)

    def blinkLastStone(self):
        """最新の石をチカチカさせる"""
        if self.lastStone:
            x, y = self.lastStone
            current_color = self.board[y][x]
            blink_color = self.blinkColor if self.lastStoneVisible else current_color
            blink_interval = 300 if self.lastStoneVisible else 600
            # 石の色を変更
            self.updateDiskColor(x, y, blink_color)
            self.lastStoneVisible = not self.lastStoneVisible
            # 指定した時間後に再度このメソッドを呼び出す
            self.blinkTimer = self.master.after(blink_interval, self.blinkLastStone)

    def updateDiskColor(self, x, y, color):
        """指定された石の色を更新する"""
        tag_name = f"disk_{x}_{y}"
        # 特定の石を削除
        self.canvas.delete(tag_name)
        # 新しい色で石を描画
        self.drawDisk(x, y, color)

    def stopBlinking(self):
        """チカチカを停止し、石を元の色に戻す"""
        if self.lastStone:
            x, y = self.lastStone
            original_color = self.board[y][x]
            self.updateDiskColor(x, y, original_color)
        if self.blinkTimer is not None:
            self.master.after_cancel(self.blinkTimer)
            self.blinkTimer = None

    def get_possible_actions(self):
        """現在の盤面から選択可能な行動をリストで返す"""
        possible_actions = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] is None:  # 医師が置かれてないマス
                    possible_actions.append((x, y))
        return possible_actions

    def make_action(self, move, player):
        """agent用アクションメソッド"""
        x, y = move
        self.board[y][x] = player

    def undo_action(self, move):
        """agent用アクション取り消しメソッド"""
        x, y = move
        self.board[y][x] = None  # 石を取り除く