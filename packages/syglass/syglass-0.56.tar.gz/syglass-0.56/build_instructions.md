## Building the Python Module
To build syGlass' Python module, you'll need to do the following from the repositories base directory `syGlass`:
- Make sure you have [Python3 64-bit](https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe)
- Run `generate.py`
- Run `setup.py`
- Build `libsyGlass` in the **Retail** configuration
- Run `buildPyglass.py`

## Building the Documentation
Note: you will need Sphinx installed. Run
```
pip install sphinx
```
To build the Sphinx documentation for the syGlass Python module, simply run the batch file in this directory with the argument `html`:
```
$ make.bat html
```
The documentation will be generated in `syGlass/pyglass/build`. Open the file `index.html` there to check out the results.

## Publishing Updates to PyPI
To publish an update, first adjust the version number in the script `setup.py` found in this directory. Then execute the following commands from this directory, changing the name of the `zip` file in the second command according to the new version number:
```
$ setup.py sdist
$ python -m twine upload dist/syglass-[version].tar.gz
```
You will need to have `twine` installed to do this. It can be installed via `pip`. You will also be prompted for PyPI credentials.

## Updating Documentation for the Web
To update the documents, clone or pull the latest version of the master branch of the istovisio.github.io repo.
Replace the existing files with the newly generated Sphinx html documentation, and commit/push.

## Installing the Python Module
To install, simply:
```
$ pip install syglass 
```
Upgrading an existing installation is similar:
```
$ pip install syglass --upgrade
```
Once that's done, you can `import syglass` from Python and use it accordingly.
