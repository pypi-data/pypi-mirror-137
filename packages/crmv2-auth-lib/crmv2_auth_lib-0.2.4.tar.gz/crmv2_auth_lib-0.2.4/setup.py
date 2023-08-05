from setuptools import find_packages, setup

setup(
    name='crmv2_auth_lib',
    packages=find_packages(include=['crmv2_auth_lib']),
    version='0.2.4',
    description='Auth Library CRMV2 Staging',
    author='mrizkyff',
    license='MIT',
    install_requires=[
        'pyjwt',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test'
)