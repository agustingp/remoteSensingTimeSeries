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
        self._images_directory =  "D:/data/images"
        self._csv_input = self._images_directory + "\\output.csv"
        self._csv_output = self._images_directory + "\\output_interpolated.csv" 

   
    def run(self):
       
        #open the samples values
        df_converted = pd.read_csv(self._csv_input,header=0, index_col=None)  

        df_X = df_converted.iloc[:,6:] # 6  there are 6 columns before time series. Check temporal sampling, line 183
        df_interpolated = df_X.copy(deep=True)
        
        df_interpolated.iloc[:,0::3] =df_X.iloc[:,0::3].interpolate(method='linear', limit_direction='forward', axis=1) # interpolate NIR
        df_interpolated.iloc[:,1::3] =df_X.iloc[:,1::3].interpolate(method='linear', limit_direction='forward', axis=1) # interpolate G
        df_interpolated.iloc[:,2::3] =df_X.iloc[:,2::3].interpolate(method='linear', limit_direction='forward', axis=1) # interpolate R

        df_interpolated['label'] = df_converted['label']
        df_interpolated['class1'] = df_converted['class1']
        df_interpolated['subclass1'] = df_converted['subclass1']
        df_interpolated['multiuse'] = df_converted['multiuse']
        df_interpolated['originfid'] = df_converted['originfid']
        df_interpolated['my_label'] = df_converted['my_label']

        df_interpolated.to_csv(self._csv_output)


if __name__ == "__main__":   
    pipeline = pipeline()
    pipeline.run()