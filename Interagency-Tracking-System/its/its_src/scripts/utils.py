
"""
# Description:  Utilities used in scripts and notebooks.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
import yaml
from datetime import datetime

# file directory
cur_dir = os.path.dirname(os.path.dirname(os.getcwd()))

def init_gdb():
    """
    Returns local paths to current version and scratch .gdb's and makes them 
    if they don't exist.
    usage: insert this line of code into all other scripts at the top:
    workspace, scratch_workspace = init_gdb()
    """
    # three_up = os.path.abspath(os.path.join(__file__, "../../.."))
    one_up = os.path.abspath(os.path.join(__file__, "../../.."))

    # parse settings file
    with open(os.path.join(one_up, "settings.yml")) as file:
        settings = yaml.full_load(file)

    # make original gdb workspace and scratchWorkspace dynamic
    # original_gdb = os.path.join(three_up,"Interagency Tracking System.gdb")
    workspace = os.path.join(cur_dir, 'Interagency Tracking System.gdb')
    scratch_workspace = os.path.join(cur_dir, 'scratch.gdb')
    
    for w in [workspace, scratch_workspace]:
        if not os.path.exists(w):
            print(f'Creating new FileGDB: {w}')
            arcpy.management.CreateFileGDB(os.path.dirname(w), os.path.basename(w))

    return workspace, scratch_workspace


def unique_rename(scratch_fc: str, input_fc: str):
    """
    Creates unique name and renames a scratch object
    Renamed structure: {input_id}_{scratch_id}_{datestring}

    args:

    scratch_fc: full file path of scratch fc you want to rename ("Pts_enrichment_RCD"))
    input_fc: name of the original input fc for the tool (e.g. "enrich_pts_in")
    """
    scratch_id = os.path.basename(scratch_fc)
    input_id = os.path.basename(
        input_fc
    )  # for now, keep the whole basename including the date string
    date_id = datetime.utcnow().strftime("%Y-%m-%d").replace("-", "")  # like 20221216
    new_name = f"{input_id}_{scratch_id}_{date_id}"
    renamed = arcpy.management.Rename(scratch_fc, new_name)
    return new_name


def delete_scratch_files(gdb, delete_fc, delete_table, delete_ds):
    """
    Deletes all layers in the scratch GDB

    args:

    gdb: full file path to GDB from which you want to delete all files
    delete_table: yes or no (or really anything else)
    delete_fc: yes or no (or really anything else)
    delete_ds: yes or no (or really anything else)

    """
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses()
    tables = arcpy.ListTables()
    ds_list = arcpy.ListDatasets()
    # [print(f"   Deleting Scratch Files from {gdb}")]
    # feature classes
    if delete_fc == "yes":
        for fc in fc_list:
            arcpy.Delete_management(fc)
    else:
        print("did not delete scratch feature classes")
    # tables
    if delete_table == "yes":
        for table in tables:
            arcpy.Delete_management(table)
    else:
        print("did not delete scratch tables")
    # data sets
    if delete_ds == "yes":
        for ds in ds_list:
            arcpy.Delete_management(ds)
    else:
        print("did not delete scratch datasets")


def check_exists(fc_list: list, workspace):
    """
    Checks if all datasets exist, returning a list of non-existent datasets if applicable
    """
    arcpy.env.workspace = workspace
    [print(f"Dataset does not exist: {fc}") for fc in fc_list if not arcpy.Exists(fc)]


def og_file_input(prefix: str, filetype: str, gdb, suffix: str=None):
    """
    Finds input file in the "b_Originals" folder in the workspace
    args:
    gdb: full file path to GDB from which you want to delete all files
    prefix: prefix of desired file
    filetype: type of feature class desired (Point, Line, Polyline, Polygon, etc.)
    """
    arcpy.env.workspace = gdb
    file_list = arcpy.ListFeatureClasses(feature_type=filetype)
    files_w_prefix = []
    for filename in file_list:
        if filename.startswith(prefix):
            if ((not suffix) or filename.endswith(suffix)):
                files_w_prefix.append(filename)
                

    if len(files_w_prefix) == 0:
        raise FileNotFoundError(
            f"File does not match criteria. prefix: {prefix}, file type: {filetype}, workspace: {gdb}"
        )

    files_w_prefix.sort()
    most_recent = files_w_prefix[-1]
    return most_recent

def check_schema_lock(input):
    """
    Checks the schema lock on input files
    args:
    input: full file path to file you want to have schema lock on
    """
    if not arcpy.Exists(input):
        [print(f"Dataset does not exist: {input}")]
    else:
        if arcpy.TestSchemaLock(input):
            [print(f"Available for schema lock: {input}")]
        else:
            raise arcpy.ExecuteError(
                f"Cannot get exclusive schema lock for {input}. Either being edited or in use by another application or service."
            )

#TODO fix and insert runner into scripts
def runner(workspace:str,scratch_workspace:str):
    arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace, 
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'", 
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        transferDomains=False, 
        transferGDBAttributeProperties=False, 
        overwriteOutput = True,
    )

