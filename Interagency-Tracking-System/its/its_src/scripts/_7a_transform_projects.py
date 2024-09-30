"""
# Description: This is the start of the dataset transformation scripts.
#              This script will transform the flat appended files into the 
#              relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from .utils import init_gdb

### geopandas dissolve alternative
import geopandas as gpd
from shapely import MultiPolygon, Polygon


workspace, scratch_workspace = init_gdb()

def TransformProjects(
    In_Poly,
    In_Pts,
    In_Lns,
    Out_Poly,
):
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
        # scratch outputs
        temp_poly = os.path.join(scratch_workspace, "temp_poly")
        temp_pts = os.path.join(scratch_workspace, "temp_pts")
        temp_lns = os.path.join(scratch_workspace, "temp_lns")
        pts_buffered = os.path.join(scratch_workspace, "pts_buffered")
        lns_buffered = os.path.join(scratch_workspace, "lns_buffered")

        ## START TOOL CHAIN
        # Buffer points and lines using activity quantity and line length
        copy_1 = arcpy.CopyFeatures_management(In_Pts, temp_pts)

        print("Start buffer selection")

        select_copy_1 = arcpy.SelectLayerByAttribute_management(
            copy_1,
            "NEW_SELECTION", 
            "ACTIVITY_QUANTITY IS NOT NULL AND ACTIVITY_QUANTITY <> 0" 
        )
        

        calc_buffer_1 = arcpy.management.CalculateField(
            select_copy_1,
            "BufferMeters",
            "math.sqrt((!ACTIVITY_QUANTITY!*4046.86)/3.14159)",
        )

        print("Start buffering 1")

        buffer_pts_1 = arcpy.analysis.PairwiseBuffer(
            in_features=calc_buffer_1,
            out_feature_class=pts_buffered,
            buffer_distance_or_field="BufferMeters",
            dissolve_option="NONE"
        )

        copy_2 = arcpy.CopyFeatures_management(In_Lns, temp_lns)

        print("Start post selection")

        select_copy_2 = arcpy.SelectLayerByAttribute_management(
            copy_2,
            "NEW_SELECTION", 
            "Shape_Length IS NOT NULL AND Shape_Length <> 0" 
        )
        
        calc_buffer_2 = arcpy.management.CalculateField(
            select_copy_2,
            "BufferMeters",
            "(!ACTIVITY_QUANTITY!*4046.86)/!Shape_Length!/2",
        )

        ### pre load select to before buffer to avoid null causing error 99999 in Calculate Field
        #select_1 = arcpy.SelectLayerByAttribute_management(
        #    calc_buffer_2,
        #    "NEW_SELECTION", 
        #    "BufferMeters IS NOT NULL" 
        #)

        print("Start buffering 2")

        buffer_lns_1 = arcpy.analysis.PairwiseBuffer(
            in_features=calc_buffer_2,
            out_feature_class=lns_buffered,
            buffer_distance_or_field="BufferMeters",
            dissolve_option="NONE"
        )

        copy_3 = arcpy.CopyFeatures_management(In_Poly, temp_poly)

        add_field_2 = arcpy.AddField_management(
            copy_3, 
            "BufferMeters",
            field_type="TEXT"
        )

        # Append point and line buffers to polygons
        append_1 = arcpy.Append_management([
            buffer_pts_1, 
            buffer_lns_1
            ],
            add_field_2,
            schema_type="NO_TEST",
        )

        print("Start dissolve by features")

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
                "BatchID_p",
                "Val_Status_p",
                "Val_Msg_p",
                "Val_RunDate_p",
                "Review_Status_p",
                "Review_Msg_p",
                "Review_RunDate_p",
                "Dataload_Status_p",
                "Dataload_Msg_p",
            ]
        """
        dissolve_1 = arcpy.management.Dissolve(
            in_features=append_1,
            out_feature_class=Out_Poly,
            dissolve_field=dissolve_field,
        )
        """
        print("Start loading temp_poly to gdf")
        pre_dissolve_gdf = gpd.read_file(
            os.path.dirname(temp_poly), 
            driver="OpenFileGDB", 
            layer=os.path.basename(temp_poly))
        print("Start dissolving by UID")
        pre_dissolve_gdf["TEMP_UID"] = pre_dissolve_gdf.set_index(dissolve_field).index.factorize()[0]
        dissolve_out = pre_dissolve_gdf.dissolve(by="TEMP_UID").reset_index(drop=True)
        
        print("Start saving to out_poly")
        dissolve_out["geometry"] = [MultiPolygon([feature]) if isinstance(feature, Polygon) \
                                    else feature for feature in dissolve_out["geometry"]]
        
        dissolve_out[dissolve_field] = dissolve_out[dissolve_field].astype(str)
        dissolve_out.to_file(
            scratch_workspace, 
            driver="OpenFileGDB", 
            layer='temp_gdf_Out_Poly_7a'
        )

        arcpy.CopyFeatures_management(os.path.join(scratch_workspace, 'temp_gdf_Out_Poly_7a'), Out_Poly)



        print("Dissolve complete")
        GUID_1 = arcpy.management.AddGlobalIDs(
            in_datasets=[Out_Poly]
        )

    return Out_Poly 