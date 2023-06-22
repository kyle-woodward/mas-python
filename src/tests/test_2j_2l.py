#%%
# import arcpy
from scripts._2l_Crosswalk import Crosswalk
from scripts._2j_Standardize_Domains import StandardizeDomains
# from sys import argv
from scripts.utils import init_gdb, check_exists
import os
# import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
# date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

# input
input = os.path.join(workspace, "d_Enriched", "OEIS_2020_2022_poly_enriched_20230405")

Crosswalk(Input_Table = input)
# StandardizeDomains(Input_Table = input)
# %%
