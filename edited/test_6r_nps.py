from utils import init_gdb, unique_rename
import os
original_gdb, workspace, scratch_workspace = init_gdb()
from _6r_nps_20221123 import rFlatFuelsTreatmentDraft
import datetime

date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216
output_enriched = os.path.join(workspace,'d_Enriched','nps_flat_fuels_enriched_'+date_id)
output_standardized = os.path.join(workspace,'c_Standardized','nps_flat_fuels_standardized_'+date_id)
rFlatFuelsTreatmentDraft(output_standardized,output_enriched,)