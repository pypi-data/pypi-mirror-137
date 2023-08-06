import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="hexdragon",
    version="0.0.7",
    description="Print a file as coloured hexadecimal to console",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/0xflotus/hexdragon",
    author="0xflotus",
    author_email="0xflotus+pypi@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["hexdragon"],
    include_package_data=True,
    install_requires=["argparse"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["hexdragon=hexdragon.__main__:main"]},
)
