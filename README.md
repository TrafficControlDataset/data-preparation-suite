# Data Parsing and Processing

This repository contains a CSV file and a Jupyter notebook for parsing and processing the data contained in the file.

## Data parsing

The python script, `dataParsingToCsv.py`, contains the data parsing from log-files to the final data set that is published via  https://doi.org/10.3929/ethz-b-000556642

This script can be utilized for any traffic signal controller events, where the protocol needs to be specified with the variables defined in the header of
the script. 

## Notebook

The Jupyter notebook, `data_usage.ipynb`, contains code for checking and processing the data from https://doi.org/10.3929/ethz-b-000556642. The notebook uses the `pandas` library to read the CSV file into a DataFrame, clean and preprocess the data, and perform some basic analysis.

The notebook is divided into the following sections:

1. **Data Loading**
2. **Data Cleaning and Preprocessing**
3. **Sample Feature computation**

## Getting Started

To run the Jupyter notebook, you'll need to have Python 3 and the following libraries installed:

- pandas
- numpy
- datetime
- matplotlib
- requests
- zipfile
- io
