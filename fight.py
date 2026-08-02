print("fight.py loaded")
import js
import random

dice_values = []
current_damage = 0
enemy_hp = None
enemy_max_hp = None
current_wave = None
max_wave = None
exp = 0
exp_max = 5
level = 1

def start_wave(wave=None):
    global current_wave
    global enemy_hp, enemy_atk
    global enemy_img_idle, enemy_img_warn, enemy_img_attack
    global enemy_action_interval
    global enemy_interval, enemy_interval_max
    global enemy_exp_total

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
    enemy_img_attack = [e["img_attack"] for e in enemies]
    enemy_action_interval = [e["action_interval"] for e in enemies]
    enemy_interval = [e["action_interval"] for e in enemies]
    enemy_interval_max = enemy_interval.copy()
    enemy_exp_total = sum(e["exp"] for e in enemies)

    enemy_count = len(enemies)

    # ▼ JS に UI 更新を送る
    js.setWave(current_wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)
    js.setEnemyImages(enemy_img_idle)  # ★ 初期画像をセット
    js.setEnemyInterval(enemy_interval)
    js.setPlayerHP(player_hp)

    if current_wave == 1:
        js.setPlayerMaxHP(player_hp);
    
    js.showWaveStart(current_wave)

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
    roles = []   # ← 複数役を入れる配列

    # ファイブダイス
    if counts == [5]:
        roles += ["one_pair", "three_kind", "four_kind", "five_kind"]
        multiplier = 5.0
        role = "ファイブダイス"

    # フォーダイス
    elif counts == [4,1]:
        roles += ["one_pair", "three_kind", "four_kind"]
        multiplier = 3.0
        role = "フォーダイス"

    # フルハウス
    elif counts == [3,2]:
        roles += ["one_pair", "two_pair", "three_kind", "full_house"]
        multiplier = 2.0
        role = "フルハウス"

    # スリーダイス
    elif counts == [3,1,1]:
        roles += ["one_pair", "three_kind"]
        multiplier = 1.5
        role = "スリーダイス"

    # ツーペア
    elif counts == [2,2,1]:
        roles += ["one_pair", "two_pair"]
        multiplier = 1.3
        role = "ツーペア"

    # ワンペア
    elif counts == [2,1,1,1]:
        roles += ["one_pair"]
        multiplier = 1.1
        role = "ワンペア"

    # ストレート
    elif unique == [1,2,3,4,5] or unique == [2,3,4,5,6]:
        roles += ["straight"]
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
    global enemy_hp, current_wave, enemy_interval, enemy_interval_max, player_hp

    dmg = js.getDamageValue()
    target = js.getTargetIndex()

    # ターゲット選択処理
    target = js.getTargetIndex()

    # ★ 死んだ敵ならHP最小の敵を選ぶし、なんならtargetなしでもいい感じに動く
    if target < 0 or enemy_hp[target] <= 0:
        target = get_lowest_hp_target(enemy_hp)
        js.highlightTarget(target)

    # ▼ ダメージ反映
    enemy_hp[target] -= dmg
    if enemy_hp[target] < 0:
        enemy_hp[target] = 0
        js.killEnemy(target)

    js.setEnemyHP(enemy_hp)
    js.enemyHitEffect(target)
    js.showDamage(target, dmg)
    js.slashEffect(target)

    # ▼ 全滅チェック
    if all(hp <= 0 for hp in enemy_hp):
        add_temp_exp(enemy_exp_total)
        start_wave()
        return

    # ▼ ★ 攻撃後：敵インターバルを減らす
    for i in range(len(enemy_interval)):
        if enemy_hp[i] <= 0:
            continue

        enemy_interval[i] -= 1

        # JSに表示更新
        js.updateEnemyInterval(i, enemy_interval[i])

        # ▼ ★ インターバルが0なら敵攻撃
        if enemy_interval[i] <= 0:
            player_hp -= enemy_atk[i]
            if player_hp < 0:
                player_hp = 0

            js.updatePlayerHP(player_hp)

            # インターバル初期化
            enemy_interval[i] = enemy_interval_max[i]
            js.updateEnemyInterval(i, enemy_interval[i])

            # プレイヤー死亡チェック
            if player_hp <= 0:
                js.gameOver()
                return

    # ▼ ★ 攻撃後：リロール回数リセット
    js.resetReroll()

    # ▼ 次のターンへ（サイコロ振り直し）
    start_turn()

#生きてる敵にターゲット
def get_lowest_hp_target(enemy_hp):
    min_hp = None
    target = None

    for i, hp in enumerate(enemy_hp):
        if hp > 0:  # 生きてる敵だけ
            if min_hp is None or hp < min_hp:
                min_hp = hp
                target = i

    return target

#経験値の処理
def add_temp_exp(amount):
    global exp, exp_max, level

    exp += amount

    # レベルアップ回数を数える
    level_up_count = 0
    while exp >= exp_max:
        exp -= exp_max
        level += 1
        level_up_count += 1

    # UI更新
    js.setLevel(level)
    js.setExp(exp, exp_max)

    # スキル選択フェーズへ移行
    if level_up_count > 0:
        js.startSkillSelect(level_up_count)
    else:
        js.onExpGained(amount)

    return

#スキルの選択するよ

def get_skill_choices():
    skills = []

    # 特殊スキル一覧
    special_skills = [
        {"id": 100, "name": "攻撃速度アップ", "type": "aspd", "value": 1},
        {"id": 101, "name": "クリティカル率アップ", "type": "crit", "value": 5},
        {"id": 102, "name": "HP自動回復", "type": "regen", "value": 2},
    ]

    # ステータス強化スキル生成
    def generate_stat_skill():
        # 50% 攻撃力、50% 体力
        if random.random() < 0.5:
            stat_type = "atk"
            stat_name = "攻撃力"
        else:
            stat_type = "hp"
            stat_name = "体力"

        # +5 / +10 / +20 の確率
        r = random.random()
        if r < 0.6:
            value = 5
        elif r < 0.9:
            value = 10
        else:
            value = 20

        return {
            "id": random.randint(1, 9999),  # 固有ID（必要なら固定化してもOK）
            "name": f"{stat_name} +{value}",
            "type": stat_type,
            "value": value
        }

    # 3枠を独立抽選
    for _ in range(3):
        r = random.random()

        if r < 0.3:
            # 特殊スキル
            skills.append(random.choice(special_skills))
        else:
            # ステータス強化
            skills.append(generate_stat_skill())

    return skills