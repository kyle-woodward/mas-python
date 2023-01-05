#%%
import arcpy
from sys import argv
from utils import init_gdb, delete_scratch_files
import os
original_gdb, workspace, scratch_workspace = init_gdb()

Pts_enrichment_Veg = os.path.join(scratch_workspace, "Pts_enrichment_Veg")
Pts_enrichment_copy = os.path.join(scratch_workspace, "Pts_enrichment_copy")
Pts_enrichment_Own = os.path.join(scratch_workspace, "Pts_enrichment_Own")
Pts_enrichment_RCD = os.path.join(scratch_workspace, "Pts_enrichment_RCD")

delete_scratch_files(gdb = os.path.join(scratch_workspace))

# arcpy.env.workspace = scratch_workspace
# fc_list = arcpy.ListFeatureClasses()
# tables = arcpy.ListTables()
# ds_list = arcpy.ListDatasets()

# #feature classes
# for fc in fc_list:
#     arcpy.Delete_management(fc)

# #tables
# for table in tables:
#     arcpy.Delete_management(table)

# #data sets
# for ds in ds_list:
#     arcpy.Delete_management(ds)
# # %%g
# %%
