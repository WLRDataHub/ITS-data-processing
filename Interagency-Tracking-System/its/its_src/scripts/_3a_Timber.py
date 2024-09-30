"""
# Description:  Converts the non-spatial MS Excel spreadsheet supplied by the California 
#               Timber Industry into the Task Force standardized schema including synthetic
#               geospatial locations off the Coast of California allowing this data to be
#               included in the Activities and Footprints Reports.  
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: July 3, 2024
"""

import datetime

start1 = datetime.datetime.now()

import os
import arcpy
import sys
from sys import argv
from ._1_add_fields import AddFields
from ._1_assign_domains import AssignDomains
from ._3_enrichments_pts import enrich_points
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()


def Timber(input_fc, output_enriched, delete_scratch=True):
    with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace,
        outputCoordinateSystem=arcpy.SpatialReference(
            "NAD 1983 California (Teale) Albers (Meters)"
        ),  # WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference(
            "NAD 1983 California (Teale) Albers (Meters)"
        ),  # WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'",
        preserveGlobalIds=True,
        qualifiedFieldNames=False,
        transferDomains=False,
        transferGDBAttributeProperties=False,
        overwriteOutput=True,
    ):
        print(f"Start Time {start1}")

        # define intermediary objects in scratch
        output_standardized = os.path.join(scratch_workspace, "Timber_standardized")

        ### BEGIN TOOL CHAIN
        # Convert the non-spatial timber industry excel file to a table in the gdb.
        #   Rename fields from the table. Add the standard fields. Import attributes 
        #   to the standard fields.
        print("Performing Standardization")
        print("   step 1/4 convert Excel sheet to table")

        # Process: Excel To Table (Excel To Table) (conversion)
        Timber_Industry_table = os.path.join(scratch_workspace, "Timber_Industry_table")
        excel_to_table_1 = arcpy.conversion.ExcelToTable(
            input_fc,
            Timber_Industry_table,
            Sheet="Sheet1",
            cell_range="A2:N26",
        )

        print("   step 2/4 rename and add fields")
        alterfield_1 = arcpy.management.AlterField(
            in_table=excel_to_table_1,
            field="ACTIVITY_DESCRIPTION",
            new_field_name="ACTIVITY_DESCRIPTION_",
            clear_field_alias="CLEAR_ALIAS"
        )

        alterfield_2 = arcpy.management.AlterField(
            in_table=alterfield_1,
            field="BROAD_VEGETATION_TYPE",
            new_field_name="BROAD_VEGETATION_TYPE_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_3 = arcpy.management.AlterField(
            in_table=alterfield_2,
            field="ACTIVITY_STATUS",
            new_field_name="ACTIVITY_STATUS_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_4 = arcpy.management.AlterField(
            in_table=alterfield_3,
            field="ACTIVITY_QUANTITY",
            new_field_name="ACTIVITY_QUANTITY_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_5 = arcpy.management.AlterField(
            in_table=alterfield_4,
            field="ACTIVITY_START",
            new_field_name="ACTIVITY_START_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_6 = arcpy.management.AlterField(
            in_table=alterfield_5,
            field="ACTIVITY_END",
            new_field_name="ACTIVITY_END_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_7 = arcpy.management.AlterField(
            in_table=alterfield_6,
            field="ADMINISTERING_ORG",
            new_field_name="ADMINISTERING_ORG_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_8 = arcpy.management.AlterField(
            in_table=alterfield_7,
            field="COUNTY",
            new_field_name="COUNTY_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_9 = arcpy.management.AlterField(
            in_table=alterfield_8,
            field="IN_WUI",
            new_field_name="IN_WUI_",
            clear_field_alias="CLEAR_ALIAS"
        )
        alterfield_10 = arcpy.management.AlterField(
            in_table=alterfield_9,
            field="PRIMARY_OWNERSHIP_GROUP",
            new_field_name="PRIMARY_OWNERSHIP_GROUP_",
            clear_field_alias="CLEAR_ALIAS"
        )

        addfields_1 = AddFields(Input_Table=alterfield_10)

        print("   step 3/4 calculate fields")
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_1 = arcpy.management.CalculateField(
            in_table=alterfield_10,
            field="ACTIVITY_DESCRIPTION",
            expression="!ACTIVITY_DESCRIPTION_!"
        )

        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_2 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_1,
            field="ACTIVITY_CAT",
            expression="!ACTIVITY_CATEGORY!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_3 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_2,
            field="BROAD_VEGETATION_TYPE",
            expression="!BROAD_VEGETATION_TYPE_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_4 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_3,
            field="BVT_USERD",
            expression="!IS_BVT_USER_DEFINED!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_5 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_4,
            field="ACTIVITY_STATUS",
            expression="!ACTIVITY_STATUS_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_6 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_5,
            field="ACTIVITY_QUANTITY",
            expression="!ACTIVITY_QUANTITY_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_7 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_6,
            field="ACTIVITY_UOM",
            expression="!ACTIVITY_UNITS!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_8 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_7,
            field="ACTIVITY_START",
            expression="!ACTIVITY_START_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_9 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_8,
            field="ACTIVITY_START",
            expression="!ACTIVITY_START_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_10 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_9,
            field="ACTIVITY_END",
            expression="!ACTIVITY_END_!"
        )

        # set admin org to 'timber companies'
        arcpy.management.CalculateField(
            in_table=Calculate_Fields_10,
            field="ADMINISTERING_ORG",
            expression="'Timber Companies'"
        )
        
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_11 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_10,
            field="ADMIN_ORG_NAME",
            expression="!ADMINISTERING_ORG_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_12 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_11, 
            field="COUNTY", 
            expression="!COUNTY_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_13 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_12, 
            field="IN_WUI", 
            expression="!IN_WUI_!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_14 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_13,
            field="REGION",
            expression="!TASK_FORCE_REGION!"
        )
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_15 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_14,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression="!PRIMARY_OWNERSHIP_GROUP_!"
        )
        
        # Process: Calculate Fund Source (Calculate Field) (management)
        Calculate_Fields_16 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_15,
            field="PRIMARY_FUNDING_SOURCE",
            expression="'PRIVATE'"
        )

        # Process: Calculate Fund Org (Calculate Field) (management)
        Calculate_Fields_17 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_16,
            field="PRIMARY_FUNDING_ORG",
            expression="'PRIVATE_INDUSTRY'"
        )

        # Process: Calculate Agency (Calculate Field) (management)
        Calculate_Fields_18 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_17, 
            field="AGENCY", 
            expression="!ADMIN_ORG_NAME!"
        )

        # Process: Calculate Imp Org (Calculate Field) (management)
        Calculate_Fields_19 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_18,
            field="IMPLEMENTING_ORG",
            expression="!ADMIN_ORG_NAME!"
        )

        # Process: Calculate Data Steward (Calculate Field) (management)
        Calculate_Fields_20 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_19,
            field="ORG_ADMIN_p",
            expression="!ADMIN_ORG_NAME!"
        )

        # Process: Calculate Data Steward 2 (Calculate Field) (management)
        Calculate_Fields_21 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_20,
            field="ORG_ADMIN_t",
            expression="!ADMIN_ORG_NAME!"
        )

        # Process: Calculate Data Steward 3 (Calculate Field) (management)
        Calculate_Fields_22 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_21,
            field="ORG_ADMIN_a",
            expression="!ADMIN_ORG_NAME!"
        )

        # Process: Calculate Primary Fund Source 2 (Calculate Field) (management)
        Calculate_Fields_23 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_22,
            field="PRIMARY_FUND_SRC_NAME",
            expression="!PRIMARY_FUNDING_SOURCE!"
        )

        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        Calculate_Fields_24 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_23,
            field="PRIMARY_FUND_ORG_NAME",
            expression="!PRIMARY_FUNDING_ORG!"
        )

        # Process: Calculate Source (Calculate Field) (management)
        Calculate_Fields_25 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_24,
            field="Source",
            expression='"Industrial Timber"'
        )

        # Process: Remove spaces from end of Activity Description Field (Calculate Field) (management)
        Calculate_Fields_26 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_25,
            field="ACTIVITY_DESCRIPTION",
            expression="ifelse(!ACTIVITY_DESCRIPTION!)",
            code_block="""def ifelse(Act):
                        if Act == \"Fuel Break (pursuant to FPRs)\":
                            return \"Thinning (Manual)\"
                        elif Act == \"Fuel Break\": 
                            return \"Thinning (Manual)\"     
                        elif Act == \"Group Selection\":
                            return \"Group Selection Harvest\"
                        elif Act == \"Group Selection \":
                            return \"Group Selection Harvest\"
                        elif Act == \"Rehabilitation of Understocked Area \":
                            return \"Rehabilitation of Understocked Area\"
                        else:
                            return Act.strip()"""
        )

        # Process: Calculate Crosswalk Field (Calculate Field) (management)
        Calculate_Fields_27 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_26,
            field="Crosswalk",
            expression="!ACTIVITY_DESCRIPTION!"
        )

        # Process: Calculate Geometry Type (Calculate Field) (management)
        Calculate_Fields_28 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_27, 
            field="TRMT_GEOM", 
            expression="'POINT'"
        )

        

        # Add simulated locations to the feature class.  Latitudes and Longitude 
        #   coordinates were chosen to be within the simulated ownership polygon
        #   in the ownership layer off the coast of California.  Points are spaced 
        #   far enough appart so that the acrage based buffers don't overlap.

        # Process: Calculate Lat (Calculate Field) (management)
        Calculate_Fields_29 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_28,
            field="LATITUDE",
            expression="ifelse(!ACTIVITY_DESCRIPTION!)",
            code_block="""def ifelse(ACT):
                            if ACT == 'Aspen/Meadow/Wet Area Restoration':
                                return '37.482646'
                            elif ACT == 'Chipping':
                                return '37.627402'
                            elif ACT == 'Commercial Thin':
                                return '37.465931'
                            elif ACT == 'Group Selection Harvest':
                                return '37.464555'
                            elif ACT == 'Herbicide Application':
                                return '37.655861'
                            elif ACT == 'Lop and Scatter':
                                return '37.551419'
                            elif ACT == 'Mastication':
                                return '37.462986'
                            elif ACT == 'Mowing':
                                return '37.4928'
                            elif ACT == 'Oak Woodland Management':
                                return '37.534775'
                            elif ACT == 'Pile Burning':
                                return '37.572375'
                            elif ACT == 'Piling':
                                return '37.461292'
                            elif ACT == 'Rehabilitation of Understocked Area':
                                return '37.525904'
                            elif ACT == 'Single Tree Selection':
                                return '37.523401'
                            elif ACT == 'Thinning (Manual)':
                                return '37.625516'
                            elif ACT == 'Transition Harvest':
                                return '37.506553'
                            elif ACT == 'Tree Planting':
                                return '37.534028'
                            elif ACT == 'Variable Retention Harvest':
                                return '37.520369'
	
                            # Added by Kai to process 2023 data
                            elif ACT == 'Alternative Prescription':
                                return '37.488371'
                            elif ACT == 'Fuel Break (pursuant to FPRs)':
                                return '37.473531'
                            elif ACT == 'Group Selection':
                                return '37.465912'
                            elif ACT == 'Invasive Plant Removal':
                                return '37.614452'
                            elif ACT == 'Landing Treated':
                                return '37.605668'
                            elif ACT == 'Roadway Clearance':
                                return '37.407632'
                            elif ACT == 'Sanitation Harvest':
                                return '37.591843'
                            elif ACT == 'Site Preparation':
                                return '37.562715'
                            elif ACT == 'Thinning (Mechanical)':
                                return '37.551381'
                            else:
                                print(ACT)
                                exit()
                        """
        )

        # Process: Calculate Long (Calculate Field) (management)
        Calculate_Fields_30 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_29,
            field="LONGITUDE",
            expression="ifelse(!ACTIVITY_DESCRIPTION!)",
            code_block="""def ifelse(ACT):
                            if ACT == 'Aspen/Meadow/Wet Area Restoration':
                                return '-123.21911033'
                            elif ACT == 'Chipping':
                                return '-123.249295'
                            elif ACT == 'Commercial Thin':
                                return '-123.390699'
                            elif ACT == 'Group Selection Harvest':
                                return '-123.438758'
                            elif ACT == 'Herbicide Application':
                                return '-123.47236'
                            elif ACT == 'Lop and Scatter':
                                return '-123.222054'
                            elif ACT == 'Mastication':
                                return '-123.49278'
                            elif ACT == 'Mowing':
                                return '-123.219545'
                            elif ACT == 'Oak Woodland Management':
                                return '-123.221341'
                            elif ACT == 'Pile Burning':
                                return '-123.222952'
                            elif ACT == 'Piling':
                                return '-123.550139'
                            elif ACT == 'Rehabilitation of Understocked Area':
                                return '-123.459845'
                            elif ACT == 'Single Tree Selection':
                                return '-123.545137'
                            elif ACT == 'Thinning (Manual)':
                                return '-123.317925'
                            elif ACT == 'Transition Harvest':
                                return '-123.220133'
                            elif ACT == 'Tree Planting':
                                return '-123.322739'
                            elif ACT == 'Variable Retention Harvest':
                                return '-123.220724'
	
                            # Added by Kai to process 2023 data
                            elif ACT == 'Alternative Prescription':
                                return '-123.339323'
                            elif ACT == 'Fuel Break (pursuant to FPRs)':
                                return '-123.349238'
                            elif ACT == 'Group Selection':
                                return '-123.358234'
                            elif ACT == 'Invasive Plant Removal':
                                return '-123.483481'
                            elif ACT == 'Landing Treated':
                                return '-123.498283'
                            elif ACT == 'Roadway Clearance':
                                return '-123.423823'
                            elif ACT == 'Sanitation Harvest':
                                return '-123.573429'
                            elif ACT == 'Site Preparation':
                                return '-123.523224'
                            elif ACT == 'Thinning (Mechanical)':
                                return '-123.573398'


                        """
        )

        print(f"Converting Table to Points FC")
        Timber_Industry_XYTableToPoint = os.path.join(
            scratch_workspace, "Timber_Industry_XYTableToPoint"
        )
        XY_1 = arcpy.management.XYTableToPoint(
            in_table=Calculate_Fields_30,
            out_feature_class=Timber_Industry_XYTableToPoint,
            x_field="LONGITUDE",
            y_field="LATITUDE",
            coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'
        )

        # Process: Pairwise Dissolve (Pairwise Dissolve) (analysis) to remove duplicate 
        #   activity descriptions (Combines similar records, sums Activity Acres)

        Timber_Industr_PairwiseDisso = output_standardized

        arcpy.analysis.PairwiseDissolve(
            in_features=XY_1,
            out_feature_class=Timber_Industr_PairwiseDisso,
            dissolve_field=[
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
            "Val_Status_t",
            "Val_MSG_t",
            "Val_RunDate_t",
            "Review_Status_t",
            "Review_Msg_t",
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
            "COUNTS_TO_MAS"
            ],
            statistics_fields=[["ACTIVITY_QUANTITY", "SUM"]],
            multi_part="SINGLE_PART"
        )

        # Process: Alter Field (Alter Field) (management)
        Alter_Field_1 = arcpy.management.AlterField(
            in_table=Timber_Industr_PairwiseDisso,
            field="SUM_ACTIVITY_QUANTITY",
            new_field_name="ACTIVITY_QUANTITY",
            clear_field_alias="CLEAR_ALIAS"
        )

        # Process: Calculate Project ID (Calculate Field) (management)
        Calculate_Fields_31 = arcpy.management.CalculateField(
            in_table=Alter_Field_1,
            field="PROJECTID_USER",
            expression="'TI'+'-'+str(!OBJECTID!)"
        )

        # Process: Calculate Project Name (Calculate Field) (management)
        Calculate_Fields_32 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_31,
            field="PROJECT_NAME",
            expression="!PROJECTID_USER!"
        )

        # Process: Calculate Treatment ID (Calculate Field) (management)
        Calculate_Fields_33 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_32,
            field="TRMTID_USER",
            expression="!PROJECTID_USER!"
        )

        # Process: Calculate Project Name (2) (Calculate Field) (management)
        Calculate_Fields_34 = arcpy.management.CalculateField(
            in_table=Calculate_Fields_33, 
            field="PROJECTNAME_", 
            expression="None"
        )

        # Process: Copy Features (2) (Copy Features) (management)
        Timber_Industrial_enriched = os.path.join(
            scratch_workspace, "Timber_Industrial_enriched_temp"
        )
        arcpy.management.CopyFeatures(
            in_features=Calculate_Fields_34,
            out_feature_class=Timber_Industrial_enriched,
        )

        # add non-existing filler columns
        for f in ['BatchID', 'BatchID_p', 'Review_MSG_t']:
            arcpy.management.CalculateField(
                in_table=Timber_Industrial_enriched, 
                field=f, 
                expression="''"
            )

        # Remove non-schema fields
        keepfields_1 = KeepFields(Timber_Industrial_enriched)


        import pandas as pd

        table = keepfields_1 
        fields = [field.name for field in arcpy.ListFields(table)] 

        data = []
        with arcpy.da.SearchCursor(table, fields) as cursor:
            for row in cursor:
                data.append(row)

        df = pd.DataFrame(data, columns=fields)

        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns
        # print(df)

        print(f"Saving Output Standardized")
        Count1 = arcpy.management.GetCount(keepfields_1)
        print("standardized has {} records".format(Count1[0]))

        # Enrich the dataset
        print("Performing Enrichments")
        enrich_points(enrich_pts_in=keepfields_1, enrich_pts_out=output_enriched)


        # #####################################################
        # Fix issues
        # #####################################################

        # Set the column BROAD_VEGETATION_TYPE to 'FOREST'
        arcpy.management.CalculateField(
           in_table=output_enriched,  # Input table or feature class
           field="BROAD_VEGETATION_TYPE",  # Field to be updated
           expression="'FOREST'",  # Expression to set the value
           expression_type="PYTHON3"  # Specify Python 3 syntax
        )

        # Create a dictionary to store the mapping
        activity_mapping = {
            "AMW_AREA_RESTOR": ("WATSHD_IMPRV", "MTN_MEADOW_RESTOR"),
            "CHIPPING": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "COMM_THIN": ("TIMB_HARV", "OTHER_FUELS_REDUCTION"),
            "GRP_SELECTION_HARVEST": ("TIMB_HARV", "BIOMASS_UTIL"),
            "HERBICIDE_APP": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "LOP_AND_SCAT": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "MASTICATION": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "MOWING": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "OAK_WDLND_MGMT": ("WATSHD_IMPRV", "OTHER_FUELS_REDUCTION"),
            "PILE_BURN": ("BENEFICIAL_FIRE", "OTHER_FUELS_REDUCTION"),
            "PILING": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "REHAB_UNDRSTK_AREA": ("TIMB_HARV", "ECO_RESTOR"),
            "SINGLE_TREE_SELECTION": ("TIMB_HARV", "BIOMASS_UTIL"),
            "THIN_MAN": ("MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "TRANSITION_HARVEST": ("TIMB_HARV", "BIOMASS_UTIL"),
            "TREE_PLNTING": ("TREE_PLNTING", "REFORESTATION"),
            "VARIABLE_RETEN_HARVEST": ("TIMB_HARV", "BIOMASS_UTIL")
        }

        # Create an update cursor
        with arcpy.da.UpdateCursor(output_enriched, ["ACTIVITY_DESCRIPTION", "ACTIVITY_CAT", "PRIMARY_OBJECTIVE"]) as cursor:
            for row in cursor:
                activity_description = row[0]
                if activity_description in activity_mapping:
                    row[1] = activity_mapping[activity_description][0]  # ACTIVITY_CAT
                    row[2] = activity_mapping[activity_description][1]  # PRIMARY_OBJECTIVE
                    cursor.updateRow(row)

        value_mapping = {
            "Roadway Clearance": ("ROAD_CLEAR", "MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "Alternative Prescription": ("TRANSITION_HARVEST", "TIMB_HARV", "BIOMASS_UTIL"),
            "Sanitation Harvest": ("SANI_HARVEST", "TIMB_HARV", "BIOMASS_UTIL"),
            "Landing Treated": ("LANDING_TRT", "MECH_HFR", "OTHER_FUELS_REDUCTION"),
            "Invasive Plant Removal": ("INV_PLANT_REMOVAL", "MECH_HFR", "ECO_RESTOR")
        }

        fields = ["CROSSWALK", "ACTIVITY_DESCRIPTION", "ACTIVITY_CAT", "PRIMARY_OBJECTIVE"]
        with arcpy.da.UpdateCursor(output_enriched, fields) as cursor:
            for row in cursor:
                crosswalk_value = row[0]  # CROSSWALK value
                if crosswalk_value in value_mapping:
                    # Update the other fields based on the mapping
                    row[1] = value_mapping[crosswalk_value][0]  # ACTIVITY_DESCRIPTION
                    row[2] = value_mapping[crosswalk_value][1]  # ACTIVITY_CAT
                    row[3] = value_mapping[crosswalk_value][2]  # PRIMARY_OBJECTIVE
                    cursor.updateRow(row)

        arcpy.management.CalculateField(
            in_table=output_enriched,
            field="CROSSWALK",
            expression="!ACTIVITY_DESCRIPTION!",
            expression_type="PYTHON3"
        )

        expression = "set_count_to_mas(!ACTIVITY_DESCRIPTION!)"
        code_block = """
def set_count_to_mas(activity_description):
    if activity_description in ['AMW_AREA_RESTOR', 'OAK_WDLND_MGMT']:
        return 'YES'
    else:
        return 'YES'
"""

        # Use CalculateField to update the "COUNT_TO_MAS" field
        arcpy.management.CalculateField(
            in_table=output_enriched,
            field="COUNTS_TO_MAS",
            expression=expression,
            expression_type="PYTHON3",
            code_block=code_block
        )

        print("Update completed successfully.")

        # print("="*70)
        # print("output_enriched")
        # print("="*70)

        table = output_enriched
        fields = [field.name for field in arcpy.ListFields(table)] 

        data = []
        with arcpy.da.SearchCursor(table, fields) as cursor:
            for row in cursor:
                data.append(row)

        df = pd.DataFrame(data, columns=fields)

        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns
        # print(df)

        print(f"Saving Output Enriched")
        Count3 = arcpy.management.GetCount(output_enriched)
        print("     enriched has {} records".format(Count3[0]))

        AssignDomains(in_table=output_enriched)

        if delete_scratch:
            print("Deleting Scratch Files")
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes"
            )

        end1 = datetime.datetime.now()
        elapsed1 = end1 - start1
        hours, remainder1 = divmod(elapsed1.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print(
            f"Timber script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete"
        )
