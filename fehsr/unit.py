from enum import Enum

NO_SKILL_LABEL = '----'


class SkillType(Enum):
    WEAPON_TYPE = 'weapon_type'
    MOVEMENT_TYPE = 'movement_type'
    HP = 'hp'
    ATTACK = 'attack'
    SPEED = 'speed'
    DEFENCE = 'defence'
    RESIST = 'resist'
    WEAPON = 'weapon'
    ASSIST = 'assist'
    SPECIAL = 'special'
    PASSIVE_A = 'passive_a'
    PASSIVE_B = 'passive_b'
    PASSIVE_C = 'passive_c'


# 推薦可能なスキルタイプ
RECOMMENDABLE_SKILL_TYPE_LIST = [
    SkillType.ASSIST, SkillType.SPECIAL,
    SkillType.PASSIVE_A, SkillType.PASSIVE_B, SkillType.PASSIVE_C,
]


class Unit:
    '''
    ユニットの情報を扱うクラス
    '''
    __slots__ = ['name'] + [t.value for t in SkillType]

    def __init__(self, status_dict):
        '''
        :param dict status_dict: ユニットのステータス

        status_dict は data/ 以下に置かれた yaml を読み込んだ dict
        '''
        self.name = status_dict['name']
        self.weapon_type = status_dict['weapon_type']
        self.movement_type = status_dict['movement_type']
        self.hp = status_dict['hp']
        self.attack = status_dict['attack']
        self.speed = status_dict['speed']
        self.defence = status_dict['defence']
        self.resist = status_dict['resist']
        self.weapon = NO_SKILL_LABEL
        self.assist = NO_SKILL_LABEL
        self.special = NO_SKILL_LABEL
        self.passive_a = NO_SKILL_LABEL
        self.passive_b = NO_SKILL_LABEL
        self.passive_c = NO_SKILL_LABEL

        if 'weapon' in status_dict:
            self.weapon = status_dict['weapon']
        if 'assist' in status_dict:
            self.assist = status_dict['assist']
        if 'special' in status_dict:
            self.special = status_dict['special']
        if 'passive_a' in status_dict:
            self.passive_a = status_dict['passive_a']
        if 'passive_b' in status_dict:
            self.passive_b = status_dict['passive_b']
        if 'passive_c' in status_dict:
            self.passive_c = status_dict['passive_c']
