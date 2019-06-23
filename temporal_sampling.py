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
        self._temporal_ordered_file = self._images_directory + '\ordered_images.txt'
        self._vrt_file = self._images_directory + "\\all.vrt"
        self._vector_classes = "D:/data/double_cropped_14SC.shp"
        self._class_of_interest = "class1"
        self._statistics_xml = self._images_directory + "\\instats.xml"
        self._sample_strategy = "all"
        self._outrates_file = self._images_directory + "\\outrates.csv"
        self._sqlite_samples = self._images_directory + "\\all.sqlite"
        self._sqlite_output = self._images_directory + "\\samples_values.sqlite"
        self._csv_converted = self._images_directory + "\\samples_values.csv"
        self._csv_output = self._images_directory + "\\output.csv"

    def sortImage(self, image):     
        file_name = image.split("\\",3)[3]
        print(file_name)
        date = file_name.split("_", 9)
        return datetime.strptime(date[3], '%Y%m%d') 

   
    def run(self):
        filtered_images = []
        for root, dirs, files in os.walk(self._images_directory):
            for file in files:
                if (re.search("sr_ndvi",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)        

        
        
        # Sort the list in ascending order of dates  
        filtered_images.sort(key = self.sortImage)

        band_date_dict= collections.OrderedDict()

        for idx, date in enumerate(filtered_images):
            date = datetime.strptime(date.split("\\",3)[3].split("_", 9)[3], '%Y%m%d')
            if (date in band_date_dict.keys()): # there is already a value in the bucket   [band_0, band_N]               
                band_date_dict[date] = band_date_dict[date] + ['band_'+str(idx)]
            else: 
                band_date_dict[date] = ['band_'+str(idx)] # we initialize the bucket / list ==>  [band_0]
        print(band_date_dict) 

        # 2 days range 
        dti = pd.date_range('2014-01-01', periods=183, freq='2D')
        df_dates = dti.to_frame(index=False)
        print(df_dates.iloc[:,0])

        dates = []
        for date in df_dates.iloc[:,0]:
            dates.append(date)
        print(dates)
       
        print(band_date_dict.keys())
        print(len(band_date_dict.keys()))

        writer=csv.writer(open(self._csv_output,'wb'), dialect='excel', encoding='utf-8')
        writer.writerow(['class1', 'subclass1', 'label'] + dates)
        
              
        for idx, row in df_converted.iterrows():
            row_info = []
            #add extra sample information
            row_info.append(row['class1'])
            row_info.append(row['subclass1'])
            row_info.append(row['label'])
            for date in dates:
                date_plus_one_day = date + timedelta(days=1) 
                bag = []
                if (date in band_date_dict.keys()): # if the date matches exactly the range date
                    for band in band_date_dict[date]:
                        bag.append(row[band])
                
                if(date_plus_one_day in band_date_dict.keys()):
                     for band in band_date_dict[date_plus_one_day]:
                        bag.append(row[band])

                bag_filtered = list(filter(lambda x: x != -9999, bag))
                if (len(bag_filtered)== 0):
                    bag_filtered.append('N/A')
                row_info.append(bag_filtered[0])        
            writer.writerow(row_info)


if __name__ == "__main__":   
    pipeline = pipeline()
    pipeline.run()