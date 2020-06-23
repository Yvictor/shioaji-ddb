from setuptools import find_packages, setup

requirements = [
    "shioaji",
    "dolphindb",
    "redis",
    "msgpack",
    "pytest",
    "pytest-mock",
]

setup(
    name="sjddb",
    version="0.0.1",
    author="YVictor",
    author_email="yvictor3141@gmail.com",
    url="https://github.com/Yvictor/shioaji-ddb",
    description="Shioaji and dolphindb integration.",
    zip_safe=False,
    install_requires=requirements,
    packages=find_packages(exclude=["tests*", "notebooks*", "data*", "ddb*"]),
    platforms="any",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Cython",
        "Programming Language :: C++",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
