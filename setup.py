from setuptools import setup

desc = "A small, 1-d Roguelike, suitable for killing a few minutes"
homeurl = "https://github.com/eigenhombre/tunnerl"

setup(
    name="tunnerl",
    author="John Jacobsen",
    author_email="eigenhombre@gmail.com",
    packages=["tunnerl"],
    description=desc,
    long_description=(desc +
                      ".  See " + homeurl +
                      " for more information."),
    entry_points={
        'console_scripts': [
            'tunnerl = tunnerl.main:main',
        ],
    },
    url=homeurl,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["blessed==1.19.1"],
)
