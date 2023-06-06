#%%
import arcpy
from scripts._6q_pfirs import PFIRS
from sys import argv
from edited.scripts.utils import init_gdb
import os
import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

input_fc = os.path.join(workspace, "a_Originals", "PFIRS_2018_2022")
output_standardized = os.path.join(workspace, "c_Standardized", f'PFIRS_standardized_{date_id}')
output_enriched = os.path.join(workspace, "d_Enriched",f'PFIRS_enriched_{date_id}') 
treat_poly = os.path.join(workspace, "e_Appended","Treat_n_harvests_polygons_20221115")
PFIRS(input_fc, output_standardized, output_enriched, treat_poly)
# # %%
 # %%
