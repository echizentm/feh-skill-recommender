import glob
import os
import re
import sys
import yaml
from argparse import ArgumentParser
from .recommender import Recommender
from .unit import Unit, SkillType, NO_SKILL_LABEL

MODEL_FILE_NAME = 'model.pickle'


def main():
    parser = ArgumentParser()
    parser.add_argument(
        'unit_name', type=str,
        help='推薦スキルを表示するユニット名',
    )
    parser.add_argument(
        '--data_dir', '-d', type=str, default='data/',
        help='学習を行うデータのあるディレクトリ',
    )
    parser.add_argument(
        '--train', '-t', action='store_true',
        help='再学習を行う場合は指定する',
    )
    parser.add_argument(
        '--svm_c', '-c', type=float, default=100.0,
        help='SVM のパラメータ C (詳しい人向け)',
    )
    args = parser.parse_args()

    sys.stderr.write("loading data files.\n")
    unit_list = []
    for file_name in glob.glob(os.path.join(args.data_dir, 'unit', '*.yaml')):
        with open(file_name, 'r') as f:
            unit_dict_list = yaml.load(f)
            unit_list += [Unit(unit_dict) for unit_dict in unit_dict_list]
    sys.stderr.write("done.\n")

    recommender = Recommender(args.data_dir, args.svm_c)
    if os.path.exists(MODEL_FILE_NAME) and not args.train:
        sys.stderr.write("loading model file.\n")
        recommender.load(MODEL_FILE_NAME)
        sys.stderr.write("done.\n")
    else:
        sys.stderr.write("training data.\n")
        recommender.fit(unit_list)
        accuracy = recommender.get_accuracy(unit_list)
        sys.stderr.write("accuracy: {}\n".format(accuracy))
        recommender.save(MODEL_FILE_NAME)
        sys.stderr.write("done.\n")

    # '名前1' で検索した時は '名前2' や '名前3' は取得せずに '名前' だけを取得する
    if re.fullmatch(r'.*[^1]1\Z', args.unit_name):
        name_pattern = re.compile(r'(男|女|紋章|蒼炎|暁|覚醒)?{}'.format(args.unit_name[:-1]))
    else:
        name_pattern = re.compile(r'(男|女|紋章|蒼炎|暁|覚醒)?{}[0-9]*'.format(args.unit_name))
    searched_unit_list = [
        unit for unit in unit_list if name_pattern.fullmatch(unit.name)
    ]
    searched_unit_list = sorted(searched_unit_list, key=lambda x: x.name)
    if len(searched_unit_list) == 0:
        print('unit not found.')
        return

    recommended_skill_dict = recommender.predict(searched_unit_list)
    for i, unit in enumerate(searched_unit_list):
        print('name: {}'.format(unit.name))
        for skill_type in SkillType:
            current_value = getattr(unit, skill_type.value)
            if skill_type in recommended_skill_dict and current_value == NO_SKILL_LABEL:
                print('{}: {} => {}'.format(skill_type.value, current_value, recommended_skill_dict[skill_type][i]))
            else:
                print('{}: {}'.format(skill_type.value, current_value))
        print('total_parameter: {}'.format(unit.total_parameter))
        print('weighted_total_parameter: {}'.format(unit.weighted_total_parameter))


if __name__ == '__main__':
    main()
