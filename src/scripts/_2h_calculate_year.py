"""
# Description: 
#               
#               
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
# import os
# from sys import argv
from scripts.utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()

def Year(Year_Input):  # 2h Calculate Year
    arcpy.env.overwriteOutput = True

    # Process: Calculate Calendar Year (Calculate Field) (management)
    year_calculated = arcpy.management.CalculateField(
        in_table=Year_Input,
        field="Year",
        expression="Year($feature.ACTIVITY_END)",
        expression_type="ARCADE",
        code_block="",
        field_type="LONG",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Year as Text (Calculate Field) (management)
    year_txt_calculated = arcpy.management.CalculateField(
        in_table=year_calculated,
        field="Year_txt",
        expression="!Year!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Fed FY (Calculate Field) (management)
    #TODO simplify code block
    year_fed_fy = arcpy.management.CalculateField(
        in_table=year_txt_calculated,
        field="Federal_FY",
        expression="ifelse(!ACTIVITY_END!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(DATE): 
            if DATE is None:
                return None
            elif DATE >= datetime.datetime(1994,10,1) and DATE < datetime.datetime(1995,10,1):
                return 1995
            elif DATE >= datetime.datetime(1995,10,1) and DATE < datetime.datetime(1996,10,1):
                return 1996
            elif DATE >= datetime.datetime(1996,10,1) and DATE < datetime.datetime(1997,10,1):
                return 1997
            elif DATE >= datetime.datetime(1997,10,1) and DATE < datetime.datetime(1998,10,1):
                return 1998
            elif DATE >= datetime.datetime(1998,10,1) and DATE < datetime.datetime(1999,10,1):
                return 1999
            elif DATE >= datetime.datetime(1999,10,1) and DATE < datetime.datetime(2000,10,1):
                return 2000
            elif DATE >= datetime.datetime(2000,10,1) and DATE < datetime.datetime(2001,10,1):
                return 2001
            elif DATE >= datetime.datetime(2001,10,1) and DATE < datetime.datetime(2002,10,1):
                return 2002
            elif DATE >= datetime.datetime(2002,10,1) and DATE < datetime.datetime(2003,10,1):
                return 2003
            elif DATE >= datetime.datetime(2003,10,1) and DATE < datetime.datetime(2004,10,1):
                return 2004
            elif DATE >= datetime.datetime(2004,10,1) and DATE < datetime.datetime(2005,10,1):
                return 2005
            elif DATE >= datetime.datetime(2005,10,1) and DATE < datetime.datetime(2006,10,1):
                return 2006
            elif DATE >= datetime.datetime(2006,10,1) and DATE < datetime.datetime(2007,10,1):
                return 2007
            elif DATE >= datetime.datetime(2007,10,1) and DATE < datetime.datetime(2008,10,1):
                return 2008
            elif DATE >= datetime.datetime(2008,10,1) and DATE < datetime.datetime(2009,10,1):
                return 2009
            elif DATE >= datetime.datetime(2009,10,1) and DATE < datetime.datetime(2010,10,1):
                return 2010
            elif DATE >= datetime.datetime(2010,10,1) and DATE < datetime.datetime(2011,10,1):
                return 2011
            elif DATE >= datetime.datetime(2011,10,1) and DATE < datetime.datetime(2012,10,1):
                return 2012
            elif DATE >= datetime.datetime(2012,10,1) and DATE < datetime.datetime(2013,10,1):
                return 2013
            elif DATE >= datetime.datetime(2013,10,1) and DATE < datetime.datetime(2014,10,1):
                return 2014
            elif DATE >= datetime.datetime(2014,10,1) and DATE < datetime.datetime(2015,10,1):
                return 2015
            elif DATE >= datetime.datetime(2015,10,1) and DATE < datetime.datetime(2016,10,1):
                return 2016
            elif DATE >= datetime.datetime(2016,10,1) and DATE < datetime.datetime(2017,10,1):
                return 2017
            elif DATE >= datetime.datetime(2017,10,1) and DATE < datetime.datetime(2018,10,1):
                return 2018
            elif DATE >= datetime.datetime(2018,10,1) and DATE < datetime.datetime(2019,10,1):
                return 2019
            elif DATE >= datetime.datetime(2019,10,1) and DATE < datetime.datetime(2020,10,1):
                return 2020
            elif DATE >= datetime.datetime(2020,10,1) and DATE < datetime.datetime(2021,10,1):
                return 2021
            elif DATE >= datetime.datetime(2021,10,1) and DATE < datetime.datetime(2022,10,1):
                return 2022
            elif DATE >= datetime.datetime(2022,10,1) and DATE < datetime.datetime(2023,10,1):
                return 2023
            elif DATE >= datetime.datetime(2023,10,1) and DATE < datetime.datetime(2024,10,1):
                return 2024
            elif DATE >= datetime.datetime(2024,10,1) and DATE < datetime.datetime(2025,10,1):
                return 2025
            elif DATE >= datetime.datetime(2025,10,1) and DATE < datetime.datetime(2026,10,1):
                return 2026
            else:
                return None""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate State FY (Calculate Field) (management)
    #TODO simplify code block
    year_final = arcpy.management.CalculateField(
        in_table=year_fed_fy,
        field="State_FY",
        expression="ifelse(!ACTIVITY_END!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(DATE):
            if DATE is None:
                return None
            elif DATE >= datetime.datetime(1994,7,1) and DATE < datetime.datetime(1995,7,1):
                return 1995
            elif DATE >= datetime.datetime(1995,7,1) and DATE < datetime.datetime(1996,7,1):
                return 1996
            elif DATE >= datetime.datetime(1996,7,1) and DATE < datetime.datetime(1997,7,1):
                return 1997
            elif DATE >= datetime.datetime(1997,7,1) and DATE < datetime.datetime(1998,7,1):
                return 1998
            elif DATE >= datetime.datetime(1998,7,1) and DATE < datetime.datetime(1999,7,1):
                return 1999
            elif DATE >= datetime.datetime(1999,7,1) and DATE < datetime.datetime(2000,7,1):
                return 2000
            elif DATE >= datetime.datetime(2000,7,1) and DATE < datetime.datetime(2001,7,1):
                return 2001
            elif DATE >= datetime.datetime(2001,7,1) and DATE < datetime.datetime(2002,7,1):
                return 2002
            elif DATE >= datetime.datetime(2002,7,1) and DATE < datetime.datetime(2003,7,1):
                return 2003
            elif DATE >= datetime.datetime(2003,7,1) and DATE < datetime.datetime(2004,7,1):
                return 2004
            elif DATE >= datetime.datetime(2004,7,1) and DATE < datetime.datetime(2005,7,1):
                return 2005
            elif DATE >= datetime.datetime(2005,7,1) and DATE < datetime.datetime(2006,7,1):
                return 2006
            elif DATE >= datetime.datetime(2006,7,1) and DATE < datetime.datetime(2007,7,1):
                return 2007
            elif DATE >= datetime.datetime(2007,7,1) and DATE < datetime.datetime(2008,7,1):
                return 2008
            elif DATE >= datetime.datetime(2008,7,1) and DATE < datetime.datetime(2009,7,1):
                return 2009
            elif DATE >= datetime.datetime(2009,7,1) and DATE < datetime.datetime(2010,7,1):
                return 2010
            elif DATE >= datetime.datetime(2010,7,1) and DATE < datetime.datetime(2011,7,1):
                return 2011
            elif DATE >= datetime.datetime(2011,7,1) and DATE < datetime.datetime(2012,7,1):
                return 2012
            elif DATE >= datetime.datetime(2012,7,1) and DATE < datetime.datetime(2013,7,1):
                return 2013
            elif DATE >= datetime.datetime(2013,7,1) and DATE < datetime.datetime(2014,7,1):
                return 2014
            elif DATE >= datetime.datetime(2014,7,1) and DATE < datetime.datetime(2015,7,1):
                return 2015
            elif DATE >= datetime.datetime(2015,7,1) and DATE < datetime.datetime(2016,7,1):
                return 2016
            elif DATE >= datetime.datetime(2016,7,1) and DATE < datetime.datetime(2017,7,1):
                return 2017
            elif DATE >= datetime.datetime(2017,7,1) and DATE < datetime.datetime(2018,7,1):
                return 2018
            elif DATE >= datetime.datetime(2018,7,1) and DATE < datetime.datetime(2019,7,1):
                return 2019
            elif DATE >= datetime.datetime(2019,7,1) and DATE < datetime.datetime(2020,7,1):
                return 2020
            elif DATE >= datetime.datetime(2020,7,1) and DATE < datetime.datetime(2021,7,1):
                return 2021
            elif DATE >= datetime.datetime(2021,7,1) and DATE < datetime.datetime(2022,7,1):
                return 2022
            elif DATE >= datetime.datetime(2022,7,1) and DATE < datetime.datetime(2023,7,1):
                return 2023
            elif DATE >= datetime.datetime(2023,7,1) and DATE < datetime.datetime(2024,7,1):
                return 2024
            elif DATE >= datetime.datetime(2024,7,1) and DATE < datetime.datetime(2025,7,1):
                return 2025
            elif DATE >= datetime.datetime(2025,7,1) and DATE < datetime.datetime(2026,7,1):
                return 2026
            else:
                return None""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    return year_final


# if __name__ == "__main__":
#     runner(workspace,scratch_workspace,Year, *argv[1:])
#     # Global Environment settings
#     with arcpy.EnvManager(
#         extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",
#         outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
#         preserveGlobalIds=True,
#         qualifiedFieldNames=False,
#         scratchWorkspace=scratch_workspace,
#         transferDomains=True,
#         transferGDBAttributeProperties=True,
#         workspace=workspace,
#     ):
#         Year(Input_Table=os.path.join(workspace, "WFR_TF_Template"))
