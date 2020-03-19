import setuptools

NAME = "revolut_to_homebank"

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setuptools.setup(
    name=NAME,
    version="0.0.1",
    author="Maciej Pawlikowski",
    author_email="bystrzak14@gmail.com",
    description="Script converting Revolut statements to Homebank CSV format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bystrzak/revolut_to_homebank.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    scripts=['bin/rev2hb'],
)
