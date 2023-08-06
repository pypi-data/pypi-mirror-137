
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="scpQCA",
    version="0.0.1",
    author="Manqing FU",
    author_email="fumanqing@outlook.com",
    description="scpQCA package for python processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #  install_requires=[], # 比如["flask>=0.10"]
    #  url="https://www.baidu.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)