# モンテカルロ木探索などを用いた五目並べ対戦ゲーム

あまり頭が良くないので，const.py内のNUM_LINEを15にして，対戦エージェントをtest_comにした方が楽しめます．

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
