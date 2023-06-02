#%%
import arcpy
from scripts._7a_enrichments_polygon import aEnrichmentsPolygon1
from sys import argv
from scripts.utils import init_gdb, runner
import os
import datetime
original_gdb, workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# CalVTP_standardized_20220923="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\CalVTP_standardized_20220923"):  # 7a Enrichments Polygon
enrich_out = os.path.join(workspace,'d_Enriched',f'_1_TEST_enriched_{date_id}')
enrich_in = os.path.join(workspace,'c_Standardized','Tahoe_Forest_Fuels_Tx_standardized_20221017')
aEnrichmentsPolygon1(enrich_out, enrich_in)
# %%
