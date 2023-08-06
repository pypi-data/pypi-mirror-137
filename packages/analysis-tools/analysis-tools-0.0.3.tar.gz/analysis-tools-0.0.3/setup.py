import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="analysis-tools",
    version="0.0.3",
    author="Dongjin Yoon",
    author_email="djyoon0223@gmail.com",
    description="Analysis tools for machine learning projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djy-git/analysis-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
