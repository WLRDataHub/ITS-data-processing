
import arcpy
import os

# Set the workspace for the source and destination geodatabases
workspace = r"Z:\\home\\arc\\tmp\\Interagency_Tracking_System.gdb"
# workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

crosstable = os.path.join(workspace, "Crosswalk")

field_list = [field.name for field in arcpy.ListFields(crosstable)] 
print(f"        Fields: {field_list}")


desc = arcpy.Describe(crosstable)

# Check if it's a spatial table
table_name = "Crosswalk"
if desc.dataType == "Table" or desc.dataType == "TableView":
    print(f"The table {table_name} is a non-spatial table.")
elif desc.dataType == "FeatureClass":
    print(f"The table {table_name} is a spatial table.")
else:
    print(f"The data type of {table_name} is {desc.dataType}.")