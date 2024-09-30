#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Converts the California Department of Transportation's Fuels  
#              Treatments dataset into the Task Force standardized schema.  
#              Dataset is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
from scripts._3a_CalTrans import CalTrans
from scripts.utils import init_gdb, check_schema_lock #, og_file_input

workspace, scratch_workspace = init_gdb()

# INPUTS
# will need to acquire updated versions and update file names
input_lines21 = os.path.join(workspace, "b_Originals", "VMP_Highway_Summary_2021")
input_lines22 = os.path.join(workspace, "b_Originals", "VMP_Highway_Summary_2022")
input_table21 = os.path.join(workspace, "VMP_Activities_Table_2021_Closeout_Date_Added")
input_table22 = os.path.join(workspace, "VMP_Activities_Table_2022_Closeout_Date_Added")

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20230711

# OUTPUTS
output_lines_enriched = os.path.join(workspace, "c_Enriched",f'CalTrans_act_ln_enriched_{date_id}') 

check_schema_lock(input_lines21)
check_schema_lock(input_lines22)
check_schema_lock(input_table21)
check_schema_lock(input_table22)
check_schema_lock(output_lines_enriched)


# In[2]:


CalTrans(input_lines21, input_lines22, input_table21, input_table22, output_lines_enriched)

