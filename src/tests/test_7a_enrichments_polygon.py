#%%
import arcpy
from scripts._7a_enrichments_polygon import aEnrichmentsPolygon1
from sys import argv
from scripts.utils import init_gdb, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()

enrich_out = os.path.join(workspace,'d_Enriched','OEIS_test123')
enrich_in = os.path.join(workspace,'c_Standardized','OEIS_2020_2022_poly_standardized_20230201')
aEnrichmentsPolygon1(enrich_out, enrich_in)
# %%
