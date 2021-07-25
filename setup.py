from setuptools import find_packages, setup
from genetic_algorithm import __version__

requirements = []
with open("requirements.txt", "r") as f:
    for line in f.readlines():
        line = line.replace("\n", "")
        requirements.append(line)

setup(
    name="Genetic Algorithm",
    version=__version__,
    packages=find_packages(),
    entry_points=dict(console_scripts=["ga-cli=cli:main"]),
    description="Genetic Algorithm",
    author="Rafael Silva Del Lama",
    author_email="rafaels.dellama@gmail.com",
    install_requires=requirements,
    tests_require=["pytest", "pytest-flake8", "pytest-cov"],
    include_package_data=True,
)
