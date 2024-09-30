#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description:  Outputs a Microsoft Excel sheet to be analyzed with a pivot table to 
#               produce a footprint acres report as well as a point featureclass.
#
#               "Footprint" is defined as treated acres within a treatment area 
#               irrespective of how many activities occurred within the treatment area.
#
#               This process uses a "Spaghetti and Meatballs" approach.  We first 
#               create the Spaghetti by using the "Feature to Polygon" tool.  
#               We use the "Identify" to attach ownership, vegetation, and region 
#               attributes to the Spaghetti. Then we create Meatballs using the 
#               "Feature to Points" tool.  Finally, we create the report with 
#               "Summarize Within" to find the Maximum Activity Quantity within a polygon.
#
# Known Issues: This tool under reports CalTrans footprints due to the way CalTrans 
#               reports treatment activities by road segment.
#
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""

import os
import datetime
import arcpy
from scripts.utils import init_gdb, check_schema_lock, delete_scratch_files, og_file_input

workspace, scratch_workspace = init_gdb()

arcpy.EnvManager(
    workspace=workspace,
    scratchWorkspace=scratch_workspace,
    outputCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),  # WKID 3310
    cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),  # WKID 3310
    extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'",
    preserveGlobalIds=True,
    qualifiedFieldNames=False,
    transferDomains=False,
    transferGDBAttributeProperties=False,
    overwriteOutput=True,
)

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace("-", "")  # like 20221216

# INPUTS
# change path to the most updated inputs
treat_poly = og_file_input(prefix="Treat_n_harvests_polygons_",filetype="Polygon",gdb=os.path.join(workspace, "d_Appended"),)
input_fc_poly = os.path.join(workspace, "d_Appended", treat_poly)
treat_pt = og_file_input(prefix="Treat_n_harvests_points_",filetype="Point",gdb=os.path.join(workspace, "d_Appended"),)
input_fc_pt = os.path.join(workspace, "d_Appended", treat_pt)
treat_ln = og_file_input(prefix="Treat_n_harvests_lines_",filetype="Line",gdb=os.path.join(workspace, "d_Appended"),)
input_fc_ln = os.path.join(workspace, "d_Appended", treat_ln)

WFR_TF_Template = os.path.join(workspace, "a_Reference", "WFR_TF_Template")
Reference_Data = os.path.join(workspace, "a_Reference", "Own_Veg_Region_WUI")

# Edit where clause for footprints report
Footprints_where_clause = "(Year = 2022)"  # And (Agency = 'Industrial Timber' or AGENCY = 'CALEPA' Or AGENCY = 'CALSTA' Or AGENCY = 'CNRA' Or AGENCY = 'DOD' Or AGENCY = 'DOI' Or AGENCY = 'USDA')"

# OUTPUTS
output_footprint = os.path.join(workspace, f"Footprint_Report_2022_{date_id}")
output_footprint_pts = os.path.join(workspace, "f_Report_Data", f"Footprint_pts_{date_id}")
output_excel_report = os.path.join("..", f"Draft_Footprints_Report_Counts_to_MAS_2022_{date_id}a.xlsx")

data = arcpy.GetParameterAsText(0)

check_schema_lock(input_fc_poly)
check_schema_lock(input_fc_ln)
check_schema_lock(input_fc_pt)
check_schema_lock(output_footprint)

# In[ ]:


# POINTS
# Create polygons from points based on Activity Acres

Updated_Input_Table = arcpy.management.AddField(
    in_table=input_fc_pt, 
    field_name="BufferMeters", 
    field_type="DOUBLE"
)

scratch_pt_1 = os.path.join(scratch_workspace, "Treat_n_harvests_points_CopyFeatures")

select_1 = arcpy.Select_analysis(
    in_features=Updated_Input_Table,
    out_feature_class=scratch_pt_1,
    where_clause="ACTIVITY_QUANTITY IS NOT NULL And ACTIVITY_UOM = 'AC'",
)

calc_buffer_1 = arcpy.management.CalculateField(
    Updated_Input_Table,
    "BufferMeters",
    "math.sqrt((!ACTIVITY_QUANTITY!*4046.86)/3.14159)",
    expression_type="PYTHON3",
)

scratch_pt_2 = os.path.join(
    scratch_workspace, "Treat_n_harvests_points_CopyFeatures_Yes"
)

select_2 = arcpy.Select_analysis(
    in_features=calc_buffer_1,
    out_feature_class=scratch_pt_2,
    where_clause="COUNTS_TO_MAS = 'YES' And BufferMeters IS NOT NULL",
)

scratch_pt_3 = os.path.join(scratch_workspace, "scratch_pt_3")

buffer_pts_1 = arcpy.analysis.PairwiseBuffer(
    in_features=select_2,
    out_feature_class=scratch_pt_3,
    buffer_distance_or_field="BufferMeters",
)

# In[3]:


