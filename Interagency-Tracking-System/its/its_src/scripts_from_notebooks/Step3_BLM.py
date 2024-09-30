#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Converts the U.S. Department of Interior, Bureau 
#              of Land Management's fuels treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.             
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
import arcpy
from scripts.utils import init_gdb, check_schema_lock, og_file_input
from scripts._3a_BLM import Model_BLM

workspace, scratch_workspace = init_gdb()

from scripts._1_tables_to_domains import TablesToDomains
TablesToDomains(scratch_workspace)

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace("-", "")  # like 20221216

# INPUTS
# will need to be downloaded from here https://gis.blm.gov/caarcgis/rest/services/VegTreatments/BLM_CA_VTRT/FeatureServer/0

BLM_url = "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Census_States/FeatureServer"
input_fc = os.path.join(workspace, "b_Originals", "BLM_20240305")
# if arcpy.Exists(input_fc):
#    arcpy.management.Delete(input_fc)
if not arcpy.Exists(input_fc):
    # BLM_poly = arcpy.management.CopyFeatures(BLM_url, input_fc)
    BLM_poly = arcpy.management.CopyFeatures("Z:\\home\\arc\\tmp\\its\\BLM\\BLM_20240305.shp", input_fc)

# BLM_poly = og_file_input(prefix = 'BLM_', filetype = 'Polygon', gdb = os.path.join(workspace, "b_Originals"))
# input_fc = os.path.join(workspace,'b_Originals',BLM_poly)

California = os.path.join(workspace, "a_Reference", "California")

# OUTPUTS
output_enriched = os.path.join(workspace, "c_Enriched", f"BLM_enriched_{date_id}")

data = arcpy.GetParameterAsText(0)

# START and END YEARS
startyear = 2020
endyear = 2025

check_schema_lock(input_fc)
check_schema_lock(output_enriched)

# In[2]:


Model_BLM(
    output_enriched, 
    input_fc, 
    startyear, 
    endyear, 
    California
)

