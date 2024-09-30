#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Consolidates all standardized and enriched datasets into a
#              point, line, and polygon feature class.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
import arcpy
from scripts._1_assign_domains import AssignDomains
from scripts.utils import init_gdb, og_file_input 
from scripts._4_metadata_append import pt_metadata, ln_metadata, poly_metadata

workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# Reference
WFR_TF_Template = os.path.join(workspace,'a_Reference','WFR_TF_Template')


# In[2]:


## POINTS
# INPUTS
nfpors_pt = og_file_input(prefix = 'nfpors_fuels_treatments_pts_enriched_', filetype = 'Point', gdb = os.path.join(workspace, 'c_Enriched'))
nfpors_fuels_treatments_pts_enriched = os.path.join(workspace,'c_Enriched', nfpors_pt)

pfirs_pt = og_file_input(prefix = 'PFIRS_enriched_', filetype = 'Point', gdb = os.path.join(workspace, 'c_Enriched'))
PFIRS_enriched = os.path.join(workspace,'c_Enriched', pfirs_pt)

cnra_pt = og_file_input(prefix = 'CNRA_enriched_pt_', filetype = 'Point', gdb = os.path.join(workspace, 'c_Enriched'))
CNRA_Enriched_pt = os.path.join(workspace,'c_Enriched',cnra_pt)

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
    
    points = arcpy.management.CreateFeatureclass(
        out_path=os.path.join(workspace,'d_Appended'), 
        out_name=f"Treat_n_harvests_points_{date_id}", 
        geometry_type="POINT", 
        template=[WFR_TF_Template], 
        spatial_reference=3310, #"NAD 1983 California (Teale) Albers (Meters)"), 
        )

    point_append = arcpy.management.Append(
        inputs=[nfpors_fuels_treatments_pts_enriched, 
                CNRA_Enriched_pt, 
                PFIRS_enriched
                ], 
        target=points, 
        schema_type="TEST", 
        field_mapping="", 
        )

    point_append_ad = AssignDomains(in_table=point_append)

    point_append_md = pt_metadata(point_append_ad)    


# In[11]:


##LINES
# Inputs
caltrans_ln = og_file_input(prefix = 'CalTrans_act_ln_enriched_', filetype = 'Line', gdb = os.path.join(workspace, 'c_Enriched'))
CalTrans_act_ln_enriched = os.path.join(workspace,'c_Enriched', caltrans_ln)

cnra_ln = og_file_input(prefix = 'CNRA_enriched_ln_', filetype = 'Line', gdb = os.path.join(workspace, 'c_Enriched'))
CNRA_Enriched_ln = os.path.join(workspace,'c_Enriched',cnra_ln)

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
    
    lines = arcpy.management.CreateFeatureclass(
        out_path=os.path.join(workspace,'d_Appended'), 
        out_name=f"Treat_n_harvests_lines_{date_id}", 
        geometry_type="POLYLINE", 
        template=[WFR_TF_Template], 
        spatial_reference=3310, #"NAD 1983 California (Teale) Albers (Meters)", 
    )

    lines_append = arcpy.management.Append(
        inputs=[CalTrans_act_ln_enriched, 
                CNRA_Enriched_ln
                ], 
        target=lines, 
        schema_type="TEST", 
        field_mapping="", 

        )

    lines_append_ad = AssignDomains(in_table=lines_append)

    lines_append_md = ln_metadata(lines_append_ad) 


# In[10]:


## POLYGON
# Inputs
blm_poly = og_file_input(prefix = 'BLM_enriched_', filetype = 'Polygon', gdb = os.path.join(workspace, 'c_Enriched'))
BLM_enriched = os.path.join(workspace,'c_Enriched',blm_poly)

cnra_poly = og_file_input(prefix = 'CNRA_enriched_poly_', filetype = 'Polygon', gdb = os.path.join(workspace, 'c_Enriched'))
CNRA_Enriched_poly = os.path.join(workspace,'c_Enriched',cnra_poly)

nfpors_poly = og_file_input(prefix = 'nfpors_fuels_treatments_polys_enriched_', filetype = 'Polygon', gdb = os.path.join(workspace, 'c_Enriched'))
nfpors_fuels_treatments_enriched = os.path.join(workspace,'c_Enriched', nfpors_poly)

nps_poly = og_file_input(prefix = 'nps_flat_fuels_enriched_', filetype = 'Polygon', gdb = os.path.join(workspace, 'c_Enriched'))
nps_flat_fuels_enriched = os.path.join(workspace,'c_Enriched',nps_poly)

usfs_poly = og_file_input(prefix = 'usfs_edw_facts_common_attributes_enriched_', filetype = 'Polygon', gdb = os.path.join(workspace, 'c_Enriched'))
usfs_edw_facts_common_attributes_enriched = os.path.join(workspace,'c_Enriched',usfs_poly)

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

    polygons = arcpy.management.CreateFeatureclass(
        out_path=os.path.join(workspace,'d_Appended'), 
        out_name=f"Treat_n_harvests_polygons_{date_id}", 
        geometry_type="POLYGON", 
        template=[WFR_TF_Template], 
        spatial_reference=3310, #"NAD 1983 California (Teale) Albers (Meters)", 
        )

    polygons_append = arcpy.management.Append(
        inputs=[
                nfpors_fuels_treatments_enriched, 
                usfs_edw_facts_common_attributes_enriched, 
                nps_flat_fuels_enriched, 
                CNRA_Enriched_poly, 
                BLM_enriched
                ], 
        target=polygons, 
        schema_type="TEST", 
        field_mapping="", 
        )

    polygons_append_ad = AssignDomains(in_table=polygons_append)

    polygons_append_md = poly_metadata(polygons_append_ad) 

