import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import StandardScaler


class FeatureEncoder:
    '''
    ユニットの情報を機械学習の特徴量に変換するクラス
    '''
    __slots__ = ['_label_binarizer', '_standard_scaler']

    def __init__(self):
        self._label_binarizer = LabelBinarizer()
        self._standard_scaler = StandardScaler()

    def fit(self, feature_list):
        '''
        :param [int or str] feature_list: 特徴量のリスト
        '''
        if not self._is_label_feature_list(feature_list):
            self._standard_scaler.fit(np.array(feature_list, dtype=np.float32).reshape(-1, 1))
            return

        self._label_binarizer.fit(feature_list)

    def transform(self, feature_list):
        '''
        :param [int or str] feature_list: 特徴量のリスト
        :rtype: ndarray
        :return: エンコードされた特徴量
        '''
        if not self._is_label_feature_list(feature_list):
            return self._standard_scaler.transform(np.array(feature_list, dtype=np.float32).reshape(-1, 1))

        return self._label_binarizer.transform(feature_list)

    def fit_transform(self, feature_list):
        '''
        :param [int or str] feature_list: 特徴量のリスト
        :rtype: ndarray
        :return: エンコードされた特徴量
        '''
        self.fit(feature_list)
        return self.transform(feature_list)

    def _is_label_feature_list(self, feature_list):
        if len(feature_list) == 0:
            return False
        if not isinstance(feature_list[0], str):
            return False
        return True
