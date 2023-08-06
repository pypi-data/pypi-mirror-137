import pathlib

import setuptools

long_description = pathlib.Path("README.md").read_text()
required_packages = pathlib.Path("requirements.txt").read_text().splitlines()

setuptools.setup(
    name="znipy",
    version="0.1.0",
    author="zincwarecode",
    author_email="zincwarecode@gmail.com",
    description="Easy imports from Jupyter Notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zincware/ZnIPy",
    download_url="https://github.com/zincware/ZnIPy/archive/beta.tar.gz",
    keywords=["IPython", "Jupyter", "ZnTrack"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=required_packages,
)
