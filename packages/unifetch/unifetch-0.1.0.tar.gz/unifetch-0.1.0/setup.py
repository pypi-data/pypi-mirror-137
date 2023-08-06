from setuptools import setup, find_packages
setup(
    name='unifetch',
    version='0.1.0',
    description='Unifetch is a python script that will display the logo and motto of a UK university',
    author='Luke Briggs',
    author_email='contact@lukebriggs.dev',
    url='https://github.com/LukeBriggsDev/unifetch',
    packages=find_packages(include=["unifetch", "unifetch.*"]),
    package_data={'unifetch': ['crests/*', "universities.json", "ASCII_generator/fonts/*"]},

    install_requires=[
        "numpy==1.22.1",
        "opencv-python==4.5.5.62",
        "Pillow==9.0.1",
    ]
)