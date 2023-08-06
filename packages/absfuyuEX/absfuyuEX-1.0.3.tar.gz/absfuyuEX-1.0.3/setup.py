"""
SETUP FILE
----------
"""

import setuptools
import os



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "src/absfuyuEX", "version.py")) as fp:
    exec(fp.read())


setuptools.setup(
    name="absfuyuEX",
    version=__version__,
    author="somewhatcold (AbsoluteWinter)",
    author_email="this.is.a.fake.mail@fakemail.absfuyu.com",
    description="A dlc for absfuyu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbsoluteWinter/absfuyu-extra",
    project_urls={
        "Bug Tracker": "https://github.com/AbsoluteWinter/absfuyu-extra/issues",
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
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=[
        "absfuyu",
        "numpy",# 1.22.1
        "pandas",# 1.4.0
        "matplotlib",# 3.5.1
        #"convertdate",# 2.4.0
        "LunarCalendar", # 0.0.9
    ],
    include_package_data=True,
    package_data={"": ["pkg_data/*"]},
)


# TO BUILD:
# python -m build
# python setup.py sdist bdist_wheel

# TO UPLOAD:
# twine upload dist/*