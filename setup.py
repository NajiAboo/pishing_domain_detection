from typing import List

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

from setuptools import setup,find_packages

__version__ = "0.0.0"

REPO_NAME = "PISHING_DOMAIN_DETECTION"
AUTHOR_USER_NAME = "NAJIABOO"
SRC_REPO = "pishingdomaindetection"
AUTHOR_EMAIL = "aboonaji@gmail.com"


HYPHEN_E_DOT = "-e ."


REQUIREMENT_FILE_NAME="requirements.txt"


def get_requirements_list() -> List[str]:
    """
    Description: This function is going to return list of requirement
    mention in requirements.txt file
    return This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Pishing domain detection",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    #package_dir={"": "src"},
    #packages=setuptools.find_packages(where="src")
    packages=find_packages(), 
    install_requires=get_requirements_list()
)
