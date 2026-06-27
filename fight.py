print("fight.py loaded")
import js
import random

dice_values = []
current_damage = 0

# ▼ ターン開始
def start_turn():
    global dice_values, current_damage

    dice_values = roll_all_dice()
    js.updateDiceUI(dice_values)

    dmg, mult, role = calc_damage(dice_values)
    current_damage = dmg

    # JS にダメージ情報を渡す
    js.showDamageInfo(dmg, mult, role)

    js.enableAttackButton()

# ▼ サイコロ5個を振る
def roll_all_dice():
    return [random.randint(1,6) for _ in range(5)]


# ▼ ダメージ計算（役判定）
def calc_damage(values):
    from collections import Counter
    c = Counter(values)
    counts = sorted(c.values(), reverse=True)
    unique = sorted(c.keys())

    base = sum(values)
    multiplier = 1.0
    role = "役なし"

    if counts == [5]:
        multiplier = 5.0
        role = "ファイブダイス"
    elif counts == [4,1]:
        multiplier = 3.0
        role = "フォーダイス"
    elif counts == [3,2]:
        multiplier = 2.0
        role = "フルハウス"
    elif counts == [3,1,1]:
        multiplier = 1.5
        role = "スリーダイス"
    elif counts == [2,2,1]:
        multiplier = 1.3
        role = "ツーペア"
    elif unique == [1,2,3,4,5] or unique == [2,3,4,5,6]:
        multiplier = 2.5
        role = "ストレート"

    damage = int(base * multiplier)
    return damage, multiplier, role


def apply_damage_to_enemy(dmg):
    global enemy_hp
    enemy_hp[0] -= dmg  # とりあえず1体目に攻撃
    if enemy_hp[0] < 0:
        enemy_hp[0] = 0

# ▼ 攻撃ボタンが押された
def on_attack_button():
    global current_damage

    # ★ 仮の処理（後で本物に置き換える）
    print("攻撃ボタンが押されたよ。ダメージ:", current_damage)

    # 敵の行動（仮）
    print("敵の行動フェーズ（仮）")

    # 次のターンへ
    start_turn()
