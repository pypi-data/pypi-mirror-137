# How to use this Readme.
in VSCODE: press `ctrl shift v` to view this readme.
For users: simply install from Pypi. (see below)
For devs: read on.
the source folder contains all files to build the char package
inside the characterization_ams folder, all packages are found.
Refer to setuptools for more info on the build process.
https://setuptools.pypa.io/en/latest/userguide/quickstart.html

# For USERS
Simplest way is to install the wheel package from pypi.
`pip install characterization-ams`
Alternatively, the package can be built from source.

# For DEVELOPERS
Package dependencies should be defined in setup.cfg
### Step 0: update local repo
`git pull`

### Step 1: Create VENV (highly recommended) and install required packages for building package
On windows:

`python -m venv venv`

activate your venv:
-in vs code, press F1 - `python: select interpreter` - and select your venv
-otherwise, run:

`.\venv\Scripts\activate`

`pip install -r requirements.txt`


### Step 2: install package for editing and testing (recommended for local use)
`pip install --editable . `


### Step 3: test the package
if your venv is activated you can run:

`pytest` or `python -m pytest`

### Step 4: Commit changes
`git add`
`git commit`
`git push`

In case remote has diverged from local, please rebase.

### Step 5: release and TAG (ONLY WHEN STABLE)
commit your changes, create a tag and don't forget to push the tag.
`git tag 1.2.3`
`git push --tags`

### Step 6: Build for distribution:
`python -m build`

### Step 7: Upload to Pypi:
CLEAN the DIST folder, make sure only the latest stable packages are there.
`twine check dist/*`
`twine upload dist/*`

enter your pypi credentials. done.


## more info.

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

### optional:Using in jupyter notebooks with virtualenv:
when you installed the package in your global python this is not needed
`python -m venv venv (if not made already)`
`source venv/bin/activate`
`pip install jupyter notebook`
`ipython kernel install --user --name=venv`
`jupyter notebook`
Then, click kernel - change kernel -venv


### TBD
upload to pypi
