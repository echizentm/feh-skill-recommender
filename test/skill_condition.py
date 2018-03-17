import unittest
from fehsr.skill_condition import SkillCondition
from fehsr.unit import Unit, SkillType


class TestSkillCondition(unittest.TestCase):
    def test_is_recommendable(self):
        skill_condition = SkillCondition()
        self.assertTrue(skill_condition.is_recommendable(SkillType.PASSIVE_B, '速さの封印3'))
        self.assertFalse(skill_condition.is_recommendable(SkillType.PASSIVE_B, '氷の封印'))

    def test_is_allowed(self):
        unit = Unit({
            'name': 'アルフォンス', 'weapon_type': '剣', 'movement_type': '歩兵',
            'hp': 43, 'attack': 51, 'speed': 25, 'defence': 32, 'resist': 22,
        })
        skill_condition = SkillCondition()
        self.assertTrue(skill_condition.is_allowed_to_unit(unit, SkillType.PASSIVE_B, '剣殺し3'))
        self.assertFalse(skill_condition.is_allowed_to_unit(unit, SkillType.PASSIVE_B, '槍殺し3'))
        self.assertFalse(skill_condition.is_allowed_to_unit(unit, SkillType.PASSIVE_B, '神罰の杖3'))


if __name__ == '__main__':
    unittest.main()
