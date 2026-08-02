import js

def init_game(stage_name):
    from js import register_events
    import fight
    stage = stage_data.to_py()  # JSから渡されたJSON

    # ▼ ステージ開始時の初期化
    dice_list = [
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6],
        [1,2,3,4,5,6]
    ]

    max_wave = stage["wave_max"]

    level = 1
    exp = 0
    exp_max = 5
    player_hp = 100 + perm_hp_bonus
    player_atk = perm_atk_bonus
    player_crit = 0
    player_life = 0
    player_value_ten = 0    
    reroll_max = 3

    # ▼ UI更新（ステージ開始時だけ）
    js.setLevel(level)
    js.setExp(exp, exp_max)
    js.setWave(1, max_wave)
    js.setRerollMax(reroll_max)

    # ▼ fight.py にステージ情報を渡す
    fight.stage_data = stage
    fight.max_wave = max_wave
    fight.player_hp = player_hp
    fight.player_atk = player_atk

    print("ゲーム初期化完了:", stage_name)

    globals()["on_attack_button"] = fight.on_attack_button

    register_events()

    # ▼ wave1 を開始（敵情報は fight.py が処理）
    fight.start_wave(1)