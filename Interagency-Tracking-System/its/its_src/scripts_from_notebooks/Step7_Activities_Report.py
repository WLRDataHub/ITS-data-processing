#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Description: Output a Microsoft Excel sheet to be analyzed with a pivot table to 
#              produce an activities report
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
import arcpy
from scripts._1_assign_domains import AssignDomains
from scripts.utils import init_gdb, delete_scratch_files, check_schema_lock, og_file_input

workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

arcpy.EnvManager(
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
        )

# START and END YEARS
startyear = 2021
endyear = 2022

report_clause=f"COUNTS_TO_MAS = 'YES' and Year <= {endyear} and Year >= {startyear}" # and ACTIVITY_CAT = 'BENEFICIAL_FIRE'"

# INPUTS
treat_poly = og_file_input(prefix = 'Treat_n_harvests_polygons_', filetype = 'Polygon', gdb = os.path.join(workspace, "d_Appended"))
input_fc_poly = os.path.join(workspace, 'd_Appended', treat_poly)
treat_pt = og_file_input(prefix = 'Treat_n_harvests_points_', filetype = 'Point', gdb = os.path.join(workspace, "d_Appended"))
input_fc_pt = os.path.join(workspace, 'd_Appended', treat_pt)
treat_ln = og_file_input(prefix = 'Treat_n_harvests_lines_', filetype = 'Line', gdb = os.path.join(workspace, "d_Appended"))
input_fc_ln = os.path.join(workspace, 'd_Appended', treat_pt)

WFR_TF_Template = os.path.join(workspace,'a_Reference','WFR_TF_Template')


# OUTPUTS
output_all_pts = os.path.join(workspace,'f_Report_Data',f'Activities_Report_{date_id}')
# Activities_Report_Table = os.path.join(workspace, f'Activities_Report_Table_{date_id}')
Output_Excel = fr"Draft Activities Report {date_id}a.xlsx"

data = arcpy.GetParameterAsText(0)

check_schema_lock(input_fc_pt)
check_schema_lock(input_fc_ln)
check_schema_lock(input_fc_poly)
check_schema_lock(output_all_pts)

# In[2]:


arcpy.env.overwriteOutput = True

Temp_Table_1 = os.path.join(scratch_workspace, "Temp_Table_1")
arcpy.conversion.ExportTable(
    in_table=input_fc_pt,
    out_table=Temp_Table_1,
    use_field_alias_as_name="NOT_USE_ALIAS",
    # where_clause=report_clause,
)

Temp_Table_2 = os.path.join(scratch_workspace, "Temp_Table_2")
arcpy.conversion.ExportTable(
    in_table=input_fc_ln,
    out_table=Temp_Table_2,
    use_field_alias_as_name="NOT_USE_ALIAS",
    where_clause=report_clause,
)

Temp_Table_3 = os.path.join(scratch_workspace, "Temp_Table_3")
arcpy.conversion.ExportTable(
    in_table=input_fc_poly,
    out_table=Temp_Table_3,
    use_field_alias_as_name="NOT_USE_ALIAS",
    where_clause=report_clause,
)

# In[3]:


Activities_Report_Table = arcpy.management.CreateTable(
    out_path=scratch_workspace,
    out_name=f"Activities_Report_Table_{date_id}",
    template=[WFR_TF_Template],
)

