import arcpy

# Set the workspace to your geodatabase
arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\Interagency_Tracking_System.gdb"
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"
# arcpy.env.workspace = r"Z:\\home\\arc\\tmp\\its\\scratch.gdb"




# Specify the name of the feature class you want to check
# feature_class_name = "Broad_Vegetation_Types"
# feature_class_name = "California"
feature_class_name = "Crosswalk"

# Full path to the feature class
feature_class_path = f"{arcpy.env.workspace}\\{feature_class_name}"


#######################################################
# Check if the feature class exists
if arcpy.Exists(feature_class_path):
    print(f"The feature class {feature_class_name} exists in the geodatabase.")

    field_list = [field.name for field in arcpy.ListFields(feature_class_path)]                                                                     
    print(f"Fields: {field_list}")        

    # with arcpy.da.SearchCursor(feature_class_path, ['OBJECTID', 'USFS_Activity_Code', 'Original_Activity', 'Sources', 'Activity', 'Activity_Descr', 'Residue_Fate', 'Objective', 'Counts_to_MAS']) as cursor:
    #    for row in cursor:
    #        print('~~~~~~>', row)


########################################################
# Use ListDatasets to get a list of all feature datasets
feature_datasets = arcpy.ListDatasets()

# Check if there are any feature datasets
if feature_datasets:
    print("List of feature datasets:")
    for dataset in feature_datasets:
        print("="*70)
        print(f"List of feature classes in the feature dataset {dataset}:")
        print("="*70)
        print(dataset)

	# Use ListFeatureClasses to get a list of all feature classes in the feature dataset
        feature_classes = arcpy.ListFeatureClasses("*", "All", dataset)

        # Check if there are any feature classes
        if feature_classes:
            for feature_class in feature_classes:
                print("     ", feature_class)

                field_list = [field.name for field in arcpy.ListFields(feature_class)]                                                                            
                # print(f"        Fields: {field_list}")    		

                # Check the number of features
                feature_count = arcpy.management.GetCount(feature_class).getOutput(0)
                print(f"          Number of features: {feature_count}")

        else:
            print(f"    No feature classes found in the feature dataset {dataset}.")



###########################################################
# Use ListDomains to get a list of all domains in the geodatabase
domains = arcpy.da.ListDomains()

# Check if there are any domains
if domains:
    print("\nList of domains:")
    for domain in domains:
        print(f"    Name: {domain.name}, Type: {domain.domainType}, Description: {domain.description}")
else:
    print("    No domains found in the geodatabase.")

