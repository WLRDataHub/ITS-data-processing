"""
# Description: Converts the California Department of Transportation's Fuels Treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.             
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime
start1 = datetime.datetime.now()

import os
import arcpy
from ._1_add_fields import AddFields
from ._1_assign_domains import AssignDomains
from ._3_enrichments_lines import enrich_lines
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

# update merge code with geopandas, due to arcpy KEEP_ALL not working
import geopandas as gpd
import pandas as pd

workspace, scratch_workspace = init_gdb()
# TODO add print steps

def CalTrans(
    input_lst,
    output_lines_enriched,
    delete_scratch=True,
    data_year=2022
):
    if data_year==2022:
        input_lines21,input_lines22,input_table21,input_table22 = input_lst
    elif data_year==2023:
        input_lines,input_table = input_lst
    else:
        raise Exception("only 2022 and 2023 data avaialable")
    

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
        overwriteOutput = True
    ):
        print(f"Start Time {start1}")
        if data_year==2022:
            # define intermediary objects in scratch
            
            CalTrans_scratch = os.path.join(scratch_workspace, "CalTrans_scratch")
            CalTrans21_scratch = os.path.join(scratch_workspace, "CalTrans21_scratch")
            CalTrans22_scratch = os.path.join(scratch_workspace, "CalTrans22_scratch")
            output_lines_standardized = os.path.join(scratch_workspace, "CalTrans_standardized")
            
            ### BEGIN TOOL CHAIN
            print("Part 1 join features and tables")
            print("     step 1/8 add 2021 join")
            """
            input_table21_join = arcpy.management.AddJoin(
                in_layer_or_view=input_lines21,
                in_field="HIghwayID",
                join_table=input_table21,
                join_field="HighwayID",
                join_type="KEEP_ALL",
                index_join_fields="INDEX_JOIN_FIELDS",
            )

            print("     step 2/8 save features")
            input_table21_join_copy = arcpy.management.CopyFeatures(
                input_table21_join, CalTrans21_scratch
            )

            # remove join needed to prevent modification of original data set
            arcpy.RemoveJoin_management(input_table21_join)
            
            

            Count1 = arcpy.management.GetCount(input_table21_join_copy)
            print("        input_table21_join_copy has {} records".format(Count1[0]))
            """

            CalTrans21_table = gpd.read_file(
                os.path.dirname(input_table21), 
                driver="OpenFileGDB", 
                layer=os.path.basename(input_table21))
            
            CalTrans21_lines = gpd.read_file(
                os.path.dirname(input_lines21),                 
                driver="OpenFileGDB", 
                layer=os.path.basename(input_lines21))
            
            input_table21_join = CalTrans21_table.merge(
                CalTrans21_lines, 
                how = 'left', 
                left_on='HighwayID', 
                right_on='HIghwayID').set_geometry("geometry_y").drop('geometry_x', axis=1)
            

            input_table21_join.to_file(
                os.path.dirname(CalTrans21_scratch), 
                driver="OpenFileGDB", 
                layer=os.path.basename(CalTrans21_scratch))

            print("        input_table21_join_copy has {} records".format(len(input_table21_join)))

            print("     step 3/8 add 2022 join")

            """
            input_table22_join = arcpy.management.AddJoin(
                in_layer_or_view=input_lines22,
                in_field="HIghwayID",
                join_table=input_table22,
                join_field="Highway_ID",
                join_type="KEEP_ALL",
                index_join_fields="INDEX_JOIN_FIELDS",
            )

            print("     step 4/8 save features")
            input_table22_join_copy = arcpy.management.CopyFeatures(
                input_table22_join, CalTrans22_scratch
            )
            
            Count2 = arcpy.management.GetCount(input_table22_join_copy)
            print("        input_table22_join_copy has {} records".format(Count2[0]))

            # remove join needed to prevent modification of original data set
            arcpy.RemoveJoin_management(input_table22_join)

            """

            CalTrans22_table = gpd.read_file(
                os.path.dirname(input_table22), 
                driver="OpenFileGDB", 
                layer=os.path.basename(input_table22))
            
            CalTrans22_lines = gpd.read_file(
                os.path.dirname(input_lines22),                 
                driver="OpenFileGDB", 
                layer=os.path.basename(input_lines22))
            
            input_table22_join = CalTrans22_table.merge(
                CalTrans22_lines, 
                how = 'left', 
                left_on='Highway_ID', 
                right_on='HIghwayID').set_geometry("geometry_y").drop('geometry_x', axis=1)
            

            input_table22_join.to_file(
                os.path.dirname(CalTrans22_scratch), 
                driver="OpenFileGDB", 
                layer=os.path.basename(CalTrans22_scratch))

            print("        input_table22_join_copy has {} records".format(len(input_table22_join)))


            output_table_gdf = pd.concat([input_table21_join, input_table22_join], ignore_index=True, axis=0)
            
            output_table_gdf.to_file(os.path.dirname(CalTrans_scratch), 
                driver="OpenFileGDB", 
                layer=os.path.basename(CalTrans_scratch))

            print("     step 5/8 combine 2021 and 2022")
            """
            print("   Appending Lines")
            CalTransLns_scratch = arcpy.management.CreateFeatureclass(
                out_path=scratch_workspace, 
                out_name="CalTransLns_scratch", 
                geometry_type="POLYLINE", 
                template=CalTrans22_scratch
                )

            
            append1_input = [CalTrans21_scratch, CalTrans22_scratch]
            """
        if data_year==2023:
            # define intermediary objects in scratch
            CalTrans_scratch = os.path.join(scratch_workspace, "CalTrans_scratch")
            output_lines_standardized = os.path.join(scratch_workspace, "CalTrans_standardized")
            
            ### BEGIN TOOL CHAIN
            print("Part 1 join features and tables")
            print("     step 1/8 add 2023 join")

            CalTrans_table = gpd.read_file(
                os.path.dirname(input_table), 
                driver="OpenFileGDB", 
                layer=os.path.basename(input_table))
            
            CalTrans_lines = gpd.read_file(
                os.path.dirname(input_lines),                 
                driver="OpenFileGDB", 
                layer=os.path.basename(input_lines))   
            
            input_table_join =CalTrans_table.merge(
                CalTrans_lines, 
                how = 'outer', 
                on=['Highway_ID', 'Calendar_Year']).set_geometry("geometry_y").drop('geometry_x', axis=1)

            print("     step 2/8 save features")
            input_table_join.to_file(
                os.path.dirname(CalTrans_scratch), 
                driver="OpenFileGDB", 
                layer=os.path.basename(CalTrans_scratch))

            print("        input_table_join has {} records".format(len(input_table_join)))

            print("     skipping step 3/8-5/8 in 2023 with no seperate files")
        # Use this append or the following append with field mapping depending on the situation.


        Count3 = arcpy.management.GetCount(CalTrans_scratch)
        print("       CalTransLns_append has {} records".format(Count3[0]))

        print("Part 2: Performing Standardization")
        print("     step 6/8 repair geometry")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=CalTrans_scratch,
            delete_null="KEEP_NULL",
            validation_method="ESRI",
        )

        print("     step 7/8 alter & add fields")
            
        
        ### remove combine fields in 2023 with no seperate files
        if data_year==2022:
            field="County"
        else:
            field="Begin_County"

        alterfield_1 = arcpy.management.AlterField(
            in_table=repair_geom_1,
            field=field,
            new_field_name="County2",
            new_field_alias="County2",
            field_type="TEXT",
            clear_field_alias="DO_NOT_CLEAR",
        )

        alterfield_2 = arcpy.management.AlterField(
            in_table=alterfield_1,
            field="Activity_Description",
            new_field_name="Activity_Description_",
            new_field_alias="Activity_Description_",
            field_type="TEXT",
            clear_field_alias="DO_NOT_CLEAR",
        )

        if data_year==2022:
            
            alterfield_3 = arcpy.management.AlterField(
                in_table=alterfield_2,
                field="TRMTID_USER",
                new_field_name="TRMTID_USER_2",
                new_field_alias="TRMTID_USER_2",
                field_type="TEXT",
                clear_field_alias="DO_NOT_CLEAR",
            )

        else:
            alterfield_3 = alterfield_2

        addfields_1 = AddFields(Input_Table=alterfield_3, alter_fields=True)     

        print("     step 8/8 transfer attributes")

        if data_year==2022:
            expression = "!HighwayID!"
        else:
            expression = "!Highway_ID!"
        calc_field_1 = arcpy.management.CalculateField(
            in_table=alterfield_3,
            field="PROJECTID_USER",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="AGENCY",
            expression='"CALSTA"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="ORG_ADMIN_p",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="ORG_ADMIN_t",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="ORG_ADMIN_a",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="PROJECT_CONTACT",
            expression='"Division of Maintenance"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PROJECT_EMAIL",
            expression='"andrew.lozano@dot.ca.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="ADMINISTERING_ORG",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="ADMIN_ORG_NAME",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"GENERAL_FUND"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"GENERAL_FUND"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="PRIMARY_FUNDING_ORG",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        if data_year==2022:
            expression="str(!HIghwayID!)+'-'+str(!From_PM!)+'-'+str(!To_PM!)"
        else:
            expression="str(!Highway_ID!)+'-'+str(!From_PM_C!)+'-'+str(!To_PM_C!)"

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="TRMTID_USER",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS"
        )

        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="TREATMENT_AREA",
            expression="ifelse(!UOM!, !Production_Quantity!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(UOM, Q):
                            if UOM == "ACRE" or UOM == 'AC':
                                return Q
                            else:
                                return None""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # NOTE: A unique Activity ID for each record is required for the line enrichment tool to work properly

        if data_year==2022:
            expression="'CALTRANS-'+str(!Work_Order!)+'-'+str(!OBJECTID!)"
        else:
            expression="'CALTRANS-'+str(!Work_Order_Number!)+'-'+str(!OBJECTID!)"
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVID_USER",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        if data_year==2022:
            expression="!DISTRICT_CODE!"
        else:
            expression="!District!"

        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="IMPLEMENTING_ORG",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17,
            field="IMPLEM_ORG_NAME",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="ACTIVITY_UOM",
            expression="ifelse(!UOM!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Unit):
                            if Unit == 'ACRE':
                                return 'AC'
                            else:
                                return Unit""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="ACTIVITY_QUANTITY",
            expression="!Production_Quantity!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="ACTIVITY_STATUS",
            expression='"COMPLETE"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        if data_year==2022:
            expression="None"
        else:
            expression="!WorkBeginDate!"

        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="ACTIVITY_START",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        if data_year==2022:
            expression="!Charge_Date!"
        else:
            expression="!WorkEndDate!"

        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="ACTIVITY_END",
            expression=expression,
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Source",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )


        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="Crosswalk",
            expression="!Activity_Description_!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25,
            field="TRMT_GEOM",
            expression="'LINE'",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        
        print("Saving Standardized Output")
        standardized_1 = arcpy.management.CopyFeatures(
            in_features=calc_field_26,
            out_feature_class=output_lines_standardized,
        )

        keepfields_1 = KeepFields(standardized_1)

        print("Enriching Dataset")
        lines_enriched_1 = enrich_lines(
            line_fc=keepfields_1
        ) 

        print(f"Saving Enriched Output")
        lines_enriched_2 = arcpy.management.CopyFeatures(
            in_features=lines_enriched_1,
            out_feature_class=output_lines_enriched,
        )

        Count4 = arcpy.management.GetCount(output_lines_enriched)
        print("   output_enriched has {} records".format(Count4[0]))

        calc_field_27 = arcpy.management.CalculateField(
            in_table=lines_enriched_2,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression='"STATE"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )


        calc_field_28 = arcpy.management.CalculateField(
            in_table=calc_field_27,
            field="TRMTID_USER",
            expression="!PROJECTID_USER!+'-'+str(!COUNTY!)[:8]+'-'+str(!REGION!)[:3]+'-'+str(!IN_WUI!)[:3]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        AssignDomains(
            in_table=calc_field_28
        )

        if delete_scratch:
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        end1 = datetime.datetime.now()
        elapsed1 = (end1-start1)
        hours, remainder1 = divmod(elapsed1.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print(f"CalTrans script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")


