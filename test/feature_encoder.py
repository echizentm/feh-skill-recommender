import numpy as np
import unittest
from fehsr.feature_encoder import FeatureEncoder


class TestFeatureEncoder(unittest.TestCase):
    def test_fit_transform(self):
        feature_encoder = FeatureEncoder()

        number_array = feature_encoder.fit_transform([6, 8, 11])
        self.assertIsInstance(number_array, np.ndarray)
        self.assertEqual(number_array.shape, (3, 1))
        self.assertIsInstance(number_array[0][0], np.float32)

        label_array = feature_encoder.fit_transform(sorted(['鉄の剣', '鋼の剣', '銀の剣']))
        self.assertIsInstance(label_array, np.ndarray)
        self.assertEqual(list(label_array.reshape(-1)), [1, 0, 0, 0, 1, 0, 0, 0, 1])


if __name__ == '__main__':
    unittest.main()
