from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="PECF",
    version="1.0.25",
    author="Zedikon",
    author_email="mrzedikon@gmail.com",
    description="New easy and accessible configuration language",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Zedikon/PECF",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)