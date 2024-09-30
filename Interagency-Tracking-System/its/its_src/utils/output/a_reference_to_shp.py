import arcpy
import os


# Define the input feature class path
arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

feature_class_names = [
    "WFR_TF_Template",
    "California",
    "Counties",
    "Broad_Vegetation_Types",
    "CALFIRE_Ownership_Update",
    "WUI",
    "WFRTF_Regions",
    "Own_Veg_Region_WUI"]

out_folder = "Z:\\tmp\\shapefiles"  # Replace with your desired output folder

for fc_name in feature_class_names:
    fc = os.path.join(arcpy.env.workspace, 'a_Reference', fc_name)
    arcpy.conversion.FeatureClassToShapefile(fc, f"{out_folder}")
    print(f"Feature class {fc_name} successfully converted to shapefile!")