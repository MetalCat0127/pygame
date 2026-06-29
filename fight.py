print("fight.py loaded")
import js
import random

dice_values = []
current_damage = 0
enemy_hp = None
enemy_max_hp = None
current_wave = None
max_wave = None

def start_wave(wave=None):
    global current_wave, enemy_hp

    # wave が指定されていない場合は次の wave に進む
    if wave is None:
        current_wave += 1
    else:
        current_wave = wave

    # wave が最大を超えたらクリア
    if current_wave > max_wave:
        print("クリア(仮)")
        #js.showGameClear()
        return

    # waveごとの敵情報を取得
    enemies = stage_data["waves"][current_wave - 1]["enemies"]

    enemy_hp = [e["hp"] for e in enemies]
    enemy_count = len(enemies)

    # JS に UI 更新を送る
    js.setWave(current_wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)

    start_turn()

# ▼ ターン開始
def start_turn():
    global dice_values, current_damage

    dice_values = roll_all_dice()
    js.animateAllDice(dice_values)

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
    counts = sorted(c.values(), reverse=True) #ソート便利だねぇ
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
    elif counts == [2,1,1,1]:
        multiplier = 1.1
        role = "ワンペア"
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
    global enemy_hp, current_wave

    # ① ダメージ計算は JS で済んでいるので、JSから値をもらう
    dmg = js.getDamageValue()  # ← JS側で作る必要あり

    # ② ターゲット選択（JS側で選んだ index をもらう）
    target = js.getTargetIndex()

    # ③ 敵にダメージを与える
    enemy_hp[target] -= dmg

    # ④ HPが0以下なら倒す
    if enemy_hp[target] <= 0:
        enemy_hp[target] = 0

        # JSに敵HP更新を送る
        js.setEnemyHP(enemy_hp)

        # 全滅チェック
        if all(hp <= 0 for hp in enemy_hp):
            start_wave()
            return

    # ⑤ 敵HP更新
    js.setEnemyHP(enemy_hp)

    # 次のターンへ
    start_turn()