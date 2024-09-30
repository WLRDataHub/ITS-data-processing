
import os
import arcpy

# Set the workspace to your geodatabase
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\Interagency_Tracking_System.gdb"
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\scratch.gdb"
arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\USFS\\Actv_CommonAttribute_PL_Region05.gdb"


feature_classes = arcpy.ListFeatureClasses()

# Check if there are any feature classes
if feature_classes:
    for feature_class in feature_classes:
        print("     ", feature_class)

        # field_list = [field.name for field in arcpy.ListFields(feature_class)]                                                                            
        # print(f"        Fields: {field_list}")  


feature_class = os.path.join(arcpy.env.workspace, 'Actv_CommonAttribute_PL')

field_list = [field.name for field in arcpy.ListFields(feature_class)] 
print(f"        Fields: {field_list}")

select_CA = arcpy.management.SelectLayerByAttribute(
      		in_layer_or_view=feature_class,
            	selection_type="NEW_SELECTION",
            	where_clause="STATE_ABBR = 'CA'",
            	invert_where_clause="",
            )

feature_count = arcpy.management.GetCount(select_CA).getOutput(0) 
print(f"==========> Number of features in select_CA: {feature_count}")    

# Get the spatial reference object of the feature class
spatial_ref = arcpy.Describe(select_CA).spatialReference

# Check if the spatial reference is valid
if spatial_ref:
  # Get the EPSG code if available
  if hasattr(spatial_ref, 'wkid'):
    epsg_code = spatial_ref.wkid
    print("EPSG Code:", epsg_code)
  else:
    # Provide alternative output if EPSG code unavailable
    print("Coordinate System Name:", spatial_ref.name)
else:
  print("Error: Feature class has no defined spatial reference.")


# Get a cursor to iterate through features
with arcpy.da.SearchCursor(select_CA, ["SHAPE@WKT"]) as cursor:
  for row in cursor:
    # Get the Well-Known Text (WKT) representation of the geometry
    wkt_geometry = row[0]
    print("Geometry (WKT):", wkt_geometry)


# destination_workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"
# des_BVT = os.path.join(destination_workspace, 'b_Originals','usfs_facts_edw_common_test')
# arcpy.Delete_management(des_BVT)
  