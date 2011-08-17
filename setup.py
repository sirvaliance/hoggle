import sys
import glob
import os

from setuptools import setup, find_packages

package_data_list = list()

for root, dirs, files in os.walk('hoggle/project_templates'):

    dir_path = root
    dir_list = dir_path.split('/')
    del dir_list[0]
    dir_path = "/".join(dir_list)

    for f in files:
        package_data_list.append(os.path.join(dir_path, f))

package_data_list.append("app_templates/*.txt")

print package_data_list

setup(

    name = "hoggle",
    version = "0.1",
    packages = find_packages(),
    package_data = {
        "hoggle": package_data_list,
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
