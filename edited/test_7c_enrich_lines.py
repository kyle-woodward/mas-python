#%%
import arcpy
from _7c_enrichments_lines import cEnrichmentsLines
from sys import argv
from utils import init_gdb, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()
line_fc = os.path.join(workspace,'c_Standardized','CM_CNRAExtract_TrtLn_standardized_20221110') # CM_CNRAExtract_TrtLn_standardized_20221110, CalTrans_act_ln_standardized_20220712,
cEnrichmentsLines(line_fc)
# # %%g