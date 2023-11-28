import tkinter as tk
from PIL import Image, ImageTk

import const as C


class TitleScreen:
    def __init__(self, master):
        self.master = master
        self.canvas = None

        self.difficulty = tk.StringVar(master, "Easy")  # デフォルトの難易度
        self.difficulties = ["Easy", "Medium", "Hard"]  # 難易度のオプション

        # 背景画像をロード
        self.background_image = Image.open("images/bg1.png")
        self.background_image = self.background_image.resize((C.CANVAS_SIZE, C.CANVAS_SIZE), Image.Resampling.LANCZOS)

        self.logo_image = Image.open("images/logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # ウィジェットの作成
        self.createWidgets()

    def start_game(self):
        self.canvas.pack_forget()
        from gomoenv import GomoEnv
        # ゲーム環境を開始するときに難易度を渡す
        GomoEnv(self.master, self.difficulty.get())

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

        # 背景画像をキャンバスに配置
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # ロゴ画像をキャンバスに配置
        self.canvas.create_image(
            C.CANVAS_SIZE / 2, 150,  # ロゴ画像の位置を調整
            image=self.logo_photo,
            anchor="center"
        )

        # 難易度選択のドロップダウンメニューをキャンバスに配置
        self.difficulty_menu = tk.OptionMenu(self.canvas, self.difficulty, *self.difficulties)
        self.difficulty_menu.config(width=10, font=('Helvetica', 12))  # オプションメニューのスタイルを設定
        difficulty_menu_window = self.canvas.create_window(
            C.CANVAS_SIZE / 2, 275,  # ドロップダウンメニューの位置をロゴの下に調整
            window=self.difficulty_menu,
            anchor="center"
        )

        # 開始ボタンの配置
        self.start_button_window = self.canvas.create_window(
            C.CANVAS_SIZE / 2, 350,  # 開始ボタンの位置を難易度選択メニューの下に調整
            window=tk.Button(
                self.canvas,
                text="ゲーム開始",
                command=self.start_game,
                padx=20, pady=10, borderwidth=0, relief=tk.FLAT
            ),
            anchor="center"
        )