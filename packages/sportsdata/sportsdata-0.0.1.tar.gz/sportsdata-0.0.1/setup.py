from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sportsdata",
    version="0.0.1",
    author="David Orkin",
    author_email="david.orkin@fuzzybumblebee.org",
    description="APIs for gathering data from professional sport websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://opensource.fuzzybumblebee.org/sportsdata",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6"

)