# LINES
# Create polygons from lines based on Activity Acres

add_field_2 = arcpy.management.AddField(
    in_table=input_fc_ln, 
    field_name="BufferMeters", 
    field_type="DOUBLE"
)

scratch_ln_1 = os.path.join(scratch_workspace, "Treat_n_harvests_lns_CopyFeatures")

select_3 = arcpy.Select_analysis(
    in_features=add_field_2,
    out_feature_class=scratch_ln_1,
    where_clause="ACTIVITY_QUANTITY IS NOT NULL And ACTIVITY_UOM = 'AC'",
)

Treat_n_harvests_points_20221030_3_ = arcpy.management.CalculateField(
    in_table=select_3,
    field="BufferMeters",
    expression="(!ACTIVITY_QUANTITY!*4046.86)/!Shape_Length!/2",
    expression_type="PYTHON3",
)

scratch_ln_2 = os.path.join(scratch_workspace, "Treat_n_harvests_lns_CopyFeatures_Yes")

select_4 = arcpy.Select_analysis(
    in_features=add_field_2,
    out_feature_class=scratch_ln_2,
    where_clause="COUNTS_TO_MAS = 'YES'",
)

select_5 = arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=select_4,
    selection_type="NEW_SELECTION",
    where_clause="BufferMeters >= 200 And Source = 'CalTrans'",
    invert_where_clause="INVERT",
)

scratch_ln_3 = os.path.join(scratch_workspace, "Treat_n_harvests_lns_Buffer")
arcpy.analysis.PairwiseBuffer(
    in_features=select_5,
    out_feature_class=scratch_ln_3,
    buffer_distance_or_field="BufferMeters",
)  # line_end_type="FLAT")

# In[4]:


# POLYGON

select_6 = arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=input_fc_poly, 
    where_clause="COUNTS_TO_MAS = 'YES'"
)

select_7 = arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=select_6,
    selection_type="SUBSET_SELECTION",
    where_clause="TREATMENT_AREA < 100000",
)

scratch_poly_1 = os.path.join(scratch_workspace, "Treat_n_harvests_poly_CopyFeatures")

arcpy.management.CopyFeatures(
    in_features=select_7,
    out_feature_class=scratch_poly_1,
)

# In[5]:


# APPEND point buffers, line buffers, and polygons

Footprints_Append = arcpy.management.CreateFeatureclass(
    out_path=scratch_workspace, 
    out_name="Footprints_Append", 
    geometry_type="POLYGON", 
    template=WFR_TF_Template
    )

append_1 = arcpy.management.Append(
    inputs=[
        scratch_pt_3,
        scratch_ln_3,
        scratch_poly_1,
    ],
    target=Footprints_Append,
    schema_type="NO_TEST",
)


# In[6]:


# This Feature Class is used to create both the Spaghetti and the Meatballs

select_8 = os.path.join(scratch_workspace, "Footprints_Append_Where")

arcpy.analysis.Select(
    in_features=append_1,
    out_feature_class=select_8,
    where_clause=Footprints_where_clause,
)

# check results
result = arcpy.management.GetCount(select_8)
print("{} has {} records".format(select_8, result[0]))

# In[8]:


#
# Create Meatballs
#

Meatballs = os.path.join(workspace, "Meatballs")

arcpy.management.FeatureToPoint(
    in_features=select_8,
    out_feature_class=Meatballs,
    point_location="INSIDE",
)

arcpy.DefineProjection_management(
    Meatballs, arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)")
)


# In[ ]:


#
# Create the Spaghetti
#

Spaghetti = os.path.join(scratch_workspace, "Spaghetti")
arcpy.analysis.PairwiseDissolve(
    in_features=select_8,
    out_feature_class=Spaghetti,
    dissolve_field=["TRMTID_USER"],
)

Spaghetti_FeatureToPolygon = os.path.join(scratch_workspace, "Spaghetti_FeatureToPolygon")

arcpy.management.FeatureToPolygon(
    in_features=[Spaghetti], 
    out_feature_class=Spaghetti_FeatureToPolygon
)

# check results
result = arcpy.management.GetCount(Spaghetti_FeatureToPolygon)
print("{} has {} records".format(Spaghetti_FeatureToPolygon, result[0]))

Spaghetti_Delete_Fields = arcpy.management.DeleteField(
    in_table=Spaghetti_FeatureToPolygon,
    drop_field=["FID_Spaghetti_Dissolve", "TRMTID_USER"],
)

# In[11]:


# Add Sauce: Ownership, Vegetation, and Region attributes to the Spaghetti
Sauce = Reference_Data

Spaghetti_n_Sauce = os.path.join(workspace, "Spaghetti_n_Sauce")

arcpy.analysis.Identity(
    in_features=Spaghetti_Delete_Fields,
    identity_features=Sauce,
    out_feature_class=Spaghetti_n_Sauce,
    join_attributes="NO_FID",
)

