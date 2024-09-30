import arcpy

# Set the workspace to your geodatabase
arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

# Get a list of all feature classes
feature_classes = arcpy.ListFeatureClasses()

# Print each feature class name
for fc in feature_classes:
  if fc == 'Meatballs':
    arcpy.Delete_management(fc)
  print(fc)


# Get a list of all tables
tables = arcpy.ListTables()

# Print each table name
for table in tables:
  print(table)

  field_list = [field.name for field in arcpy.ListFields(table)]                                                                            
  field_list.sort()
  # print(f"        Fields: {field_list}")    		

      