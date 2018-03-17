import unittest
from fehsr.unit import Unit, SkillType, NO_SKILL_LABEL
from fehsr.classifier import Classifier
from fehsr.skill_condition import SkillCondition


class TestClassifier(unittest.TestCase):
    def test_fit_predict(self):
        status_dict_1 = {
            'name': 'アルフォンス', 'weapon_type': '剣', 'movement_type': '歩兵',
            'hp': 43, 'attack': 51, 'speed': 25, 'defence': 32, 'resist': 22,
            'passive_a': '鬼神の一撃3',
        }
        status_dict_2 = {
            'name': 'シャロン', 'weapon_type': '槍', 'movement_type': '歩兵',
            'hp': 43, 'attack': 48, 'speed': 35, 'defence': 29, 'resist': 22,
            'passive_a': '速さ3',
        }
        unit_list = [Unit(status_dict_1), Unit(status_dict_2)]

        classifier = Classifier(SkillCondition())
        classifier.fit(unit_list, SkillType.PASSIVE_A)
        passive_a_list = classifier.predict(unit_list, SkillType.PASSIVE_A)
        self.assertEqual(list(passive_a_list), ['鬼神の一撃3', '速さ3'])

        classifier.fit(unit_list, SkillType.PASSIVE_B)
        passive_b_list = classifier.predict(unit_list, SkillType.PASSIVE_B)
        self.assertEqual(list(passive_b_list), [NO_SKILL_LABEL, NO_SKILL_LABEL])

if __name__ == '__main__':
    unittest.main()
