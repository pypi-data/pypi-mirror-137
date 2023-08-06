import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="teyxos.webhooks",
    version="1.0.0",
    description="A simple discord-webhook tool for python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Teyxos",
    author_email="teyxosesp@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["webhooks"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={},
)
