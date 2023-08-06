import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PPSAW",
    version = "0.0.1",
    author = "Joshua \"Phosphorescent\" Mankelow",
    description = "A Python PandaScore API Wrapper",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Phosphorescentt/PPSAW",
    project_urls = {
        "Bug Tracker": "https://github.com/Phosphorescentt/PPSAW/issues",
        },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        ],
    package_dir = {"": "src"}, 
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
)
