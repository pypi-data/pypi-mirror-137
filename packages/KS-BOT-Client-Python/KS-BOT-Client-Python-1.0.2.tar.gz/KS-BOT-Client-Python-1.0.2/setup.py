import pathlib
from setuptools import *

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="KS-BOT-Client-Python",
    version="1.0.2",
    description="Python framework for interacting with KS-BOT, without any app",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KidsSMIT/KS-BOT-Client-Python",
    project_urls={
      "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    author="Kids SMIT",
    author_email="codingwithcn@gmail.com",
    license="MIT",
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = ["python-socketio[client]", "requests"],
    include_package_data = True,
    zip_safe = False,
)
