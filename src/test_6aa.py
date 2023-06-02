#%%
import arcpy
from scripts._6aa_DOC_Ag import DOC6
from sys import argv
from scripts.utils import init_gdb
import os
import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

DOC_Ag_Standardized = os.path.join(workspace, "c_Standardized", f'DOC_Ag_standardized_{date_id}') 
DOC_Ag_enriched = os.path.join(workspace, "d_Enriched", f'DOC_Ag_enriched_{date_id}')
DOC_Ag_OG = os.path.join(workspace, "a_Originals", "DOC_Ag_easements_Range2022")

DOC6(DOC_Ag_Standardized, DOC_Ag_enriched, DOC_Ag_OG)
# %%
