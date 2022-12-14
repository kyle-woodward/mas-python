import arcpy
from _7a_enrichments_polygon import aEnrichmentsPolygon1
from sys import argv
from utils import init_gdb, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()
# CalVTP_standardized_20220923="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\CalVTP_standardized_20220923"):  # 7a Enrichments Polygon
enrich_out = os.path.join(workspace,'d_Enriched','testEnrichments_CalVTP_standardized_20220923')
enrich_in = os.path.join(workspace,'c_Standardized','CalVTP_standardized_20220923_1')
aEnrichmentsPolygon1(enrich_out, enrich_in)