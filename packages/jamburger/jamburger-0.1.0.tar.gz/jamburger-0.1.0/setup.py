from setuptools import find_packages, setup
setup(
    name='jamburger',
    packages=find_packages(include=['jamburger']),
    version='0.1.0',
    description='My first Python library',
    author='Jam-Burger',
    license='MIT',
    install_requires=['pygame'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)