Appended = arcpy.management.Append(
    inputs=[Temp_Table_1, Temp_Table_2, Temp_Table_3],
    target=Activities_Report_Table,
    schema_type="NO_TEST",
    field_mapping="""PROJECTID_USER \"PROJECT ID USER\" true true false 50 Text 0 0,First,#,Temp_Table_1,PROJECTID_USER,0,50,Temp_Table_2,PROJECTID_USER,0,50,Temp_Table_3,PROJECTID_USER,0,50;
    AGENCY \"AGENCY_DEPARTMENT\" true true false 150 Text 0 0,First,#,Temp_Table_1,AGENCY,0,150,Temp_Table_2,AGENCY,0,150,Temp_Table_3,AGENCY,0,150;
    ORG_ADMIN_p \"ORG DATA STEWARD\" true true false 150 Text 0 0,First,#,Temp_Table_1,ORG_ADMIN_p,0,150,Temp_Table_2,ORG_ADMIN_p,0,150,Temp_Table_3,ORG_ADMIN_p,0,150;
    PROJECT_CONTACT \"PROJECT CONTACT\" true true false 100 Text 0 0,First,#,Temp_Table_1,PROJECT_CONTACT,0,100,Temp_Table_2,PROJECT_CONTACT,0,100,Temp_Table_3,PROJECT_CONTACT,0,100;
    PROJECT_EMAIL \"PROJECT EMAIL\" true true false 100 Text 0 0,First,#,Temp_Table_1,PROJECT_EMAIL,0,100,Temp_Table_2,PROJECT_EMAIL,0,100,Temp_Table_3,PROJECT_EMAIL,0,100;
    ADMINISTERING_ORG \"ADMINISTERING ORG\" true true false 150 Text 0 0,First,#,Temp_Table_1,ADMINISTERING_ORG,0,150,Temp_Table_2,ADMINISTERING_ORG,0,150,Temp_Table_3,ADMINISTERING_ORG,0,150;
    PROJECT_NAME \"PROJECT NAME\" true true false 150 Text 0 0,First,#,Temp_Table_1,PROJECT_NAME,0,150,Temp_Table_2,PROJECT_NAME,0,150,Temp_Table_3,PROJECT_NAME,0,150;
    PROJECT_STATUS \"PROJECT STATUS\" true true false 25 Text 0 0,First,#,Temp_Table_1,PROJECT_STATUS,0,25,Temp_Table_2,PROJECT_STATUS,0,25,Temp_Table_3,PROJECT_STATUS,0,25;
    PROJECT_START \"PROJECT START\" true true false 8 Date 0 0,First,#,Temp_Table_1,PROJECT_START,-1,-1,Temp_Table_2,PROJECT_START,-1,-1,Temp_Table_3,PROJECT_START,-1,-1;
    PROJECT_END \"PROJECT END\" true true false 8 Date 0 0,First,#,Temp_Table_1,PROJECT_END,-1,-1,Temp_Table_2,PROJECT_END,-1,-1,Temp_Table_3,PROJECT_END,-1,-1;
    PRIMARY_FUNDING_SOURCE \"PRIMARY_FUNDING_SOURCE\" true true false 130 Text 0 0,First,#,Temp_Table_1,PRIMARY_FUNDING_SOURCE,0,130,Temp_Table_2,PRIMARY_FUNDING_SOURCE,0,130,Temp_Table_3,PRIMARY_FUNDING_SOURCE,0,130;
    PRIMARY_FUNDING_ORG \"PRIMARY_FUNDING_ORG\" true true false 130 Text 0 0,First,#,Temp_Table_1,PRIMARY_FUNDING_ORG,0,130,Temp_Table_2,PRIMARY_FUNDING_ORG,0,130,Temp_Table_3,PRIMARY_FUNDING_ORG,0,130;
    IMPLEMENTING_ORG \"IMPLEMENTING_ORG\" true true false 150 Text 0 0,First,#,Temp_Table_1,IMPLEMENTING_ORG,0,150,Temp_Table_2,IMPLEMENTING_ORG,0,150,Temp_Table_3,IMPLEMENTING_ORG,0,150;
    LATITUDE \"LATITUDE CENTROID\" true true false 8 Double 0 0,First,#,Temp_Table_1,LATITUDE,-1,-1,Temp_Table_2,LATITUDE,-1,-1,Temp_Table_3,LATITUDE,-1,-1;
    LONGITUDE \"LONGITUDE CENTROID\" true true false 8 Double 0 0,First,#,Temp_Table_1,LONGITUDE,-1,-1,Temp_Table_2,LONGITUDE,-1,-1,Temp_Table_3,LONGITUDE,-1,-1;
    BatchID_p \"Batch ID\" true true false 40 Text 0 0,First,#,Temp_Table_1,BATCHID_p,0,40,Temp_Table_2,BATCHID_p,0,40,Temp_Table_3,BATCHID_p,0,40;
    Val_Status_p \"Validation Status\" true true false 15 Text 0 0,First,#,Temp_Table_1,VAL_STATUS_p,0,15,Temp_Table_2,VAL_STATUS_p,0,15,Temp_Table_3,VAL_STATUS_p,0,15;
    Val_Message_p \"Validation Message\" true true false 15 Text 0 0,First,#,Temp_Table_1,Val_Message_p,0,15,Temp_Table_2,Val_Message_p,0,15,Temp_Table_3,Val_Message_p,0,15;
    Val_RunDate_p \"Validation Run Date\" true true false 8 Date 0 0,First,#,Temp_Table_1,VAL_RUNDATE_p,-1,-1,Temp_Table_2,VAL_RUNDATE_p,-1,-1,Temp_Table_3,VAL_RUNDATE_p,-1,-1;
    Review_Status_p \"Review Status\" true true false 15 Text 0 0,First,#,Temp_Table_1,REVIEW_STATUS_p,0,15,Temp_Table_2,REVIEW_STATUS_p,0,15,Temp_Table_3,REVIEW_STATUS_p,0,15;
    Review_Message_p \"Review Message\" true true false 15 Text 0 0,First,#,Temp_Table_1,Review_Message_p,0,15,Temp_Table_2,Review_Message_p,0,15,Temp_Table_3,Review_Message_p,0,15;
    Review_RunDate_p \"Review Run Date\" true true false 8 Date 0 0,First,#,Temp_Table_1,REVIEW_RUNDATE_p,-1,-1,Temp_Table_2,REVIEW_RUNDATE_p,-1,-1,Temp_Table_3,REVIEW_RUNDATE_p,-1,-1;
    Dataload_Status_p \"Dataload Status\" true true false 15 Text 0 0,First,#,Temp_Table_1,DATALOAD_STATUS_p,0,15,Temp_Table_2,DATALOAD_STATUS_p,0,15,Temp_Table_3,DATALOAD_STATUS_p,0,15;
    Dataload_Msg_p \"Dataload Message\" true true false 15 Text 0 0,First,#,Temp_Table_1,DATALOAD_MSG_p,0,15,Temp_Table_2,DATALOAD_MSG_p,0,15,Temp_Table_3,DATALOAD_MSG_p,0,15;
    TRMTID_USER \"TREATMENT ID USER\" true true false 50 Text 0 0,First,#,Temp_Table_1,TRMTID_USER,0,50,Temp_Table_2,TRMTID_USER,0,50,Temp_Table_3,TRMTID_USER,0,50;
    PROJECTID \"PROJECTID\" true true false 50 Text 0 0,First,#,Temp_Table_1,PROJECTID,0,50,Temp_Table_2,PROJECTID,0,50,Temp_Table_3,PROJECTID,0,50;
    PROJECTNAME_ \"PROJECT NAME\" true true false 150 Text 0 0,First,#,Temp_Table_1,PROJECTNAME_,0,150,Temp_Table_2,PROJECTNAME_,0,150,Temp_Table_3,PROJECTNAME_,0,150;
    ORG_ADMIN_t \"ORG DATA STEWARD\" true true false 150 Text 0 0,First,#,Temp_Table_1,ORG_ADMIN_t,0,150,Temp_Table_2,ORG_ADMIN_t,0,150,Temp_Table_3,ORG_ADMIN_t,0,150;PRIMARY_OWNERSHIP_GROUP \"PRIMARY OWNERSHIP GROUP\" true true false 25 Text 0 0,First,#,Temp_Table_1,PRIMARY_OWNERSHIP_GROUP,0,25,Temp_Table_2,PRIMARY_OWNERSHIP_GROUP,0,25,Temp_Table_3,PRIMARY_OWNERSHIP_GROUP,0,25;
    PRIMARY_OBJECTIVE \"PRIMARY OBJECTIVE\" true true false 65 Text 0 0,First,#,Temp_Table_1,PRIMARY_OBJECTIVE,0,65,Temp_Table_2,PRIMARY_OBJECTIVE,0,65,Temp_Table_3,PRIMARY_OBJECTIVE,0,65;
    SECONDARY_OBJECTIVE \"SECONDARY OBJECTIVE\" true true false 65 Text 0 0,First,#,Temp_Table_1,SECONDARY_OBJECTIVE,0,65,Temp_Table_2,SECONDARY_OBJECTIVE,0,65,Temp_Table_3,SECONDARY_OBJECTIVE,0,65;
    TERTIARY_OBJECTIVE \"TERTIARY OBJECTIVE\" true true false 65 Text 0 0,First,#,Temp_Table_1,TERTIARY_OBJECTIVE,0,65,Temp_Table_2,TERTIARY_OBJECTIVE,0,65,Temp_Table_3,TERTIARY_OBJECTIVE,0,65;
    TREATMENT_STATUS \"TREATMENT STATUS\" true true false 25 Text 0 0,First,#,Temp_Table_1,TREATMENT_STATUS,0,25,Temp_Table_2,TREATMENT_STATUS,0,25,Temp_Table_3,TREATMENT_STATUS,0,25;
    COUNTY \"COUNTY\" true true false 35 Text 0 0,First,#,Temp_Table_1,COUNTY,0,35,Temp_Table_2,COUNTY,0,35,Temp_Table_3,COUNTY,0,35;IN_WUI \"IN WUI\" true true false 30 Text 0 0,First,#,Temp_Table_1,IN_WUI,0,30,Temp_Table_2,IN_WUI,0,30,Temp_Table_3,IN_WUI,0,30;REGION \"TASK FORCE REGION\" true true false 25 Text 0 0,First,#,Temp_Table_1,REGION,0,25,Temp_Table_2,REGION,0,25,Temp_Table_3,REGION,0,25;
    TREATMENT_AREA \"TREATMENT AREA (GIS ACRES)\" true true false 8 Double 0 0,First,#,Temp_Table_1,TREATMENT_AREA,-1,-1,Temp_Table_2,TREATMENT_AREA,-1,-1,Temp_Table_3,TREATMENT_AREA,-1,-1;
    TREATMENT_START \"TREATMENT START\" true true false 8 Date 0 0,First,#,Temp_Table_1,TREATMENT_START,-1,-1,Temp_Table_2,TREATMENT_START,-1,-1,Temp_Table_3,TREATMENT_START,-1,-1;
    TREATMENT_END \"TREATMENT END\" true true false 8 Date 0 0,First,#,Temp_Table_1,TREATMENT_END,-1,-1,Temp_Table_2,TREATMENT_END,-1,-1,Temp_Table_3,TREATMENT_END,-1,-1;
    RETREATMENT_DATE_EST \"RETREATMENT DATE ESTIMATE\" true true false 8 Date 0 0,First,#,Temp_Table_1,RETREATMENT_DATE_EST,-1,-1,Temp_Table_2,RETREATMENT_DATE_EST,-1,-1,Temp_Table_3,RETREATMENT_DATE_EST,-1,-1;
    TREATMENT_NAME \"TREATMENT NAME\" true true false 150 Text 0 0,First,#,Temp_Table_1,TREATMENT_NAME,0,150,Temp_Table_2,TREATMENT_NAME,0,150,Temp_Table_3,TREATMENT_NAME,0,150;
    BatchID \"BATCH ID (TREATMENT)\" true true false 40 Text 0 0,First,#,Temp_Table_1,BatchID,0,40,Temp_Table_2,BatchID,0,40,Temp_Table_3,BatchID,0,40;
    Val_Status_t \"Validation Status\" true true false 15 Text 0 0,First,#,Temp_Table_1,VAL_STATUS_t,0,15,Temp_Table_2,VAL_STATUS_t,0,15,Temp_Table_3,VAL_STATUS_t,0,15;
    Val_Message_t \"Validation Message\" true true false 15 Text 0 0,First,#,Temp_Table_1,Val_Message_t,0,15,Temp_Table_2,Val_Message_t,0,15,Temp_Table_3,Val_Message_t,0,15;
    Val_RunDate_t \"Validation Run Date\" true true false 8 Date 0 0,First,#,Temp_Table_1,VAL_RUNDATE_t,-1,-1,Temp_Table_2,VAL_RUNDATE_t,-1,-1,Temp_Table_3,VAL_RUNDATE_t,-1,-1;
    Review_Status_t \"Review Status\" true true false 15 Text 0 0,First,#,Temp_Table_1,REVIEW_STATUS_t,0,15,Temp_Table_2,REVIEW_STATUS_t,0,15,Temp_Table_3,REVIEW_STATUS_t,0,15;
    Review_Message_t \"Review Message\" true true false 15 Text 0 0,First,#,Temp_Table_1,Review_Message_t,0,15,Temp_Table_2,Review_Message_t,0,15,Temp_Table_3,Review_Message_t,0,15;
    Review_RunDate_t \"Review Run Date\" true true false 8 Date 0 0,First,#,Temp_Table_1,REVIEW_RUNDATE_t,-1,-1,Temp_Table_2,REVIEW_RUNDATE_t,-1,-1,Temp_Table_3,REVIEW_RUNDATE_t,-1,-1;
    Dataload_Status_t \"Dataload Status\" true true false 15 Text 0 0,First,#,Temp_Table_1,DATALOAD_STATUS_t,0,15,Temp_Table_2,DATALOAD_STATUS_t,0,15,Temp_Table_3,DATALOAD_STATUS_t,0,15;
    Dataload_Msg_t \"Dataload Message\" true true false 15 Text 0 0,First,#,Temp_Table_1,DATALOAD_MSG_t,0,15,Temp_Table_2,DATALOAD_MSG_t,0,15,Temp_Table_3,DATALOAD_MSG_t,0,15;
    ACTIVID_USER \"ACTIVITYID USER\" true true false 50 Text 0 0,First,#,Temp_Table_1,ACTIVID_USER,0,50,Temp_Table_2,ACTIVID_USER,0,50,Temp_Table_3,ACTIVID_USER,0,50;
    TREATMENTID_ \"TREATMENTID\" true true false 50 Text 0 0,First,#,Temp_Table_1,TREATMENTID_,0,50,Temp_Table_2,TREATMENTID_,0,50,Temp_Table_3,TREATMENTID_,0,50;
    ORG_ADMIN_a \"ORG DATA STEWARD\" true true false 150 Text 0 0,First,#,Temp_Table_1,ORG_ADMIN_a,0,150,Temp_Table_2,ORG_ADMIN_a,0,150,Temp_Table_3,ORG_ADMIN_a,0,150;
    ACTIVITY_DESCRIPTION \"ACTIVITY DESCRIPTION\" true true false 70 Text 0 0,First,#,Temp_Table_1,ACTIVITY_DESCRIPTION,0,70,Temp_Table_2,ACTIVITY_DESCRIPTION,0,70,Temp_Table_3,ACTIVITY_DESCRIPTION,0,70;
    ACTIVITY_CAT \"ACTIVITY CATEGORY\" true true false 40 Text 0 0,First,#,Temp_Table_1,ACTIVITY_CAT,0,40,Temp_Table_2,ACTIVITY_CAT,0,40,Temp_Table_3,ACTIVITY_CAT,0,40;
    BROAD_VEGETATION_TYPE \"BROAD VEGETATION TYPE\" true true false 50 Text 0 0,First,#,Temp_Table_1,BROAD_VEGETATION_TYPE,0,50,Temp_Table_2,BROAD_VEGETATION_TYPE,0,50,Temp_Table_3,BROAD_VEGETATION_TYPE,0,50;
    BVT_USERD \"IS BVT USER DEFINED\" true true false 3 Text 0 0,First,#,Temp_Table_1,BVT_USERD,0,3,Temp_Table_2,BVT_USERD,0,3,Temp_Table_3,BVT_USERD,0,3;
    ACTIVITY_STATUS \"ACTIVITY STATUS\" true true false 25 Text 0 0,First,#,Temp_Table_1,ACTIVITY_STATUS,0,25,Temp_Table_2,ACTIVITY_STATUS,0,25,Temp_Table_3,ACTIVITY_STATUS,0,25;
    ACTIVITY_QUANTITY \"ACTIVITY QUANTITY\" true true false 8 Double 0 0,First,#,Temp_Table_1,ACTIVITY_QUANTITY,-1,-1,Temp_Table_2,ACTIVITY_QUANTITY,-1,-1,Temp_Table_3,ACTIVITY_QUANTITY,-1,-1;
    ACTIVITY_UOM \"ACTIVITY UNITS\" true true false 15 Text 0 0,First,#,Temp_Table_1,ACTIVITY_UOM,0,15,Temp_Table_2,ACTIVITY_UOM,0,15,Temp_Table_3,ACTIVITY_UOM,0,15;
    ACTIVITY_START \"ACTIVITY START\" true true false 8 Date 0 0,First,#,Temp_Table_1,ACTIVITY_START,-1,-1,Temp_Table_2,ACTIVITY_START,-1,-1,Temp_Table_3,ACTIVITY_START,-1,-1;
    ACTIVITY_END \"ACTIVITY END\" true true false 8 Date 0 0,First,#,Temp_Table_1,ACTIVITY_END,-1,-1,Temp_Table_2,ACTIVITY_END,-1,-1,Temp_Table_3,ACTIVITY_END,-1,-1;
    ADMIN_ORG_NAME \"ADMINISTRATION ORGANIZATION NAME\" true true false 150 Text 0 0,First,#,Temp_Table_1,ADMIN_ORG_NAME,0,150,Temp_Table_2,ADMIN_ORG_NAME,0,150,Temp_Table_3,ADMIN_ORG_NAME,0,150;
    IMPLEM_ORG_NAME \"IMPLEMENTATION ORGANIZATION NAME\" true true false 150 Text 0 0,First,#,Temp_Table_1,IMPLEM_ORG_NAME,0,150,Temp_Table_2,IMPLEM_ORG_NAME,0,150,Temp_Table_3,IMPLEM_ORG_NAME,0,150;
    PRIMARY_FUND_SRC_NAME \"PRIMARY FUND SOURCE NAME\" true true false 100 Text 0 0,First,#,Temp_Table_1,PRIMARY_FUND_SRC_NAME,0,100,Temp_Table_2,PRIMARY_FUND_SRC_NAME,0,100,Temp_Table_3,PRIMARY_FUND_SRC_NAME,0,100;
    PRIMARY_FUND_ORG_NAME \"PRIMARY FUND ORGANIZATION NAME\" true true false 100 Text 0 0,First,#,Temp_Table_1,PRIMARY_FUND_ORG_NAME,0,100,Temp_Table_2,PRIMARY_FUND_ORG_NAME,0,100,Temp_Table_3,PRIMARY_FUND_ORG_NAME,0,100;
    SECONDARY_FUND_SRC_NAME \"SECONDARY FUND SOURCE NAME\" true true false 100 Text 0 0,First,#,Temp_Table_1,SECONDARY_FUND_SRC_NAME,0,100,Temp_Table_2,SECONDARY_FUND_SRC_NAME,0,100,Temp_Table_3,SECONDARY_FUND_SRC_NAME,0,100;
    SECONDARY_FUND_ORG_NAME \"SECONDARY FUND ORGANIZATION NAME\" true true false 100 Text 0 0,First,#,Temp_Table_1,SECONDARY_FUND_ORG_NAME,0,100,Temp_Table_2,SECONDARY_FUND_ORG_NAME,0,100,Temp_Table_3,SECONDARY_FUND_ORG_NAME,0,100;
    TERTIARY_FUND_SRC_NAME \"TERTIARY FUND SOURCE NAME\" true true false 100 Text 0 0,First,#,Temp_Table_1,TERTIARY_FUND_SRC_NAME,0,100,Temp_Table_2,TERTIARY_FUND_SRC_NAME,0,100,Temp_Table_3,TERTIARY_FUND_SRC_NAME,0,100;
    TERTIARY_FUND_ORG_NAME \"TERTIARY FUND ORGANIZATION NAME\" true true false 100 Text 0 0,First,#,Temp_Table_1,TERTIARY_FUND_ORG_NAME,0,100,Temp_Table_2,TERTIARY_FUND_ORG_NAME,0,100,Temp_Table_3,TERTIARY_FUND_ORG_NAME,0,100;
    ACTIVITY_PRCT \"ACTIVITY PERCENT\" true true false 2 Short 0 0,First,#,Temp_Table_1,ACTIVITY_PRCT,-1,-1,Temp_Table_2,ACTIVITY_PRCT,-1,-1,Temp_Table_3,ACTIVITY_PRCT,-1,-1;
    RESIDUE_FATE \"RESIDUE FATE\" true true false 35 Text 0 0,First,#,Temp_Table_1,RESIDUE_FATE,0,35,Temp_Table_2,RESIDUE_FATE,0,35,Temp_Table_3,RESIDUE_FATE,0,35;
    RESIDUE_FATE_QUANTITY \"RESIDUE FATE QUANTITY\" true true false 8 Double 0 0,First,#,Temp_Table_1,RESIDUE_FATE_QUANTITY,-1,-1,Temp_Table_2,RESIDUE_FATE_QUANTITY,-1,-1,Temp_Table_3,RESIDUE_FATE_QUANTITY,-1,-1;
    RESIDUE_FATE_UNITS \"RESIDUE FATE UNITS\" true true false 5 Text 0 0,First,#,Temp_Table_1,RESIDUE_FATE_UNITS,0,5,Temp_Table_2,RESIDUE_FATE_UNITS,0,5,Temp_Table_3,RESIDUE_FATE_UNITS,0,5;ACTIVITY_NAME \"ACTIVITY NAME\" true true false 150 Text 0 0,First,#,Temp_Table_1,ACTIVITY_NAME,0,150,Temp_Table_2,ACTIVITY_NAME,0,150,Temp_Table_3,ACTIVITY_NAME,0,150;VAL_STATUS_a \"VALIDATION STATUS\" true true false 15 Text 0 0,First,#,Temp_Table_1,VAL_STATUS_a,0,15,Temp_Table_2,VAL_STATUS_a,0,15,Temp_Table_3,VAL_STATUS_a,0,15;
    VAL_MSG_a \"VALIDATION MESSAGE\" true true false 15 Text 0 0,First,#,Temp_Table_1,VAL_MSG_a,0,15,Temp_Table_2,VAL_MSG_a,0,15,Temp_Table_3,VAL_MSG_a,0,15;
    VAL_RUNDATE_a \"VALIDATION RUN DATE\" true true false 8 Date 0 0,First,#,Temp_Table_1,VAL_RUNDATE_a,-1,-1,Temp_Table_2,VAL_RUNDATE_a,-1,-1,Temp_Table_3,VAL_RUNDATE_a,-1,-1;
    REVIEW_STATUS_a \"REVIEW STATUS\" true true false 15 Text 0 0,First,#,Temp_Table_1,REVIEW_STATUS_a,0,15,Temp_Table_2,REVIEW_STATUS_a,0,15,Temp_Table_3,REVIEW_STATUS_a,0,15;
    REVIEW_MSG_a \"REVIEW MESSAGE\" true true false 15 Text 0 0,First,#,Temp_Table_1,REVIEW_MSG_a,0,15,Temp_Table_2,REVIEW_MSG_a,0,15,Temp_Table_3,REVIEW_MSG_a,0,15;
    REVIEW_RUNDATE_a \"REVIEW RUN DATE\" true true false 8 Date 0 0,First,#,Temp_Table_1,REVIEW_RUNDATE_a,-1,-1,Temp_Table_2,REVIEW_RUNDATE_a,-1,-1,Temp_Table_3,REVIEW_RUNDATE_a,-1,-1;
    DATALOAD_STATUS_a \"DATALOAD STATUS\" true true false 15 Text 0 0,First,#,Temp_Table_1,DATALOAD_STATUS_a,0,15,Temp_Table_2,DATALOAD_STATUS_a,0,15,Temp_Table_3,DATALOAD_STATUS_a,0,15;
    DATALOAD_MSG_a \"DATALOAD MESSAGE\" true true false 15 Text 0 0,First,#,Temp_Table_1,DATALOAD_MSG_a,0,15,Temp_Table_2,DATALOAD_MSG_a,0,15,Temp_Table_3,DATALOAD_MSG_a,0,15
    Source \"Source\" true true false 65 Text 0 0,First,#,Temp_Table_1,Source,0,65,Temp_Table_2,Source,0,65,Temp_Table_3,Source,0,65;
    Year \"Calendar Year\" true true false 4 Long 0 0,First,#,Temp_Table_1,Year,-1,-1,Temp_Table_2,Year,-1,-1,Temp_Table_3,Year,-1,-1;
    Year_txt \"Year as Text\" true true false 255 Text 0 0,First,#,Temp_Table_1,Year_txt,0,255,Temp_Table_2,Year_txt,0,255,Temp_Table_3,Year_txt,0,255;
    Act_Code \"USFS Activity Code\" true true false 4 Long 0 0,First,#,Temp_Table_1,Act_Code,-1,-1,Temp_Table_2,Act_Code,-1,-1,Temp_Table_3,Act_Code,-1,-1;Crosswalk \"Crosswalk Activities\" true true false 150 Text 0 0,First,#,Temp_Table_1,Crosswalk,0,150,Temp_Table_2,Crosswalk,0,150,Temp_Table_3,Crosswalk,0,150;
    Federal_FY \"Federal FY\" true true false 4 Long 0 0,First,#,Temp_Table_1,Federal_FY,-1,-1,Temp_Table_2,Federal_FY,-1,-1,Temp_Table_3,Federal_FY,-1,-1;
    State_FY \"State FY\" true true false 4 Long 0 0,First,#,Temp_Table_1,State_FY,-1,-1,Temp_Table_2,State_FY,-1,-1,Temp_Table_3,State_FY,-1,-1;
    TRMT_GEOM \"TREATMENT GEOMETRY\" true true false 10 Text 0 0,First,#,Temp_Table_1,TRMT_GEOM,0,10,Temp_Table_2,TRMT_GEOM,0,10,Temp_Table_3,TRMT_GEOM,0,10;
    COUNTS_TO_MAS \"COUNTS TOWARDS MAS\" true true false 3 Text 0 0,First,#,Temp_Table_1,COUNTS_TO_MAS,0,3,Temp_Table_2,COUNTS_TO_MAS,0,3,Temp_Table_3,COUNTS_TO_MAS,0,3""",
)

