import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phd_dataset_util",
    version="0.1.4",
    author="Thiago Nóbrega",
    author_email="thiagonobrega@gmail.com",
    description="A package that aims to execute the basic data processing from my phd experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiaonobrega/ml_ds_util",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)