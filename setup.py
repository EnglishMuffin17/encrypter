from setuptools import setup, find_packages

read_README = open('README.txt', mode='r')
README = "".join(read_README.readlines())
read_README.close()

setup(
    name="KnitCryption",
    version="2.0.8",
    packages=find_packages(),
    scripts=[],
    install_requires=["docutils>=0.3"],
    package_data={
        "": [".txt"]
    },
    author="Keenan W. Wilkinson",
    author_email="keenanwilkinson@outlook.com",
    description="Encrytion package to assist in hiding data",
    long_description=README,
    license="GPL-3.0 license",
    url="https://github.com/WilkinsonK/KnitCryption"
)
