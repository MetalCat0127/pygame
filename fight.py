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
    global current_wave
    global enemy_hp, enemy_atk
    global enemy_img_idle, enemy_img_warn, enemy_img_attack
    global enemy_action_interval

    # wave が指定されていない場合は次の wave に進む
    if wave is None:
        current_wave += 1
    else:
        current_wave = wave

    # wave が最大を超えたらクリア
    if current_wave > max_wave:
        print("クリア(仮)")
        return

    # waveごとの敵情報を取得
    enemies = stage_data["waves"][current_wave - 1]["enemies"]

    # ▼ JSON の情報を全部取り込む
    enemy_hp = [e["hp"] for e in enemies]
    enemy_atk = [e["atk"] for e in enemies]
    enemy_img_idle = [e["img_idle"] for e in enemies]
    enemy_img_warn = [e["img_warn"] for e in enemies]
    enemy_img_attack = [e["img_attack"] for e in enemies]
    enemy_action_interval = [e["action_interval"] for e in enemies]

    enemy_count = len(enemies)

    # ▼ JS に UI 更新を送る
    js.setWave(current_wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)
    js.setEnemyImages(enemy_img_idle)  # ★ 初期画像をセット

    start_turn()


# ▼ ターン開始
def start_turn():
    global dice_values

    dice_values = roll_all_dice()
    js.startTurnJS(dice_values)

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

    dmg = js.getDamageValue()
    target = js.getTargetIndex()

    # ★ ターゲット未選択（-1とかNone）のときは「HPが一番低い敵」を選ぶ
    if target is None or target < 0:
        # 生きている敵の中で最もHPが低い index
        alive = [(i, hp) for i, hp in enumerate(enemy_hp) if hp > 0]
        if not alive:
            return  # ありえないけど保険
        target = min(alive, key=lambda x: x[1])[0]

    enemy_hp[target] -= dmg

    if enemy_hp[target] <= 0:
        enemy_hp[target] = 0
        js.setEnemyHP(enemy_hp)

        if all(hp <= 0 for hp in enemy_hp):
            start_wave()
            return

    js.setEnemyHP(enemy_hp)
    start_turn()