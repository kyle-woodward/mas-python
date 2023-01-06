from utils import init_gdb, unique_rename
import os
import datetime
from _6g_nfpors_haz_fuels_treatments import Model71
original_gdb, workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216
nfpors_current_fy = os.path.join(workspace,'a_Originals','nfpors_current_fy_20221110') # would be a more recently downloaded dataset as they become available
output_standardized = os.path.join(workspace,'c_Standardized','nfpors_fuels_treatments_pts_standardized_'+date_id)
output_enriched = os.path.join(workspace, 'd_Enriched','nfpors_fuels_treatments_pts_enriched_'+date_id)

# def Model71(nfpors_fuels_treatments_pts_standardized_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\nfpors_fuels_treatments_pts_standardized_20221110", nfpors_current_fy_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\nfpors_current_fy_20221110", nfpors_fuels_treatments_pts_enriched_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\nfpors_fuels_treatments_pts_enriched_20221110"):  # 6g nfpors_haz_fuels_treatments
Model71(nfpors_current_fy, output_standardized, output_enriched)