"""
SETUP FILE
----------
"""

import setuptools


setuptools.setup(
    name="absfuyuEX",
    keywords="utilities",
    install_requires=[
        "absfuyu>=0.13.1",
        "numpy",# 1.22.1
        "pandas",# 1.4.0
        "matplotlib",# 3.5.1
        #"convertdate",# 2.4.0
        "LunarCalendar", # 0.0.9
        "click>=8", # 8.0.3
    ],
    package_data={"": ["pkg_data/*"]},
    entry_points={
        "console_scripts": [
            "lmao=absfuyuEX.cli:greet"
        ],
    },
)


# TO BUILD:
# python -m build
# python setup.py sdist bdist_wheel

# TO UPLOAD:
# twine upload dist/*