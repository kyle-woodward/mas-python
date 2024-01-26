"""
# Description: Assign domains to ITS schema fields
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts.utils import init_gdb

original_gdb, workspace, scratch_workspace = init_gdb()

def AssignDomains(in_table):  # 2b Assign Domains
    arcpy.env.overwriteOutput = True

    # Process: Assign Domain To AGENCY Field (Assign Domain To Field) (management)
    D_ORGANIZATION = arcpy.management.AssignDomainToField(
        in_table=in_table, field_name="AGENCY", domain_name="D_AGENCY", subtype_code=[]
    )

    # Process: Assign Domain To ORG_ADMIN_p Field (Assign Domain To Field) (management)
    ORG_ADMIN_p = arcpy.management.AssignDomainToField(
        in_table=D_ORGANIZATION,
        field_name="ORG_ADMIN_p",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To ADMINISTERING_ORG Field (Assign Domain To Field) (management)
    ADMINISTERING_ORG = arcpy.management.AssignDomainToField(
        in_table=ORG_ADMIN_p,
        field_name="ADMINISTERING_ORG",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To PROJECT_STATUS Field (Assign Domain To Field) (management)
    PROJECT_STATUS = arcpy.management.AssignDomainToField(
        in_table=ADMINISTERING_ORG,
        field_name="PROJECT_STATUS",
        domain_name="D_STATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To PRIMARY_FUNDING_SOURCE Field (Assign Domain To Field) (management)
    PRIMARY_FUNDING_SOURCE = arcpy.management.AssignDomainToField(
        in_table=PROJECT_STATUS,
        field_name="PRIMARY_FUNDING_SOURCE",
        domain_name="D_FNDSRC",
        subtype_code=[],
    )

    # Process: Assign Domain To PRIMARY_FUNDING_ORG Field (Assign Domain To Field) (management)
    PRIMARY_FUNDING_ORG = arcpy.management.AssignDomainToField(
        in_table=PRIMARY_FUNDING_SOURCE,
        field_name="PRIMARY_FUNDING_ORG",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To VAL_STATUS_p Field (Assign Domain To Field) (management)
    Val_Status_p = arcpy.management.AssignDomainToField(
        in_table=PRIMARY_FUNDING_ORG,
        field_name="Val_Status_p",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To VAL_MSG_p Field (Assign Domain To Field) (management)
    Val_Message_p = arcpy.management.AssignDomainToField(
        in_table=Val_Status_p,
        field_name="Val_Message_p",
        domain_name="D_VERFIEDMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To REVIEW_STATUS_p Field (Assign Domain To Field) (management)
    Review_Status_p = arcpy.management.AssignDomainToField(
        in_table=Val_Message_p,
        field_name="Review_Status_p",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To REVIEW_MSG_p Field (Assign Domain To Field) (management)
    Review_Message_p = arcpy.management.AssignDomainToField(
        in_table=Review_Status_p,
        field_name="Review_Message_p",
        domain_name="D_VERFIEDMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To DATALOAD_STATUS_p Field (Assign Domain To Field) (management)
    Dataload_Status_p = arcpy.management.AssignDomainToField(
        in_table=Review_Message_p,
        field_name="Dataload_Status_p",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To DATALOAD_MSG_p Field (Assign Domain To Field) (management)
    Dataload_Msg_p = arcpy.management.AssignDomainToField(
        in_table=Dataload_Status_p,
        field_name="Dataload_Msg_p",
        domain_name="D_DATAMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To ORG_ADMIN_t Field (Assign Domain To Field) (management)
    ORG_ADMIN_t = arcpy.management.AssignDomainToField(
        in_table=Dataload_Msg_p,
        field_name="ORG_ADMIN_t",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To PRIMARY_OWNERSHIP_GROUP Field (Assign Domain To Field) (management)
    PRIMARY_OWNERSHIP_GROUP = arcpy.management.AssignDomainToField(
        in_table=ORG_ADMIN_t,
        field_name="PRIMARY_OWNERSHIP_GROUP",
        domain_name="D_PR_OWN_GR",
        subtype_code=[],
    )

    # Process: Assign Domain To PRIMARY_OBJECTIVE Field (Assign Domain To Field) (management)
    PRIMARY_OBJECTIVE = arcpy.management.AssignDomainToField(
        in_table=PRIMARY_OWNERSHIP_GROUP,
        field_name="PRIMARY_OBJECTIVE",
        domain_name="D_OBJECTIVE",
        subtype_code=[],
    )

    # Process: Assign Domain To SECONDARY_OBJECTIVE Field (Assign Domain To Field) (management)
    SECONDARY_OBJECTIVE = arcpy.management.AssignDomainToField(
        in_table=PRIMARY_OBJECTIVE,
        field_name="SECONDARY_OBJECTIVE",
        domain_name="D_OBJECTIVE",
        subtype_code=[],
    )

    # Process: Assign Domain To TERTIARY_OBJECTIVE Field (Assign Domain To Field) (management)
    TERTIARY_OBJECTIVE = arcpy.management.AssignDomainToField(
        in_table=SECONDARY_OBJECTIVE,
        field_name="TERTIARY_OBJECTIVE",
        domain_name="D_OBJECTIVE",
        subtype_code=[],
    )

    # Process: Assign Domain To TREATMENT_STATUS Field (Assign Domain To Field) (management)
    TREATMENT_STATUS = arcpy.management.AssignDomainToField(
        in_table=TERTIARY_OBJECTIVE,
        field_name="TREATMENT_STATUS",
        domain_name="D_STATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To COUNTY Field (Assign Domain To Field) (management)
    COUNTY = arcpy.management.AssignDomainToField(
        in_table=TREATMENT_STATUS,
        field_name="COUNTY",
        domain_name="D_CNTY",
        subtype_code=[],
    )

    # Process: Assign Domain To IN_WUI Field (Assign Domain To Field) (management)
    IN_WUI = arcpy.management.AssignDomainToField(
        in_table=COUNTY, field_name="IN_WUI", domain_name="D_IN_WUI", subtype_code=[]
    )

    # Process: Assign Domain To REGION Field (Assign Domain To Field) (management)
    REGION = arcpy.management.AssignDomainToField(
        in_table=IN_WUI, field_name="REGION", domain_name="D_TASKFORCE", subtype_code=[]
    )

    # Process: Assign Domain To VAL_STATUS_t Field (Assign Domain To Field) (management)
    Val_Status_t = arcpy.management.AssignDomainToField(
        in_table=REGION,
        field_name="Val_Status_t",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To VAL_MSG_t Field (Assign Domain To Field) (management)
    Val_Message_t = arcpy.management.AssignDomainToField(
        in_table=Val_Status_t,
        field_name="Val_Message_t",
        domain_name="D_VERFIEDMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To REVIEW_STATUS_t Field (Assign Domain To Field) (management)
    Review_Status_t = arcpy.management.AssignDomainToField(
        in_table=Val_Message_t,
        field_name="Review_Status_t",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To REVIEW_MSG_t Field (Assign Domain To Field) (management)
    Review_Message_t = arcpy.management.AssignDomainToField(
        in_table=Review_Status_t,
        field_name="Review_Message_t",
        domain_name="D_VERFIEDMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To DATALOAD_STATUS_t Field (Assign Domain To Field) (management)
    Dataload_Status_t = arcpy.management.AssignDomainToField(
        in_table=Review_Message_t,
        field_name="Dataload_Status_t",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To DATALOAD_MSG_t Field (Assign Domain To Field) (management)
    Dataload_Msg_t = arcpy.management.AssignDomainToField(
        in_table=Dataload_Status_t,
        field_name="Dataload_Msg_t",
        domain_name="D_DATAMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To ORG_ADMIN_a Field (Assign Domain To Field) (management)
    ORG_ADMIN_a = arcpy.management.AssignDomainToField(
        in_table=Dataload_Msg_t,
        field_name="ORG_ADMIN_a",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To ACTIVITY_DESCRIPTION Field (Assign Domain To Field) (management)
    ACTIVITY_DESCRIPTION = arcpy.management.AssignDomainToField(
        in_table=ORG_ADMIN_a,
        field_name="ACTIVITY_DESCRIPTION",
        domain_name="D_ACTVDSCRP",
        subtype_code=[],
    )

    # Process: Assign Domain To ACTIVITY_CAT Field (Assign Domain To Field) (management)
    ACTIVITY_CAT = arcpy.management.AssignDomainToField(
        in_table=ACTIVITY_DESCRIPTION,
        field_name="ACTIVITY_CAT",
        domain_name="D_ACTVCAT",
        subtype_code=[],
    )

    # Process: Assign Domain To BROAD_VEGETATION_TYPE Field (Assign Domain To Field) (management)
    BROAD_VEGETATION_TYPE = arcpy.management.AssignDomainToField(
        in_table=ACTIVITY_CAT,
        field_name="BROAD_VEGETATION_TYPE",
        domain_name="D_BVT",
        subtype_code=[],
    )

    # Process: Assign Domain To BVT_USERD Field (Assign Domain To Field) (management)
    BVT_USERD = arcpy.management.AssignDomainToField(
        in_table=BROAD_VEGETATION_TYPE,
        field_name="BVT_USERD",
        domain_name="D_USERDEFINED",
        subtype_code=[],
    )

    # Process: Assign Domain To ACTIVITY_STATUS Field (Assign Domain To Field) (management)
    ACTIVITY_STATUS = arcpy.management.AssignDomainToField(
        in_table=BVT_USERD,
        field_name="ACTIVITY_STATUS",
        domain_name="D_STATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To ACTIVITY_UOM Field (Assign Domain To Field) (management)
    ACTIVITY_UOM = arcpy.management.AssignDomainToField(
        in_table=ACTIVITY_STATUS,
        field_name="ACTIVITY_UOM",
        domain_name="D_UOM",
        subtype_code=[],
    )

    # Process: Assign Domain To ADMIN_ORG_NAME Field (Assign Domain To Field) (management)
    ADMIN_ORG_NAME = arcpy.management.AssignDomainToField(
        in_table=ACTIVITY_UOM,
        field_name="ADMIN_ORG_NAME",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To IMPLEM_ORG_NAME Field (Assign Domain To Field) (management)
    IMPLEM_ORG_NAME = arcpy.management.AssignDomainToField(
        in_table=ADMIN_ORG_NAME,
        field_name="IMPLEM_ORG_NAME",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To PRIMARY_FUND_SRC_NAME Field (Assign Domain To Field) (management)
    PRIMARY_FUND_SRC_NAME = arcpy.management.AssignDomainToField(
        in_table=IMPLEM_ORG_NAME,
        field_name="PRIMARY_FUND_SRC_NAME",
        domain_name="D_FNDSRC",
        subtype_code=[],
    )

    # Process: Assign Domain To PRIMARY_FUND_ORG_NAME Field (Assign Domain To Field) (management)
    PRIMARY_FUND_ORG_NAME = arcpy.management.AssignDomainToField(
        in_table=PRIMARY_FUND_SRC_NAME,
        field_name="PRIMARY_FUND_ORG_NAME",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To SECONDARY_FUND_SRC_NAME Field (Assign Domain To Field) (management)
    SECONDARY_FUND_SRC_NAME = arcpy.management.AssignDomainToField(
        in_table=PRIMARY_FUND_ORG_NAME,
        field_name="SECONDARY_FUND_SRC_NAME",
        domain_name="D_FNDSRC",
        subtype_code=[],
    )

    # Process: Assign Domain To SECONDARY_FUND_ORG_NAME Field (Assign Domain To Field) (management)
    SECONDARY_FUND_ORG_NAME = arcpy.management.AssignDomainToField(
        in_table=SECONDARY_FUND_SRC_NAME,
        field_name="SECONDARY_FUND_ORG_NAME",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To TERTIARY_FUND_SRC_NAME Field (Assign Domain To Field) (management)
    TERTIARY_FUND_SRC_NAME = arcpy.management.AssignDomainToField(
        in_table=SECONDARY_FUND_ORG_NAME,
        field_name="TERTIARY_FUND_SRC_NAME",
        domain_name="D_FNDSRC",
        subtype_code=[],
    )

    # Process: Assign Domain To TERTIARY_FUND_ORG_NAME Field (Assign Domain To Field) (management)
    TERTIARY_FUND_ORG_NAME = arcpy.management.AssignDomainToField(
        in_table=TERTIARY_FUND_SRC_NAME,
        field_name="TERTIARY_FUND_ORG_NAME",
        domain_name="D_ORGANIZATION",
        subtype_code=[],
    )

    # Process: Assign Domain To RESIDUE_FATE Field (Assign Domain To Field) (management)
    RESIDUE_FATE = arcpy.management.AssignDomainToField(
        in_table=TERTIARY_FUND_ORG_NAME,
        field_name="RESIDUE_FATE",
        domain_name="D_RESIDUEFATE",
        subtype_code=[],
    )

    # Process: Assign Domain To RESIDUE_FATE_UNITS Field (Assign Domain To Field) (management)
    RESIDUE_FATE_UNITS = arcpy.management.AssignDomainToField(
        in_table=RESIDUE_FATE,
        field_name="RESIDUE_FATE_UNITS",
        domain_name="D_UOM",
        subtype_code=[],
    )

    # Process: Assign Domain To VAL_STATUS_a Field (Assign Domain To Field) (management)
    VAL_STATUS_a = arcpy.management.AssignDomainToField(
        in_table=RESIDUE_FATE_UNITS,
        field_name="VAL_STATUS_a",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To VAL_MSG_a Field (Assign Domain To Field) (management)
    VAL_MSG_a = arcpy.management.AssignDomainToField(
        in_table=VAL_STATUS_a,
        field_name="VAL_MSG_a",
        domain_name="D_VERFIEDMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To REVIEW_STATUS_a Field (Assign Domain To Field) (management)
    REVIEW_STATUS_a = arcpy.management.AssignDomainToField(
        in_table=VAL_MSG_a,
        field_name="REVIEW_STATUS_a",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To REVIEW_MSG_a Field (Assign Domain To Field) (management)
    REVIEW_MSG_a = arcpy.management.AssignDomainToField(
        in_table=REVIEW_STATUS_a,
        field_name="REVIEW_MSG_a",
        domain_name="D_VERFIEDMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To DATALOAD_STATUS_a Field (Assign Domain To Field) (management)
    DATALOAD_STATUS_a = arcpy.management.AssignDomainToField(
        in_table=REVIEW_MSG_a,
        field_name="DATALOAD_STATUS_a",
        domain_name="D_DATASTATUS",
        subtype_code=[],
    )

    # Process: Assign Domain To DATALOAD_MSG_a Field (Assign Domain To Field) (management)
    DATALOAD_MSG_a = arcpy.management.AssignDomainToField(
        in_table=DATALOAD_STATUS_a,
        field_name="DATALOAD_MSG_a",
        domain_name="D_DATAMSG",
        subtype_code=[],
    )

    # Process: Assign Domain To TRMT_GEOM Field (Assign Domain To Field) (management)
    TRMT_GEOM = arcpy.management.AssignDomainToField(
        in_table=DATALOAD_MSG_a,
        field_name="TRMT_GEOM",
        domain_name="D_TRMT_GEOM",
        subtype_code=[],
    )

    # Process: Assign Domain To COUNTS_TO_MAS Field (Assign Domain To Field) (management)
    COUNTS_TO_MAS = arcpy.management.AssignDomainToField(
        in_table=TRMT_GEOM,
        field_name="COUNTS_TO_MAS",
        domain_name="D_USERDEFINED",
        subtype_code=[],
    )

    return COUNTS_TO_MAS
