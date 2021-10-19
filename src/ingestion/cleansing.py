#pip install pandas
import regex as re
import pandas as pd
import numpy as np
import csv
import sys

    #def cleanse(str):
if __name__== "__main__":
    
    # Run the file by typing cleasning.py "filename.csv" inside the directory
    data= pd.read_csv(sys.argv[1])
    #Examine the shape of the data
    data.shape
    #Explore null cells
    data.isnull()
    #View total of null values by column
    data.isnull().sum()
    # Remove rows where all values are missing
    data.dropna(inplace = True, how='all')
    #Remove all null values
    data=data.dropna()

    # Store the dataframe as a new CSV
    # Give the location you would like to have the file saved.
    data.to_csv(r'C:\locationPath\Cleansed.csv',index=False)


class Cleansing:

    def __init__(self):
        pass

    # Given a filepath, cleanse the file
    def cleanse(self, source):
        pass
