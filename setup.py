from setuptools import setup

setup(
    name="oned",
    packages=["oned"],
    entry_points={
        'console_scripts': [
            'oned = oned.main:main',
        ],
    },
    install_requires=["blessed==1.19.1"],
)
