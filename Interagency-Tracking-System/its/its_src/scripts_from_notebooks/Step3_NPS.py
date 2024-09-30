#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Converts the U.S. Department of Interior, National 
#              Park Service's fuels treatments dataset 
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
from scripts._3a_NPS import NPS

workspace, scratch_workspace = init_gdb()
arcpy.env.overwriteOutput = True

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# INPUTS
# NOTE: Update input as necessary
# nps_poly = og_file_input(prefix = 'nps_flat_fuels_', filetype = 'Polygon', gdb = os.path.join(workspace, "a_Originals"))
# input_fc = os.path.join(workspace,'b_Originals', nps_poly) # need to download this beforehand
# nps_flat_fuels_20021102 = os.path.join(original_gdb, 'a_Originals', 'nps_flat_fuels_20021102')

nps_api = 'https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/s_Completed_Perimeters_Past_5FY_View/FeatureServer/0'
nps_fs = arcpy.FeatureSet(nps_api)
input_fc = os.path.join(workspace,'b_Originals', f'nps_flat_fuels_{date_id}')
get_nps_pt = arcpy.CopyFeatures_management(nps_fs, input_fc)
print("NPS features copied from rest service")


# START and END YEARS
startyear = 2020
endyear = 2025

# OUTPUTS
output_enriched = os.path.join(workspace,'c_Enriched',f'nps_flat_fuels_enriched_{date_id}')

check_schema_lock(input_fc)
check_schema_lock(output_enriched)

# In[2]:


NPS(input_fc, startyear, endyear, output_enriched)
