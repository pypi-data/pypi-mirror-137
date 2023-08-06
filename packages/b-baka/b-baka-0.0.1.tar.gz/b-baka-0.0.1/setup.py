import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="b-baka",
    version="0.0.1",
    description="A simple and lightweight web framework for begginers.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arnavthedumbass/b-baka",
    author="arnavthedumbass",
    author_email="snowneotv@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=[],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "baka=Baka.__main__:do_GET"
        ]
    },
)