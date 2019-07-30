from datetime import datetime 
import os
import re
import subprocess
import otbApplication
import pandas as pd
import numpy as np
import unicodecsv as csv
import collections
from datetime import timedelta  
#import sqlite3


class pipeline(object):

    def __init__(self):
        self._images_directory = "D:/data/images"
        self._csv_input = self._images_directory + "\\output.csv"
        self._csv_output = self._images_directory + "\\output_interpolated.csv"   

   
    def run(self):
       
        #open the samples values
        df_converted = pd.read_csv(self._csv_input,header=0, index_col=None)
        df_interpolated = df_converted.iloc[:,3:184].interpolate(method='linear', limit_direction='forward', axis=1)
        #add extra sample information
        df_interpolated['label'] = df_converted['label']
        df_interpolated['class1'] = df_converted['class1']
        df_interpolated['subclass1'] = df_converted['subclass1']

        df_interpolated.to_csv(self._csv_output)

if __name__ == "__main__":   
    pipeline = pipeline()
    pipeline.run()