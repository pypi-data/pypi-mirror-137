from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A numpy clone written in C and ported to Python using ctypes.'
LONG_DESCRIPTION = 'A numpy clone written in C and ported to Python using ctypes.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="zumpy",
    version=VERSION,
    author="Zach Weaver",
    author_email="zachlweaver00@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'zumpy', 'array', 'matrix'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)