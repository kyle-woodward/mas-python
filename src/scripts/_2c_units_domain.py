import arcpy
from sys import argv
import os
from .utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()


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


if __name__ == "__main__":
    runner(workspace, scratch_workspace, Units, "*argv[1:]")
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",
    # outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
    # preserveGlobalIds=True,
    # qualifiedFieldNames=False,
    # scratchWorkspace=scratch_workspace,
    # transferDomains=True,
    # transferGDBAttributeProperties=True,
    # workspace=workspace):
    #     Units(in_table=os.path.join(workspace,"StateParks_XY_enriched_20220708_modifiedAcres_1")) #testing on a dataset that i had edited the field's values back to 'Acres' from 'AC'
