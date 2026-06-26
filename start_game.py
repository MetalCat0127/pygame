import js

def init_game(stage_name):
    stage = stage_data  # ← JS から渡された JSON を受け取る

    dice_list = [
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6]
    ],

    max_wave = stage["wave_max"]
    enemy_list = stage["enemies"]


    enemy_hp = [e["hp"] for e in enemy_list]
    enemy_count = len(enemy_list)

    level = 1
    exp = 0
    wave = 1

    js.setLevel(level)
    js.setExp(exp)
    js.setWave(wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)

    print("ゲーム初期化完了:", stage_name)
