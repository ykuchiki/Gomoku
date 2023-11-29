# モンテカルロ木探索などを用いた五目並べ対戦ゲーム

現在誠意実装中です．
ベースラインは完成してるので，一応遊べます．

poetryで環境を構築してください
```
poetry install
```

以下のコマンドで実行します．
```
poetry run python main.py
```

MacBookのAppleシリコンをお使いの方は，TkinterのGUI不具合が起こる可能性があります．
以下のコードで実行したら動くかもしれません．

```
arch -arm64 python main.py
```

![sample](images/sample.png)

## 今後実装予定
1. CPUの難易度別