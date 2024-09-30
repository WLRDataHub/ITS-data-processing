"""
# Description: Removes fields that don't match the schema
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def KeepFields(Keep_table):
    print("          removing unnecessary fields")
    arcpy.env.overwriteOutput = True

    field_list = [field.name for field in arcpy.ListFields(Keep_table)]      
    print(f"        field_list before: {field_list}")  

    fields_kept = arcpy.management.DeleteField(
        in_table=Keep_table,
        drop_field=[
            "PROJECTID_USER",
            "AGENCY",
            "ORG_ADMIN_p",
            "PROJECT_CONTACT",
            "PROJECT_EMAIL",
            "ADMINISTERING_ORG",
            "PROJECT_NAME",
            "PROJECT_STATUS",
            "PROJECT_START",
            "PROJECT_END",
            "PRIMARY_FUNDING_SOURCE",
            "PRIMARY_FUNDING_ORG",
            "IMPLEMENTING_ORG",
            "LATITUDE",
            "LONGITUDE",
            "BatchID_p",
            "Val_Status_p",
            "Val_MSG_p",
            "Val_RunDate_p",
            "Review_Status_p",
            "Review_MSG_p",
            "Review_RunDate_p",
            "Dataload_Status_p",
            "Dataload_Msg_p",
            "TRMTID_USER",
            "PROJECTID",
            "PROJECTNAME_",
            "ORG_ADMIN_t",
            "PRIMARY_OWNERSHIP_GROUP",
            "PRIMARY_OBJECTIVE",
            "SECONDARY_OBJECTIVE",
            "TERTIARY_OBJECTIVE",
            "TREATMENT_STATUS",
            "COUNTY",
            "IN_WUI",
            "REGION",
            "TREATMENT_AREA",
            "TREATMENT_START",
            "TREATMENT_END",
            "RETREATMENT_DATE_EST",
            "TREATMENT_NAME",
            "BatchID", # BatchID_t is 2022 CNRA, BatchID is 2023 and USFS
            "Val_Status_t",
            "Val_MSG_t",
            "Val_RunDate_t",
            "Review_Status_t",
            "Review_MSG_t",
            "Review_RunDate_t",
            "Dataload_Status_t",
            "Dataload_Msg_t",
            "ACTIVID_USER",
            "TREATMENTID_",
            "ORG_ADMIN_a",
            "ACTIVITY_DESCRIPTION",
            "ACTIVITY_CAT",
            "BROAD_VEGETATION_TYPE",
            "BVT_USERD",
            "ACTIVITY_STATUS",
            "ACTIVITY_QUANTITY",
            "ACTIVITY_UOM",
            "ACTIVITY_START",
            "ACTIVITY_END",
            "ADMIN_ORG_NAME",
            "IMPLEM_ORG_NAME",
            "PRIMARY_FUND_SRC_NAME",
            "PRIMARY_FUND_ORG_NAME",
            "SECONDARY_FUND_SRC_NAME",
            "SECONDARY_FUND_ORG_NAME",
            "TERTIARY_FUND_SRC_NAME",
            "TERTIARY_FUND_ORG_NAME",
            "ACTIVITY_PRCT",
            "RESIDUE_FATE",
            "RESIDUE_FATE_QUANTITY",
            "RESIDUE_FATE_UNITS",
            "ACTIVITY_NAME",
            # "BatchID_a",
            "VAL_STATUS_a",
            "VAL_MSG_a",
            "VAL_RUNDATE_a",
            "REVIEW_STATUS_a",
            "REVIEW_MSG_a",
            "REVIEW_RUNDATE_a",
            "DATALOAD_STATUS_a",
            "DATALOAD_MSG_a",
            "Source",
            "Year",
            "Year_txt",
            "Act_Code",
            "Crosswalk",
            "Federal_FY",
            "State_FY",
            "TRMT_GEOM",
            "COUNTS_TO_MAS",
        ],
        method="KEEP_FIELDS",
    )

    field_list = [field.name for field in arcpy.ListFields(fields_kept)]      
    print(f"        field_list after: {field_list}")  

    return fields_kept
