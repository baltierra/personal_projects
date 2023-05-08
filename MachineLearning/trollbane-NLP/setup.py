import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="trollbane",
    install_requires=[
        'pandas>=1.4.2'
    ],
    version='0.1.1',
    author="Manuel Martinez",
    author_email="manmart@uchicago.edu",
    description='Python package for CAPP 30254 during Spring 2022',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manmartgarc/capp-30254-trollbane",
    packages=setuptools.find_packages(),
    python_requires='>=3.9')