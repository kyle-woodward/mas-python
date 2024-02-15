"""
# Description: Standardizes domain values for OEIS utility datasets
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def UtilityVegTreat(Input_Table):
    arcpy.env.overwriteOutput = True

    Updated_Input_Table = arcpy.management.CalculateField(
        in_table=Input_Table,
        field="UtilityID",
        expression="ifelse(!UtilityID!)",
        code_block="""def ifelse(ID):
                        if ID == \"SDG&E\":
                            return \"SDGE\"
                        else:
                            return ID""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    Output_Table = arcpy.management.CalculateField(
        in_table=Updated_Input_Table,
        field="VegetationTreatmentType",
        expression="ifelse(!VegetationTreatmentType!)",
        code_block="""def ifelse(TY):
                    #    if TY.find(\"Pole%\"):
                        if 'tandard' in TY:
                            return 'Radial clearance - standard'
                        elif 'nhance' in TY:
                            return 'Radial clearance - enhanced'
                        elif 'hang' in TY:
                            return 'Overhang clearing'
                        elif 'ole' in TY:
                            return 'Pole Brushing'
                        elif 'azard' in TY:
                            return 'Tree removal - hazard tree'
                        elif 'ortal' in TY:
                            return 'Tree removal - tree mortality'
                        elif 'rimming' in TY:
                            return 'Tree trimming'
                        elif 'reak' in TY:
                            return 'Fire break creation'
                        elif 'rush' in TY:
                            return 'Brush clearance'
                        elif 'ult' in TY:
                            return 'Other or multiple treatment types - see comment'
                        else:
                            return TY""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    return Output_Table

