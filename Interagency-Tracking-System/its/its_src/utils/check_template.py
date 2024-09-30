
import arcpy
import os

# Set the workspace for the source and destination geodatabases
# workspace = r"Z:\\home\\arc\\tmp\\Interagency_Tracking_System.gdb"
workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

crosstable = os.path.join(workspace, "a_Reference", "WFR_TF_Template")
field_list = [field for field in arcpy.ListFields(crosstable)] 

for field in field_list:
    field_type = field.type
    if field.type == 'String':
        field_type = 'VARCHAR(100)'
    elif field.type == 'Integer' or field.type == 'SmallInteger':
        field_type = 'int' 
    elif field_type == 'Double':
        field_type = 'double precision'
    #print(f"{field.name} {field_type},")
    print(f"{field.name},")


