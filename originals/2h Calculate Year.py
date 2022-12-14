# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:14:10
"""
import arcpy
from sys import argv

def Year(Input_Table):  # 2h Calculate Year

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Calculate Calendar Year (Calculate Field) (management)
    Updated_Input_Table_5_ = arcpy.management.CalculateField(in_table=Input_Table, field="Year", expression="Year($feature.ACTIVITY_END)", expression_type="ARCADE", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Year as Text (Calculate Field) (management)
    Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_5_, field="Year_txt", expression="!Year!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Fed FY (Calculate Field) (management)
    Veg_Summarized_Polygons_Laye3_8_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_6_, field="Federal_FY", expression="ifelse(!ACTIVITY_END!)", expression_type="PYTHON3", code_block="""def ifelse(DATE):
    if DATE >= datetime.datetime(1994,10,1) and DATE <= datetime.datetime(1995,9,30):
        return 1995
    elif DATE >= datetime.datetime(1995,10,1) and DATE <= datetime.datetime(1996,9,30):
        return 1996
    elif DATE >= datetime.datetime(1996,10,1) and DATE <= datetime.datetime(1997,9,30):
        return 1997
    elif DATE >= datetime.datetime(1997,10,1) and DATE <= datetime.datetime(1998,9,30):
        return 1998
    elif DATE >= datetime.datetime(1998,10,1) and DATE <= datetime.datetime(1999,9,30):
        return 1999
    elif DATE >= datetime.datetime(1999,10,1) and DATE <= datetime.datetime(2000,9,30):
        return 2000
    elif DATE >= datetime.datetime(2000,10,1) and DATE <= datetime.datetime(2001,9,30):
        return 2001
    elif DATE >= datetime.datetime(2001,10,1) and DATE <= datetime.datetime(2002,9,30):
        return 2002
    elif DATE >= datetime.datetime(2002,10,1) and DATE <= datetime.datetime(2003,9,30):
        return 2003
    elif DATE >= datetime.datetime(2003,10,1) and DATE <= datetime.datetime(2004,9,30):
        return 2004
    elif DATE >= datetime.datetime(2004,10,1) and DATE <= datetime.datetime(2005,9,30):
        return 2005
    elif DATE >= datetime.datetime(2005,10,1) and DATE <= datetime.datetime(2006,9,30):
        return 2006
    elif DATE >= datetime.datetime(2006,10,1) and DATE <= datetime.datetime(2007,9,30):
        return 2007
    elif DATE >= datetime.datetime(2007,10,1) and DATE <= datetime.datetime(2008,9,30):
        return 2008
    elif DATE >= datetime.datetime(2008,10,1) and DATE <= datetime.datetime(2009,9,30):
        return 2009
    elif DATE >= datetime.datetime(2009,10,1) and DATE <= datetime.datetime(2010,9,30):
        return 2010
    elif DATE >= datetime.datetime(2010,10,1) and DATE <= datetime.datetime(2011,9,30):
        return 2011
    elif DATE >= datetime.datetime(2011,10,1) and DATE <= datetime.datetime(2012,9,30):
        return 2012
    elif DATE >= datetime.datetime(2012,10,1) and DATE <= datetime.datetime(2013,9,30):
        return 2013
    elif DATE >= datetime.datetime(2013,10,1) and DATE <= datetime.datetime(2014,9,30):
        return 2014
    elif DATE >= datetime.datetime(2014,10,1) and DATE <= datetime.datetime(2015,9,30):
        return 2015
    elif DATE >= datetime.datetime(2015,10,1) and DATE <= datetime.datetime(2016,9,30):
        return 2016
    elif DATE >= datetime.datetime(2016,10,1) and DATE <= datetime.datetime(2017,9,30):
        return 2017
    elif DATE >= datetime.datetime(2017,10,1) and DATE <= datetime.datetime(2018,9,30):
        return 2018
    elif DATE >= datetime.datetime(2018,10,1) and DATE <= datetime.datetime(2019,9,30):
        return 2019
    elif DATE >= datetime.datetime(2019,10,1) and DATE <= datetime.datetime(2020,9,30):
        return 2020
    elif DATE >= datetime.datetime(2020,10,1) and DATE <= datetime.datetime(2021,9,30):
        return 2021
    elif DATE >= datetime.datetime(2021,10,1) and DATE <= datetime.datetime(2022,9,30):
        return 2022
    elif DATE >= datetime.datetime(2022,10,1) and DATE <= datetime.datetime(2023,9,30):
        return 2023
    elif DATE >= datetime.datetime(2023,10,1) and DATE <= datetime.datetime(2024,9,30):
        return 2024
    elif DATE >= datetime.datetime(2024,10,1) and DATE <= datetime.datetime(2025,9,30):
        return 2025
    elif DATE >= datetime.datetime(2025,10,1) and DATE <= datetime.datetime(2026,9,30):
        return 2026
    else:
        return None""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate State FY (Calculate Field) (management)
    Veg_Summarized_Polygons_Laye3_7_ = arcpy.management.CalculateField(in_table=Veg_Summarized_Polygons_Laye3_8_, field="State_FY", expression="ifelse(!ACTIVITY_END!)", expression_type="PYTHON3", code_block="""def ifelse(DATE):
    if DATE >= datetime.datetime(1994,7,1) and DATE <= datetime.datetime(1995,6,30):
        return 1995
    elif DATE >= datetime.datetime(1995,7,1) and DATE <= datetime.datetime(1996,6,30):
        return 1996
    elif DATE >= datetime.datetime(1996,7,1) and DATE <= datetime.datetime(1997,6,30):
        return 1997
    elif DATE >= datetime.datetime(1997,7,1) and DATE <= datetime.datetime(1998,6,30):
        return 1998
    elif DATE >= datetime.datetime(1998,7,1) and DATE <= datetime.datetime(1999,6,30):
        return 1999
    elif DATE >= datetime.datetime(1999,7,1) and DATE <= datetime.datetime(2000,6,30):
        return 2000
    elif DATE >= datetime.datetime(2000,7,1) and DATE <= datetime.datetime(2001,6,30):
        return 2001
    elif DATE >= datetime.datetime(2001,7,1) and DATE <= datetime.datetime(2002,6,30):
        return 2002
    elif DATE >= datetime.datetime(2002,7,1) and DATE <= datetime.datetime(2003,6,30):
        return 2003
    elif DATE >= datetime.datetime(2003,7,1) and DATE <= datetime.datetime(2004,6,30):
        return 2004
    elif DATE >= datetime.datetime(2004,7,1) and DATE <= datetime.datetime(2005,6,30):
        return 2005
    elif DATE >= datetime.datetime(2005,7,1) and DATE <= datetime.datetime(2006,6,30):
        return 2006
    elif DATE >= datetime.datetime(2006,7,1) and DATE <= datetime.datetime(2007,6,30):
        return 2007
    elif DATE >= datetime.datetime(2007,7,1) and DATE <= datetime.datetime(2008,6,30):
        return 2008
    elif DATE >= datetime.datetime(2008,7,1) and DATE <= datetime.datetime(2009,6,30):
        return 2009
    elif DATE >= datetime.datetime(2009,7,1) and DATE <= datetime.datetime(2010,6,30):
        return 2010
    elif DATE >= datetime.datetime(2010,7,1) and DATE <= datetime.datetime(2011,6,30):
        return 2011
    elif DATE >= datetime.datetime(2011,7,1) and DATE <= datetime.datetime(2012,6,30):
        return 2012
    elif DATE >= datetime.datetime(2012,7,1) and DATE <= datetime.datetime(2013,6,30):
        return 2013
    elif DATE >= datetime.datetime(2013,7,1) and DATE <= datetime.datetime(2014,6,30):
        return 2014
    elif DATE >= datetime.datetime(2014,7,1) and DATE <= datetime.datetime(2015,6,30):
        return 2015
    elif DATE >= datetime.datetime(2015,7,1) and DATE <= datetime.datetime(2016,6,30):
        return 2016
    elif DATE >= datetime.datetime(2016,7,1) and DATE <= datetime.datetime(2017,6,30):
        return 2017
    elif DATE >= datetime.datetime(2017,7,1) and DATE <= datetime.datetime(2018,6,30):
        return 2018
    elif DATE >= datetime.datetime(2018,7,1) and DATE <= datetime.datetime(2019,6,30):
        return 2019
    elif DATE >= datetime.datetime(2019,7,1) and DATE <= datetime.datetime(2020,6,30):
        return 2020
    elif DATE >= datetime.datetime(2020,7,1) and DATE <= datetime.datetime(2021,6,30):
        return 2021
    elif DATE >= datetime.datetime(2021,7,1) and DATE <= datetime.datetime(2022,6,30):
        return 2022
    elif DATE >= datetime.datetime(2022,7,1) and DATE <= datetime.datetime(2023,6,30):
        return 2023
    elif DATE >= datetime.datetime(2023,7,1) and DATE <= datetime.datetime(2024,6,30):
        return 2024
    elif DATE >= datetime.datetime(2024,7,1) and DATE <= datetime.datetime(2025,6,30):
        return 2025
    elif DATE >= datetime.datetime(2025,7,1) and DATE <= datetime.datetime(2026,6,30):
        return 2026
    else:
        return None""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    return Veg_Summarized_Polygons_Laye3_7_

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]", outputCoordinateSystem="PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]", preserveGlobalIds=True, 
                          qualifiedFieldNames=False, scratchWorkspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\scratch.gdb", transferDomains=True, 
                          transferGDBAttributeProperties=True, workspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\PC414 CWI Million Acres.gdb"):
        Year(*argv[1:])
