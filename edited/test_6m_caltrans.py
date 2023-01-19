#%%
import arcpy
from _6m_caltrans_activities import CalTrans
from sys import argv
from utils import init_gdb
import os
import datetime

original_gdb, workspace, scratch_workspace = init_gdb()
date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216

input_pts = os.path.join(workspace, "a_Originals", "Vegetation_Control_FY2022_Statewide_Point_Activities")
input_polys = os.path.join(workspace, "a_Originals", "Vegetation_Control_FY2022_Statewide_Polyline_Activities")
output_lines_standardized = os.path.join(workspace, "c_standardized", f'CalTrans_act_ln_standardized_{date_id}')
output_points_standardized = os.path.join(workspace, "c_standardized", f'CalTrans_act_pts_standardized_{date_id}')
output_points_enriched = os.path.join(workspace, "d_Enriched",f'CalTrans_act_pts_enriched_{date_id}') 
output_lines_enriched = os.path.join(workspace, "d_Enriched",f'CalTrans_act_ln_enriched_{date_id}') 
CalTrans(input_pts, input_polys, output_lines_standardized, output_points_standardized, output_points_enriched, output_lines_enriched)
# # %%
 # %%
