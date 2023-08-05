import imp
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name='TeXlinter',
    version='1.1.0',    
    description='A small linter for LaTex',
    long_description=long_description,
    author='Marcus Björnbäck',
    author_email='smacke123b@gmail.com',
    license='BSD 2-clause',
    scripts=['TeXlinter', 'rules.JSON'],
    packages=setuptools.find_packages(),

    classifiers=[
        'License :: OSI Approved :: BSD License',  
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
)
