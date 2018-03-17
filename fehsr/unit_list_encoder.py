import numpy as np
from .feature_encoder import FeatureEncoder
from .unit import SkillType


class UnitListEncoder:
    '''
    ユニットのリストを機械学習で扱える形式に変換するクラス
    '''
    __slots__ = ['_feature_encoder_dict']

    def __init__(self):
        self._feature_encoder_dict = {}
        for skill_type in SkillType:
            self._feature_encoder_dict[skill_type] = FeatureEncoder()

    def fit(self, unit_list):
        '''
        :param [Unit] unit_list: Unit のリスト
        '''
        for skill_type in SkillType:
            self._feature_encoder_dict[skill_type].fit(
                [getattr(unit, skill_type.value) for unit in unit_list]
            )

    def transform(self, unit_list, ignore_skill_type=None):
        '''
        :param [Unit] unit_list: Unit のリスト
        :param SkillType ignore_skill_type: 特徴ベクトルに含めないスキルタイプ
        :rtype: ndarray
        :return: Unit から抽出した特徴ベクトル
        '''
        feature_array = None
        for skill_type in SkillType:
            if ignore_skill_type and skill_type == ignore_skill_type:
                continue

            feature_array = self._concatenate_array(
                feature_array,
                self._feature_encoder_dict[skill_type].transform(
                    [getattr(unit, skill_type.value) for unit in unit_list]
                ),
            )
        return feature_array

    def fit_transform(self, unit_list, ignore_skill_type=None):
        '''
        :param [Unit] unit_list: Unit のリスト
        :param SkillType ignore_skill_type: 特徴ベクトルに含めないスキルタイプ
        :rtype: ndarray
        :return: Unit から抽出した特徴ベクトル
        '''
        self.fit(unit_list)
        return self.transform(unit_list, ignore_skill_type)

    def _concatenate_array(self, array1, array2):
        if array1 is None:
            return array2

        return np.concatenate((array1, array2), axis=1)
