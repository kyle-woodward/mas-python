#%%
import arcpy
from scripts._6y_CalVTP_20221208 import CalVTP
from sys import argv
from scripts.utils import init_gdb
import os
import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

CalVTP_enriched= os.path.join(workspace, 'd_Enriched', f'CalVTP_enriched_{date_id}')
CalVTP_standardized= os.path.join(workspace, 'c_Standardized', f'CalVTP_standardized_{date_id}')
CalVTP_OG = os.path.join(workspace, 'a_Originals', 'CalVTP_20220923') 

CalVTP(CalVTP_enriched, CalVTP_standardized, CalVTP_OG)