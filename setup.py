from setuptools import find_packages, setup

setup(
    name='mpmrt',
    packages=find_packages(include=['mpmrt']),
    version='0.1.0',
    description='A python multiprocessing wrapper for ryu mrt export reader',
    author='Elias F. Fyksen',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)