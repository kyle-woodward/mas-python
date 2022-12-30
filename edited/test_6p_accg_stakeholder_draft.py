#%%
import arcpy
from _6p_accg_stakeholder_draft import pACCGStakeholderDraft
from sys import argv
from utils import init_gdb, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()
accg_fc = os.path.join(workspace, "accg_stkhldr_prjt_2021") 
pACCGStakeholderDraft(input_fc = accg_fc)
# # %%g
# %%
