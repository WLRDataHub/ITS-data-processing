import arcpy
import os


caltran = r"Z:\\home\\arc\\tmp\\its\\CalTrans\\CalTrans_20230711.gdb"
caltran2 = r"Z:\\home\\arc\\tmp\\its\\CalTrans\\Caltrans_Vegetation_Management_Program_20230614.gdb"

destination_workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

src = os.path.join(caltran, "VMP_Activities_Table_2021_Closeout_Date_Added")
des = os.path.join(destination_workspace, "VMP_Activities_Table_2021_Closeout_Date_Added")
arcpy.Copy_management(src, des)

src = os.path.join(caltran, "VMP_Activities_Table_2022_Closeout_Date_Added")
des = os.path.join(destination_workspace, "VMP_Activities_Table_2022_Closeout_Date_Added")
arcpy.Copy_management(src, des)

src = os.path.join(caltran2, "VMP_Highway_Summary_2021")
des = os.path.join(destination_workspace, "b_Originals", "VMP_Highway_Summary_2021")
arcpy.management.CopyFeatures(src, des)

src = os.path.join(caltran2, "VMP_Highway_Summary_2022")
des = os.path.join(destination_workspace, "b_Originals", "VMP_Highway_Summary_2022")
arcpy.management.CopyFeatures(src, des)

