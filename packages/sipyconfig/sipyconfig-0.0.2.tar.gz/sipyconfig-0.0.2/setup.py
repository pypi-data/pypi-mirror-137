"""
setup.py for python module
"""
import setuptools

with open("README.md", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sipyconfig",
    version="0.0.2",
    author="Teichi",
    author_email="tobias@teichmann.top",
    description="Python replacement for the functionality of SportIdent Config+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Teigi/sipyconfig",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 1 - Planning",
        "Operating System :: Unix",
        "Development Status :: 4 - Beta",
        "Typing :: Typed",
        "Topic :: Utilities"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["pyserial"]
)
