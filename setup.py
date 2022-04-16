import io
import os
import re

import setuptools


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "yolov5", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


setuptools.setup(
    name="yolov5",
    version=get_version(),
    author="Vincent Scharf",
    license="GPL",
    description="Packaged version of the Yolov5 object detector",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    install_requires=get_requirements(),
    extras_require={"tests": ["pytest"]},
    data_files=[('', ['requirements.txt'])],
    include_package_data=True,
    options={'bdist_wheel': {'python_tag': 'py36.py37.py38'}},
)
