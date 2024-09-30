import arcpy
import os


# Define the input feature class path
arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

feature_class_names = [
      "BLM_20240305"
]

out_folder = "Z:\\tmp\\shapefiles"  # Replace with your desired output folder

for fc_name in feature_class_names:
    fc = os.path.join(arcpy.env.workspace, 'b_Originals', fc_name)
    arcpy.conversion.FeatureClassToShapefile(fc, f"{out_folder}")
    print(f"Feature class {fc_name} successfully converted to shapefile!")