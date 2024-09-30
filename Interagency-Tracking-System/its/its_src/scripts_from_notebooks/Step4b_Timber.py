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
from scripts._3a_Timber import Timber
from scripts.utils import init_gdb, check_schema_lock#, og_file_input

workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20230821

# INPUTS
# NOTE: Update input dataset as necessary
#input_fc = os.path.join("..\..", "Timber Industry Acres 2022 for SIG 21Aug2023.xlsx")

# input_fc = os.path.join("\..", "Industry_nonspatial_2023_AlanFormattedForITS_20240904_USEME.xlsx")

# input_fc = r'Z:\home\arc\tmp\its\Industry_nonspatial_2023_AlanFormattedForITS_20240904_USEME.xlsx'
input_fc = r'Z:\home\arc\tmp\its\Timber_Industry_Acres_2021_for_UCSD_27Sep2024.xlsx'
# input_fc = r'Z:\home\arc\tmp\its\Timber_Industry_Acres_2022_for_UCSD_27Sep2024.xlsx'
# input_fc = r'Z:\home\arc\tmp\its\Timber_Industry_Acres_2023_for_UCSD_20Sep2024.xlsx'


# OUTPUTS
# timestamped outputs
output_enriched = os.path.join(workspace, "c_Enriched", f'Timber_Industry_2021_enriched_{date_id}') 
# output_enriched = os.path.join(workspace, "c_Enriched", f'Timber_Industry_2022_enriched_{date_id}') 
# output_enriched = os.path.join(workspace, "c_Enriched", f'Timber_Industry_2023_enriched_{date_id}') 


# check_schema_lock(input_fc)
check_schema_lock(output_enriched)


# In[2]:


Timber(
    input_fc, 
    output_enriched
    )

