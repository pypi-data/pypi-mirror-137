from setuptools import find_packages, setup

setup(
    name='al_codes',
    version='0.1',
    author='Carla Madureira',
    author_email='labs@empiricus.com.br, carla.madureira@empiricus.com.br',
    packages=find_packages(include=['al_codes']),
    description='Compilation of most used functions in al projects',
    setup_requires=['chalice==1.21.8', 'boto3==1.16.55', 'requests', 'dataclasses', 'requests'],
    url='https://www.empiricus.com.br',
    license="Apache License, Version 2.0"
)
