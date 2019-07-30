# Time-series extraction from Satellite Imagery
## This code is supporting a paper submitted for publication at *HICSS*

> García Pereira, A., Ojo, A., Curry E., & Porwol L. **Enabling GeoAI model development for sustainable agricultural practices.** *Manuscript submitted for publication*

## Prerequisites
These scripts rely on Python 3.5.0, Orfeo Toolbox (https://www.orfeo-toolbox.org/CookBook/Installation.html) and GDAL 2.2.1, among other common libraries. 

## Satellite Imagery

These scripts are designed to work with Landsat Level-2 products (cross calibrated radiometrically and geometrically across instruments to allow for time series stacking of scenes across instruments: Landsat 8, Landsat 7, Landsat 4-5)

## Scripts 

The scripts are avialable in two versions:  
a) single_band: the sampling extraction is performed over a single band (e.g. NDVI) and the temporal sampling is done with the shape: 
> [date1.NDVI, date2.NDVI,....,dateN.NDVI]

b) multiple_bands: the sample extraction is performed over three bands: NIR, G, R. The temporal sampling is done with the shape:
> [date1.NIR, date1.G, date1.R, date2.NIR, date2.G, date2.R..., dateN.NIR, dateN.G, dateN.R]


## Inputs

*sampling_extraction.py & temporal_sampling.py*
**_images_directory** --> directory where the satellite imagery products are located
**_vector_classes** --> shapefile containing the labeled polygons
**_class_of_interest** --> polygons' class of interest to perform the sampling at the pixel level
**_sample_strategy** --> byclass|constant|percent|total|smallest|all check: https://www.orfeo-toolbox.org/CookBook/Applications/app_SampleSelection.html

*temporal_sampling.py*
**initial date** --> initial date for the sampling to start. e.g "2014-01-01" 
**periods** --> amount of temporal observations. Varies depending on the frequency and the desired time range. E.g. 183 periods for a one-year range using two days sampling (2D)
**frequency** --> e.g. "2D", "3D"


## Examples

Running the scripts

```console
foo@bar:~$ python sampling_extraction.py
```
```console
foo@bar:~$ python temporal_sampling.py
```
```console
foo@bar:~$ python interpolation.py
```

## Outputs

After executing the pipeline of scripts, the file "output_interpolated.csv" will contain, for each row, the time-series at the pixel level in the following shape:
> [date1.NIR, date1.G, date1.R, date2.NIR, date2.G, date2.R..., dateN.NIR, dateN.G, dateN.R, class1, subclass1, multiuse, originfid, my_label ]

Note that the columns "class1, subclass1, multiuse, originfid, my_label" are extracted from the shapefile cotaining the labeled polygons. 
















