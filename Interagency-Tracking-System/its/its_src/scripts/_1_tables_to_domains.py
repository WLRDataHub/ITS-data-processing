"""
# Description: Creates Domains from Excel File
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from scripts.utils import init_gdb

workspace, scratch_workspace = init_gdb()

def TablesToDomains(workspace):
    arcpy.env.overwriteOutput = True

    Excel = "D:\\WORK\\wildfire\\Interagency-Tracking-System\\its\\its_src\\Domain_Tables_20231004.xlsx"

    # D_OBJECTIVE_ = os.path.join(Excel, "D_OBJECTIVE$") haha
    D_OBJECTIVE_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_OBJECTIVE')    

    # D_STATUS_ = os.path.join(Excel, "D_STATUS")
    D_STATUS_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_STATUS')    

    # D_CNTY_ = os.path.join(Excel, "D_CNTY$")
    D_CNTY_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_CNTY')    

    D_IN_WUI_ = os.path.join(Excel, "D_IN_WUI$")
    D_IN_WUI_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_IN_WUI')    

    D_ACTVDSCRP_ = os.path.join(Excel, "D_ACTVDSCRP$")
    D_ACTVDSCRP_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_ACTVDSCRP')    

    D_ACTVCAT_ = os.path.join(Excel, "D_ACTVCAT$")
    D_ACTVCAT_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_ACTVCAT')    

    D_USERDEFINED_ = os.path.join(Excel, "D_USERDEFINED$")
    D_USERDEFINED_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_USERDEFINED')    

    D_BVT_ = os.path.join(Excel, "D_BVT$")
    D_BVT_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_BVT')    

    D_RESIDUEFATE_ = os.path.join(Excel, "D_RESIDUEFATE$")
    D_RESIDUEFATE_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_RESIDUEFATE')    

    D_UOM_ = os.path.join(Excel, "D_UOM$")
    D_UOM_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_UOM')    

    D_TASKFORCE_ = os.path.join(Excel, "D_TASKFORCE$")
    D_TASKFORCE_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_TASKFORCE')    

    D_PR_OWN_GR_ = os.path.join(Excel, "D_PR_OWN_GR$")
    D_PR_OWN_GR_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_PR_OWN_GR')    

    D_FNDSRC_ = os.path.join(Excel, "D_FNDSRC$")
    D_FNDSRC_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_FNDSRC')    

    D_AGENCY_ = os.path.join(Excel, "D_AGENCY$")
    D_AGENCY_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_AGENCY')    

    D_ORGANIZATION_ = os.path.join(Excel, "D_ORGANIZATION$")
    D_ORGANIZATION_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_ORGANIZATION')    

    D_DATASTATUS_ = os.path.join(Excel, "D_DATASTATUS$")
    D_DATASTATUS_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_DATASTATUS')    

    D_DATAMSG_ = os.path.join(Excel, "D_DATAMSG$")
    D_DATAMSG_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_DATAMSG')    

    D_VERFIEDMSG_ = os.path.join(Excel, "D_VERFIEDMSG$")
    D_VERFIEDMSG_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_VERFIEDMSG')    

    D_TRMT_GEOM_ = os.path.join(Excel, "D_TRMT_GEOM$")
    D_TRMT_GEOM_ = arcpy.conversion.ExcelToTable(Excel, scratch_workspace, 'D_TRMT_GEOM')    


    Domain_1 = arcpy.management.TableToDomain(
        in_table=D_OBJECTIVE_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_OBJECTIVE",
        domain_description="Objectives",
        update_option="REPLACE",
    )

    Domain_2 = arcpy.management.TableToDomain(
        in_table=D_STATUS_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_STATUS",
        domain_description="Status",
        update_option="REPLACE",
    )

    Domain_3 = arcpy.management.TableToDomain(
        in_table=D_CNTY_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_CNTY",
        domain_description="County",
        update_option="REPLACE",
    )

    Domain_4 = arcpy.management.TableToDomain(
        in_table=D_IN_WUI_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_IN_WUI",
        domain_description="In WUI",
        update_option="REPLACE",
    )

    Domain_5 = arcpy.management.TableToDomain(
        in_table=D_ACTVDSCRP_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_ACTVDSCRP",
        domain_description="Activity Description",
        update_option="REPLACE",
    )

    Domain_6 = arcpy.management.TableToDomain(
        in_table=D_ACTVCAT_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_ACTVCAT",
        domain_description="Activity Category",
        update_option="REPLACE",
    )

    Domain_7 = arcpy.management.TableToDomain(
        in_table=D_USERDEFINED_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_USERDEFINED",
        domain_description="Yes / No",
        update_option="REPLACE",
    )

    Domain_8 = arcpy.management.TableToDomain(
        in_table=D_BVT_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_BVT",
        domain_description="Broad Vegetation Type",
        update_option="REPLACE",
    )

    Domain_9 = arcpy.management.TableToDomain(
        in_table=D_RESIDUEFATE_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_RESIDUEFATE",
        domain_description="Residue Fate",
        update_option="REPLACE",
    )

    Domain_10 = arcpy.management.TableToDomain(
        in_table=D_UOM_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_UOM",
        domain_description="Unit of Measure",
        update_option="REPLACE",
    )

    Domain_11 = arcpy.management.TableToDomain(
        in_table=D_TASKFORCE_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_TASKFORCE",
        domain_description="Task Force Region",
        update_option="REPLACE",
    )

    Domain_12 = arcpy.management.TableToDomain(
        in_table=D_PR_OWN_GR_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_PR_OWN_GR",
        domain_description="Ownership Group",
        update_option="REPLACE",
    )

    Domain_13 = arcpy.management.TableToDomain(
        in_table=D_FNDSRC_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_FNDSRC",
        domain_description="Funding Source",
        update_option="REPLACE",
    )

    Domain_14 = arcpy.management.TableToDomain(
        in_table=D_AGENCY_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_AGENCY",
        domain_description="Agency",
        update_option="REPLACE",
    )

    Domain_15 = arcpy.management.TableToDomain(
        in_table=D_ORGANIZATION_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_ORGANIZATION",
        domain_description="Organization or Agency",
        update_option="REPLACE",
    )

    Domain_16 = arcpy.management.TableToDomain(
        in_table=D_DATASTATUS_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_DATASTATUS",
        domain_description="Data Status",
        update_option="REPLACE",
    )

    Domain_17 = arcpy.management.TableToDomain(
        in_table=D_DATAMSG_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_DATAMSG",
        domain_description="Data Load Message",
        update_option="REPLACE",
    )

    Domain_18 = arcpy.management.TableToDomain(
        in_table=D_VERFIEDMSG_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_VERFIEDMSG",
        domain_description="Validated or Reviewed",
        update_option="REPLACE",
    )

    Domain_19 = arcpy.management.TableToDomain(
        in_table=D_TRMT_GEOM_,
        code_field="CODE",
        description_field="Descr",
        in_workspace=workspace,
        domain_name="D_TRMT_GEOM",
        domain_description="Geometry of Treatment",
        update_option="REPLACE",
    )

