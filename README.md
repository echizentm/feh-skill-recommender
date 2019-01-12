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
$ pipenv run fehsr エリウッド
loading data files.
done.
training data.
accuracy: {<SkillType.ASSIST: 'assist'>: '82 / 92', <SkillType.PASSIVE_A: 'passive_a'>: '166 / 166', <SkillType.SPECIAL: 'special'>: '140 / 149', <SkillType.PASSIVE_C: 'passive_c'>: '153 / 154', <SkillType.PASSIVE_B: 'passive_b'>: '127 / 137'}
done.
name: エリウッド
weapon_type: 剣
movement_type: 騎馬
hp: 39
attack: 50
speed: 30
defence: 23
resist: 32
weapon: 烈剣デュランダル
assist: ---- => 回り込み
special: 聖兜
passive_a: ---- => 鬼神の一撃3
passive_b: 斧殺し3
passive_c: 騎盾の紋章3
...
```

初回実行時に学習が行われ、実行したディレクトリに `model.pickle` というファイルができます。
このファイルを消すか、ツール実行時に -t を指定すると再学習が行われます。
自分でデータを増やした時とかはこれをやってください。

```
$ pipenv run fehsr [ユニット名] -t
```
