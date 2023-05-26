#%%
import arcpy
from scripts._6h_Tahoe_Forest_Fuels_20221226 import TahoeFF6
from sys import argv
from scripts.utils import init_gdb
import os
import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

TahoeFF_Tx_enriched = os.path.join(workspace, 'd_Enriched', f'Tahoe_Forest_Fuels_Tx_enriched_{date_id}')
TahoeFF_Tx_standardized = os.path.join(workspace, 'c_Standardized', f'Tahoe_Forest_Fuels_Tx_standardized_{date_id}') 
TahoeFF_Tx_OG = os.path.join(workspace, 'a_Originals', 'Tahoe_Forest_Fuels_Tx_20221017') 

TahoeFF6(TahoeFF_Tx_enriched,
         TahoeFF_Tx_standardized,
         TahoeFF_Tx_OG)
# %%
