import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="area-and-volume-calculator",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Murtaza Chulawala",                     # Full name of the author
    author_email="eklodokro@gmail.com",
    description="Area and Volume Calculator",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    install_requires=[]                     # Install other dependencies if any
)