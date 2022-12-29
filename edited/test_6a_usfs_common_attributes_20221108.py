from utils import init_gdb, unique_rename
import os
import datetime
from _6a_usfs_common_attributes_20221108 import Model7

original_gdb, workspace, scratch_workspace = init_gdb()

# def Model7(
# usfs_edw_facts_common_attributes_enriched_20220912="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\usfs_edw_facts_common_attributes_enriched_20220912", 
# usfs_haz_fuels_treatments_standardized_20220912="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\usfs_edw_facts_common_attributes_standardized_20220912", 
# Actv_CommonAttribute_PL="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\1-Spatial Data\\EDW_Actv_CommonAttribute_PL_20220912.gdb\\Actv_CommonAttribute_PL"):  # 6a usfs_common_attributes 20221108
date_id = datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

output_enriched = os.path.join(workspace,'d_Enriched',f'usfs_edw_facts_common_attributes_enriched_{date_id}')
output_standardized = os.path.join(workspace,'c_Standardized',f'usfs_edw_facts_common_attributes_standardized_{date_id}')
input_fc = os.path.join(original_gdb,'a_Originals','Actv_CommonAtt_ExportFeature')

Model7(output_enriched,output_standardized,input_fc)