arcpy.DefineProjection_management(
    Spaghetti_n_Sauce,
    arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),
)


# In[12]:


# Ensure the ownership for CalTrans projects are State

CalTrans_Projects = os.path.join(scratch_workspace, "CalTrans_Projects")

arcpy.analysis.Select(
    in_features=Footprints_Append,
    out_feature_class=CalTrans_Projects,
    where_clause="AGENCY = 'CALSTA'",
)

dissolve_1 = os.path.join(scratch_workspace, "CalTrans_Projects_Dissolve")

arcpy.analysis.PairwiseDissolve(
    in_features=CalTrans_Projects,
    out_feature_class=dissolve_1,
    dissolve_field=["AGENCY"],
)

# In[13]:


# Select CalTrans Projects to set Ownership to State
select_9 = arcpy.management.SelectLayerByLocation(
    in_layer=Spaghetti_n_Sauce,
    overlap_type="HAVE_THEIR_CENTER_IN",
    select_features=dissolve_1,
    search_distance=10,
    selection_type="NEW_SELECTION",
)

calc_field_1 = arcpy.management.CalculateField(
    in_table=select_9,
    field="PRIMARY_OWNERSHIP_GROUP",
    expression='"STATE"',
)

select_10 = arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=calc_field_1, 
    selection_type="CLEAR_SELECTION"
)

# In[14]:


add_field_3 = arcpy.management.AddField(
    in_table=select_10,
    field_name="FootprintAcres",
    field_type="DOUBLE",
    field_precision=8,
    field_scale=1,
)

calc_geom_1 = arcpy.management.CalculateGeometryAttributes(
    in_features=add_field_3,
    geometry_property=[["FootprintAcres", "AREA"]],
    area_unit="ACRES_US",
)

# In[ ]:


#
# Make Dinner
#

Dinner = os.path.join(scratch_workspace, "Dinner")

make_dinner = arcpy.SummarizeWithin_analysis(
    in_polygons=Spaghetti_n_Sauce,
    in_sum_features=Meatballs,
    out_feature_class=Dinner,
    keep_all_polygons="ONLY_INTERSECTING",
    sum_fields=[
        # ["ACTIVITY_QUANTITY", "Sum"],
        ["ACTIVITY_QUANTITY", "Mean"],
        # ["ACTIVITY_QUANTITY", "Min"],
        # ["ACTIVITY_QUANTITY", "Max"],
    ],
    shape_unit="ACRES",
)


# In[ ]:


select_11 = arcpy.analysis.Select(
    in_features=Dinner, 
    out_feature_class=output_footprint
)

arcpy.AssignDomainToField_management(
    select_11, "PRIMARY_OWNERSHIP_GROUP", "D_PR_OWN_GR"
)

arcpy.AssignDomainToField_management(
    in_table=select_11, 
    field_name="COUNTY", 
    domain_name="D_CNTY"
)

arcpy.AssignDomainToField_management(
    in_table=select_11, 
    field_name="BROAD_VEGETATION_TYPE", 
    domain_name="D_BVT"
)

arcpy.AssignDomainToField_management(
    in_table=select_11, 
    field_name="REGION", 
    domain_name="D_TASKFORCE"
)

# In[ ]:


# Process: Feature To Point (2) (Feature To Point) (management)
# Footprint_Report_2021_2022_pts = os.path.join(workspace, "f_Report_Data", output_footprint)
# if Footprint_Report_pts_20230720_lyrx and scratch_pt_3 and Value_3_:
to_pt_1 = arcpy.management.FeatureToPoint(
    in_features=select_11,
    out_feature_class=output_footprint_pts,
    point_location="INSIDE",
)

arcpy.AssignDomainToField_management(
    in_table=to_pt_1, 
    field_name="PRIMARY_OWNERSHIP_GROUP", 
    domain_name="D_PR_OWN_GR"
)
arcpy.AssignDomainToField_management(
    in_table=to_pt_1, 
    field_name="COUNTY", 
    domain_name="D_CNTY"
)
arcpy.AssignDomainToField_management(
    in_table=to_pt_1, 
    field_name="BROAD_VEGETATION_TYPE", 
    domain_name="D_BVT"
)
arcpy.AssignDomainToField_management(
    in_table=to_pt_1, 
    field_name="REGION", 
    domain_name="D_TASKFORCE"
)

arcpy.management.DeleteField(
    in_table=to_pt_1, 
    drop_field=["ORIG_FID"]
)

# In[ ]:


arcpy.conversion.TableToExcel(
    Input_Table=[select_11],
    Output_Excel_File=output_excel_report,
    Use_field_alias_as_column_header="ALIAS",
    Use_domain_and_subtype_description="DESCRIPTION",
)

# In[ ]:


delete_scratch_files(
    gdb=scratch_workspace, 
    delete_fc="yes", 
    delete_table="yes", 
    delete_ds="yes"
)
