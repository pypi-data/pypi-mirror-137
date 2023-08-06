"""
SETUP FILE
----------
"""

import setuptools
import os



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "src/absfuyu", "version.py")) as fp:
    exec(fp.read())


setuptools.setup(
    name="absfuyu",
    version=__version__,
    author="somewhatcold (AbsoluteWinter)",
    author_email="this.is.a.fake.mail@fakemail.absfuyu.com",
    description="A small collection of code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbsoluteWinter/absfuyu",
    project_urls={
        "Bug Tracker": "https://github.com/AbsoluteWinter/absfuyu/issues",
        "Documentation": "https://absolutewinter.github.io/absfuyu/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
    ],
    keywords="utilities",
    zip_safe=True, # if not working then zip_safe = False
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7, <4",
    #install_requires=["absfuyu"],
    include_package_data=True,
    package_data={"": ["dev/*.dat","pkg_data/*"]},
)