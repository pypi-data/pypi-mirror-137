import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="DCaptcha",
    version="0.0.4",
    description="Something lol",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="devAshton",
    author_email="cdnashtonn@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dcaptcha"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dcaptcha=dcaptcha.__main__:main",
        ]
    },
)