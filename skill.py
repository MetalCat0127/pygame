import js
import random

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