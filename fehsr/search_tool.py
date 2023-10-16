import glob
import os
import sys
import yaml
from argparse import ArgumentParser
from .unit import Unit, SkillType

MODEL_FILE_NAME = 'model.pickle'


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--data_dir', '-d', type=str, default='data/',
        help='検索を行うデータのあるディレクトリ',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='ユニット情報の詳細表示',
    )
    parser.add_argument(
        '--num', '-n', type=int,
        help='取得するユニット数',
    )
    parser.add_argument(
        '--key', '-k', type=str, choices=['hp', 'attack', 'speed', 'defence', 'resist'], default='hp',
        help='結果のソートに使うキー',
    )
    parser.add_argument(
        '--order', '-o', type=str, choices=['asc', 'desc'], default='desc',
        help='結果を昇順にするか降順にするか',
    )
    parser.add_argument(
        '--weapon_type', '-wt', type=str,
        help='武器タイプの検索条件',
    )
    parser.add_argument(
        '--movement_type', '-mt', type=str,
        help='移動タイプの検索条件',
    )
    parser.add_argument(
        '--weapon', '-we', type=str,
        help='武器スキルの検索条件',
    )
    parser.add_argument(
        '--assist', '-as', type=str,
        help='補助スキルの検索条件',
    )
    parser.add_argument(
        '--special', '-sp', type=str,
        help='奥義スキルの検索条件',
    )
    parser.add_argument(
        '--passive_a', '-a', type=str,
        help='Aスキルの検索条件',
    )
    parser.add_argument(
        '--passive_b', '-b', type=str,
        help='Bスキルの検索条件',
    )
    parser.add_argument(
        '--passive_c', '-c', type=str,
        help='Cスキルの検索条件',
    )
    parser.add_argument(
        '--passive_x', '-x', type=str,
        help='Xスキルの検索条件',
    )
    args = parser.parse_args()

    sys.stderr.write("loading data files.\n")
    unit_list = []
    for file_name in glob.glob(os.path.join(args.data_dir, 'unit', '*.yaml')):
        with open(file_name, 'r') as f:
            unit_dict_list = yaml.load(f)
            unit_list += [Unit(unit_dict) for unit_dict in unit_dict_list]
    sys.stderr.write("done.\n")

    sys.stderr.write("filtering units.\n")
    if args.weapon_type:
        unit_list = [unit for unit in unit_list if args.weapon_type in unit.weapon_type]
    if args.movement_type:
        unit_list = [unit for unit in unit_list if args.movement_type in unit.movement_type]
    if args.weapon:
        unit_list = [unit for unit in unit_list if args.weapon in unit.weapon]
    if args.assist:
        unit_list = [unit for unit in unit_list if args.assist in unit.assist]
    if args.special:
        unit_list = [unit for unit in unit_list if args.special in unit.special]
    if args.passive_a:
        unit_list = [unit for unit in unit_list if args.passive_a in unit.passive_a]
    if args.passive_b:
        unit_list = [unit for unit in unit_list if args.passive_b in unit.passive_b]
    if args.passive_c:
        unit_list = [unit for unit in unit_list if args.passive_c in unit.passive_c]
    if args.passive_x:
        unit_list = [unit for unit in unit_list if args.passive_x in unit.passive_x]
    sys.stderr.write("done.\n")

    sys.stderr.write("sorting units.\n")
    unit_list = sorted(
        unit_list,
        key=lambda x: getattr(x, args.key),
        reverse=(True if args.order == 'desc' else False),
    )
    if args.num:
        unit_list = unit_list[:args.num]
    sys.stderr.write("done.\n")

    for unit in unit_list:
        if args.verbose:
            print('name: {}'.format(unit.name))
            for skill_type in SkillType:
                current_value = getattr(unit, skill_type.value)
                print('{}: {}'.format(skill_type.value, current_value))
                print('total_parameter: {}'.format(unit.total_parameter))
                print('weighted_total_parameter: {}'.format(unit.weighted_total_parameter))
        else:
            elem_list = [unit.name]
            elem_list += list([str(getattr(unit, skill_type.value)) for skill_type in SkillType])
            elem_list += [str(unit.total_parameter), str(unit.weighted_total_parameter)]
            print(' / '.join(elem_list))


if __name__ == '__main__':
    main()
