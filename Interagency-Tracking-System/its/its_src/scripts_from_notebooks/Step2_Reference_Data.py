"""
# Description: Pulls and formats reference data needed for enrichments
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from scripts._2_veg_types import veg
from scripts._2_ownership import ownership
from scripts._2_WUI import wui
from scripts.utils import init_gdb

workspace, scratch_workspace = init_gdb()


California = "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Census_States/FeatureServer/0"
California2 = os.path.join(workspace, "a_Reference", "California")
if not arcpy.Exists(California2):
    California3 = arcpy.Select_analysis(California, California2, "STATE_ABBR = 'CA'")

Counties = "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Census_Counties/FeatureServer/0"
Counties2 = os.path.join(workspace, "a_Reference", "Counties")
if not arcpy.Exists(Counties2):
    Counties3 = arcpy.Select_analysis(Counties, Counties2, "STATE_ABBR = 'CA'")

veg()


# Download Forest_own1.tif from https://www.fs.usda.gov/rds/archive/catalog/RDS-2020-0044
ownership()


wui()
