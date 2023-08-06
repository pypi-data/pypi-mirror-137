from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='unifetch',
    version='0.1.4',
    description='Unifetch is a python script that will display the logo and motto of a UK university',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Luke Briggs',
    author_email='contact@lukebriggs.dev',
    url='https://github.com/LukeBriggsDev/unifetch',
    packages=find_packages(include=["unifetch", "unifetch.*"]),
    package_data={'unifetch': ['crests/*', "universities.json", "ASCII_generator/fonts/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],

    install_requires=[
        "numpy==1.22.1",
        "opencv-python==4.5.5.62",
        "Pillow==9.0.1",
    ]
)