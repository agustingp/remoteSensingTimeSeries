from datetime import datetime 
import os
import re
import subprocess
import otbApplication
 #import sqlite3


class pipeline(object):

    def __init__(self):
        self._images_directory = "D:/data/images"
        self._temporal_ordered_file = self._images_directory + '\ordered_images.txt'
        self._vrt_file = self._images_directory + "\\all.vrt"
        self._vector_classes = "D:/data/double_cropped_14SC.shp" 
        self._class_of_interest = "mylabel"
        self._sample_strategy = "all"  #[byclass|constant|percent|total|smallest|all]
        self._statistics_xml = self._images_directory + "\\instats.xml"
        self._outrates_file = self._images_directory + "\\outrates.csv"
        self._sqlite_samples = self._images_directory + "\\all.sqlite"
        self._sqlite_output = self._images_directory + "\\samples_values.sqlite"
        self._csv_converted = self._images_directory + "\\samples_values.csv"


    def printDates(self, dates):  
        for i in range(len(dates)):   
            print(dates[i])  

    def sortImage(self, image):     
        file_name = image.split("\\",3)[3]
        date = file_name.split("_", 9)
        return datetime.strptime(date[3], '%Y%m%d') 

   
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

        with open(self._temporal_ordered_file, 'w') as f:
            for image in filtered_images:
                f.write("%s\n" % image)
        
        subprocess.call(["gdalbuildvrt", "-resolution", 'highest', '-separate', '-input_file_list', self._temporal_ordered_file, self._vrt_file ])


        # PolygonClassStatistics
        

        app = otbApplication.Registry.CreateApplication("PolygonClassStatistics")

        app.SetParameterString("in", self._vrt_file)
        app.SetParameterString("vec", self._vector_classes)
        app.UpdateParameters()
        app.SetParameterString("field", self._class_of_interest)
        app.SetParameterString("out", self._statistics_xml)

        app.ExecuteAndWriteOutput()

        # SampleSelection

        app = otbApplication.Registry.CreateApplication("SampleSelection")

        app.SetParameterString("in", self._vrt_file)
        app.SetParameterString("vec", self._vector_classes)
        app.SetParameterString("instats", self._statistics_xml)
        app.UpdateParameters()
        app.SetParameterString("field", self._class_of_interest)
        app.SetParameterString("strategy", self._sample_strategy)
        app.SetParameterString("outrates", self._outrates_file)
        app.SetParameterString("out", self._sqlite_samples)

        app.ExecuteAndWriteOutput()

        # SampleExtraction

        app = otbApplication.Registry.CreateApplication("SampleExtraction")

        app.SetParameterString("in", self._vrt_file)
        app.SetParameterString("vec", self._sqlite_samples)

        app.UpdateParameters()
        app.SetParameterString("outfield", "prefix")
        app.SetParameterString("outfield.prefix.name", "band_")
        app.SetParameterString("field", self._class_of_interest)
        app.SetParameterString("out", self._sqlite_output)

        app.ExecuteAndWriteOutput()

if __name__ == "__main__":   
    pipeline = pipeline()
    pipeline.run()