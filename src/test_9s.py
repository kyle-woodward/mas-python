#%%
import arcpy
from scripts._9_Transform_20230307 import Transform2
from sys import argv
from scripts.utils import init_gdb, runner
import os
import requests
original_gdb, workspace, scratch_workspace = init_gdb()

Treat_n_harvests_polygons_20221215 = os.path.join(workspace, 'e_Appended', 'Treat_n_harvests_polygons_20221115')
Treatments_Activities_poly = os.path.join(workspace, 'f_Transformed', 'Treatments_Activities_poly')
Treat_n_harvests_points_20221215 = os.path.join(workspace, 'e_Appended', 'Treat_n_harvests_points_20221115')
Treat_n_harvests_lines_20221215 = os.path.join(workspace, 'e_Appended', 'Treat_n_harvests_lines_20230201')
Treatments_Activities_pts = os.path.join(workspace, 'f_Transformed', 'Treatments_Activities_pts')
Treatments_Activities_lns = os.path.join(workspace, 'f_Transformed', 'Treatments_Activities_lns')
CNRA_Activities = os.path.join(workspace, 'Activity_Table')
CNRA_Projects_2_ = os.path.join(workspace, 'Project_Poly')
CNRA_Projects_3_ = os.path.join(workspace, 'Project_Poly')
CNRA_Treatments_2_= os.path.join(workspace, 'Treatment_Poly')
CNRA_Projects = os.path.join(workspace, 'Project_Poly')
CNRA_Treatments = os.path.join(workspace, 'Treatment_Line')
CNRA_Treatments_3_ = os.path.join(workspace, 'Treatment_Point')
Transform2(Treat_n_harvests_polygons_20221215, 
               Treatments_Activities_poly, 
               Treat_n_harvests_points_20221215, 
               Treat_n_harvests_lines_20221215, 
               Treatments_Activities_pts, 
               Treatments_Activities_lns, 
               CNRA_Activities, 
               CNRA_Projects_2_, 
               CNRA_Projects_3_, 
               CNRA_Treatments_2_, 
               CNRA_Projects, 
               CNRA_Treatments, 
               CNRA_Treatments_3_)

# CNRA_Projects_2_ = os.path.join(workspace, 'Project_Poly')
# CNRA_Projects_3_ = requests.get('https://services1.arcgis.com/jUJYIo9tSA7EHvfZ/arcgis/rest/services/CNRA_VegTrmtData_Master_v5/FeatureServer/3', auth=('SageGrouse21', '1x5Rgx*xs'))
# CNRA_Treatments_2_= os.path.join(workspace, 'a_Originals', 'CNRA_Treatments_test')
# CNRA_Projects = requests.get('https://services1.arcgis.com/jUJYIo9tSA7EHvfZ/arcgis/rest/services/CNRA_VegTrmtData_Master_v5/FeatureServer/3', auth=('SageGrouse21', '1x5Rgx*xs'))

# # # %%g
# %%
