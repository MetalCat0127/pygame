import json
import js

def __init__():
    dice_faces = [
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6]
    ]
    js.setDiceFaces(dice_faces) #ここでjsに初期値を渡す

def on_enemy_defeated():
    js.addExp(20)  # JSの経験値バーを更新