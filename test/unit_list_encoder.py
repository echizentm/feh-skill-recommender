import numpy as np
import unittest
from fehsr.unit import Unit
from fehsr.unit_list_encoder import UnitListEncoder


class TestUnitListEncoder(unittest.TestCase):
    def test_fit_transform(self):
        status_dict_1 = {
            'name': 'アルフォンス', 'weapon_type': '剣', 'movement_type': '歩兵',
            'hp': 43, 'attack': 51, 'speed': 25, 'defence': 32, 'resist': 22,
        }
        status_dict_2 = {
            'name': 'シャロン', 'weapon_type': '槍', 'movement_type': '歩兵',
            'hp': 43, 'attack': 48, 'speed': 35, 'defence': 29, 'resist': 22,
        }
        unit_list = [Unit(status_dict_1), Unit(status_dict_2)]

        unit_array = UnitListEncoder().fit_transform(unit_list)
        self.assertIsInstance(unit_array, np.ndarray)
        self.assertEqual(unit_array.shape, (2, 13))


if __name__ == '__main__':
    unittest.main()
