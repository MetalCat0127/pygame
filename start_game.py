print("start_game.py loaded")

def init_game(stage_name):
    import js
    from fight import start_turn
    stage = stage_data.to_py()  # ← JS から渡された JSON を受け取る

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
    exp_max = 10
    wave = 1
    reroll_max = 3

    js.setLevel(level)
    js.setExp(exp, exp_max)
    js.setWave(wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)
    js.setRerollMax(reroll_max)

    print("ゲーム初期化完了:", stage_name)

    js.register_events()

    start_turn()