# In[4]:


Select_1 = arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=Appended, where_clause=report_clause
)

XY_pts = arcpy.management.XYTableToPoint(
    in_table=Select_1,
    out_feature_class=output_all_pts,
    x_field="LONGITUDE",
    y_field="LATITUDE",
    coordinate_system=4269,  # "GCS_WGS_1984"
)

# In[5]:


AssignDomains(in_table=XY_pts)

delete_fields_1 = arcpy.management.DeleteField(
    in_table=XY_pts,
    drop_field=[
        "AGENCY",
        "ADMINISTERING_ORG",
        "PRIMARY_OWNERSHIP_GROUP",
        "COUNTY",
        "REGION",
        "ACTIVITY_DESCRIPTION",
        "ACTIVITY_CAT",
        "BROAD_VEGETATION_TYPE",
        "ACTIVITY_STATUS",
        "ACTIVITY_QUANTITY",
        "ACTIVITY_UOM",
        "ACTIVITY_END",
    ],
    method="KEEP_FIELDS",
)

Repaired_Input_Features = arcpy.management.RepairGeometry(
    in_features=delete_fields_1
)

# In[6]:


Add_EntityType = arcpy.management.AddField(
    Repaired_Input_Features, 
    "Entity_Type", 
    "TEXT", 
    field_length=25
)

# In[7]:


ITSALL_Value_2_ = arcpy.management.CalculateField(
    in_table=Add_EntityType,
    field="Entity_Type",
    expression="ifelse(!AGENCY!)",
    code_block="""def ifelse(Agency):
                    if Agency in ['CALEPA', 'CALSTA', 'CNRA']:
                        return 'State'
                    if Agency in ['DOD', 'DOI', 'USDA']:
                        return 'Federal'
                    if Agency == 'Industrial Timber' or Agency == 'TIMBER':
                        return 'Timber Companies'
                    else:
                        return None""",
)

# In[8]:


# Activities_Report_Table = arcpy.management.CreateTable(out_path=scratch_workspace, out_name=f"Activities_Report_Table", template=[WFR_TF_Template])
arcpy.conversion.TableToExcel(
    Input_Table=[ITSALL_Value_2_],
    Output_Excel_File=Output_Excel,
    Use_field_alias_as_column_header="ALIAS",
    Use_domain_and_subtype_description="DESCRIPTION",
)

# In[9]:


print("   Deleting Scratch Files")
delete_scratch_files(
    gdb=scratch_workspace, 
    delete_fc="yes", 
    delete_table="yes", 
    delete_ds="yes"
)
