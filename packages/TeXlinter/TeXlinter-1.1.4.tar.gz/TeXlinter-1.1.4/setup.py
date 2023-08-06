import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name='TeXlinter',
    version='1.1.4',    
    description='A small linter for LaTex',
    long_description=long_description,
    author='Marcus Björnbäck',
    author_email='smacke123b@gmail.com',
    license='BSD 2-clause',
    scripts=['TeXlinter.py', 'rules.JSON'],
    packages=setuptools.find_packages(),
    command_options={
      'nuitka': {
         # boolean option, e.g. if you cared for C commands
         '--show-scons': ("setup.py", True),
         # options without value, e.g. enforce using Clang
         '--clang': ("setup.py", None),
         # options with single values, e.g. enable a plugin of Nuitka
         '--enable-plugin': ("setup.py", 'anti-bloat'),
         # options with several values, e.g. avoiding including modules
         '--nofollow-import-to' : ("setup.py"),
         '--include-data-file': ("rules.JSON"),
      }
    },
    classifiers=[
        'License :: OSI Approved :: BSD License',  
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
)
