import sys

from setuptools import setup, find_packages

setup(

    name = "hoggle",
    version = "0.1",
    packages = find_packages(),
    package_data = {
        "hoggle": [
            "app_templates/*.txt",
        ]

    },

    # Metadata for PyPI
    description = "A static website generator from Markdown templates",
    url = "https://github.com/sirvaliance/hoggle",
    author = "Sir Valiance",
    author_email = "sir@sirvaliance.com",
    license = "BSDv3",

    entry_points = {
        'console_scripts': [
            "hoggle = hoggle.__main__:main",
        ]
    },
    install_requires = ['tornado', 'misaka'],
)
