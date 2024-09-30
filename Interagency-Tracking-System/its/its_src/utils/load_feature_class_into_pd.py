
import os
from scripts.utils import init_gdb
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor

workspace, scratch_workspace = init_gdb()
input_fc = os.path.join(workspace, "b_Originals", "BLM_20240305")
sdf = pd.DataFrame.spatial.from_featureclass(input_fc)
print(sdf)