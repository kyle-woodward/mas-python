#%%
import os
from _1b_add_fields import AddFields2
from _2b_assign_domains_big_rework import AssignDomains
from utils import init_gdb
import arcpy
original_gdb, workspace, scratch_workspace = init_gdb()
print(workspace)
in_feature_class = os.path.join(workspace,"WFR_TF_Template")
out_feature_class=os.path.join(scratch_workspace,"WFR_TF_Template_AddFields")

addedFields = AddFields2(Input_Table=in_feature_class)[0]
arcpy.management.CopyFeatures(in_features=addedFields, out_feature_class=out_feature_class, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

# assignedDomains = AssignDomains(addedFields)

# arcpy.management.CopyFeatures(in_features=assignedDomains, out_feature_class=os.path.join(workspace,"CalVTP_20220923_AddFields_AssignDomains"), config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)
# # %%
