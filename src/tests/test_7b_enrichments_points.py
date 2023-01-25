#%%
import arcpy
from scripts._7b_enrichments_pts import bEnrichmentsPoints
from sys import argv
from edited.scripts.utils import init_gdb
import os
original_gdb, workspace, scratch_workspace = init_gdb()
enrich_pts_out = os.path.join(workspace,'d_Enriched','testEnrichments_nfpors_fuels_treatments_pts_standardized_20221110')
enrich_pts_in = os.path.join(workspace,'c_Standardized','nfpors_fuels_treatments_pts_standardized_20221110_1')
bEnrichmentsPoints(enrich_pts_out, enrich_pts_in)
# # %%g

#  %%