# Setup Instructions

## Clone the repository into desired local location
In a Terminal window, run:
```
cd <desired/folder/location>
git clone https://github.com/kyle-woodward/mas-python.git
```

## Python setup
Here would like to test if the notebooks run fine selecting the original ArcGIS pro python interpreter
Otherwise, need to go thru steps we all have of installing Anaconda and copying the Pro python exe into Anaconda envs

## Running MAS Interagency Tracking System
### Update inputs
The processing workflow for each dataset requires various input (original) datasets. Ensure you have the most updated copy of each input dataset before running the notebooks, and that they are placed in the `a_Originals` feature dataset in your ESRI File Geodatabase.

Maybe have a [living document](https://docs.google.com/document/d/14RdlL0rXei1X8xqQeO2uxwIPmY1pKIlVm4L159goDak/edit) thats up to date on data sources and methods 

## Running the notebooks
From your favorite python IDE (suggested: VS Code or Jupyter Lab), open each notebook and run each cell in order.
The first cell sets up the required inputs and the new file paths to save the output datasets to. If you see this message in the cell's output:


##TODO Arcpy license levels, Packages required Pandas, ArcPy, os, datetime, time, shutil...