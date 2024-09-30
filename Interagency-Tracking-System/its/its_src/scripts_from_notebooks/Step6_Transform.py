#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description:  This script transforms the flat point, line, and polygon files
#               into the WRTF relational database. The relational database includes
#               a Project polygon that has a one-to-many relationship with the 
#               Treatment featureclasses (point, line, and polygon). The Treatments 
#               have a one-to-many relationship with the Activities table.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime

import os
from scripts._1_assign_domains import ProjectDomains, TreatmentDomains, ActivityDomains
from scripts._7a_transform_projects import TransformProjects
from scripts._7b_transform_treatments import TransformTreatments
from scripts._7c_transform_activities import TransformActivities
from scripts.utils import init_gdb, check_schema_lock, og_file_input

workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# Inputs
# finds the latest version by date (like 20240124 (YYYMMDD))
treat_poly = og_file_input(prefix = 'Treat_n_harvests_polygons_', filetype = 'Polygon', gdb = os.path.join(workspace, "d_Appended"))
Treat_n_harvests_polygons = os.path.join(workspace, 'd_Appended', treat_poly)
treat_pt = og_file_input(prefix = 'Treat_n_harvests_points_', filetype = 'Point', gdb = os.path.join(workspace, "d_Appended"))
Treat_n_harvests_points = os.path.join(workspace, 'd_Appended', treat_pt)
treat_ln = og_file_input(prefix = 'Treat_n_harvests_lines_', filetype = 'Line', gdb = os.path.join(workspace, "d_Appended"))
Treat_n_harvests_lines = os.path.join(workspace, 'd_Appended', treat_ln)

# Outputs
Project_Poly = os.path.join(workspace, 'e_Transformed', f'Project_poly_{date_id}')
Treatments_poly = os.path.join(workspace, 'e_Transformed', f'Treatment_poly_{date_id}')
Treatments_pts = os.path.join(workspace, 'e_Transformed', f'Treatments_pts_{date_id}')
Treatments_lns = os.path.join(workspace, 'e_Transformed', f'Treatments_lns_{date_id}')
Activities = os.path.join(workspace, f'Activity_Table_{date_id}')

check_schema_lock(Project_Poly)
check_schema_lock(Treatments_poly)
check_schema_lock(Treatments_pts)
check_schema_lock(Treatments_lns)
check_schema_lock(Activities)

# In[2]:


TransformProjects(
    In_Poly=Treat_n_harvests_polygons,
    In_Pts=Treat_n_harvests_points,
    In_Lns=Treat_n_harvests_lines,
    Out_Poly=Project_Poly,
)
ProjectDomains(in_table_p=Project_Poly)

# In[3]:


TransformTreatments(
    In_Poly=Treat_n_harvests_polygons,
    In_Pts=Treat_n_harvests_points,
    In_Lns=Treat_n_harvests_lines,
    Out_poly=Treatments_poly,
    Out_pts=Treatments_pts,
    Out_lns=Treatments_lns,
)
TreatmentDomains(in_table_t=Treatments_poly)
TreatmentDomains(in_table_t=Treatments_pts)
TreatmentDomains(in_table_t=Treatments_lns)

# In[2]:


TransformActivities(
    In_Poly=Treat_n_harvests_polygons,
    In_Pts=Treat_n_harvests_points,
    In_Lns=Treat_n_harvests_lines,
    Out_Table=Activities
)
ActivityDomains(in_table_a=Activities)

# 
