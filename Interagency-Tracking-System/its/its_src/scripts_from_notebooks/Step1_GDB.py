#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# WARNING: May overwrite your database and delete previous work
#
# Description:  Creates project database, feature datasets, and Task Force 
#               Template.  Adds domains to database
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
import time
from scripts.utils import init_gdb
from scripts._1_tables_to_domains import TablesToDomains
from scripts._1_add_fields import AddFields

workspace, scratch_workspace = init_gdb()

start = time.time()
print(f"Start Time {time.ctime()}")


# In[3]:



# Model Environment settings
with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace, 
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'", 
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        transferDomains=False, 
        transferGDBAttributeProperties=False, 
        overwriteOutput = True,
):

    ## Create Feature Datasets
    a_Reference = arcpy.management.CreateFeatureDataset(
        workspace, out_name="a_Reference"
    )

    b_Originals = arcpy.management.CreateFeatureDataset(
        workspace, out_name="b_Originals"
    )

    c_Enriched = arcpy.management.CreateFeatureDataset(
        workspace, out_name="c_Enriched"
    )

    d_Appended = arcpy.management.CreateFeatureDataset(
        workspace, out_name="d_Appended"
    )

    e_Transformed = arcpy.management.CreateFeatureDataset(
        workspace, out_name="e_Transformed"
    )

    f_Report_Data = arcpy.management.CreateFeatureDataset(
        workspace, out_name="f_Report_Data"
    )


# In[4]:


TablesToDomains(workspace)

# In[5]:


with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace, 
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'", 
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        transferDomains=False, 
        transferGDBAttributeProperties=False, 
        overwriteOutput = True,
):
    
    ## Create Template Feature Class
    Template_1 = os.path.join(workspace, "a_Reference")
    Template_2 = arcpy.CreateFeatureclass_management(
        out_path=Template_1, 
        out_name="WFR_TF_Template", 
        geometry_type="POLYGON", 
        out_alias="WFR TF Template"
    )

    AddFields(Template_2)

    end = time.time()
    print(f"Time Elapsed: {(end-start)/60} minutes")
