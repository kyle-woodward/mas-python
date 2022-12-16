#%%
import arcpy
from _7b_enrichments_pts import bEnrichmentsPoints
from sys import argv
from utils import init_gdb, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()
enrich_pts_out = os.path.join(workspace,'testEnrichments_CalVTP_standardized_pts_20220923')
enrich_pts_in = os.path.join(workspace,'CalTrans_act_pts_standardized_20220712_2')
bEnrichmentsPoints(enrich_pts_out, enrich_pts_in)
# # %%

#  %%