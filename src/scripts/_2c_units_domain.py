"""
# Description: superceeded by 2j? 
#               
#               
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
# from sys import argv
# import os
from .utils import init_gdb #, runner
# TODO add print steps, rename variables
workspace, scratch_workspace = init_gdb()


def Units(in_table):  # 2c Units Domain
    arcpy.env.overwriteOutput = True

    # Process: Calculate Unit of Measure (Calculate Field) (management)
    calculatedUOM = arcpy.management.CalculateField(
        in_table=in_table,
        field="ACTIVITY_UOM",
        expression="ifelse(!ACTIVITY_UOM!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(Units):
    if Units == \"acres\":
        return \"AC\"
    elif Units == \"ACRES\":
        return \"AC\"
    elif Units == \"Acres\":
        return \"AC\"
    elif Units == \"ACRE\":
        return \"AC\"
    elif Units == \"miles\":
        return \"MI\"
    elif Units == \"each\":
        return \"EA\"
    elif Units == \"Each\":
        return \"EA\"
    else:
        return Units""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )
    return calculatedUOM
