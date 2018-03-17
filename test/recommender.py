import unittest
from fehsr.unit import Unit, SkillType
from fehsr.recommender import Recommender


class TestRecommender(unittest.TestCase):
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

        recommender = Recommender('data')
        recommender.fit(unit_list)
        skill_dict = recommender.predict(unit_list)
        self.assertEqual(list(skill_dict[SkillType.PASSIVE_A]), ['鬼神の一撃3', '速さ3'])


if __name__ == '__main__':
    unittest.main()
