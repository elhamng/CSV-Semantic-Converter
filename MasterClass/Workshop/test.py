## from teminal use this command : python --version
## from terminal create the virtual environment using this command : python -m venv myenv
## from terminal activate the environment using the command on windows:  myenv\Scripts\activate
## from terminal activate the environment using the command on bash : source myenvb/Scripts/activate

## after activate the environment to check that use the command : which python
## it shows somethin like : /c/RDFMapping/Workshop/myenvb/Scripts/python

## from terminal check the version of pip (to manage python package): pip --version
## to install a library use : pip install pandas 
## use the requirements text file to have all necessary libraries and use the command : pip install -r requirements.txt
## to exit the program mode use : exit()
## to deactivate the environment use: deactivate




from platform import python_version
print("my python version is:")
print(python_version())





import pandas as pd
print("my pandas version is:")
print(pd.__version__)