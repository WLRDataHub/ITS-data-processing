#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Converts the California Department of Environmental Quality's 
#              Prescribed Fire Information Reporting System (PFIRS) dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.               
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
from scripts._3a_PFIRS import PFIRS
from scripts.utils import init_gdb, check_schema_lock, og_file_input

workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# INPUTS
# NOTE: Update input dataset as necessary
# pfirs = og_file_input(prefix = 'PFIRS_', filetype = 'Point', gdb = os.path.join(workspace, "b_Originals"))
pfirs = "PFIRS_2018_2022"
input_fc = os.path.join(workspace, "b_Originals", pfirs)

# OUTPUTS
# timestamped outputs
output_enriched = os.path.join(workspace, "c_Enriched",f'PFIRS_enriched_{date_id}') 

# REFERENCE (must exist already)
# NOTE: Appended polygon dataset must already exist
treat = og_file_input(prefix = 'Treat_n_harvests_polygons_', filetype = 'Polygon', gdb = os.path.join(workspace, "d_Appended"))
treat_poly = os.path.join(workspace, "d_Appended", treat)

check_schema_lock(input_fc)
check_schema_lock(output_enriched)

# In[2]:


PFIRS(
    input_fc, 
    output_enriched, 
    treat_poly
    )
