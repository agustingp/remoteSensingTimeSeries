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
        self._class_of_interest = "mylabel"
        self._statistics_xml = self._images_directory + "\\instats.xml"
        self._sample_strategy = "all"
        self._outrates_file = self._images_directory + "\\outrates.csv"
        self._sqlite_samples = self._images_directory + "\\all.sqlite"
        self._sqlite_output = self._images_directory + "\\samples_values.sqlite"
        self._csv_converted = self._images_directory + "\\santa_ana_subclass.csv"
        self._csv_output = self._images_directory + "\\output.csv"

    def sortImage(self, image):     
        file_name = image.split("\\",3)[3]
        print('filename: ')
        print(file_name)
        date = file_name.split("_", 9)
        print('date: ')
        print(date)
        print(datetime.strptime(date[3], '%Y%m%d'))
        return datetime.strptime(date[3], '%Y%m%d') 
    
    def getFileBand(self, file): 
        if (re.search("LE07",file) and re.search("sr_band4",file) and (not re.search(".xml",file))) :
            return "NIR"
        if (re.search("LC08",file) and re.search("sr_band5",file) and (not re.search(".xml",file))) :
            return "NIR"
        if (re.search("LE07",file) and re.search("sr_band3",file) and (not re.search(".xml",file))) :
            return "R"
        if (re.search("LC08",file) and re.search("sr_band4",file) and (not re.search(".xml",file))) :
            return "R"
        if (re.search("LE07",file) and re.search("sr_band2",file) and (not re.search(".xml",file))) :
            return "G"
        if (re.search("LC08",file) and re.search("sr_band3",file) and (not re.search(".xml",file))) :
            return "G"
        if (re.search("sr_ndvi",file) and (not re.search(".xml",file))) :
            return "NDVI"
        if (re.search("sr_evi",file) and (not re.search(".xml",file))) :
            return "EVI"

   
    def run(self):
        filtered_images = []
        for root, dirs, files in os.walk(self._images_directory):
            for file in files:
                if (re.search("LE07",file) and re.search("sr_band4",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)
                if (re.search("LC08",file) and re.search("sr_band5",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)
                if (re.search("LE07",file) and re.search("sr_band3",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)
                if (re.search("LC08",file) and re.search("sr_band4",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)
                if (re.search("LE07",file) and re.search("sr_band2",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)
                if (re.search("LC08",file) and re.search("sr_band3",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file) 
                if (re.search("sr_ndvi",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)
                if (re.search("sr_evi",file) and (not re.search(".xml",file))) :
                    filtered_images.append(root +'\\'+ file)

        
        
        # Sort the list in ascending order of dates  
        filtered_images.sort(key = self.sortImage)

        band_date_dict= collections.OrderedDict()

        #we create a dictionary where every date has a list [{"reference": "band_X", "band": "NIR" }]

        for idx, imageFile in enumerate(filtered_images):
            date = datetime.strptime(imageFile.split("\\",3)[3].split("_", 9)[3], '%Y%m%d')
            if (date in band_date_dict.keys()): # there is already a value in the bucket   [band_0, band_N]               
                #band_date_dict['band_'+str(idx)] = date
                band_date_dict[date] = band_date_dict[date] + [{"reference": 'band_'+str(idx), "band": self.getFileBand(imageFile)}]
            else: 
                band_date_dict[date] = [{"reference": 'band_'+str(idx), "band": self.getFileBand(imageFile)}] # we initialize the bucket / list ==>  [band_0]


        print(band_date_dict)

        # 2 days range 
        dti = pd.date_range('2014-01-01', periods=183, freq='2D')

        df_dates = dti.to_frame(index=False)
        print(df_dates.iloc[:,0])

        dates = []
        datesx5=[]
        for date in df_dates.iloc[:,0]:
            dates.append(date)
            datesx5.append(date)
            datesx5.append(date)
            datesx5.append(date)
            """
            datesx5.append(date)
            datesx5.append(date)
            """
        print(dates)

        for date in dates:
            print(date)

        print(band_date_dict.keys())
        print(len(band_date_dict.keys()))

        writer=csv.writer(open(self._csv_output,'wb'), dialect='excel', encoding='utf-8')
        writer.writerow(['class1', 'subclass1', 'label', 'multiuse', 'originfid','my_label'] + datesx5)
       
        for idx, row in df_converted.iterrows():
            row_info = []
            row_info.append(row['class1'])
            row_info.append(row['subclass1'])
            row_info.append(row['label'])
            row_info.append(row['multiuse'])
            row_info.append(row['originfid'])
            row_info.append(row['my_label'])
            
            for date in dates:
                date_plus_one_day = date + timedelta(days=1) 
                bag = []
                if (date in band_date_dict.keys()): # if the date matches exactly the range date
                    for band in band_date_dict[date]:
                        bag.append(band)
                
                if(date_plus_one_day in band_date_dict.keys()): # check following day
                     for band in band_date_dict[date_plus_one_day]:
                        bag.append(band)

                bag_filtered = list(filter(lambda x: row[x['reference']] != -9999 and row[x['reference']] != 20000, bag))
                nirBands=[]
                gBands=[]
                rBands=[]
                ndviBands=[]
                eviBands=[]
                for band in bag_filtered:
                    if(band['band']=="NIR"):
                        nirBands.append(row[band['reference']])
                    if(band['band']=="G"):
                        gBands.append(row[band['reference']])
                    if(band['band']=="R"):
                        rBands.append(row[band['reference']])
                    """
                    if(band['band']=="NDVI"):
                        ndviBands.append(row[band['reference']])
                    if(band['band']=="EVI"):
                        eviBands.append(row[band['reference']])       
                    """

                if (len(nirBands)== 0):
                    nirBands.append('N/A')
                row_info.append(nirBands[0])  
                if (len(gBands)== 0):
                    gBands.append('N/A')
                row_info.append(gBands[0])  
                if (len(rBands)== 0):
                    rBands.append('N/A')
                row_info.append(rBands[0]) 
                
                """
                if (len(ndviBands)== 0):
                    ndviBands.append('N/A')
                row_info.append(ndviBands[0])  
                if (len(eviBands)== 0):
                    eviBands.append('N/A')
                row_info.append(eviBands[0])                 
                """
            writer.writerow(row_info)


if __name__ == "__main__":   
    pipeline = pipeline()
    pipeline.run()