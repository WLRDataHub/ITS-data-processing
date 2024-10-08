"""
# Description: Converts the U.S. Department of Interior, Bureau 
#              of Land Management's fuels treatments dataset 
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
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def Model_BLM(
    output_enriched, 
    input_fc, 
    startyear, 
    endyear, 
    California, 
    delete_scratch=True
):
    # Model Environment settings
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

        # Reference
        WFR_TF_Template = os.path.join(workspace,'a_Reference','WFR_TF_Template')

        # define intermediary objects in scratch
        BLM_clip = os.path.join(scratch_workspace, "BLM_clip")
        BLM_copy = os.path.join(scratch_workspace, "BLM_copy")
        output_standardized = os.path.join(scratch_workspace, "BLM_standardized")

        ### BEGIN TOOL CHAIN
        print("Performing Standardization...")
        print("   step 1/15 Clip Features...")
        arcpy.analysis.Clip(
            in_features=input_fc, 
            clip_features=California, 
            out_feature_class=BLM_clip
        )

        print("   step 2/15 Repairing Geometry...")
        repair_geom = arcpy.management.RepairGeometry(BLM_clip)

        arcpy.management.CopyFeatures(
            in_features=repair_geom, 
            out_feature_class=BLM_copy
        )

        field_list = [field.name for field in arcpy.ListFields(BLM_copy)]
        print(f"Fields in {BLM_copy}: {field_list}")

        print("   step 3/15 Adding Fields...")
        standardized_1 = AddFields(Input_Table=BLM_copy)
        # print(standardized_1)

        standardized_1 = BLM_copy
        field_list = [field.name for field in arcpy.ListFields(standardized_1)]
        # print(f"Fields in {standardized_1}: {field_list}")

        print("   step 4/15 Transfering Attributes...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=standardized_1,
            field="PROJECTID_USER",
            expression="!UNIQUE_ID!",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1, 
            field="AGENCY", 
            expression='"DOI"'
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2, 
            field="ORG_ADMIN_p", 
            expression="'BLM'"
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3, 
            field="ORG_ADMIN_t", 
            expression="'BLM'"
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4, 
            field="ORG_ADMIN_a", 
            expression="'BLM'"
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5, 
            field="PROJECT_CONTACT", 
            expression="None"
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6, 
            field="PROJECT_EMAIL", 
            expression="None"
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_7, 
            field="ADMINISTERING_ORG", 
            expression="'BLM'"
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7, 
            field="PROJECT_NAME", 
            expression="!TREATMENT_NAME!"
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"FEDERAL"',
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="PRIMARY_FUNDING_ORG",
            expression='"NPS"',
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10, 
            field="IMPLEMENTING_ORG", 
            expression="'BLM'"
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="ACTIVITY_NAME",
            expression="!TREATMENT_NAME!",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12, 
            field="BVT_USERD", 
            expression='"NO"'
        )

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="ACTIVITY_START",
            expression="!TRTMNT_START_DT!",
            #expression="datetime.datetime.strptime(!TRTMNT_START_DT!, '%Y/%m/%d %H:%M:%S.%f')",
            expression_type="PYTHON3" 
        )


        print("   step 5/15 Calculating End Date...")
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="ACTIVITY_END",
            expression="!TRTMNT_END_DT!",
            #expression="datetime.datetime.strptime(!TRTMNT_END_DT!, '%Y/%m/%d %H:%M:%S.%f')",
            expression_type="PYTHON3"
        ) 

        ########################################################################
        # fields = arcpy.ListFields(calc_field_14)
        # for field in fields:
        #    if field.name == "ACTIVITY_END":
        #        print(f"Type of ACTIVITY_END: {field.type}")
        #    elif field.name == "TRTMNT_END":
        #        print(f"Type of TRTMNT_END: {field.type}")
        #
        # with arcpy.da.SearchCursor(calc_field_14, ['ACTIVITY_END', 'TRTMNT_END']) as cursor:
        #    for row in cursor:
        #        print('ACTIVITY_END, TRTMNT_END =====>', row[0], row[1])
        ########################################################################

        print("   step 6/15 Calculating Status...")
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVITY_STATUS",
            expression="'COMPLETE'",
        )

        print("   step 7/15 Activity Quantity...")
        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="ACTIVITY_QUANTITY",
            expression="ifelse(!BLM_ACRES!, !GIS_ACRES!)",
            code_block="""def ifelse(BLM, GIS):
                            if BLM == 0 or BLM is None:
                                return GIS
                            else:
                                return BLM""",
            field_type="DOUBLE",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17, 
            field="ACTIVITY_UOM", 
            expression='"AC"'
        )

        print("   step 8/15 Enter Field Values...")
        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18, 
            field="ADMIN_ORG_NAME", 
            expression='"BLM"'
        )
        
        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19, 
            field="IMPLEM_ORG_NAME", 
            expression="'BLM'"
        )
        
        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"FEDERAL"',
        )
        
        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"BLM"',
        )
        
        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22, 
            field="Source", 
            expression="'BLM'"
        )
        
        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Year",
            expression='Year($feature.ACTIVITY_END)',               
            expression_type="Arcade"
        )

        #calc_field_24 = arcpy.management.CalculateField(
        #    in_table=calc_field_23,
        #    field="Year",
        #    expression="datetime.datetime(!ACTIVITY_END!).strftime('%Y')",
        #    #expression="arcpy.time.FormatDate(!ACTIVITY_END!, 'yyyy')",               
        #    expression_type="PYTHON3"
        #)
        #calc_field_24 = arcpy.management.ConvertTimeField(
        #    in_table=calc_field_23, 
        #    input_time_field="ACTIVITY_END",
        #    output_time_field='Year',
        #    output_time_format='yyyy'
        #)
        

        ##############################################################
        # field_list = [field.name for field in arcpy.ListFields(calc_field_24)]                                                                            
        # print(f"        Fields: {field_list}")    		
	#
        # with arcpy.da.SearchCursor(calc_field_24, ['ACTIVITY_END', 'Year']) as cursor:
        #    for row in cursor:
        #        print('~~~~~~>', row[0], row[1])
        ########################################################################
        
        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="TRTMNT_NM",
            expression="!TRTMNT_NM!",
        )
        
        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25,
            field="TRTMNT_COMMENTS",
            expression="!TRTMNT_COMMENTS!",
        )

        print("   step 9/15 Adding original activity description to Crosswalk Field...")
        calc_field_27 = arcpy.management.CalculateField(
            in_table=calc_field_26,
            field="Crosswalk",
            # expression="ifelse(!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!Crosswalk!)",
            expression="ifelse(!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!Crosswalk!)",
            code_block="""def ifelse(type, sub, cross): 
                            if (type == 'BIOLOGICAL' or type == 1) and sub == 'CLASSICAL':
                                return 'PRESCRB_HERBIVORY'
                            if (type == 'BIOLOGICAL' or type == 1) and sub == 'NON-CLASSICAL':
                                return 'PRESCRB_HERBIVORY'
                            if sub == 'FERTILIZER':
                                return 'NOT_DEFINED'
                            if sub == 'PESTICIDE':
                                return 'PEST_CNTRL'
                            if type == 'PRESCRIBED FIRE' or type == 3:
                                return 'BROADCAST_BURN'
                            if (type == 'PHYSICAL' or type == 4) and sub == 'OTHER':
                                return 'THIN_MECH'
                            if (type == 'PHYSICAL' or type == 4) and sub == 'REMOVE':
                                return 'THIN_MECH'
                            if (type == 'PHYSICAL' or type == 4) and sub == 'PLANT':
                                return 'HABITAT_REVEG'
                            else:
                                return cross""",
        )
        
        calc_field_28 = arcpy.management.CalculateField(
            in_table=calc_field_27,
            field="Crosswalk",
            # expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            code_block="""def ifelse(Nm, type, sub, com, cross):
                            if Nm is None:
                                return cross
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'pile' in Nm:
                                return 'PILE_BURN'
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'hp' in Nm:
                                return 'PILE_BURN'
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'hand' in Nm:
                                return 'PILE_BURN'
                            elif (type == 'PHYSICAL' or type == 4) and 'road' in Nm:
                                return 'ROAD_CLEAR'
                            elif (type == 'PHYSICAL' or type == 4) and 'chip' in Nm:
                                return 'CHIPPING'
                            elif (type == 'PHYSICAL' or type == 4) and 'hand' in Nm:
                                return 'THIN_MAN'
                            elif (type == 'PHYSICAL' or type == 4) and 'masticat' in Nm:
                                return 'MASTICATION'
                            else:
                                return cross""",
        )
        
        calc_field_29 = arcpy.management.CalculateField(
            in_table=calc_field_28,
            field="Crosswalk",
            # expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            code_block="""def ifelse(Nm, type, sub, com, cross):
                            if com is None:
                                return cross
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'pile' in com:
                                return 'PILE_BURN'
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'broadcast' in com:
                                return 'BROADCAST_BURN'
                            elif (type == 'PHYSICAL' or type == 4) and 'hand' in com:
                                return 'THIN_MAN'
                            elif (type == 'PHYSICAL' or type == 4) and 'chip' in com:
                                return 'CHIPPING'
                            elif (type == 'PHYSICAL' or type == 4) and 'lop' in com:
                                return 'LOP_AND_SCAT'
                            elif (type == 'PHYSICAL' or type == 4) and 'masticat' in com:
                                return 'MASTICATION'
                            elif (type == 'PHYSICAL' or type == 4) and 'mow' in com:
                                return 'MOWING'
                            elif (type == 'PHYSICAL' or type == 4) and 'biomass' in com:
                                return 'BIOMASS_REMOVAL'
                            elif (type == 'PHYSICAL' or type == 4) and 'machine pile' in com:
                                return 'PILING'
                            else:
                                return cross""",
        )

        ########################################################################
        # feature_count = arcpy.management.GetCount(calc_field_29).getOutput(0) 
        # print(f"==========> Number of features in calc_field_29: {feature_count}")    
        # print(f"==========> startyear: {startyear}, endyear: {endyear}")
        # 
        # field_list = [field.name for field in arcpy.ListFields(calc_field_29)]                                                                            
        # print(f"        Fields: {field_list}")    		
	#
        # with arcpy.da.SearchCursor(calc_field_29, ['Year']) as cursor:
        #    for row in cursor:
        #        print('------>', row[0])
        ##########################################################################
        
        print("   step 10/15 select by years")
        select_1 = arcpy.analysis.Select(
            in_features=calc_field_29,
            out_feature_class=output_standardized,
            where_clause="Year >= %d And Year <= %d" % (startyear, endyear),
        )

        new_1 = arcpy.management.CreateFeatureclass(
            out_path=scratch_workspace, 
            out_name="BLM_standardized2", 
            geometry_type="POLYGON", 
            template=[WFR_TF_Template], 
            spatial_reference=3310, #"NAD 1983 California (Teale) Albers (Meters)", 
        )

        ########################################################################
        # feature_count = arcpy.management.GetCount(select_1).getOutput(0) 
        # print(f"==========> Number of features in select_1: {feature_count}")    
        ########################################################################

        # Appending to the template eliminates the GlobalID field
        print("   step 10/15 append to template")
        polygons_append = arcpy.management.Append(
            inputs=[
                    select_1
                    ], 
            target=new_1, 
            schema_type="NO_TEST", 
            field_mapping="", 
        )

        print("Saving Standardized Output")        
        Count1 = arcpy.management.GetCount(polygons_append)
        print("     output_standardized has {} records".format(Count1[0]))

        print("   step 10/15 Calculate Treatment Geometry...")
        calc_field_30 = arcpy.management.CalculateField(
            in_table=polygons_append, 
            field="TRMT_GEOM", 
            expression="'POLYGON'"
        )


        ################################################################
        # print('---- calc_field_30')
        # field_list = [field.name for field in arcpy.ListFields(calc_field_30)]                                                                                 
        # print(f"        Fields: {field_list}")   

        keepfields_1 = KeepFields(Keep_table=calc_field_30)

        print('---- count of rows')
        print(arcpy.management.GetCount(keepfields_1))

        ################################################################
        print('---- keepfields_1')
        field_list = [field.name for field in arcpy.ListFields(keepfields_1)] 
        print(f"        Fields: {field_list}")   

        print("   step 11/15 Enriching Dataset...")
        enrich_polygons(
            enrich_in=keepfields_1, 
            enrich_out=output_enriched
            )
        print(f"Saving Enriched Output")

        Count2 = arcpy.management.GetCount(output_enriched)
        print("output_enriched has {} records".format(Count2[0]))

        print("   step 12/15 Calculate Treatment ID...")
        calc_field_31 = arcpy.management.CalculateField(
            in_table=output_enriched,
            field="TRMTID_USER",
            expression="str(!PROJECTID_USER!)[:7]+'-'+str(!COUNTY!)[:3]+'-'+str(!PRIMARY_OWNERSHIP_GROUP!)[:4]+'-'+str(!IN_WUI![:3])+'-'+str(!PRIMARY_OBJECTIVE!)[:8]"
        )

        print("   step 13/15 Assign Domains...")
        AssignDomains(in_table=calc_field_31)

        if delete_scratch:
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        end2 = datetime.datetime.now()
        elapsed2 = (end2-start1)
        hours, remainder4 = divmod(elapsed2.total_seconds(), 3600)
        minutes, remainder5 = divmod(remainder4, 60)
        seconds, remainder6 = divmod(remainder5, 1)
        print(f"BLM script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

