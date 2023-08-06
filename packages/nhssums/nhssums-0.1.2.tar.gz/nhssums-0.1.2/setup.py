from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nhssums",
    version="0.1.2",
    author="Mark Sellors",
    author_email="python@5vcc.com",
    description="A small package to perform checksum validation on NHS numbers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sellorm/nhsnumber-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
