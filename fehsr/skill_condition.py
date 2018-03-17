import os
import yaml
from .unit import NO_SKILL_LABEL, RECOMMENDABLE_SKILL_TYPE_LIST


class SkillCondition:
    '''
    スキルに関する条件を扱うクラス
    '''
    __slots__ = ['_skill_condition_dict']

    def __init__(self, data_dir='data/skill_condition'):
        '''
        :param str data_dir: スキルを習得できる条件の書かれた YANL があるディレクトリ
        '''
        self._skill_condition_dict = {}
        for skill_type in RECOMMENDABLE_SKILL_TYPE_LIST:
            with open(os.path.join(data_dir, '{}.yaml'.format(skill_type.value)), 'r') as f:
                self._skill_condition_dict[skill_type] = yaml.load(f)

    def is_recommendable(self, skill_type, skill_name):
        '''
        :param SkillType skill_type: スキルタイプ
        :param str skill_name: スキル名
        :rtype: bool
        :return: そのスキルが推薦可能かどうか
        '''
        if skill_name == NO_SKILL_LABEL:
            return False

        skill_condition_index = None
        try:
            skill_condition_index = self._get_skill_condition_index(
                self._skill_condition_dict[skill_type], skill_name,
            )
        except ValueError:
            return True

        # 特定のユニットにしか許されていないスキルは推薦しない
        skill_condition = self._skill_condition_dict[skill_type][skill_condition_index]
        if 'allow' in skill_condition and 'name_list' in skill_condition['allow']:
            return False
        return True

    def is_allowed_to_unit(self, unit, skill_type, skill_name):
        '''
        :param Unit unit: ユニット
        :param SkillType skill_type: スキルタイプ
        :param str skill_name: スキル名
        :rtype: bool
        :return: ユニットがそのスキルを習得できるかどうか
        '''
        if skill_name == NO_SKILL_LABEL:
            return False

        skill_condition_index = None
        try:
            skill_condition_index = self._get_skill_condition_index(
                self._skill_condition_dict[skill_type], skill_name,
            )
        except ValueError:
            return True

        skill_condition = self._skill_condition_dict[skill_type][skill_condition_index]
        for condition in ['weapon_type', 'movement_type']:
            list_name = '{}_list'.format(condition)
            if (
                'allow' in skill_condition and
                list_name in skill_condition['allow'] and
                getattr(unit, condition) not in skill_condition['allow'][list_name]
            ):
                return False
            if (
                'deny' in skill_condition and
                list_name in skill_condition['deny'] and
                getattr(unit, condition) in skill_condition['deny'][list_name]
            ):
                return False
        return True

    def _get_skill_condition_index(self, skill_condition_list, skill_name):
        return [i['name'] for i in skill_condition_list].index(skill_name)
