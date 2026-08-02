import js
import random

#スキルの選択するよ
def get_skill_choices():
    skills = []

    # 特殊スキル一覧（固定ID）
    special_skills = [
        {"id": 100, "name": "攻撃速度アップ", "type": "aspd", "value": 1},
        {"id": 101, "name": "クリティカル率アップ", "type": "crit", "value": 5},
        {"id": 102, "name": "HP自動回復", "type": "regen", "value": 2},
    ]

    # ステータス強化スキル生成（固定ID）
    def generate_stat_skill():
        # 50% 攻撃力、50% 体力
        if random.random() < 0.5:
            stat_type = "atk"
            stat_name = "攻撃力"
            base_id = 10  # 攻撃力系は 11,12,13
        else:
            stat_type = "hp"
            stat_name = "体力"
            base_id = 20  # 体力系は 21,22,23

        # +5 / +10 / +20 の確率
        r = random.random()
        if r < 0.6:
            value = 5
            skill_id = base_id + 1
        elif r < 0.9:
            value = 10
            skill_id = base_id + 2
        else:
            value = 20
            skill_id = base_id + 3

        return {
            "id": skill_id,
            "name": f"{stat_name} +{value}",
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
