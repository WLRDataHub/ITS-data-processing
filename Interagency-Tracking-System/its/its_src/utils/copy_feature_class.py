
import arcpy
import os

# Set the workspace for the source and destination geodatabases
source_workspace = r"Z:\\home\\arc\\tmp\\Interagency_Tracking_System.gdb"
destination_workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

# Set the name of the feature class you want to copy
# src_BVT = os.path.join(source_workspace, "a_Reference", "Broad_Vegetation_Types")
# des_BVT = os.path.join(destination_workspace, "a_Reference", "Broad_Vegetation_Types")

# src_BVT = os.path.join(source_workspace, "a_Reference", "CALFIRE_Ownership_Update")
# des_BVT = os.path.join(destination_workspace, "a_Reference", "CALFIRE_Ownership_Update")

# src_BVT = os.path.join(source_workspace, "a_Reference", "WUI")
# des_BVT = os.path.join(destination_workspace, "a_Reference", "WUI")

# src_BVT = os.path.join(source_workspace, "a_Reference", "WFRTF_Regions")
# des_BVT = os.path.join(destination_workspace, "a_Reference", "WFRTF_Regions")

src_BVT = os.path.join(source_workspace, "a_Reference", "Own_Veg_Region_WUI")
des_BVT = os.path.join(destination_workspace, "a_Reference", "Own_Veg_Region_WUI")

# src_BVT = os.path.join(source_workspace, "b_Originals", "PFIRS_2018_2022")
# des_BVT = os.path.join(destination_workspace, "b_Originals", "PFIRS_2018_2022")

# source_workspace = r"Z:\\home\\arc\\tmp\\its\\USFS\\Actv_CommonAttribute_PL_Region05.gdb"
# src_BVT = os.path.join(source_workspace, "Actv_CommonAttribute_PL")
# des_BVT = os.path.join(destination_workspace, 'b_Originals','usfs_facts_edw_common_test')


# Use CopyFeatures to copy the feature class
arcpy.management.CopyFeatures(src_BVT, des_BVT)