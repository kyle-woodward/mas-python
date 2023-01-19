from utils import init_gdb, unique_rename
import os
original_gdb, workspace, scratch_workspace = init_gdb()
from _6r_nps import rFlatFuelsTreatmentDraft
import datetime

date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216
input_fc = os.path.join(workspace,'a_Originals','nps_flat_fuels_20221102') # need to download this beforehand
output_enriched = os.path.join(workspace,'d_Enriched','nps_flat_fuels_enriched_'+date_id)
output_standardized = os.path.join(workspace,'c_Standardized','nps_flat_fuels_standardized_'+date_id)
rFlatFuelsTreatmentDraft(input_fc, output_standardized, output_enriched)