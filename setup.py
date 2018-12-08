import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spesdebris",
    version="0.0.3",
    author="Benedek Solt Antók",
    author_email="abs@abs.ezw.me",
    description="Python-based desktop automation"
    "and cross-device communication suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ABS96/spesdebris",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
)
