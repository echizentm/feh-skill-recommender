import os
import pickle
from .unit import NO_SKILL_LABEL, RECOMMENDABLE_SKILL_TYPE_LIST
from .classifier import Classifier
from .skill_condition import SkillCondition


class Recommender:
    '''
    ユニットのリストに対して適切なスキルのリストを推薦するクラス
    '''
    __slots__ = ['_classifier_dict']

    def __init__(self, data_dir, svm_c=None):
        '''
        :param str data_dir: データの置かれたディレクトリ
        '''
        skill_condition = SkillCondition(os.path.join(data_dir, 'skill_condition'))
        self._classifier_dict = {}
        for skill_type in RECOMMENDABLE_SKILL_TYPE_LIST:
            self._classifier_dict[skill_type] = Classifier(skill_condition, svm_c)

    def fit(self, unit_list):
        '''
        :param [Unit] unit_list: Unit のリスト
        '''
        for skill_type in RECOMMENDABLE_SKILL_TYPE_LIST:
            self._classifier_dict[skill_type].fit(unit_list, skill_type)

    def predict(self, unit_list):
        '''
        :param [Unit] unit_list: Unit のリスト
        :rtype: {SkillType: [str]}
        :return: 推定結果の辞書
        '''
        result_dict = {}
        for skill_type in RECOMMENDABLE_SKILL_TYPE_LIST:
            result_dict[skill_type] = self._classifier_dict[skill_type].predict(unit_list, skill_type)
        return result_dict

    def get_accuracy(self, unit_list):
        '''
        :param [Unit] unit_list: Unit のリスト
        :rtype: {SkillType: str}
        :return: 推定正解率の辞書
        '''
        accuracy_dict = {}
        denominator_dict = {}
        prediction_dict = self.predict(unit_list)
        for skill_type, prediction_list in prediction_dict.items():
            accuracy_dict[skill_type] = 0
            denominator_dict[skill_type] = 0

            for unit, prediction in zip(unit_list, prediction_list):
                skill_type_value = getattr(unit, skill_type.value)
                if skill_type_value == NO_SKILL_LABEL:
                    continue

                denominator_dict[skill_type] += 1
                if skill_type_value == prediction:
                    accuracy_dict[skill_type] += 1

        return {k: '{} / {}'.format(v, denominator_dict[k]) for k, v in accuracy_dict.items()}

    def load(self, file_path):
        '''
        :param str file_path: モデルのパス
        '''
        with open(file_path, 'rb') as f:
            self._classifier_dict = pickle.load(f)

    def save(self, file_path):
        '''
        :param str file_path: モデルのパス
        '''
        with open(file_path, 'wb') as f:
            pickle.dump(self._classifier_dict, f)
