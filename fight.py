import js
import random

global player_atk, player_hp, player_hp_max
global player_crit, player_life, player_value_ten
global damage, dice_value
global current_wave
global enemy_hp, enemy_atk
global enemy_img_idle, enemy_img_warn, enemy_img_attack
global enemy_action_interval
global enemy_interval, enemy_interval_max
global enemy_exp_total
global exp, expmax, level
global stage_exp

dice_values = []
current_damage = 0
enemy_hp = None
enemy_max_hp = None
current_wave = None
max_wave = None
exp = 0
exp_max = 5
level = 1
player_hp_max = 100
player_atk = 0
player_crit = 0
player_life = 0
player_value_ten = 0

def start_wave(wave=None):
    global current_wave
    global enemy_hp, enemy_atk
    global enemy_img_idle, enemy_img_warn, enemy_img_attack
    global enemy_action_interval
    global enemy_interval, enemy_interval_max
    global enemy_exp_total
    global player_hp, player_hp_max
    global stage_exp
    global player_life

    # wave が指定されていない場合は次の wave に進む
    if wave is None:
        current_wave += 1
    else:
        current_wave = wave


    # wave が最大を超えたらクリア
    if current_wave > max_wave:
        js.addPermanentExp(stage_exp)   # 永続経験値加算
        js.showStageClear(stage_exp)    # UI表示
        return

    # waveごとの敵情報を取得
    stage_exp = stage_data["stage_exp"]
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

    if player_life == 1:
        if player_hp + 20 > player_hp_max:
            player_hp = player_hp_max
        else:
            player_hp += 20

    # ▼ JS に UI 更新を送る
    js.setWave(current_wave, max_wave)
    js.setEnemyCount(enemy_count)
    js.setEnemyHP(enemy_hp)
    js.setEnemyImages(enemy_img_idle)  # ★ 初期画像をセット
    js.setEnemyInterval(enemy_interval)
    js.setPlayerHP(player_hp)

    if current_wave == 1:
        player_hp_max = player_hp;
        js.setPlayerMaxHP(player_hp_max);
    
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
    global dice_value
    from collections import Counter
    c = Counter(values)
    counts = sorted(c.values(), reverse=True) #ソート便利だねぇ
    unique = sorted(c.keys())

    damage = sum(values)
    dice_value = damage
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

    damage = calc_bonus_damage(damage,dice_value)
    damage = int(damage * multiplier)
    return damage, multiplier, role


def apply_damage_to_enemy(dmg):
    global enemy_hp
    enemy_hp[0] -= dmg  # とりあえず1体目に攻撃
    if enemy_hp[0] < 0:
        enemy_hp[0] = 0

# ▼ 攻撃ボタンが押された
def on_attack_button():
    global enemy_hp, current_wave, enemy_interval, enemy_interval_max, player_hp
    global enemy_img_attack, enemy_img_idle

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
        level = add_temp_exp(enemy_exp_total)
        if not level:
            start_wave()
        return

    # ▼ ★ 攻撃後：敵インターバルを減らす
    for i in range(len(enemy_interval)):
        if enemy_hp[i] <= 0:
            continue

        enemy_interval[i] -= 1

        # JSに表示更新
        js.updateEnemyInterval(i, enemy_interval[i])

        #インターバルが1なら画像を変える
        if enemy_interval[i] == 1:
            js.updateEnemyImages(i, enemy_img_attack)

        # ▼ ★ インターバルが0なら敵攻撃
        if enemy_interval[i] <= 0:
            player_hp -= enemy_atk[i]
            if player_hp < 0:
                player_hp = 0

            js.updatePlayerHP(player_hp)
            js.updateEnemyImages(i, enemy_img_idle)

            # インターバル初期化
            enemy_interval[i] = enemy_interval_max[i]
            js.updateEnemyInterval(i, enemy_interval[i])

            # プレイヤー死亡チェック
            if player_hp <= 0:
                js.showGameOver()
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
        return True
    else:
        js.onExpGained(amount)
        return False


def apply_skill(skill_id):
    global player_atk, player_hp, player_hp_max
    global player_crit, player_life, player_value_ten
    global player_hp_temp

    player_hp_temp = player_hp_max

    # 攻撃力系
    if skill_id == 11:
        player_atk *= 1.1
    elif skill_id == 12:
        player_atk *= 1.2
    elif skill_id == 13:
        player_atk *= 1.5

    # 体力系
    if skill_id == 21:
        player_hp_max *= 1.1
        player_hp += player_hp_max - player_hp_temp
    elif skill_id == 22:
        player_hp_max *= 1.2
        player_hp += player_hp_max - player_hp_temp
    elif skill_id == 23:
        player_hp_max *= 1.5
        player_hp += player_hp_max - player_hp_temp

    js.setPlayerMaxHP(player_hp_max);
    js.setPlayerHP(player_hp);

    # 特殊スキル
    if skill_id == 100:
        player_crit = 1
    elif skill_id == 101:
        player_life = 1
    elif skill_id == 102:
        player_value_ten = 1

def calc_bonus_damage(damage,dice_value):
    global player_atk, player_crit, player_value_ten

    # ① 攻撃力の追加ダメージ
    damage += player_atk

    # ③ 出目が10以下なら2倍
    if player_value_ten == 1:
        if dice_value <= 10:
            damage *= 2

    # ② クリティカル（10%で2倍）
    if player_crit == 1:
        if random.random() < 0.10:
            damage *= 2

    return int(damage)

def put_json_data():
    global player_hp, player_hp_max, player_atk,current_wave,stage_exp
    global player_crit, player_life, player_value_ten
    global exp, expmax, level

    return {
        "progress": {
            "temp_stage": "stage" + str(stage_exp),
            "temp_wave": current_wave
        },
        "temp_state": {
            "temp_level": level,
            "temp_exp": exp,

            # ★ スキル名 → スキル値 の辞書
            "temp_skills": {
                "temp_crit": player_crit,
                "temp_life": player_life,
                "temp_value_ten": player_value_ten
            },

            "current_hp": player_hp,
            "max_hp": player_hp_max,
            "atk_bonus": player_atk
        }
    }