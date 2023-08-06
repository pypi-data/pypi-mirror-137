from setuptools import setup, find_packages


setup(
    name='oilukla',
    version='0.1_a',
    license='GPL-3.0',
    author="ENEMINT",
    author_email='enem.sup@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/EnemLTD/oilukla2d',
    keywords='game-engine 2d pyqt5',
    install_requires=[
          "setuptools>=42",
          "wheel",
          "pygame",
          "keyboard"
      ],

)