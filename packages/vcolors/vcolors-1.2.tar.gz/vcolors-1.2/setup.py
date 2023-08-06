from setuptools import setup, find_packages

VERSION = '1.2'
DESCRIPTION = 'Your terminal colored and pretty printed'
LONG_DESCRIPTION = 'A package that allows you to print colored text to the terminal, extends Color_Console'

# Setting up
setup(
    name="vcolors",
    version=VERSION,
    author="Victor Valar",
    author_email="<victor@valar.codes>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['Color_Console==10.0'],
    keywords=['python','colored', 'Color_Console','print','terminal'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)