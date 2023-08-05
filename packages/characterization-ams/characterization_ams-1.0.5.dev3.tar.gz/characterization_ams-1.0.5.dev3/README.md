# How to use this package

## Organization
the source folder contains all files to build the char package
inside the characterization_ams folder, all packages are found.
Refer to setuptools for more info on the build process.
https://setuptools.pypa.io/en/latest/userguide/quickstart.html

## For USERS
simplest way is to install the wheel package from the dist folder.
`pip install dist\characterization_ams-1.0.0-py3-none-any.whl`


## For DEVELOPERS
Package dependencies should be defined in setup.cfg

### Create VENV (highly recommended) and install required packages for building package
#### On windows:
`python -m venv venv`

activate your venv:
-in vs code, press F1 - `python: select interpreter` - and select your venv
-otherwise, run:

`.\venv\Scripts\activate`

`pip install -r requirements.txt`


### install package for editing and testing (recommended for local use)
`pip install --editable . `


### Build for distribution:
`python3 -m build`

### Using in jupyter notebooks with virtualenv:
when you installed the package in your global python this is not needed
`python -m venv venv (if not made already)`
`source venv/bin/activate`
`pip install jupyter notebook`
`ipython kernel install --user --name=venv`
`jupyter notebook`
Then, click kernel - change kernel -venv

in the dist folder you will find a wheel file
you can install it with
`pip install *.whl`


### TEST
if your venv is activated you can run:

`pytest` 

or

 `python -m pytest`

### Versioning
Versioneer is used for versioning
TAG your version on the git branch, e.g.:

1.2.3
1.2.3.dev0
1.2.3.rc1

and a version name will be provided automatically in your package.

use it like this in your code:
```
import versioneer
version=versioneer.get_version()
```

### TBD
upload to pypi
