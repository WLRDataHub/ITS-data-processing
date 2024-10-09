# Interagency Tracking System

https://wildfiretaskforce.org/treatment-dashboard/
The Wildfire & Landscape Resilience Interagency Tracking System (Interagency Tracking System) developed for the California Wildfire and Forest Resilience Task Force assembles data on wildfire and landscape resilience management activities from diverse federal, state, and other sources. Broadly, data are first standardized into the Task Force schema (v5.2 August 2023) (Appendix 1), then reference data are used to enrich the imported data with attributes for vegetation cover type, land ownership type, county, Task Force region, and whether the feature is located within the wildland-urban interface (WUI) from reference data. 
The datasets are incorporated as activity features (flat file). In the final step, the activities flat file is transformed to the Project, Treatment, Activity relational database format. The process was developed using ESRI ArcGIS Pro and converted to Python scripts for automation. Final products are available via Geodatabase Download, Web Map Service, and Dashboard. 
The Tracking System is designed to produce two primary reports: the Activities Report and the Footprint Report. The Activities Report is designed to report on the level of effort (in acres) for activities undertaken by the various reporting agencies. Activities can overlap, particularly between years. The Footprints Report removes overlaps from activities occurring on the same piece of land (e.g., thinning, then prescribed burning) during a specified time period. The Footprints Report is designed to report the acres of land (geographic area) affected by treatments. 



## Usage

Download the template geodatabase from https://gsal.sig-gis.com/portal/home/item.html?id=a09413b35e764131b8a07e717cb2b128
Several notebooks require the manual download of data.  Others download the data from api's.
The methods document can be downloaded from https://wildfiretaskforce.org/treatment-dashboard/
Edit your workspace geodatabase name in settings.yml

## Authors
SIG-GIS Original Team:
* Carl Rudeen (crudeen@sig-gis.com)
* Kayla Johnston (kjohnston@sig-gis.com)
* Kyle Woodward (kwoodward@sig-gis.com)

UCSD Modification Team:
* Johnny Lei (jil1119@ucsd.edu)
* Kai Lin (klin@ucsd.edu)
* Kate O'Laughlin (kbolaughlin@ucsd.edu)
