
import arcpy
import os

# Set the workspace for the source and destination geodatabases
source_workspace = r"Z:\\home\\arc\\tmp\\Interagency_Tracking_System.gdb"
destination_workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

src = os.path.join(source_workspace, "Crosswalk")
des = os.path.join(destination_workspace, "Crosswalk")

arcpy.Delete_management(des)
arcpy.Copy_management(src, des)

# arcpy.management.DeleteRows(des)

