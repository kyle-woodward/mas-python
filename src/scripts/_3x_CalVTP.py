"""
# Description: Converts the California Board of Forestry and Fire Protection's 
#              Vegetation Treatment Program (CalVTP) dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.            
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""

import datetime

start1 = datetime.datetime.now()
print(f"Start Time {start1}")

import os
import arcpy
from scripts._1_add_fields import AddFields
from scripts._1_assign_domains import AssignDomains
from scripts._3_enrichments_polygon import enrich_polygons
from scripts.utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def CalVTP(CalVTP_enriched, 
           CalVTP_standardized, 
           CalVTP_OG, 
           delete_scratch=True
           ):

    with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace,
        outputCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),  # WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),  # WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'",
        preserveGlobalIds=True,
        qualifiedFieldNames=False,
        transferDomains=False,
        transferGDBAttributeProperties=False,
        overwriteOutput=True,
    ):

        # define intermediary objects in scratch
        CALVTP_select_2 = os.path.join(scratch_workspace, "CALVTP_Copy")
        enriched_scratch = os.path.join(scratch_workspace, "enriched_scratch")

        ### BEGIN TOOL CHAIN
        print("step 1/30 select layer by attribute...")
        select_1 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=CalVTP_OG, 
            where_clause="Affiliation = 'non-CAL FIRE'"
        )

        print("step 2/30 select...")
        select_2 = arcpy.analysis.Select(
            in_features=select_1,
            out_feature_class=CALVTP_select_2,
            where_clause="DATE_COMPLETED IS NOT NULL",
        )

        Count1 = arcpy.management.GetCount(CALVTP_select_2)
        print("selected features have {} records".format(Count1[0]))

        print("step 3/30 repair geometry...")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=select_2, delete_null="KEEP_NULL"
        )

        print("step 4/30 alter field...")
        alter_field_1 = arcpy.management.AlterField(
            in_table=repair_geom_1, field="County", new_field_name="County_"
        )

        print("step 5/30 add fields...")
        add_fields_1 = AddFields(Input_Table=alter_field_1)

        print("step 6/30 calculate field...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=add_fields_1,
            field="PROJECTID_USER",
            expression="!PROJECT_ID!",
        )

        print("step 7/30 calculate field...")
        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1, 
            field="AGENCY", 
            expression='"CNRA"'
        )

        print("step 8/30 calculate field...")
        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2, 
            field="ORG_ADMIN_p", 
            expression='"BOF"'
        )

        print("step 9/30 calculate field...")
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="PROJECT_CONTACT",
            expression='"Kristina Wolf"'
        )

        print("step 10/30 calculate field...")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="PROJECT_EMAIL",
            expression='"Kristina.Wolf@bof.ca.gov"'
        )

        print("step 11/30 calculate field...")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="ADMINISTERING_ORG",
            expression='"BOF"'
        )

        print("step 12/30 calculate field...")
        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PRIMARY_FUNDING_SOURCE",
            expression="ifelse(!GRANT_TYPE!)",
            code_block="""def ifelse(Fund):
                            if Fund == \"1\":
                                return \"CAL FIRE Forest Health\"
                            elif Fund == \"CAL FIRE Forest Health Grant\":
                                return \"CAL FIRE Forest Health\"    
                            elif Fund == \"2\":
                                return \"CAL FIRE Fire Prevention\"
                            elif Fund == \"3\":
                                return \"CAL FIRE Urban Forestry\"
                            else:
                                return Fund"""
        )

        print("step 13/30 calculate field...")
        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="PRIMARY_FUNDING_ORG",
            expression='"BOF"',
        )

        print("step 14/30 calculate field...")
        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PRIMARY_OBJECTIVE",
            expression="elseif(!Treatment_Type!)",
            code_block="""def elseif(Treat):
                            if Treat == \"1\":
                                return \"FUEL_BREAK\"
                            elif Treat == \"2\":
                                return \"FUEL_BREAK\"
                            elif Treat == \"3\":
                                return \"ECO_RESTOR\"
                            else:
                                return Treat"""
        )

        print("step 15/30 calculate field...")
        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9, 
            field="IMPLEMENTING_ORG", 
            expression='"BOF"'
        )

        print("step 16/30 calculkate geometry attributes...")
        calc_geom_1 = arcpy.management.CalculateGeometryAttributes(
            in_features=calc_field_10,
            geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]],
            coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
            coordinate_format="DD",
        )

        print("step 17/30 calculate geometry attributes...")
        calc_geom_2 = arcpy.management.CalculateGeometryAttributes(
            in_features=calc_geom_1,
            geometry_property=[["TREATMENT_AREA", "AREA"]],
            area_unit="ACRES_US",
        )

        print("step 18/30 calculate field...")
        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_geom_2,
            field="BROAD_VEGETATION_TYPE",
            expression="ifelse(!Fuel_Type!)",
            code_block="""def ifelse(Veg):
                            if Veg == \"1\":
                                return \"GRASS_HERB\"
                            elif Veg == \"2\":
                                return \"SHRB_CHAP\"
                            elif Veg == \"3\":
                                return \"FOREST\"
                            else:
                                return Veg"""
        )

        print("step 19/30 calculate field...")
        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="ACTIVITY_STATUS",
            expression="ifelse(!Status!)",
            code_block="""def ifelse(Status):
                            if Status == \"1\":
                                return \"PLANNED\"
                            elif Status == \"2\":
                                return \"ACTIVE\"
                            elif Status == \"3\":
                                return \"COMPLETE\"
                            elif Status == \"4\":
                                return \"PROPOSED\"
                            else:
                                return Status"""
        )

        print("step 20/30 calculate field...")
        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="ACTIVITY_QUANTITY",
            expression="!Treatment_Acres!"
        )

        print("step 21/30 calculate field...")
        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13, 
            field="ACTIVITY_UOM", 
            expression='"AC"'
        )

        print("step 22/30 calculate field...")
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="ACTIVITY_END",
            expression="!DATE_COMPLETED!"
        )

        print("step 23/30 calculate field...")
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15, 
            field="Source", 
            expression='"calvtp"'
        )

        print("step 24/30 calculate field...")
        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="Crosswalk",
            expression="ifelse(!TREATMENT_ACTIVITY!)",
            code_block="""def ifelse(Act):
                            if Act == \"1\":
                                return \"Prescribed Fire (Broadcast)\"
                            elif Act == \"2\":
                                return \"Prescribed Fire (Pile Burning)\"
                            elif Act == \"3\":
                                return \"Mechanical Treatment\"
                            elif Act == \"4\":
                                return \"Manual Treatment\"
                            else:
                                return Act
                            """
        )

        print("step 25/30 copy features...")
        standardized_1 = arcpy.management.CopyFeatures(
            in_features=calc_field_17, out_feature_class=CalVTP_standardized
        )

        Count2 = arcpy.management.GetCount(standardized_1)
        print("standardized haa {} records".format(Count2[0]))

        print("step 27/30 enrich polygons...")
        enrich_polygons(
            enrich_in=standardized_1,
            enrich_out=enriched_scratch
        )

        print("step 28/30 copy features...")
        arcpy.management.CopyFeatures(
            in_features=enriched_scratch, 
            out_feature_class=CalVTP_enriched
        )

        Count3 = arcpy.management.GetCount(CalVTP_enriched)
        print("enriched haa {} records".format(Count3[0]))

        print("step 29/30 calculate field...")
        calc_field_18 = arcpy.management.CalculateField(
            in_table=CalVTP_enriched,
            field="TRMTID_USER",
            expression="!PROJECTID_USER![:7]+'-'+(!IN_WUI![:3])+'-'+(!PRIMARY_OWNERSHIP_GROUP![:1])",
        )

        print("step 30/30 assign domains...")
        AssignDomains(in_table=calc_field_18)

        print(" complete...")

        if delete_scratch:
            print("Deleting Scratch Files")
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )
