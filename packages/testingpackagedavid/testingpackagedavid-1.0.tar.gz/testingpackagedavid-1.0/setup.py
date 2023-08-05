from setuptools import setup, find_packages

setup(
    include_package_date=True,
    name='testingpackagedavid',
    version='1.0',
    author='David Graafland',
    author_email='david.graafland@gmail.com',
    packages=find_packages(),
    install_requires=['pandas'],
)