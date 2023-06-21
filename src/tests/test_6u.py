#%%
import arcpy
from scripts._6u_WCB_20221226 import WCB
from sys import argv
from scripts.utils import init_gdb
import os
import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

WCB_standardized= os.path.join(workspace, 'c_Standardized', f'WCB_standardized_{date_id}') 
WCB_OG= os.path.join(workspace, 'a_Originals', 'WCB_20221114') 

WCB(WCB_standardized, WCB_OG)
# %%
