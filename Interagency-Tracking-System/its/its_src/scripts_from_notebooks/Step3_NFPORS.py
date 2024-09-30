#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description:  Converts the U.S. Department of Interior's National 
#               Fire Plan Operations and Reporting System (NFPORS) dataset 
#               into the Task Force standardized schema.  Dataset
#               is enriched with vegetation, ownership, county, WUI, 
#               Task Force Region, and year.
#               BLM and NPS current year treatments are inlcuded but past 
#               years treatments excluded and managed by seperate notebooks.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
import datetime
from scripts.utils import init_gdb, og_file_input
from scripts._3a_NFPORS import Model_NFPORS_poly, Model_NFPORS_point

workspace, scratch_workspace = init_gdb()
arcpy.env.overwriteOutput = True

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# INPUTS
# Will need to re-download NFPORS dataset each for each update from the below web service URL
# Check that NFPORS downloads correctly because the service is throttled to limit the number of downloadable features per call 
# https://usgs.nfpors.gov/arcgis/rest/services/nfpors_WM/MapServer/15

# BLM and NPS features are processed with a different notebook from their own feature services

# finds the latest version by date (like 20240124 (YYYMMDD))
# nfpors_poly = og_file_input(prefix = 'nfpors_fuels_treatments_', filetype = 'Polygon', gdb = os.path.join(workspace, "b_Originals"))
# input_original_polys = os.path.join(workspace,'b_Originals',nfpors_poly)
input_original_polys = os.path.join(workspace,'b_Originals','nfpors_fuels_treatments_20240306')
if not arcpy.Exists(input_original_polys):
    input_original_polys = arcpy.management.CopyFeatures("Z:\\home\\arc\\tmp\\its\\NFPORS\\fuel_treatment_polygons.shp", input_original_polys)


# Downloads and saves BIA and FWS current year project points to scratch gdb prior to being appended together in Model_NFPORS
query_CA = "statename='California'"

bia_api = 'https://usgs.nfpors.gov/arcgis/rest/services/nfpors_WM/MapServer/1'
bia_fs = arcpy.FeatureSet(bia_api, query_CA)
input_original_pts_BIA = os.path.join(workspace,'b_Originals', f'NFPORSCurrentFYTreatmentsBIA_{date_id}')
get_bia_pt = arcpy.CopyFeatures_management(bia_fs, input_original_pts_BIA)
print("BIA current year points copied from rest service")

fws_api = 'https://usgs.nfpors.gov/arcgis/rest/services/nfpors_WM/MapServer/5'
fws_fs = arcpy.FeatureSet(fws_api, query_CA)
input_original_pts_FWS = os.path.join(workspace,'b_Originals', f'NFPORSCurrentFYTreatmentsFWS_{date_id}')
get_fws_pt = arcpy.CopyFeatures_management(fws_fs, input_original_pts_FWS)
print("FWS current year points copied from rest service")

# OUTPUTS
output_pts_enriched = os.path.join(workspace, 'c_Enriched',f'nfpors_fuels_treatments_pts_enriched_{date_id}')
output_polys_enriched = os.path.join(workspace,'c_Enriched',f'nfpors_fuels_treatments_polys_enriched_{date_id}')

# In[3]:


Model_NFPORS_poly(
    input_original_polys,
    output_polys_enriched, 
    output_pts_enriched
)


# In[4]:


Model_NFPORS_point(
    input_original_pts_BIA, 
    input_original_pts_FWS, 
    output_pts_enriched
)
