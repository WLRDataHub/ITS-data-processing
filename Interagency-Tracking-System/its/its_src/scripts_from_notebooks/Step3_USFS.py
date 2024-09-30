#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Converts the U.S. Forest Service EDW FACTS Common Attributes dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.            
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
from scripts._3a_USFS import Model_USFS
from scripts.utils import init_gdb, og_file_input, check_schema_lock

workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# INPUTS
# will need to be downloaded from here https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_ActivityFactsCommonAttributes_01/MapServer/0
# or the EDW Datasets page https://data.fs.usda.gov/geodata/edw/datasets.php?xmlKeyword=common+attributes

# get the most recent copy. Name should be "usfs_facts_edw_common_YYYMMDD"
usfws_recent = og_file_input(prefix = 'usfs_facts_edw_common_', filetype = 'Polygon', gdb = os.path.join(workspace, "b_Originals"))
# input_fc = os.path.join(workspace, 'b_Originals', usfs_recent)
input_fc = os.path.join(workspace,'b_Originals','usfs_facts_edw_common_test')

# OUTPUTS
output_enriched = os.path.join(workspace,'c_Enriched',f'usfs_edw_facts_common_attributes_enriched_{date_id}')

# START and END YEARS
startyear = 2020
endyear = 2025

check_schema_lock(input_fc)
check_schema_lock(output_enriched)

# In[2]:


Model_USFS(input_fc, startyear, endyear, output_enriched)
