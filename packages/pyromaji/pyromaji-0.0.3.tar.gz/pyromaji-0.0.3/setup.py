from setuptools import find_packages, setup

setup(
    name='pyromaji',
    version='0.0.3',
    author='miidas',
    url='https://github.com/miidas/pyromaji',
    description='Romaji to Hiragana conversion library',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)