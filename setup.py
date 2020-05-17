from setuptools import find_packages, setup

setup(
    name='links',
    version='1.0',
    author='SFill',
    python_requires='>=3.7',
    author_email='rootacces00@gmail.com',
    description='test app for funbox.ru',
    packages=find_packages(),
    install_requires=['flask', 'redis', 'marshmallow'],
    extras_require={'test': ['pytest']},
)
