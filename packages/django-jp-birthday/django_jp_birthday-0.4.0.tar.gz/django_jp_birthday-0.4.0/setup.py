#!/usr/bin/env python

"""The setup script."""
from os import path
from jp_birthday import __version__
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


# with open("README.md") as readme_file:
# with open("README.rst", encoding='utf-8') as readme_file:
# with open("README.md", encoding='utf-8') as readme_file:
with open(path.join(here, "README.md")) as readme_file:
    readme = readme_file.read()

# with open("HISTORY.md") as history_file:
# with open("HISTORY.rst", encoding='utf-8') as history_file:
# with open("HISTORY.md", encoding='utf-8') as history_file:
with open(path.join(here, "HISTORY.md")) as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_txt:
    requirements = [
        r.replace("\n", "") for r in requirements_txt if ("#" not in r) and ("\n" != r)
    ]
    # print("requirements", requirements)

long_description = readme
long_description += "\n\n\n -------- \n\n\n"
long_description += history

test_requirements = []

setup(
    author="shimakaze-git",
    author_email="shimakaze.soft+github@googlemail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 5 - Production/Stable",
        # "Natural Language :: English",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
    ],
    description="Django model for Japanese birthday.",
    entry_points={
        "console_scripts": [
            # "django_jp_birthday=jp_birthday.cli:main",
            # "django_jp_birthday=django_jp_birthday.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    # long_description_content_type="text/x-rst",
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="django_jp_birthday django birthday era",
    name="django_jp_birthday",
    packages=find_packages(
        include=[
            "jp_birthday",
            # "django_jp_birthday",
            # "django_jp_birthday.*"
        ]
    ),
    # test_suite="tests",
    # tests_require=test_requirements,
    url="https://github.com/shimakaze-git/django-jp-birthday",
    version=__version__,
    zip_safe=False,
)
