import arcpy

# Set the workspace to your geodatabase
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\CNRA\\CNRA_TRMTTRACKER_20230821.gdb"
arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\CalTrans\\CalTrans_20230711.gdb"
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\CalTrans\\Caltrans_Vegetation_Management_Program_20230614.gdb"

# Get a list of all feature classes
feature_classes = arcpy.ListFeatureClasses()

# Print each feature class name
for fc in feature_classes:
  print(fc)


# Get a list of all tables
tables = arcpy.ListTables()

# Print each table name
for table in tables:
  print(table)

  field_list = [field.name for field in arcpy.ListFields(table)]                                                                            
  field_list.sort()
  # print(f"        Fields: {field_list}")    		

  # with arcpy.da.SearchCursor(table, ['TREATMENTID_', 'TREATMENTID_LN', 'TREATMENTID_PT', 'TRMT_GEOM']) as cursor:                                                     
  #  for row in cursor:                                                                                                                               
  #    print('-'*70, row[3])
  #    if row[3] == 'POINT':
  #      print(f'TREATMENTID_PT: {row[2]}')                 
  #    if row[3] == 'POLYGON':
  #      print(f'TREATMENTID_: {row[0]}')         
  #    if row[3] == 'LINE':
  #      print(f'TREATMENTID_PT: {row[1]}')                         
      