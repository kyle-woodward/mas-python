#%%
import os
from _1b_add_fields import AddFields2
from _2b_assign_domains import AssignDomains
from utils import init_gdb
import arcpy
original_gdb, workspace, scratch_workspace = init_gdb()
print(workspace)
in_feature_class = os.path.join(workspace,"calmapper_copy_1")
out_feature_class=os.path.join(scratch_workspace,"calmapper_addFields")
out_feature_class2 = os.path.join(scratch_workspace,"calmapper_assignDomains")

addedFields = AddFields2(Input_Table=in_feature_class)[0]
print(addedFields)
arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

assignedDomains = AssignDomains(in_feature_class)
print(assignedDomains)
arcpy.management.CopyFeatures(in_features=assignedDomains, out_feature_class=out_feature_class2, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)
# # %%

# %%
