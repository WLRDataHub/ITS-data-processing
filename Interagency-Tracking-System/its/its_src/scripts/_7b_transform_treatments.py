"""
# Description: This is the start of the dataset transformation scripts.
#              This script will transform the flat appended files into the
#              relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from .utils import init_gdb

### geopandas dissolve alternative
import geopandas as gpd
import os
from shapely import MultiPolygon, MultiPoint, MultiLineString, Polygon, Point, LineString

workspace, scratch_workspace = init_gdb()

def TransformTreatments(
        In_Poly,
        In_Pts,
        In_Lns,
        Out_poly,
        Out_pts,
        Out_lns,
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
        # drop all else
        dissolve_field=[
                "TRMTID_USER",
                "PROJECTID_USER",
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
                "TREATMENT_START",
                "TREATMENT_END",
                "RETREATMENT_DATE_EST",
                "TREATMENT_NAME",
                "BatchID",
                "Val_Status_t",
                "Val_Msg_t",
                "Val_RunDate_t",
                "Review_Status_t",
                "Review_Msg_t",
                "Review_RunDate_t",
                "Dataload_Status_t",
                "Dataload_Msg_t",
                # "created_user",
                # "created_date",
                # "last_edited_user",
                # "last_edited_date"
            ]
        
        ## Start Poly Tool Chain

        """
        dissolve_1 = arcpy.management.Dissolve(
            in_features=In_Poly,
            out_feature_class=Out_poly,
            dissolve_field=dissolve_field,
        )
        """

        print("Start loading In_Poly to gdf")

        pre_dissolve_gdf = gpd.read_file(
            workspace, 
            driver="OpenFileGDB", 
            layer=os.path.basename(In_Poly)
        )
        print("Start dissolving by UID")
        pre_dissolve_gdf["TEMP_UID"] = pre_dissolve_gdf.set_index(dissolve_field).index.factorize()[0]
        dissolve_out = pre_dissolve_gdf.dissolve(by="TEMP_UID").reset_index(drop=True)
        
        print("Start saving to out_poly")

        dissolve_out["geometry"] = [MultiPolygon([feature]) if isinstance(feature, Polygon) \
                                    else feature for feature in dissolve_out["geometry"]]
        # cast dtype to str for all Nan fields for future domain assignment
        dissolve_out[dissolve_field] = dissolve_out[dissolve_field].astype(str)
        dissolve_out.to_file(
            scratch_workspace, 
            driver="OpenFileGDB", 
            layer='temp_gdf_Out_poly'
        )

        arcpy.CopyFeatures_management(os.path.join(scratch_workspace, 'temp_gdf_Out_poly'), Out_poly)





        addfield_1 = arcpy.management.AddField(
            in_table=Out_poly,
            field_name="TREATMENT_AREA",
            field_type="DOUBLE",
            field_alias="TREATMENT AREA (GIS ACRES)",
        )

        calcgeom_1 = arcpy.CalculateGeometryAttributes_management(
            in_features=addfield_1,
            geometry_property=[["TREATMENT_AREA","AREA"]],
            area_unit="ACRES_US"
            )

        GUID_1 = arcpy.management.AddGlobalIDs(
            in_datasets=[calcgeom_1]
        )


        ## Start Point Tool Chain

        """
        dissolve_2 = arcpy.management.Dissolve(
            in_features=In_Pts,
            out_feature_class=Out_pts,
            dissolve_field=dissolve_field,
        )
        """

        print("Start loading In_Pts to gdf")
        pre_dissolve_gdf = gpd.read_file(
            workspace, 
            driver="OpenFileGDB", 
            layer=os.path.basename(In_Pts)
        )
        print("Start dissolving by UID")
        pre_dissolve_gdf["TEMP_UID"] = pre_dissolve_gdf.set_index(dissolve_field).index.factorize()[0]
        dissolve_out = pre_dissolve_gdf.dissolve(by="TEMP_UID").reset_index(drop=True)
        
        print("Start saving to Out_pts")
        dissolve_out["geometry"] = [MultiPoint([feature]) if isinstance(feature, Point) \
                                    else feature for feature in dissolve_out["geometry"]]
        # cast dtype to str for all Nan fields for future domain assignment
        dissolve_out[dissolve_field] = dissolve_out[dissolve_field].astype(str)
        dissolve_out.to_file(
            scratch_workspace, 
            driver="OpenFileGDB", 
            layer='temp_gdf_Out_pts'
        )

        arcpy.CopyFeatures_management(os.path.join(scratch_workspace, 'temp_gdf_Out_pts'), Out_pts)



        addfield_3 = arcpy.management.AddField(
            in_table=Out_pts,
            field_name="TREATMENT_AREA",
            field_type="DOUBLE",
            field_alias="TREATMENT AREA (GIS ACRES)",
        )

        GUID_2 = arcpy.management.AddGlobalIDs(
            in_datasets=[addfield_3]
        )

        ## Start Line Tool Chain

        """
        dissolve_3 = arcpy.management.Dissolve(
            in_features=In_Lns,
            out_feature_class=Out_lns,
            dissolve_field=dissolve_field,
        )
        """

        print("Start loading In_Lns to gdf")
        pre_dissolve_gdf = gpd.read_file(
            workspace, 
            driver="OpenFileGDB", 
            layer=os.path.basename(In_Lns)
        )
        print("Start dissolving by UID")
        pre_dissolve_gdf["TEMP_UID"] = pre_dissolve_gdf.set_index(dissolve_field).index.factorize()[0]
        dissolve_out = pre_dissolve_gdf.dissolve(by="TEMP_UID").reset_index(drop=True)
        
        print("Start saving to Out_lns")
        dissolve_out["geometry"] = [MultiLineString([feature]) if isinstance(feature, LineString) \
                                    else feature for feature in dissolve_out["geometry"]]
        # cast dtype to str for all Nan fields for future domain assignment
        dissolve_out[dissolve_field] = dissolve_out[dissolve_field].astype(str)
        dissolve_out.to_file(
            scratch_workspace, 
            driver="OpenFileGDB", 
            layer='temp_gdf_Out_lns'
        )

        arcpy.CopyFeatures_management(os.path.join(scratch_workspace, 'temp_gdf_Out_lns'), Out_lns)


        addfield_5 = arcpy.management.AddField(
            in_table=Out_lns,
            field_name="TREATMENT_AREA",
            field_type="DOUBLE",
            field_alias="TREATMENT AREA (GIS ACRES)",
        )

        GUID_3 = arcpy.management.AddGlobalIDs(
            in_datasets=[addfield_5]
        )

        return Out_poly, Out_pts, Out_lns
