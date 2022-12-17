#%%
import arcpy
from _7b_enrichments_pts import bEnrichmentsPoints
from sys import argv
from utils import init_gdb, unique_rename, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()
enrich_pts_out = os.path.join(workspace,'testEnrichments_nfpors_fuels_treatments_pts_standardized_20221110')
enrich_pts_in = os.path.join(workspace,'nfpors_fuels_treatments_pts_standardized_20221110')
bEnrichmentsPoints(enrich_pts_out, enrich_pts_in)
unique_rename(scratch_fc = os.path.join(scratch_workspace, "Pts_enrichment_Veg"), input_fc = enrich_pts_in)
unique_rename(scratch_fc = os.path.join(scratch_workspace, "Pts_enrichment_copy"), input_fc = enrich_pts_in)
unique_rename(scratch_fc = os.path.join(scratch_workspace, "Pts_enrichment_Own"), input_fc = enrich_pts_in)
unique_rename(scratch_fc = os.path.join(scratch_workspace, "Pts_enrichment_RCD"), input_fc = enrich_pts_in)
# # %%g

#  %%