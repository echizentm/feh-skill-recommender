from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from .unit import NO_SKILL_LABEL
from .unit_list_encoder import UnitListEncoder


class Classifier:
    '''
    ユニットの各スキルタイプに対して適切なスキルが何かを識別するクラス
    '''
    __slots__ = [
       '_classifier', '_skill_condition',
       '_is_fitted', '_unit_list_encoder', '_label_encoder', '_label_decode_dict',
    ]

    def __init__(self, skill_condition, svm_c=None):
        '''
        :param SkillCondition skill_condition: スキル条件
        '''
        self._classifier = SVC(C=svm_c, gamma='scale') if svm_c else SVC(gamma='scale')
        self._skill_condition = skill_condition
        self._is_fitted = False
        self._unit_list_encoder = UnitListEncoder()
        self._label_encoder = LabelEncoder()
        self._label_decode_dict = {}

    def fit(self, unit_list, skill_type):
        '''
        :param [Unit] unit_list: Unit のリスト
        :param SkillType skill_type: 推定するスキルタイプ
        '''
        self._is_fitted = False

        X_train = self._unit_list_encoder.fit_transform(unit_list, ignore_skill_type=skill_type)
        y_train = self._label_encoder.fit_transform([getattr(unit, skill_type.value) for unit in unit_list])

        # sklearn の LabelEncoder.inverse_transform() を使うと謎の warn が出るので
        # とりあえずの処置で逆引き用の dict を作っています
        for unit, label in zip(unit_list, y_train):
            self._label_decode_dict[label] = getattr(unit, skill_type.value)

        train_index_list = [
            i for i, unit in enumerate(unit_list)
            if self._skill_condition.is_recommendable(skill_type, getattr(unit, skill_type.value))
        ]
        if len(train_index_list) > 0:
            self._classifier.fit(X_train[train_index_list], y_train[train_index_list])
            self._is_fitted = True

    def predict(self, unit_list, skill_type):
        '''
        :param [Unit] unit_list: Unit のリスト
        :param SkillType skill_type: 推定するスキルタイプ
        :rtype: [str]
        :return: 推定結果のリスト
        '''
        if not self._is_fitted:
            return [NO_SKILL_LABEL] * len(unit_list)

        X_test = self._unit_list_encoder.transform(unit_list, ignore_skill_type=skill_type)
        y_test = self._classifier.predict(X_test)
        return self._id_to_skill_name(unit_list, y_test, skill_type)

    def _id_to_skill_name(self, unit_list, y_test, skill_type):
        skill_name_list = []
        for unit, index in zip(unit_list, y_test):
            skill_name = self._label_decode_dict[index]
            if self._skill_condition.is_allowed_to_unit(unit, skill_type, skill_name):
                skill_name_list.append(skill_name)
            else:
                skill_name_list.append(getattr(unit, skill_type.value))
        return skill_name_list
