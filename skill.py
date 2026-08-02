import js
import random

#スキルの選択するよ
def get_skill_choices():
    skills = []

    # 特殊スキル一覧（固定ID）
    special_skills = [
        {"id": 100, "name": "クリティカル率アップ", "type": "crit", "value": 10},
        {"id": 101, "name": "wave終了時にHPが回復", "type": "life", "value": 20},
        {"id": 102, "name": "出目が10以下の時攻撃力アップ", "type": "value_ten", "value": 2},
    ]

    # ステータス強化スキル生成（固定ID）
    def generate_stat_skill():
        # どちらのステータスを生成するか（50% / 50%）
        if random.random() < 0.5:
            stat_type = "atk"
            stat_name = "攻撃力"
            base_id = 10  # 11,12,13
        else:
            stat_type = "hp"
            stat_name = "最大体力"
            base_id = 20  # 21,22,23

        # +5 / +10 / +20 の確率
        r = random.random()
        if r < 0.6:
            value = 1.1
            skill_id = base_id + 1
        elif r < 0.9:
            value = 1.2
            skill_id = base_id + 2
        else:
            value = 1.5
            skill_id = base_id + 3

        return {
            "id": skill_id,
            "name": f"{stat_name} +{value} + 倍",
            "type": stat_type,
            "value": value
        }

    # 3枠を独立抽選
    for _ in range(3):
        r = random.random()

        if r < 0.3:
            skills.append(random.choice(special_skills))
        else:
            skills.append(generate_stat_skill())

    return skills