import js

dice_values = []
current_damage = 0

def start_turn():
    global dice_values, current_damage

    # 1. サイコロを振り直す
    dice_values = roll_all_dice()

    # 2. JS に送って UI 更新
    js.updateDiceUI(dice_values)

    # 3. ダメージ計算
    current_damage = calc_damage(dice_values)

    # 4. 攻撃ボタンを有効化
    js.enableAttackButton()


def roll_all_dice():
    import random
    return [random.randint(1,6) for _ in range(5)]


def calc_damage(values):
    # 例：合計値をダメージにする
    return sum(values)


def on_attack_button():
    global current_damage

    # 1. 敵にダメージ
    apply_damage_to_enemy(current_damage)

    # 2. JS に敵HP更新を送る
    js.updateEnemyHP(enemy_hp)

    # 3. 敵の行動へ
    enemy_action()

    # 4. 次のターンへ
    start_turn()
