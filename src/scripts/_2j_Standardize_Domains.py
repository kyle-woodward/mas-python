# -*- coding: utf-8 -*-
"""
"""
import arcpy
from sys import argv
from scripts.utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()

def StandardizeDomains(Input_Table):  # 2j Standardize Domains

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Calculate Agency (Calculate Field) (management)
    update_agency = arcpy.management.CalculateField(in_table=Input_Table.__str__().format(**locals(),**globals()), 
                                                             field="AGENCY", 
                                                             expression="ifelse(!AGENCY!)", 
                                                             code_block="""def ifelse(Ag):
    if Ag == 'CA Environmental Protection Agency':
        return 'CALEPA'
    elif Ag == 'CA State Transportation Agency':
        return 'CALSTA'
    elif Ag == 'CA Natural Resources Agency':
        return 'CNRA'
    elif Ag == 'Department of Defense':
        return 'DOD'
    elif Ag == 'Department of the Interior':
        return 'DOI'
    elif Ag == 'Department of Agriculture':
        return 'USDA'
    elif Ag == 'Other':
        return 'OTHER'
    else:
        return Ag
        """)[0]

    # Process: Calculate Project Data Steward (Calculate Field) (management)
    update_org_admin_p = arcpy.management.CalculateField(in_table=update_agency, 
                                                              field="ORG_ADMIN_p", 
                                                              expression="ifelse(!ORG_ADMIN_p!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Admin Org (Calculate Field) (management)
    update_administering_org = arcpy.management.CalculateField(in_table=update_org_admin_p, 
                                                             field="ADMINISTERING_ORG", 
                                                             expression="ifelse(!ADMINISTERING_ORG!)", 
                                                             code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Project Status (Calculate Field) (management)
    update_project_status = arcpy.management.CalculateField(in_table=update_administering_org, 
                                                              field="PROJECT_STATUS", 
                                                              expression="ifelse(!PROJECT_STATUS!)", 
                                                              code_block="""def ifelse(Stat):
    if Stat == 'Active':
        return 'ACTIVE'
    elif Stat == 'Active*':
        return 'ACTIVE'
    elif Stat == 'Complete':
        return 'COMPLETE'
    elif Stat == 'Cancelled':
        return 'CANCELLED'
    elif Stat == 'Outyear':
        return 'OUTYEAR'
    elif Stat == 'Planned':
        return 'PLANNED'
    elif Stat == 'Proposed':
        return 'PROPOSED'
    else:
        return Stat""")

    # Process: Calculate Ord Data Steward (Calculate Field) (management)
    update_org_admin_p_2 = arcpy.management.CalculateField(in_table=update_project_status, 
                                                              field="ORG_ADMIN_p", 
                                                              expression="ifelse(!ORG_ADMIN_p!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Fund Source (Calculate Field) (management)
    update_primary_funding_source = arcpy.management.CalculateField(in_table=update_org_admin_p_2, 
                                                              field="PRIMARY_FUNDING_SOURCE", 
                                                              expression="ifelse(!PRIMARY_FUNDING_SOURCE!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Greenhouse Gas Reduction Fund':
        return 'GHG_REDUC_FUND_GGRF'
    elif Org == 'Proposition 68 Bond Funds':
        return 'PROP_68_BOND_FUNDS'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: General Fund':
        return 'GENERAL_FUND_SB170_2021'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: GGRF':
        return 'GGRF_SB170_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: General Fund':
        return 'GENERAL_FUND_SB85_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: GGRF':
        return 'GGRF_SB85_2021'
    elif Org == 'State General Fund':
        return 'GENERAL_FUND'
    elif Org == 'Other State Funds':
        return 'OTHER_STATE_FUNDS'
    elif Org == 'Federal':
        return 'FEDERAL'
    elif Org == 'Local':
        return 'LOCAL'
    elif Org == 'Private':
        return 'PRIVATE'
    else:
        return Org""")

    # Process: Calculate Fund Org (Calculate Field) (management)
    update_primary_funding_org = arcpy.management.CalculateField(in_table=update_primary_funding_source, 
                                                              field="PRIMARY_FUNDING_ORG", 
                                                              expression="ifelse(!PRIMARY_FUNDING_ORG!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Treatment Data Steward (Calculate Field) (management)
    update_org_admin_t = arcpy.management.CalculateField(in_table=update_primary_funding_org, 
                                                              field="ORG_ADMIN_t", 
                                                              expression="ifelse(!ORG_ADMIN_t!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Ownership (Calculate Field) (management)
    update_primary_ownership_group = arcpy.management.CalculateField(in_table=update_org_admin_t, 
                                                              field="PRIMARY_OWNERSHIP_GROUP", 
                                                              expression="ifelse(!PRIMARY_OWNERSHIP_GROUP!)", 
                                                              code_block="""def ifelse(Own):
    if Own == 'Federal':
        return 'FEDERAL'
    elif Own == 'Local':
        return 'LOCAL'
    elif Own == 'NGO':
        return 'NGO'
    elif Own == 'Private - Industrial':
        return 'PRIVATE_INDUSTRY'
    elif Own == 'Private - Non-Industrial':
        return 'PRIVATE_NON-INDUSTRY'
    elif Own == 'State':
        return 'STATE'
    elif Own == 'Tribal':
        return 'TRIBAL'
    else:
        return Own""")

    # Process: Calculate Objective (Calculate Field) (management)
    update_primary_objective = arcpy.management.CalculateField(in_table=update_primary_ownership_group, 
                                                             field="PRIMARY_OBJECTIVE", 
                                                             expression="ifelse(!PRIMARY_OBJECTIVE!)", 
                                                             code_block="""def ifelse(OBJ):
    if OBJ in ['BIOMASS_UTIL', 
    'BURNED_AREA_RESTOR', 
    'CARBON_STORAGE', 
    'CULTURAL_BURN', 
    'ECO_RESTOR', 
    'FIRE_PREVENTION', 
    'FOREST_PEST_CNTRL', 
    'FOREST_STEWARDSHIP', 
    'FUEL_BREAK', 
    'HABITAT_RESTOR', 
    'INV_SPECIES_CNTRL', 
    'LAND_PROTECTION', 
    'MTN_MEADOW_RESTOR', 
    'NON-TIMB_PRODUCTS', 
    'OTHER_FOREST_MGMT', 
    'OTHER_FUELS_REDUCTION', 
    'PRESCRB_FIRE', 
    'RECREATION', 
    'REFORESTATION', 
    'RIPARIAN_RESTOR', 
    'ROADWAY_CLEARANCE', 
    'SITE_PREP', 
    'TIMBER_HARVEST', 
    'UTIL_RIGHT_OF_WAY', 
    'WATSHD_RESTOR', 
    'WETLAND_RESTOR', 'NOT_DEFINED']:
        return OBJ
    elif OBJ ==\"Biomass Utilization\":
        return \"BIOMASS_UTIL\"
    elif OBJ == \"Burned Area Restoration\":
        return \"BURNED_AREA_RESTOR\"
    elif OBJ == \"Carbon Storage\":
        return \"CARBON_STORAGE\"
    elif OBJ == \"Cultural Burn\":
        return \"CULTURAL_BURN\"
    elif OBJ == \"Ecological Restoration\":
        return \"ECO_RESTOR\"
    elif OBJ == \"Fire Prevention\":
        return \"FIRE_PREVENTION\"
    elif OBJ == \"Forest Pest Control\":
        return \"FOREST_PEST_CNTRL\"
    elif OBJ == \"Forestland Stewardship\":
        return \"FOREST_STEWARDSHIP\"
    elif OBJ == \"Fuel Break\":
        return \"FUEL_BREAK\"
    elif OBJ == \"Habitat Restoration\":
        return \"HABITAT_RESTOR\"
    elif OBJ == \"Invasive Species Control\":
        return \"INV_SPECIES_CNTRL\"
    elif OBJ == \"Land Protection\":
        return \"LAND_PROTECTION\"
    elif OBJ == \"Mountain Meadow Restoration\":
        return \"MTN_MEADOW_RESTOR\"
    elif OBJ == \"Non-Timber Products\":
        return \"NON-TIMB_PRODUCTS\"
    elif OBJ == \"Other Forest Management\":
        return \"OTHER_FOREST_MGMT\"
    elif OBJ == \"Other Fuels Reduction\":
        return \"OTHER_FUELS_REDUCTION\"
    elif OBJ == \"Prescribed Fire\":
        return \"PRESCRB_FIRE\"
    elif OBJ == \"Recreation\":
        return \"RECREATION\"
    elif OBJ == \"Reforestation\":
        return \"REFORESTATION\"
    elif OBJ == \"Riparian Restoration\":
        return \"RIPARIAN_RESTOR\"
    elif OBJ == \"Roadway Clearance\":
        return \"ROADWAY_CLEARANCE\"
    elif OBJ == \"Site Preparation\":
        return \"SITE_PREP\"
    elif OBJ == \"Timber Harvest\":
        return \"TIMBER_HARVEST\"
    elif OBJ == \"Utility Right of Way Clearance\":
        return \"UTIL_RIGHT_OF_WAY\"
    elif OBJ == \"Watershed Restoration\":
        return \"WATSHD_RESTOR\"
    elif OBJ == \"Wetland Restoration\":
        return \"WETLAND_RESTOR\"
    elif OBJ == \"Not Defined\":
        return \"NOT_DEFINED\"
    elif OBJ == None:
        return 'TBD'
    else:
        return OBJ""")

    # Process: Calculate Objective (2) (Calculate Field) (management)
    update_secondary_objective = arcpy.management.CalculateField(in_table=update_primary_objective, 
                                                             field="SECONDARY_OBJECTIVE", 
                                                             expression="ifelse(!SECONDARY_OBJECTIVE!)", 
                                                             code_block="""def ifelse(OBJ):
    if OBJ in ['BIOMASS_UTIL', 
    'BURNED_AREA_RESTOR', 
    'CARBON_STORAGE', 
    'CULTURAL_BURN', 
    'ECO_RESTOR', 
    'FIRE_PREVENTION', 
    'FOREST_PEST_CNTRL', 
    'FOREST_STEWARDSHIP', 
    'FUEL_BREAK', 
    'HABITAT_RESTOR', 
    'INV_SPECIES_CNTRL', 
    'LAND_PROTECTION', 
    'MTN_MEADOW_RESTOR', 
    'NON-TIMB_PRODUCTS', 
    'OTHER_FOREST_MGMT', 
    'OTHER_FUELS_REDUCTION', 
    'PRESCRB_FIRE', 
    'RECREATION', 
    'REFORESTATION', 
    'RIPARIAN_RESTOR', 
    'ROADWAY_CLEARANCE', 
    'SITE_PREP', 
    'TIMBER_HARVEST', 
    'UTIL_RIGHT_OF_WAY', 
    'WATSHD_RESTOR', 
    'WETLAND_RESTOR', 'NOT_DEFINED']:
        return OBJ
    elif OBJ ==\"Biomass Utilization\":
        return \"BIOMASS_UTIL\"
    elif OBJ == \"Burned Area Restoration\":
        return \"BURNED_AREA_RESTOR\"
    elif OBJ == \"Carbon Storage\":
        return \"CARBON_STORAGE\"
    elif OBJ == \"Cultural Burn\":
        return \"CULTURAL_BURN\"
    elif OBJ == \"Ecological Restoration\":
        return \"ECO_RESTOR\"
    elif OBJ == \"Fire Prevention\":
        return \"FIRE_PREVENTION\"
    elif OBJ == \"Forest Pest Control\":
        return \"FOREST_PEST_CNTRL\"
    elif OBJ == \"Forestland Stewardship\":
        return \"FOREST_STEWARDSHIP\"
    elif OBJ == \"Fuel Break\":
        return \"FUEL_BREAK\"
    elif OBJ == \"Habitat Restoration\":
        return \"HABITAT_RESTOR\"
    elif OBJ == \"Invasive Species Control\":
        return \"INV_SPECIES_CNTRL\"
    elif OBJ == \"Land Protection\":
        return \"LAND_PROTECTION\"
    elif OBJ == \"Mountain Meadow Restoration\":
        return \"MTN_MEADOW_RESTOR\"
    elif OBJ == \"Non-Timber Products\":
        return \"NON-TIMB_PRODUCTS\"
    elif OBJ == \"Other Forest Management\":
        return \"OTHER_FOREST_MGMT\"
    elif OBJ == \"Other Fuels Reduction\":
        return \"OTHER_FUELS_REDUCTION\"
    elif OBJ == \"Prescribed Fire\":
        return \"PRESCRB_FIRE\"
    elif OBJ == \"Recreation\":
        return \"RECREATION\"
    elif OBJ == \"Reforestation\":
        return \"REFORESTATION\"
    elif OBJ == \"Riparian Restoration\":
        return \"RIPARIAN_RESTOR\"
    elif OBJ == \"Roadway Clearance\":
        return \"ROADWAY_CLEARANCE\"
    elif OBJ == \"Site Preparation\":
        return \"SITE_PREP\"
    elif OBJ == \"Timber Harvest\":
        return \"TIMBER_HARVEST\"
    elif OBJ == \"Utility Right of Way Clearance\":
        return \"UTIL_RIGHT_OF_WAY\"
    elif OBJ == \"Watershed Restoration\":
        return \"WATSHD_RESTOR\"
    elif OBJ == \"Wetland Restoration\":
        return \"WETLAND_RESTOR\"
    elif OBJ == \"Not Defined\":
        return \"NOT_DEFINED\"
    elif OBJ == None:
        return None
    else:
        return OBJ""")

    # Process: Calculate Objective (3) (Calculate Field) (management)
    update_tertiary_objective = arcpy.management.CalculateField(in_table=update_secondary_objective, 
                                                             field="TERTIARY_OBJECTIVE", 
                                                             expression="ifelse(!TERTIARY_OBJECTIVE!)", 
                                                             code_block="""def ifelse(OBJ):
    if OBJ in ['BIOMASS_UTIL', 
    'BURNED_AREA_RESTOR', 
    'CARBON_STORAGE', 
    'CULTURAL_BURN', 
    'ECO_RESTOR', 
    'FIRE_PREVENTION', 
    'FOREST_PEST_CNTRL', 
    'FOREST_STEWARDSHIP', 
    'FUEL_BREAK', 
    'HABITAT_RESTOR', 
    'INV_SPECIES_CNTRL', 
    'LAND_PROTECTION', 
    'MTN_MEADOW_RESTOR', 
    'NON-TIMB_PRODUCTS', 
    'OTHER_FOREST_MGMT', 
    'OTHER_FUELS_REDUCTION', 
    'PRESCRB_FIRE', 
    'RECREATION', 
    'REFORESTATION', 
    'RIPARIAN_RESTOR', 
    'ROADWAY_CLEARANCE', 
    'SITE_PREP', 
    'TIMBER_HARVEST', 
    'UTIL_RIGHT_OF_WAY', 
    'WATSHD_RESTOR', 
    'WETLAND_RESTOR', 'NOT_DEFINED']:
        return OBJ
    elif OBJ ==\"Biomass Utilization\":
        return \"BIOMASS_UTIL\"
    elif OBJ == \"Burned Area Restoration\":
        return \"BURNED_AREA_RESTOR\"
    elif OBJ == \"Carbon Storage\":
        return \"CARBON_STORAGE\"
    elif OBJ == \"Cultural Burn\":
        return \"CULTURAL_BURN\"
    elif OBJ == \"Ecological Restoration\":
        return \"ECO_RESTOR\"
    elif OBJ == \"Fire Prevention\":
        return \"FIRE_PREVENTION\"
    elif OBJ == \"Forest Pest Control\":
        return \"FOREST_PEST_CNTRL\"
    elif OBJ == \"Forestland Stewardship\":
        return \"FOREST_STEWARDSHIP\"
    elif OBJ == \"Fuel Break\":
        return \"FUEL_BREAK\"
    elif OBJ == \"Habitat Restoration\":
        return \"HABITAT_RESTOR\"
    elif OBJ == \"Invasive Species Control\":
        return \"INV_SPECIES_CNTRL\"
    elif OBJ == \"Land Protection\":
        return \"LAND_PROTECTION\"
    elif OBJ == \"Mountain Meadow Restoration\":
        return \"MTN_MEADOW_RESTOR\"
    elif OBJ == \"Non-Timber Products\":
        return \"NON-TIMB_PRODUCTS\"
    elif OBJ == \"Other Forest Management\":
        return \"OTHER_FOREST_MGMT\"
    elif OBJ == \"Other Fuels Reduction\":
        return \"OTHER_FUELS_REDUCTION\"
    elif OBJ == \"Prescribed Fire\":
        return \"PRESCRB_FIRE\"
    elif OBJ == \"Recreation\":
        return \"RECREATION\"
    elif OBJ == \"Reforestation\":
        return \"REFORESTATION\"
    elif OBJ == \"Riparian Restoration\":
        return \"RIPARIAN_RESTOR\"
    elif OBJ == \"Roadway Clearance\":
        return \"ROADWAY_CLEARANCE\"
    elif OBJ == \"Site Preparation\":
        return \"SITE_PREP\"
    elif OBJ == \"Timber Harvest\":
        return \"TIMBER_HARVEST\"
    elif OBJ == \"Utility Right of Way Clearance\":
        return \"UTIL_RIGHT_OF_WAY\"
    elif OBJ == \"Watershed Restoration\":
        return \"WATSHD_RESTOR\"
    elif OBJ == \"Wetland Restoration\":
        return \"WETLAND_RESTOR\"
    elif OBJ == \"Not Defined\":
        return \"NOT_DEFINED\"
    elif OBJ == None:
        return None
    else:
        return OBJ""")

    # Process: Calculate Treatment Status (Calculate Field) (management)
    update_treatment_status = arcpy.management.CalculateField(in_table=update_tertiary_objective, 
                                                              field="TREATMENT_STATUS", 
                                                              expression="ifelse(!TREATMENT_STATUS!)", 
                                                              code_block="""def ifelse(Stat):
    if Stat == 'Active':
        return 'ACTIVE'
    elif Stat == 'Active*':
        return 'ACTIVE'
    elif Stat == 'Complete':
        return 'COMPLETE'
    elif Stat == 'Cancelled':
        return 'CANCELLED'
    elif Stat == 'Outyear':
        return 'OUTYEAR'
    elif Stat == 'Planned':
        return 'PLANNED'
    elif Stat == 'Proposed':
        return 'PROPOSED'
    else:
        return Stat""")

    # Process: Calculate County (Calculate Field) (management)
    update_county = arcpy.management.CalculateField(in_table=update_treatment_status, 
                                                              field="COUNTY", 
                                                              expression="ifelse(!COUNTY!)", 
                                                              code_block="""def ifelse(County):
    if County == 'Alameda' or County == 'ALAMEDA':
        return 'ALA'
    elif County == 'Alpine' or County == 'ALPINE':
        return 'ALP'
    elif County == 'Amador' or County == 'AMADOR':
        return 'AMA'
    elif County == 'Butte' or County == 'BUTTE':
        return 'BUT'
    elif County == 'Calaveras' or County == 'CALAVERAS':
        return 'CAL'
    elif County == 'Colusa' or County == 'COLUSA':
        return 'COL'
    elif County == 'Contra Costa' or County == 'CONTRA COSTA':
        return 'CC'
    elif County == 'Del Norte' or County == 'DEL NORTE':
        return 'DN'
    elif County == 'El Dorado' or County == 'EL DORADO':
        return 'ED'
    elif County == 'Fresno' or County == 'FRESNO':
        return 'FRE'
    elif County == 'Glenn' or County == 'GLENN':
        return 'GLE'
    elif County == 'Humboldt' or County == 'HUMBOLDT':
        return 'HUM'
    elif County == 'Imperial' or County == 'IMPERIAL':
        return 'IMP'
    elif County == 'Inyo' or County == 'INYO':
        return 'INY'
    elif County == 'Kern' or County == 'KERN':
        return 'KER'
    elif County == 'Kings' or County == 'KINGS':
        return 'KIN'
    elif County == 'Lake' or County == 'LAKE':
        return 'LAK'
    elif County == 'Lassen' or County == 'LASSEN':
        return 'LAS'
    elif County == 'Los Angeles' or County == 'LOS ANGELES':
        return 'LA'
    elif County == 'Madera' or County == 'MADERA':
        return 'MAD'
    elif County == 'Marin' or County == 'MARIN':
        return 'MRN'
    elif County == 'Mariposa' or County == 'MARIPOSA':
        return 'MPA'
    elif County == 'Mendocino' or County == 'MENDOCINO':
        return 'MEN'
    elif County == 'Merced' or County == 'MERCED':
        return 'MER'
    elif County == 'Modoc' or County == 'MODOC':
        return 'MOD'
    elif County == 'Monterey' or County == 'MONTEREY':
        return 'MON'
    elif County == 'Mono' or County == 'MONO':
        return 'MNO'
    elif County == 'Napa' or County == 'NAPA':
        return 'NAP'
    elif County == 'Nevada' or County == 'NEVADA':
        return 'NEV'
    elif County == 'Orange' or County == 'ORANGE':
        return 'ORA'
    elif County == 'Placer' or County == 'PLACER':
        return 'PLA'
    elif County == 'Plumas' or County == 'PLUMAS':
        return 'PLU'
    elif County == 'Riverside' or County == 'RIVERSIDE':
        return 'RIV'
    elif County == 'Sacramento' or County == 'SACRAMENTO':
        return 'SAC'
    elif County == 'San Benito' or County == 'SAN BENITO':
        return 'SBT'
    elif County == 'San Bernardino' or County == 'SAN BERNARDINO':
        return 'SBD'
    elif County == 'San Diego' or County == 'SAN DIEGO':
        return 'SD'
    elif County == 'San Francisco' or County == 'SAN FRANCISCO':
        return 'SF'
    elif County == 'San Joaquin' or County == 'SAN JOAQUIN':
        return 'SJ'
    elif County == 'San Luis Obispo' or County == 'SAN LUIS OBISPO':
        return 'SLO'
    elif County == 'San Mateo' or County == 'SAN MATEO':
        return 'SM'
    elif County == 'Santa Barbara' or County == 'SANTA BARBARA':
        return 'SB'
    elif County == 'Santa Clara' or County == 'SANTA CLARA':
        return 'SCL'
    elif County == 'Santa Cruz' or County == 'SANTA CRUZE':
        return 'SCR'
    elif County == 'Shasta' or County == 'SHASTA':
        return 'SHA'
    elif County == 'Sierra' or County == 'SIERRA':
        return 'SIE'
    elif County == 'Siskiyou' or County == 'SISKIYOU':
        return 'SIS'
    elif County == 'Solano' or County == 'SOLANO':
        return 'SOL'
    elif County == 'Sonoma' or County == 'SONOMA':
        return 'SON'
    elif County == 'Stanislaus' or County == 'STANISLAUS':
        return 'STA'
    elif County == 'Sutter' or County == 'SUTTER':
        return 'SUT'
    elif County == 'Tehama' or County == 'TEHAMA':
        return 'TEH'
    elif County == 'Tuolumne' or County == 'TUOLUMNE':
        return 'TUO'
    elif County == 'Trinity' or County == 'TRINITY':
        return 'TRI'
    elif County == 'Tulare' or County == 'TULARE':
        return 'TUL'
    elif County == 'Ventura' or County == 'VENTURA':
        return 'VEN'
    elif County == 'Yolo' or County == 'YOLO':
        return 'YOL'
    elif County == 'Yuba' or County == 'YUBA':
        return 'YUB'
    else:
        return County""")

    # Process: Calculate WUI (Calculate Field) (management)
    update_in_wui = arcpy.management.CalculateField(in_table=update_county, 
                                                              field="IN_WUI", 
                                                              expression="ifelse(!IN_WUI!)", 
                                                              code_block="""def ifelse(WUI):
    if WUI == 'WUI (user defined)':
        return 'WUI_USER_DEFINED'
    elif WUI == 'Non-WUI (user defined)':
        return 'NON-WUI_USER_DEFINED'
    elif WUI == 'WUI (auto populated)':
        return 'WUI_AUTO_POP'
    elif WUI == 'Non-WUI (auto populated)':
        return 'NON-WUI_AUTO_POP'
    else:
        return WUI""")

    # Process: Calculate Region (Calculate Field) (management)
    update_region = arcpy.management.CalculateField(in_table=update_in_wui, 
                                                             field="REGION", 
                                                             expression="ifelse(!REGION!)", 
                                                             code_block="""def ifelse(Region):
    if Region == 'Central Coast':
        return 'CENTRAL_COAST'
    elif Region == 'North Coast':
        return 'NORTH_COAST'
    elif Region == 'Sierra Nevada':
        return 'SIERRA_NEVADA'
    elif Region == 'Southern California':
        return 'SOUTHERN_CA'
    elif Region == 'Coastal-Inland':
        return 'CENTRAL_COAST'
    elif Region == 'COASTAL_INLAND':
        return 'CENTRAL_COAST'
    elif Region == 'North Coast-Inland':
        return 'NORTH_COAST'
    elif Region == 'NORTH_COAST_INLAND':
        return 'NORTH_COAST'
    elif Region == 'Sierra-Cascade-Inyo':
        return 'SIERRA_NEVADA'
    elif Region == 'SIERRA_CASCADE_INYO':
        return 'SIERRA_NEVADA'
    else:
        return Region""")

    # Process: Calculate Activity Data Steward (Calculate Field) (management)
    update_org_admin_a = arcpy.management.CalculateField(in_table=update_region, 
                                                              field="ORG_ADMIN_a", 
                                                              expression="ifelse(!ORG_ADMIN_a!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Activity Description (Calculate Field) (management)
    update_activity_description = arcpy.management.CalculateField(in_table=update_org_admin_a, 
                                                              field="ACTIVITY_DESCRIPTION", 
                                                              expression="ifelse(!ACTIVITY_DESCRIPTION!)", 
                                                              code_block="""def ifelse(ACT):
    if ACT in ['AMW_AREA_RESTOR', 
    'BIOMASS_REMOVAL', 
    'BROADCAST_BURN', 
    'CHAIN_CRUSH', 
    'CHIPPING', 
    'CLEARCUT', 
    'COMM_THIN', 
    'CONVERSION', 
    'DISCING', 
    'DOZER_LINE', 
    'EASEMENT', 
    'ECO_HAB_RESTORATION', 
    'EROSION_CONTROL', 
    'FEE_TITLE', 
    'GRP_SELECTION_HARVEST', 
    'HABITAT_REVEG', 
    'HANDLINE', 
    'HERBICIDE_APP', 
    'INV_PLANT_REMOVAL', 
    'LAND_ACQ', 
    'LANDING_TRT', 
    'LOP_AND_SCAT', 
    'MASTICATION', 
    'MOWING', 
    'NONCOM_THIN_MAN', 
    'NONCOM_THIN_MECH', 
    'NOT_DEFINED', 
    'OAK_WDLND_MGMT', 
    'PEST_CNTRL', 
    'PILE_BURN', 
    'PILING', 
    'PL_TREAT_BURNED', 
    'PRESCRB_HERBIVORY', 
    'PRUNING', 
    'REHAB_UNDRSTK_AREA', 
    'ROAD_CLEAR', 
    'ROAD_OBLITERATION', 
    'SALVG_HARVEST', 
    'SANI_HARVEST', 
    'SEED_TREE_PREP_STEP', 
    'SEED_TREE_REM_STEP', 
    'SEED_TREE_SEED_STEP', 
    'SEEDBED_PREP', 
    'SHELTERWD_PREP_STEP', 
    'SHELTERWD_REM_STEP', 
    'SHELTERWD_SEED_STEP', 
    'SINGLE_TREE_SELECTION', 
    'SITE_PREP', 
    'SLASH_DISPOSAL', 
    'SP_PRODUCTS', 
    'STREAM_CHNL_IMPRV', 
    'THIN_MAN', 
    'THIN_MECH', 
    'TRANSITION_HARVEST', 
    'TREE_FELL', 
    'TREE_PLNTING', 
    'TREE_RELEASE_WEED', 
    'TREE_SEEDING', 
    'UTIL_RIGHTOFWAY_CLR', 
    'VARIABLE_RETEN_HARVEST', 
    'WETLAND_RESTOR', 
    'WM_RESRC_BENEFIT', 
    'YARDING']:
        return ACT
    elif ACT == \"Aspen/Meadow/Wet Area Restoration\":
        return \"AMW_AREA_RESTOR\"
    elif ACT == \"Biomass Removal\":
        return \"BIOMASS_REMOVAL\"
    elif ACT == \"Broadcast Burn\":
        return \"BROADCAST_BURN\"
    elif ACT == \"Chaining/Crushing\":
        return \"CHAIN_CRUSH\"
    elif ACT == \"Chipping\":
        return \"CHIPPING\"
    elif ACT == \"Clearcut\":
        return \"CLEARCUT\"
    elif ACT == \"Commercial Thin\":
        return \"COMM_THIN\"
    elif ACT == \"Conversion\":
        return \"CONVERSION\"
    elif ACT == \"Discing\":
        return \"DISCING\"
    elif ACT == \"Dozer\":
        return \"DOZER_LINE\"
    elif ACT == \"Easement\":
        return \"EASEMENT\"
    elif ACT == \"Erosion Control\":
        return \"EROSION_CONTROL\"
    elif ACT == \"Group Selection Harvest\":
        return \"GRP_SELECTION_HARVEST\"
    elif ACT == \"Habitat Revegetation\":
        return \"HABITAT_REVEG\"
    elif ACT == \"Handline\":
        return \"HANDLINE\"
    elif ACT == \"Herbicide Application\":
        return \"HERBICIDE_APP\"
    elif ACT == \"Invasive Plant Removal\":
        return \"INV_PLANT_REMOVAL\"
    elif ACT == \"Land Acquisitions\":
        return \"LAND_ACQ\"
    elif ACT == \"Landing Treated - Area Mitigated\":
        return \"LANDING_TRT\"
    elif ACT == \"Lop and Scatter\":
        return \"LOP_AND_SCAT\"
    elif ACT == \"Mastication\":
        return \"MASTICATION\"
    elif ACT == \"Mowing\":
        return \"MOWING\"
    elif ACT == \"Noncommercial Thinning (Mechanical)\":
        return \"NONCOM_THIN_MECH\"
    elif ACT == \"Noncommercial Thinning (Manual)\":
        return \"NONCOM_THIN_MAN\"
    elif ACT == \"Oak Woodland Management\":
        return \"OAK_WDLND_MGMT\"
    elif ACT == \"Pest Control\":
        return \"PEST_CNTRL\"
    elif ACT == \"Pile Burning\":
        return \"PILE_BURN\"
    elif ACT == \"Piling\":
        return \"PILING\"
    elif ACT == \"Planned Treatment Burned in Wildfire\":
        return \"PL_TREAT_BURNED\"
    elif ACT == \"Precommercial Thinning (Manual)\":
        return \"THIN_MAN\"
    elif ACT == \"Precommercial Thinning (Mechanical)\":
        return \"THIN_MECH\"
    elif ACT == \"Prescribed Herbivory\":
        return \"PRESCRB_HERBIVORY\"
    elif ACT == \"Pruning\":
        return \"PRUNING\"
    elif ACT == \"Rehabilitation of Understocked Area\":
        return \"REHAB_UNDRSTK_AREA\"
    elif ACT == 'Road Clearance':
        return 'ROAD_CLEAR'
    elif ACT == \"Road Obliteration\":
        return \"ROAD_OBLITERATION\"
    elif ACT == \"Salvage Harvest\":
        return \"SALVG_HARVEST\"
    elif ACT == \"Sanitation Harvest\":
        return \"SANI_HARVEST\"
    elif ACT == \"Seedbed Preparation\":
        return \"SEEDBED_PREP\"
    elif ACT == \"Seed Tree Prep Step\":
        return \"SEED_TREE_PREP_STEP\"
    elif ACT == \"Seed Tree Removal Step\":
        return \"SEED_TREE_REM_STEP\"
    elif ACT == \"Seed Tree Seed Step\":
        return \"SEED_TREE_SEED_STEP\"
    elif ACT == \"Shelterwood Prep Step\":
        return \"SHELTERWD_PREP_STEP\"
    elif ACT == \"Shelterwood Removal Step\":
        return \"SHELTERWD_REM_STEP\"
    elif ACT == \"Shelterwood Seed Step\":
        return \"SHELTERWD_SEED_STEP\"
    elif ACT == \"Single Tree Selection\":
        return \"SINGLE_TREE_SELECTION\"
    elif ACT == \"Site Preparation\":
        return \"SITE_PREP\"
    elif ACT == \"Slash Disposal\":
        return \"SLASH_DISPOSAL\"
    elif ACT == 'Special Products Removal':
        return 'SP_PRODUCTS'
    elif ACT == \"Stream Channel Improvement\":
        return \"STREAM_CHNL_IMPRV\"
    elif ACT == \"Thinning (Manual)\":
        return \"THIN_MAN\"
    elif ACT == \"Thinning (Mechanical)\":
        return \"THIN_MECH\"
    elif ACT == \"Transition Harvest\":
        return \"TRANSITION_HARVEST\"
    elif ACT == \"Tree Planting\":
        return \"TREE_PLNTING\"
    elif ACT == \"Tree Release and Weed\":
        return \"TREE_RELEASE_WEED\"
    elif ACT == \"Tree Seeding\":
        return \"TREE_SEEDING\"
    elif ACT == \"Trees Felled (> 6in dbh)\":
        return \"TREE_FELL\"
    elif ACT == \"Variable Retention Harvest\":
        return \"VARIABLE_RETEN_HARVEST\"
    elif ACT == \"Wetland Restoration\":
        return \"WETLAND_RESTOR\"
    elif ACT == \"Wildfire Managed for Resource Benefit\":
        return \"WM_RESRC_BENEFIT\"
    elif ACT == \"Yarding/Skidding\":
        return \"YARDING\"
    elif ACT == \"Not Defined\":
        return \"NOT_DEFINED\"
    elif ACT == None:
        return \"TBD\"
    else:
        return \"TBD\"""")

    # Process: Calculate Activity Category (Calculate Field) (management)
    update_activity_cat = arcpy.management.CalculateField(in_table=update_activity_description, 
                                                          field="ACTIVITY_CAT", 
                                                          expression="ifelse(!ACTIVITY_CAT!)", 
                                                          code_block="""def ifelse(Cat):
    if Cat == 'Mechanical and Hand Fuels Reduction':
        return 'MECH_HFR'
    elif Cat == 'Beneficial Fire':
        return 'BENEFICIAL_FIRE'
    elif Cat == 'Grazing':
        return 'GRAZING'
    elif Cat == 'Land Protection':
        return 'LAND_PROTEC'
    elif Cat == 'Sanitation & Salvage':
        return 'SANI_SALVG'
    elif Cat == 'Timber Harvest':
        return 'TIMB_HARV'
    elif Cat == 'Tree Planting':
        return 'TREE_PLNTING'
    elif Cat == 'Watershed & Habitat Improvement':
        return 'WATSHD_IMPRV'
    elif Cat == 'Not Defined':
        return 'NOT_DEFINED'
    else:
        return Cat""")

    # Process: Calculate BVT (Calculate Field) (management)
    update_bvt = arcpy.management.CalculateField(in_table=update_activity_cat, 
                                                              field="BROAD_VEGETATION_TYPE", 
                                                              expression="ifelse(!BROAD_VEGETATION_TYPE!)", 
                                                              code_block="""def ifelse(VEG):
    if VEG == \"Agriculture\":
        return \"AGRICULTURE\"
    elif VEG == \"Barren/Other\":
        return \"SPARSE\"
    elif VEG == 'Sparse':
        return 'SPARSE'
    elif VEG == \"Conifer Forest\":
        return \"FOREST\"
    elif VEG == \"Conifer Woodland\":
        return \"FOREST\"
    elif VEG == \"Desert Shrub\":
        return \"SHRB_CHAP\"
    elif VEG == \"Desert Woodland\":
        return \"FOREST\"
    elif VEG == 'Forest':
        return 'FOREST'
    elif VEG == \"Hardwood Forest\":
        return \"FOREST\"
    elif VEG == \"Hardwood Woodland\":
        return \"FOREST\"
    elif VEG == 'Grass/Herbaceous':
        return 'GRASS_HERB'
    elif VEG == \"Herbaceous\":
        return \"GRASS_HERB\"
    elif VEG == \"Shrub\":
        return \"SHRB_CHAP\"
    elif VEG == 'Shrublands and Chaparral':
        return 'SHRB_CHAP'
    elif VEG == \"Urban\":
        return \"URBAN\"
    elif VEG == \"Water\":
        return \"WATER\"
    elif VEG == \"Wetland\":
        return \"WETLAND\"
    elif VEG == \"Tree\":
        return \"FOREST\"
    else:
        return VEG""")

    # Process: Calculate BVT ID (Calculate Field) (management)
    update_bvt_userd = arcpy.management.CalculateField(in_table=update_bvt, 
                                                              field="BVT_USERD", 
                                                              expression="ifelse(!BVT_USERD!)", 
                                                              code_block="""def ifelse(YN):
    if YN == 'Yes':
        return 'YES'
    elif YN == 'No':
        return 'NO'
    else:
        return YN
        """)

    # Process: Calculate Activity Status (Calculate Field) (management)
    update_activity_status = arcpy.management.CalculateField(in_table=update_bvt_userd, 
                                                             field="ACTIVITY_STATUS", 
                                                             expression="ifelse(!ACTIVITY_STATUS!)", 
                                                             code_block="""def ifelse(Stat):
    if Stat == 'Active':
        return 'ACTIVE'
    elif Stat == 'Active*':
        return 'ACTIVE'
    elif Stat == 'Complete':
        return 'COMPLETE'
    elif Stat == 'Cancelled':
        return 'CANCELLED'
    elif Stat == 'Outyear':
        return 'OUTYEAR'
    elif Stat == 'Planned':
        return 'PLANNED'
    elif Stat == 'Proposed':
        return 'PROPOSED'
    else:
        return Stat""")

    # Process: Calculate Units (Calculate Field) (management)
    update_activity_uom = arcpy.management.CalculateField(in_table=update_activity_status, 
                                                             field="ACTIVITY_UOM", 
                                                             expression="ifelse(!ACTIVITY_UOM!)", 
                                                             code_block="""def ifelse(Units):
    if Units == \"acres\":
        return \"AC\"
    elif Units == \"ACRES\":
        return \"AC\"
    elif Units == \"Acres\":
        return \"AC\"
    elif Units == \"ACRE\":
        return \"AC\"
    elif Units == \"Ac\":
        return \"AC\"
    elif Units == \"each\":
        return \"EA\"
    elif Units == \"Each\":
        return \"EA\"
    elif Units == \"Ea\":
        return \"EA\"
    elif Units == \"Hours\":
        return \"HR\"
    elif Units == \"Hour\":
        return \"HR\"
    elif Units == \"Hr\":
        return \"HR\"
    elif Units == \"miles\":
        return \"MI\"
    elif Units == \"Mi\":
        return \"MI\"
    elif Units == \"mi\":
        return \"MI\"
    elif Units == \"mile\":
        return \"MI\"
    elif Units == \"Mile\":
        return \"MI\"
    elif Units == \"Other\":
        return \"OTHER\"
    elif Units == \"Ton\":
        return \"TON\"
    elif Units == \"Tons\":
        return \"TON\"
    else:
        return Units""")

    # Process: Calculate Activity Admin (Calculate Field) (management)
    update_admin_org_name = arcpy.management.CalculateField(in_table=update_activity_uom, 
                                                              field="ADMIN_ORG_NAME", 
                                                              expression="ifelse(!ADMIN_ORG_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Act Fund Source (Calculate Field) (management)
    update_primary_fund_src_name = arcpy.management.CalculateField(in_table=update_admin_org_name, 
                                                              field="PRIMARY_FUND_SRC_NAME", 
                                                              expression="ifelse(!PRIMARY_FUND_SRC_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Greenhouse Gas Reduction Fund':
        return 'GHG_REDUC_FUND_GGRF'
    elif Org == 'Proposition 68 Bond Funds':
        return 'PROP_68_BOND_FUNDS'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: General Fund':
        return 'GENERAL_FUND_SB170_2021'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: GGRF':
        return 'GGRF_SB170_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: General Fund':
        return 'GENERAL_FUND_SB85_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: GGRF':
        return 'GGRF_SB85_2021'
    elif Org == 'State General Fund':
        return 'GENERAL_FUND'
    elif Org == 'Other State Funds':
        return 'OTHER_STATE_FUNDS'
    elif Org == 'Federal':
        return 'FEDERAL'
    elif Org == 'Local':
        return 'LOCAL'
    elif Org == 'Private':
        return 'PRIVATE'
    else:
        return Org""")

    # Process: Calculate Act Fund Org (Calculate Field) (management)
    update_primary_fund_org_name = arcpy.management.CalculateField(in_table=update_primary_fund_src_name, 
                                                              field="PRIMARY_FUND_ORG_NAME", 
                                                              expression="ifelse(!PRIMARY_FUND_ORG_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Act Fund Source (2) (Calculate Field) (management)
    update_secondary_fund_src_name = arcpy.management.CalculateField(in_table=update_primary_fund_org_name, 
                                                              field="SECONDARY_FUND_SRC_NAME", 
                                                              expression="ifelse(!SECONDARY_FUND_SRC_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Greenhouse Gas Reduction Fund':
        return 'GHG_REDUC_FUND_GGRF'
    elif Org == 'Proposition 68 Bond Funds':
        return 'PROP_68_BOND_FUNDS'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: General Fund':
        return 'GENERAL_FUND_SB170_2021'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: GGRF':
        return 'GGRF_SB170_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: General Fund':
        return 'GENERAL_FUND_SB85_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: GGRF':
        return 'GGRF_SB85_2021'
    elif Org == 'State General Fund':
        return 'GENERAL_FUND'
    elif Org == 'Other State Funds':
        return 'OTHER_STATE_FUNDS'
    elif Org == 'Federal':
        return 'FEDERAL'
    elif Org == 'Local':
        return 'LOCAL'
    elif Org == 'Private':
        return 'PRIVATE'
    else:
        return Org""")

    # Process: Calculate Act Fund Org (2) (Calculate Field) (management)
    update_secondary_fund_src_name_2 = arcpy.management.CalculateField(in_table=update_secondary_fund_src_name, 
                                                              field="SECONDARY_FUND_SRC_NAME", 
                                                              expression="ifelse(!SECONDARY_FUND_SRC_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Act Fund Source (3) (Calculate Field) (management)
    update_tertiary_fund_src_name = arcpy.management.CalculateField(in_table=update_secondary_fund_src_name_2, 
                                                              field="TERTIARY_FUND_SRC_NAME", 
                                                              expression="ifelse(!TERTIARY_FUND_SRC_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Greenhouse Gas Reduction Fund':
        return 'GHG_REDUC_FUND_GGRF'
    elif Org == 'Proposition 68 Bond Funds':
        return 'PROP_68_BOND_FUNDS'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: General Fund':
        return 'GENERAL_FUND_SB170_2021'
    elif Org == 'SB 170 (2021) Wildfire Resilience Fund: GGRF':
        return 'GGRF_SB170_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: General Fund':
        return 'GENERAL_FUND_SB85_2021'
    elif Org == 'SB 85 (2021) Wildfire Resilience Early Action: GGRF':
        return 'GGRF_SB85_2021'
    elif Org == 'State General Fund':
        return 'GENERAL_FUND'
    elif Org == 'Other State Funds':
        return 'OTHER_STATE_FUNDS'
    elif Org == 'Federal':
        return 'FEDERAL'
    elif Org == 'Local':
        return 'LOCAL'
    elif Org == 'Private':
        return 'PRIVATE'
    else:
        return Org""")

    # Process: Calculate Act Fund Org (3) (Calculate Field) (management)
    update_tertiary_fund_src_name_2 = arcpy.management.CalculateField(in_table=update_tertiary_fund_src_name, 
                                                              field="TERTIARY_FUND_ORG_NAME", 
                                                              expression="ifelse(!TERTIARY_FUND_ORG_NAME!)", 
                                                              code_block="""def ifelse(Org):
    if Org == 'Baldwin Hills Conservancy':
        return 'BHC'
    elif Org == 'Bureau of Indian Affairs':
        return 'BIA'
    elif Org == 'Bureau of Land Management':
        return 'BLM'
    elif Org == 'CA Board of Forestry and Fire Protection':
        return 'BOF'
    elif Org == 'CAL FIRE':
        return 'CALFIRE'
    elif Org == 'CA Department of Transportation':
        return 'CALTRANS'
    elif Org == 'CA Air Resources Board':
        return 'CARB'
    elif Org == 'CA Conservation Corps':
        return 'CCC'
    elif Org == 'CA Department of Fish and Wildlife':
        return 'CDFW'
    elif Org == 'Coachella Valley Mountains Conservancy':
        return 'CVMC'
    elif Org == 'CA Department of Conservation':
        return 'DOC'
    elif Org == 'CA Department of Water Resources':
        return 'DWR'
    elif Org == 'US Fish and Wildlife Service':
        return 'FWS'
    elif Org == 'Mountains Recreation and Conservation Authority':
        return 'MRCA'
    elif Org == 'National Park Service':
        return 'NPS'
    elif Org == 'Natural Resources Conservation Service':
        return 'NRCS'
    elif Org == 'Office of Energy Infrastructure Safety':
        return 'OEIS'
    elif Org == 'CA State Parks':
        return 'PARKS'
    elif Org == 'San Gabriel and Lower Los Angeles Rivers and Mountains Conservancy':
        return 'RMC'
    elif Org == 'State Coastal Conservancy':
        return 'SCC'
    elif Org == 'San Diego River Conservancy':
        return 'SDRC'
    elif Org == 'State Lands Commission':
        return 'SLC'
    elif Org == 'Santa Monica Mountains Conservancy':
        return 'SMMC'
    elif Org == 'Sierra Nevada Conservancy':
        return 'SNC'
    elif Org == 'Tahoe Conservancy':
        return 'TAHOE'
    elif Org == 'U.S. Forest Service':
        return 'USFS'
    elif Org == 'CA Wildlife Conservation Board':
        return 'WCB'
    elif Org == 'State Water Resources Control Board':
        return 'WRCB'
    elif Org == 'Other':
        return 'OTHER'
    else:
        return Org""")

    # Process: Calculate Residue (Calculate Field) (management)
    update_residue_fate = arcpy.management.CalculateField(in_table=update_tertiary_fund_src_name_2, 
                                                              field="RESIDUE_FATE", 
                                                              expression="ifelse(!RESIDUE_FATE!)", 
                                                              code_block="""def ifelse(Fate):
    if Fate == 'Biochar or Other Pyrolysis':
        return 'BIOCHAR_PYROLYSIS'
    elif Fate == 'Broadcast Burn':
        return 'BROADCAST_BURN'
    elif Fate == 'Chipping':
        return 'CHIPPING'
    elif Fate == 'Durable Products':
        return 'DURABLE_PRODUCTS'
    elif Fate == 'Firewood':
        return 'FIREWOOD'
    elif Fate == 'Landfill':
        return 'LANDFILL'
    elif Fate == 'Left on Site':
        return 'LEFT_ON_SITE'
    elif Fate == 'Liquid Fuels':
        return 'LIQUID_FUELS'
    elif Fate == 'Lop and Scatter':
        return 'LOP_SCATTER'
    elif Fate == 'No Residue/Not Applicable':
        return 'NO_RESIDUE/NOT_APPLICABLE'
    elif Fate == 'Offsite Bioenergy':
        return 'OFFSITE_BIOENERGY'
    elif Fate == 'Other':
        return 'OTHER'
    elif Fate == 'Pile Burning':
        return 'PILE_BURNING'
    elif Fate == 'Short-Lived Products':
        return 'SHORT-LIVED_PRODUCTS'
    elif Fate == 'Unknown':
        return 'UNKNOWN'
    else:
        return Fate""")

    # Process: Calculate Units (2) (Calculate Field) (management)
    update_residue_fate_units = arcpy.management.CalculateField(in_table=update_residue_fate, 
                                                              field="RESIDUE_FATE_UNITS", 
                                                              expression="ifelse(!RESIDUE_FATE_UNITS!)", 
                                                              code_block="""def ifelse(UOM):
    if UOM == 'Acres':
        return 'AC'
    elif UOM == 'Each':
        return 'EA'
    elif UOM == 'Hours':
        return 'HR'
    elif UOM == 'Miles':
        return 'MI'
    elif UOM == 'Other':
        return 'OTHER'
    elif UOM == 'Tons':
        return 'TON'
    else:
        return UOM""")

    # Process: Calculate Geometry Type (Calculate Field) (management)
    update_trmt_geom = arcpy.management.CalculateField(in_table=update_residue_fate_units, 
                                                              field="TRMT_GEOM", 
                                                              expression="ifelse(!TRMT_GEOM!)", 
                                                              code_block="""def ifelse(Geom):
    if Geom == 'Point':
        return 'POINT'
    elif Geom == 'Line':
        return 'LINE'
    elif Geom == 'Polygon':
        return 'POLYGON'
    elif Geom == 'No Shape':
        return 'NO SHAPE'
    else:
        return Geom""")

    # Process: Calculate Counts Towards (Calculate Field) (management)
    final_output = arcpy.management.CalculateField(in_table=update_trmt_geom, 
                                                              field="COUNTS_TO_MAS", 
                                                              expression="ifelse(!COUNTS_TO_MAS!)", 
                                                              code_block="""def ifelse(YN):
    if YN == 'Yes':
        return 'YES'
    elif YN == 'No':
        return 'NO'
    else:
        return YN
        """)

    return final_output

if __name__ == '__main__':
        runner(workspace,scratch_workspace,StandardizeDomains, '*argv[1:]')
    # Global Environment settings
    # with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True, 
    #                       qualifiedFieldNames=False, scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", transferGDBAttributeProperties=True, 
    #                       workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     StandardizeDomains(*argv[1:])
