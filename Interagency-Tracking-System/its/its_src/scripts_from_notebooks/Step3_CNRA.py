#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Converts the California Department of Natural Resources' 
#              Fuels Treatments Tracker points, lines, and polygons datasets 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
from scripts.utils import init_gdb, check_schema_lock
from scripts._3a_CNRA_Points import CNRA_pts_Model
from scripts._3a_CNRA_Lines import CNRA_lns_Model
from scripts._3a_CNRA_Polygons import CNRA_poly_Model

workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace("-", "")  # like 20221216

# INPUTS
# will need to be acquired from CNRA
# change path to the most updated inputs
# cnra_gdb = os.path.join("..", "CNRA", "CNRA_TRMTTRACKER_20240117.gdb")
cnra_gdb = os.path.join("..", "CNRA", "CNRA_TRMTTRACKER_20230821.gdb")
input_pt_fc = os.path.join(cnra_gdb, "Treatment_Point")
input_ln_fc = os.path.join(cnra_gdb, "Treatment_Line")
input_poly_fc = os.path.join(cnra_gdb, "Treatment_Poly")
# Activity_Table = os.path.join(cnra_gdb, "Activities")
Activity_Table = os.path.join(cnra_gdb, "Activity_Table")
Project_Poly= os.path.join(cnra_gdb, "Project_Poly")
WFR_TF_Template = os.path.join(workspace, "a_Reference", "WFR_TF_Template")

# OUTPUTS
# mpt (multipoint) | use if needed
# output_mpt_enriched = os.path.join(workspace, "c_Enriched", f"CNRA_enriched_mpt_{date_id}")
output_pt_enriched = os.path.join(workspace, "c_Enriched", f"CNRA_enriched_pt_{date_id}")
output_ln_enriched = os.path.join(workspace, "c_Enriched", f"CNRA_enriched_ln_{date_id}")
output_poly_enriched = os.path.join(workspace, "c_Enriched", f"CNRA_enriched_poly_{date_id}")

check_schema_lock(input_pt_fc)
check_schema_lock(input_ln_fc)
check_schema_lock(input_poly_fc)
check_schema_lock(Activity_Table)
check_schema_lock(Project_Poly)
# check_schema_lock(output_mpt_enriched)
check_schema_lock(output_pt_enriched)
check_schema_lock(output_ln_enriched)
check_schema_lock(output_poly_enriched)

# In[2]:


CNRA_poly_Model(
    input_poly_fc, 
    Activity_Table, 
    Project_Poly, 
    WFR_TF_Template, 
    output_poly_enriched
    )

# In[3]:


CNRA_lns_Model(
    input_ln_fc, 
    Activity_Table, 
    Project_Poly, 
    WFR_TF_Template, 
    output_ln_enriched
    )

# In[4]:


CNRA_pts_Model(
    input_pt_fc, 
    Activity_Table, 
    Project_Poly, 
    WFR_TF_Template, 
    output_pt_enriched
    )
# multi_pt_to_pt = arcpy.management.FeatureToPoint(output_mpt_enriched, output_pt_enriched, "INSIDE")
