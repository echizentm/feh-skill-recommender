# feh-skill-recommender

## 概要

このツールは[ファイアーエムブレムヒーローズ](https://fire-emblem-heroes.com/ja/)のユニットのスキルの空きスロットに入れるスキルを推薦するツールです。
空いているスロットに何を入れたらいいかわからないよ、というときに使います。
遊びで作ったやつなので、ご利用は自己責任でお願いします。

## インストール

```
$ pipenv install
```

## 使い方

```
$ pipenv run fehsr [ユニット名]
```

例えば以下のような感じ。

```
$ pipenv run fehsr ラインハルト1
loading data files.
done.
loading model file.
done.
name: ラインハルト
weapon_type: 青魔
movement_type: 騎馬
hp: 38
attack: 41
speed: 18
defence: 27
resist: 25
weapon: ダイムサンダ
assist: ---- => ----
special: 烈雷
passive_a: ---- => 鬼神の一撃3
passive_b: 待ち伏せ3
passive_c: 騎刃の紋章
total_parameter: 149
weighted_total_parameter: 141
...
```

初回実行時に学習が行われ、実行したディレクトリに `model.pickle` というファイルができます。
このファイルを消すか、ツール実行時に -t を指定すると再学習が行われます。
自分でデータを増やした時とかはこれをやってください。

```
$ pipenv run fehsr [ユニット名] -t
```
