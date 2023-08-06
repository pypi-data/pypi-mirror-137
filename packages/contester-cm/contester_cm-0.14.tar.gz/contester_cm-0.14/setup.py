import src
from setuptools import setup

with open('readme.md', 'r', encoding='utf-8') as file:
    readme = file.read()


setup(
    name='contester_cm',                                   # название пакета
    version=src.version,                                   # версия (указана в файле __init__.py пакета src)
    author='FullDungeon',
    author_email='ddd.dungeon@gmail.com',
    description='создание задач для Contester 2.4',        # краткое описание
    long_description=readme,                               # полное опсиание (файл readme.md)
    long_description_content_type='text/markdown',
    url='https://github.com/FullDungeon/python_pip',
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    # install_requires=['colorama'],
    packages=['src'],
    package_data={
        'src': [
            'static/checker.cpp',
            'static/info.ini',
            'static/statement.md',
            'static/tests/01',
            'static/tests/01.a',
        ]
    },
    entry_points={                                         # точка входа
        'console_scripts': [
            'contester-cm = src.cmd:run',
        ],
    },
)


