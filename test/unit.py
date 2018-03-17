import unittest
from fehsr.unit import Unit, NO_SKILL_LABEL


class TestUnit(unittest.TestCase):
    def test_init(self):
        status_dict = {
            'name': 'アルフォンス',
            'weapon_type': '剣',
            'movement_type': '歩兵',
            'hp': 43,
            'attack': 51,
            'speed': 25,
            'defence': 32,
            'resist': 22,
            'weapon': 'フォルクヴァング',
            'special': '太陽',
            'passive_a': '鬼神の一撃3',
            'passive_c': '攻撃の紋章3',
        }
        unit = Unit(status_dict)

        self.assertEqual(unit.name, 'アルフォンス')
        self.assertEqual(unit.weapon_type, '剣')
        self.assertEqual(unit.movement_type, '歩兵')
        self.assertEqual(unit.hp, 43)
        self.assertEqual(unit.attack, 51)
        self.assertEqual(unit.speed, 25)
        self.assertEqual(unit.defence, 32)
        self.assertEqual(unit.resist, 22)
        self.assertEqual(unit.weapon, 'フォルクヴァング')
        self.assertEqual(unit.assist, NO_SKILL_LABEL)
        self.assertEqual(unit.special, '太陽')
        self.assertEqual(unit.passive_a, '鬼神の一撃3')
        self.assertEqual(unit.passive_b, NO_SKILL_LABEL)
        self.assertEqual(unit.passive_c, '攻撃の紋章3')


if __name__ == '__main__':
    unittest.main()
