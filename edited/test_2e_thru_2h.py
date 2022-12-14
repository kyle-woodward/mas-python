#%%
import os
from _1b_add_fields import AddFields2
from _2b_assign_domains import AssignDomains
from _2c_units_domain import Units
from _2d_calculate_activity import Activity
from _2e_calculate_objective import Objective 
from _2f_calculate_category import Category
from _2g_calculate_residue_fate import Residue
from _2h_calculate_year import Year
from utils import init_gdb
import arcpy
original_gdb, workspace, scratch_workspace = init_gdb()
print(workspace)
in_feature_class = os.path.join(workspace, "BLM_20220627")
out_feature_class = os.path.join(scratch_workspace,"BLM_20220627_addFields")
out_feature_class1 = os.path.join(scratch_workspace,"BLM_20220627_assignDomains")
out_feature_class2 = os.path.join(scratch_workspace,"BLM_20220627_unitsDomains")
out_feature_class3 = os.path.join(scratch_workspace,"BLM_20220627_calcAct")
out_feature_class3= os.path.join(scratch_workspace,"BLM_20220627_calcObj")
out_feature_class5 = os.path.join(scratch_workspace,"BLM_20220627_calcCat")
out_feature_class6 = os.path.join(scratch_workspace, "BLM_20220627_calcRes")
out_feature_class7 = os.path.join(scratch_workspace, "BLM_20220627_calcYear")

##works
# addedFields = AddFields2(Input_Table=in_feature_class)[0]
# print(addedFields)
# arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

## ExecuteError: ERROR 000112: Domain does not exist.
# assignedDomains = AssignDomains(out_feature_class)[0]
# print(assignedDomains)
# arcpy.management.CopyFeatures(in_features=assignedDomains, out_feature_class=out_feature_class1, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

##works
# unitDomains = Units(in_table=out_feature_class1)[0]
# print(unitDomains)
# arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class2, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

## ExecuteError: ERROR 000539: Invalid field Fuels_Treatments_Piles_Crosswalk.Activity
# calcAct = Activity(Input_Table=out_feature_class2)[0]
# print(calcAct)
# arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class3, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

## ExecuteError: ERROR 000539: Invalid field Fuels_Treatments_Piles_Crosswalk.Objective
# calcObj = Objective(Input_Table=out_feature_class3)[0]
# print(calcObj)
# arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class4, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

# ## works but doesn't fill the column with anything because it needs previous tools to work...
# calcCat = Category(Input_Table=out_feature_class2)[0]
# print(calcCat)
# arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class5, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

## ExecuteError: ERROR 000539: Invalid field Fuels_Treatments_Piles_Crosswalk.Residue_Fate
# calcRes = Residue(Input_Table=out_feature_class5)[0]
# print(calcRes)
# arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class6, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

##
calcYear = Year(Input_Table=out_feature_class5)[0]
print(calcYear)
arcpy.management.CopyFeatures(in_features=in_feature_class, out_feature_class=out_feature_class7, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)
# # %%

# %%