"""
Setup script for pyXPhySpec
"""

import io
import os
from setuptools import setup

install_requires = [
    "pywin32",
]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.md")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="pyxphyspec",
    version="0.3",
    description="Python wrapper for XPhySpec",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Justin Zhou",
    author_email="juzhyo@gmail.com",
    url="https://github.com/juzhyo/pyXPHySpec/",
    install_requires=install_requires,
    license="GPLv2",
    keywords="xphyspec",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering",
    ],
)
