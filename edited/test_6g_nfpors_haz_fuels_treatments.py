from utils import init_gdb
import os
import datetime
from _6g_nfpors_haz_fuels_treatments import Model71
original_gdb, workspace, scratch_workspace = init_gdb()

date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

# The input originals must be downloaded from external source, and their paths updated here
input_original_polys = os.path.join(workspace,'a_Originals','nfpors_fuels_treatments_20220906')
input_original_pts_BIA = os.path.join(workspace,'a_Originals','NFPORSCurrentFYTreatmentsBIA')
input_original_pts_FWS = os.path.join(workspace,'a_Originals','NFPORSCurrentFYTreatmentsFWS')

# these are setup to output new 'timestamped' outputs
output_original_polys = os.path.join(workspace,'a_Originals','nfpors_current_fy_'+date_id) # created from aggregating the two NFPORS web service layers
output_pts_standardized = os.path.join(workspace,'c_Standardized','nfpors_fuels_treatments_pts_standardized_'+date_id)
output_pts_enriched = os.path.join(workspace, 'd_Enriched','nfpors_fuels_treatments_pts_enriched_'+date_id)
output_polys_standardized = os.path.join(workspace,'c_Standardized','nfpors_fuels_treatments_polys_standardized_'+date_id)
output_polys_enriched = os.path.join(workspace,'d_Enriched','nfpors_fuels_treatments_polys_enriched_'+date_id)

# def Model71(nfpors_fuels_treatments_pts_standardized_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\nfpors_fuels_treatments_pts_standardized_20221110", nfpors_current_fy_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\nfpors_current_fy_20221110", nfpors_fuels_treatments_pts_enriched_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\nfpors_fuels_treatments_pts_enriched_20221110"):  # 6g nfpors_haz_fuels_treatments
Model71(input_original_polys,
input_original_pts_BIA, 
input_original_pts_FWS, 
output_original_polys, 
output_polys_standardized, 
output_polys_enriched, 
output_pts_standardized, 
output_pts_enriched
)