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
    from collections import Counter
    c = Counter(values)
    counts = sorted(c.values(), reverse=True)
    unique = sorted(c.keys())

    base = sum(values)
    multiplier = 1.0

    # ファイブダイス
    if counts == [5]:
        multiplier = 5.0

    # フォーダイス
    elif counts == [4,1]:
        multiplier = 3.0

    # フルハウス
    elif counts == [3,2]:
        multiplier = 2.0

    # スリーダイス
    elif counts == [3,1,1]:
        multiplier = 1.5

    # ツーペア
    elif counts == [2,2,1]:
        multiplier = 1.3

    # ストレート（1-5 or 2-6）
    elif unique == [1,2,3,4,5] or unique == [2,3,4,5,6]:
        multiplier = 2.5

    # 役なし
    else:
        multiplier = 1.0

    return int(base * multiplier)


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
