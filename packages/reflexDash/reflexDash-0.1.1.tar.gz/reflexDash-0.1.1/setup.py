import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
name="reflexDash",
version="0.1.1",
author="Dorian Drevon",
author_email="drevondorian@gmail.com",
description="source codes and configuration files to monitor small power data",
long_description=long_description,
long_description_content_type="text/markdown",
# url="https://github.com/pypa/sampleproject",
# project_urls={
#     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
# },
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
packages=['reflexDash'],
package_data={'': ['confFiles/*','confFiles/pictures/*']},
include_package_data=True,
install_requires=['dorianUtilsModulaire==4.0.10'],
python_requires=">=3.8"
)
