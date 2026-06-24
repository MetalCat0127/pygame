import js
import json

print("おめでとう！")

def init_game(stage_name):
    # ▼ JSON を読み込む
    with open(f"get_stage/{stage_name}.json", "r") as f:
        stage = json.load(f)

    # ▼ JSON から値を取り出す
    dice_faces = stage["dice"]
    enemy_list = stage["enemies"]
    max_wave = stage["wave_max"]

    # ▼ 敵の数とHPを抽出
    enemy_list = stage["enemies"]
    enemy_hp = [e["hp"] for e in enemy_list]
    enemy_count = len(enemy_list)

    # ▼ プレイヤー情報（固定初期値）
    level = 1
    exp = 0

    # ▼ wave 初期値
    wave = 1

    # ▼ JS に渡す（UI 更新）
    js.setDiceFaces(dice_faces)
    js.setLevel(level)
    js.setExp(exp)
    js.setWave(wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)

    print("ゲーム初期化完了:", stage_name)
