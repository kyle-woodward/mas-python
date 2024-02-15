"""
# Description: Add ITS schema template fields to a table 
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts._1_assign_domains import AssignDomains
from scripts.utils import init_gdb

workspace, scratch_workspace = init_gdb()

def FieldExists(
    featureclass, fieldname
):  # Start if function to check if field exist
    fieldList = arcpy.ListFields(featureclass, fieldname)

    fieldCount = len(fieldList)

    if fieldCount == 1:
        return True
    else:
        return False


def AlterExisting(schema, featureclass):
    fieldnames = [i[0] for i in schema]
    types = [i[1] for i in schema]
    aliases = [i[2] for i in schema]
    lengths = [i[3] for i in schema]

    for name, type, alias, length in zip(fieldnames, types, aliases, lengths):
        if FieldExists(featureclass, name):
            print(f"field {name} Exists: altering it to {name}_")
            altered = arcpy.management.AlterField(
                in_table=featureclass,
                field=name,
                new_field_name=name + "_",
                new_field_alias="",
                field_type=type,
                field_length=length,
                field_is_nullable="NULLABLE",
                clear_field_alias="CLEAR_ALIAS",
            )
    # return altered # referenced before assignment error when if clause conditions never met, altered is never defined...
    return featureclass


def AddFields(Input_Table, alter_fields=False):
    """
    Adds a defined schema of fields to a feature class;

    Input_Table: input table or feature class
    alter_fields: if an original field in the dataset matches one of the new fields, alter it to 'FIELDNAME_'.
    """
    arcpy.env.overwriteOutput = True

    # Fields to add and their other settings passed to arcpy.management.AddFields()
    schema = [
        ["PROJECTID_USER", "TEXT", "PROJECT ID USER", "40", "", ""],
        ["AGENCY", "TEXT", "AGENCY_DEPARTMENT", "150", "", ""],
        ["ORG_ADMIN_p", "TEXT", "ORG DATA STEWARD", "150", "", ""],
        ["PROJECT_CONTACT", "TEXT", "PROJECT CONTACT", "100", "", ""],
        ["PROJECT_EMAIL", "TEXT", "PROJECT EMAIL", "100", "", ""],
        ["ADMINISTERING_ORG", "TEXT", "ADMINISTERING ORG", "150", "", ""],
        ["PROJECT_NAME", "TEXT", "PROJECT NAME", "150", "", ""],
        ["PROJECT_STATUS", "TEXT", "PROJECT STATUS", "25", "", ""],
        ["PROJECT_START", "DATE", "PROJECT START", "8", "", ""],
        ["PROJECT_END", "DATE", "PROJECT END", "8", "", ""],
        ["PRIMARY_FUNDING_SOURCE", "TEXT", "PRIMARY_FUNDING_SOURCE", "130", "", ""],
        ["PRIMARY_FUNDING_ORG", "TEXT", "PRIMARY_FUNDING_ORG", "130", "", ""],
        ["IMPLEMENTING_ORG", "TEXT", "IMPLEMENTING_ORG", "150", "", ""],
        ["LATITUDE", "DOUBLE", "LATITUDE CENTROID", "8", "", ""],
        ["LONGITUDE", "DOUBLE", "LONGITUDE CENTROID", "8", "", ""],
        ["BatchID_p", "TEXT", "Batch ID", "40", "", ""],
        ["Val_Status_p", "TEXT", "Validation Status", "15", "", ""],
        ["Val_Message_p", "TEXT", "Validation Message", "15", "", ""],
        ["Val_RunDate_p", "DATE", "Validation Run Date", "8", "", ""],
        ["Review_Status_p", "TEXT", "Review Status", "15", "", ""],
        ["Review_Message_p", "TEXT", "Review Message", "15", "", ""],
        ["Review_RunDate_p", "DATE", "Review Run Date", "8", "", ""],
        ["Dataload_Status_p", "TEXT", "Dataload Status", "15", "", ""],
        ["Dataload_Msg_p", "TEXT", "Dataload Message", "15", "", ""],
        ["TRMTID_USER", "TEXT", "TREATMENT ID USER", "50", "", ""],
        ["PROJECTID", "TEXT", "PROJECTID", "50", "", ""],
        ["PROJECTNAME_", "TEXT", "PROJECT NAME", "150", "", ""],
        ["ORG_ADMIN_t", "TEXT", "ORG DATA STEWARD", "150", "", ""],
        ["PRIMARY_OWNERSHIP_GROUP", "TEXT", "PRIMARY OWNERSHIP GROUP", "25", "", ""],
        ["PRIMARY_OBJECTIVE", "TEXT", "PRIMARY OBJECTIVE", "65", "", ""],
        ["SECONDARY_OBJECTIVE", "TEXT", "SECONDARY OBJECTIVE", "65", "", ""],
        ["TERTIARY_OBJECTIVE", "TEXT", "TERTIARY OBJECTIVE", "65", "", ""],
        ["TREATMENT_STATUS", "TEXT", "TREATMENT STATUS", "25", "", ""],
        ["COUNTY", "TEXT", "COUNTY", "35", "", ""],
        ["IN_WUI", "TEXT", "IN WUI", "30", "", ""],
        ["REGION", "TEXT", "TASK FORCE REGION", "25", "", ""],
        ["TREATMENT_AREA", "DOUBLE", "TREATMENT AREA (GIS ACRES)", "8", "", ""],
        ["TREATMENT_START", "DATE", "TREATMENT START", "8", "", ""],
        ["TREATMENT_END", "DATE", "TREATMENT END", "8", "", ""],
        ["RETREATMENT_DATE_EST", "DATE", "RETREATMENT DATE ESTIMATE", "8", "", ""],
        ["TREATMENT_NAME", "TEXT", "TREATMENT NAME", "150", "", ""],
        ["BatchID", "TEXT", "BATCH ID (TREATMENT)", "40", "", ""],
        ["Val_Status_t", "TEXT", "Validation Status", "15", "", ""],
        ["Val_Message_t", "TEXT", "Validation Message", "15", "", ""],
        ["Val_RunDate_t", "DATE", "Validation Run Date", "8", "", ""],
        ["Review_Status_t", "TEXT", "Review Status", "15", "", ""],
        ["Review_Message_t", "TEXT", "Review Message", "15", "", ""],
        ["Review_RunDate_t", "DATE", "Review Run Date", "8", "", ""],
        ["Dataload_Status_t", "TEXT", "Dataload Status", "15", "", ""],
        ["Dataload_Msg_t", "TEXT", "Dataload Message", "15", "", ""],
        ["ACTIVID_USER", "TEXT", "ACTIVITYID USER", "50", "", ""],
        ["TREATMENTID_", "TEXT", "TREATMENTID", "50", "", ""],
        ["ORG_ADMIN_a", "TEXT", "ORG DATA STEWARD", "150", "", ""],
        ["ACTIVITY_DESCRIPTION", "TEXT", "ACTIVITY DESCRIPTION", "70", "", ""],
        ["ACTIVITY_CAT", "TEXT", "ACTIVITY CATEGORY", "40", "", ""],
        ["BROAD_VEGETATION_TYPE", "TEXT", "BROAD VEGETATION TYPE", "50", "", ""],
        ["BVT_USERD", "TEXT", "IS BVT USER DEFINED", "3", "", ""],
        ["ACTIVITY_STATUS", "TEXT", "ACTIVITY STATUS", "25", "", ""],
        ["ACTIVITY_QUANTITY", "DOUBLE", "ACTIVITY QUANTITY", "8", "", ""],
        ["ACTIVITY_UOM", "TEXT", "ACTIVITY UNITS", "15", "", ""],
        ["ACTIVITY_START", "DATE", "ACTIVITY START", "8", "", ""],
        ["ACTIVITY_END", "DATE", "ACTIVITY END", "8", "", ""],
        ["ADMIN_ORG_NAME", "TEXT", "ADMINISTRATION ORGANIZATION NAME", "150", "", ""],
        ["IMPLEM_ORG_NAME", "TEXT", "IMPLEMENTATION ORGANIZATION NAME", "150", "", ""],
        ["PRIMARY_FUND_SRC_NAME", "TEXT", "PRIMARY FUND SOURCE NAME", "100", "", ""],
        ["PRIMARY_FUND_ORG_NAME","TEXT","PRIMARY FUND ORGANIZATION NAME","100","","",],
        ["SECONDARY_FUND_SRC_NAME","TEXT","SECONDARY FUND SOURCE NAME","100","","",],
        ["SECONDARY_FUND_ORG_NAME","TEXT","SECONDARY FUND ORGANIZATION NAME","100","","",],
        ["TERTIARY_FUND_SRC_NAME", "TEXT", "TERTIARY FUND SOURCE NAME", "100", "", ""],
        ["TERTIARY_FUND_ORG_NAME","TEXT","TERTIARY FUND ORGANIZATION NAME","100","","",],
        ["ACTIVITY_PRCT", "SHORT", "ACTIVITY PERCENT", "3", "", ""],
        ["RESIDUE_FATE", "TEXT", "RESIDUE FATE", "35", "", ""],
        ["RESIDUE_FATE_QUANTITY", "DOUBLE", "RESIDUE FATE QUANTITY", "8", "", ""],
        ["RESIDUE_FATE_UNITS", "TEXT", "RESIDUE FATE UNITS", "5", "", ""],
        ["ACTIVITY_NAME", "TEXT", "ACTIVITY NAME", "150", "", ""],
        ["VAL_STATUS_a", "TEXT", "VALIDATION STATUS", "15", "", ""],
        ["VAL_MSG_a", "TEXT", "VALIDATION MESSAGE", "15", "", ""],
        ["VAL_RUNDATE_a", "DATE", "VALIDATION RUN DATE", "8", "", ""],
        ["REVIEW_STATUS_a", "TEXT", "REVIEW STATUS", "15", "", ""],
        ["REVIEW_MSG_a", "TEXT", "REVIEW MESSAGE", "15", "", ""],
        ["REVIEW_RUNDATE_a", "DATE", "REVIEW RUN DATE", "8", "", ""],
        ["DATALOAD_STATUS_a", "TEXT", "DATALOAD STATUS", "15", "", ""],
        ["DATALOAD_MSG_a", "TEXT", "DATALOAD MESSAGE", "15", "", ""],
        ["Source", "TEXT", "Source", "65", "", ""],
        ["Year", "LONG", "Calendar Year", "", "", ""],
        ["Year_txt", "TEXT", "Year as Text", "4", "", ""],
        ["Act_Code", "LONG", "USFS Activity Code", "", "", ""],
        ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""],
        ["Federal_FY", "LONG", "Federal FY", "", "", ""],
        ["State_FY", "LONG", "State FY", "", "", ""],
        ["TRMT_GEOM", "TEXT", "TREATMENT GEOMETRY", "10", "", ""],
        ["COUNTS_TO_MAS", "TEXT", "COUNTS TOWARDS MAS", "3", "", ""],
    ]

    # alter existing fields found in schema
    if alter_fields:
        altered = AlterExisting(schema, Input_Table)

    add_fields = arcpy.management.AddFields(
        in_table=Input_Table, field_description=schema
    )

    Assign_Domains_ = AssignDomains(in_table=add_fields)

    return Assign_Domains_

