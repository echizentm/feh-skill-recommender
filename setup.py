from setuptools import setup, find_packages


with open('requirements.txt') as f:
    setup(
        name='feh-skill-recommender',
        version='0.1.0',
        description='FEH skill recommender tool',
        long_description='FEH skill recommender tool',
        author='echizen_tm',
        author_email='echizentm@gmail.com',
        install_requires=f.readlines(),
        url='https://github.com/echizentm/feh-skill-recommender',
        license='',
        packages=find_packages(),
        entry_points='''
            [console_scripts]
            feh-skill-recommender=fehsr.command_line_tool:main
        ''',
    )
