
import arcpy
import os

source_workspace = r"Z:\\home\\arc\\tmp\\its\\Interagency Tracking System.gdb"

src = os.path.join(source_workspace, "b_Originals", "NFPORSCurrentFYTreatmentsBIA_20240309")
# arcpy.Delete_management(src)

src = os.path.join(source_workspace, "b_Originals", "NFPORSCurrentFYTreatmentsFWS_20240309")
# arcpy.Delete_management(src)

src = os.path.join(source_workspace, "b_Originals", "nps_flat_fuels_20240309")
# arcpy.Delete_management(src)


src = os.path.join(source_workspace, "c_Enriched", "BLM_enriched_20240309")
# arcpy.Delete_management(src)

src = os.path.join(source_workspace, "c_Enriched", "nps_flat_fuels_enriched_20240309")
# arcpy.Delete_management(src)

src = os.path.join(source_workspace, "c_Enriched", "nfpors_fuels_treatments_polys_enriched_20240309")
# arcpy.Delete_management(src)

src = os.path.join(source_workspace, "c_Enriched", "nfpors_fuels_treatments_pts_enriched_20240309")
# arcpy.Delete_management(src)

# src = os.path.join(source_workspace, "c_Enriched", "usfs_edw_facts_common_attributes_enriched_20240311")
# arcpy.Delete_management(src) 

src = os.path.join(source_workspace, "c_Enriched", "CNRA_enriched_ln_20240312")
arcpy.Delete_management(src) 

src = os.path.join(source_workspace, "c_Enriched", "CNRA_enriched_poly_20240312")
arcpy.Delete_management(src) 





