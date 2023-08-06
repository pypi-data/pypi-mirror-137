from setuptools import setup, find_packages


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open('requirements_dev.txt') as f:
    requirements = f.read().splitlines()

'''
- Increment the MAJOR version when you make 
incompatible API changes.
- Increment the MINOR version when you add 
functionality in a backwards-compatible manner.
- Increment the PATCH version when you make 
backwards-compatible bug fixes.

'''
setup(
    name="supplychainmodelhelper",
    version="0.2.5",
    author="Marcel Fuhrmann",
    author_email="dr.marcel.fuhrmann@gmail.com",
    description="A package to help with your supply chain model",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/DjMaFu/supplychainmodulator",
    packages=find_packages(),
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=6.2.2"],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)