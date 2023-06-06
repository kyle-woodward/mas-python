#%%
import arcpy
from scripts._7a_enrichments_polygon import enrich_polygons
from sys import argv
from scripts.utils import init_gdb, runner
import os
import datetime
original_gdb, workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','') # like 20221216

# CalVTP_standardized_20220923="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\CalVTP_standardized_20220923"):  # 7a Enrichments Polygon
<<<<<<< HEAD:src/test_7a_enrichments_polygon.py
enrich_out = os.path.join(workspace,'d_Enriched','testEnrichments_CalVTP_standardized_20220923')
enrich_in = os.path.join(workspace,'c_Standardized','CalVTP_standardized_20220923')
enrich_polygons(enrich_out, enrich_in)
=======
enrich_out = os.path.join(workspace,'d_Enriched',f'_1_TEST_enriched_{date_id}')
enrich_in = os.path.join(workspace,'c_Standardized','Tahoe_Forest_Fuels_Tx_standardized_20221017')
aEnrichmentsPolygon1(enrich_out, enrich_in)
>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227:src/tests/test_7a_enrichments_polygon.py
# %%
