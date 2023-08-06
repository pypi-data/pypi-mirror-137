# FirstImpression Default Python Library
This library is used in Python for the scala enviroment.

## Upload to PyPi
To upload your changes to pypi follow the following steps:
* Save all your work
* Update the version number in the setup.py
* Run the following commands
```PowerShell
py -m pip install wheel
py -m pip install twine
```
* Make sure you go to the FirstImpression folder where setup.py is located
* Run the following commands
```PowerShell
py .\setup.py sdist bdist_wheel
py -m twine upload .\dist\*<YOUR_VERSION>*
```
* When running this command you need to fill in the username and password of the PyPi account. This can be found in LastPass

## Installing package
To install this package run
```PowerShell
py -m pip install firstimpression #Python3
python -m pip install firstimpression #Python2
```
