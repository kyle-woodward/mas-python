"""
# Description:  Adds metadata to the appended dataset(s).
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import shutil
import arcpy
from arcpy import metadata as md

arcpy.env.overwriteOutput = True

# Standard Metadata
ITS_tags = 'ITS, Million Acres, Vegetation Management, Forest Resilience, Fuels Reduction, Forest Health, California, Forest, Fire, Interagency Tracking System, California Wildfire & Forest Resilience Task Force'
ITS_summary = 'California Wildfire & Landscape Resilience Interagency Treatments for 2022'
ITS_description = """WildfireTaskForce.org
As California works toward ambitious wildfire and landscape resilience goals, transparency and effective planning tools are critical to success. This beta version of the California Wildfire and Landscape Interagency Treatment Dashboard, for the first time ever in California, provides a single source for displaying recently completed (2022) forest and wildland projects from over a dozen different federal and state agencies.
What is the Wildfire & Landscape Resilience Interagency Treatment Dashboard?
The Dashboard is a first-of-its-kind platform that displays the location and extent of federal and state wildfire and landscape resilience treatments throughout the state. The Dashboard is a highly interactive online tool by which users can sort treatments by region, county, land ownership, and more. By charting the work of what has been accomplished to date, the Dashboard can be used to guide practitioners on where to plan new projects."""
ITS_credits = 'California Wildfire & Forest Resilience Task Force, Climate and Wildfire Institute, Spatial Informatics Group, CA Natural Resources Agency, US Forest Service, CA Air Resources Board, CA Department of Forestry and Fire Protection, CA Department of Transportation, CA Department of Conservation, US Department of Interior, CA Resource Conservation Districts'
ITS_accessConstraints = 'Neither California Wildfire and Forest Resilience Task Force nor Climate and Wildfire Institute makes any warranty, expressed or implied, including the warranties of merchantability and fitness for a particular purpose, nor assumes any legal liability or responsibility for the accuracy, reliability, completeness or utility of these geospatial data, or for the improper or incorrect use of these geospatial data. These geospatial data and related maps or graphics are not legal documents and are not intended to be used as such. The data and maps may not be used to determine title, ownership, legal descriptions or boundaries, legal jurisdiction, or restrictions that may be in place on either public or private land. The data are dynamic and may change over time. The user is responsible to verify the limitations of the geospatial data and to use the data accordingly.'
ITS_thumb = 'ITS Logos2.jpg'

def pt_metadata(pt_feature_class):
    
    # Create a metadata object
    pt_md = md.Metadata(pt_feature_class)
    pt_md.title = 'Interagency Tracking System Points'
    pt_md.tags = ITS_tags
    pt_md.summary = ITS_summary
    pt_md.description = ITS_description
    pt_md.credits = ITS_credits
    pt_md.accessConstraints = ITS_accessConstraints
    shutil.copy('ITS Logos.jpg','ITS Logos2.jpg') # copy the file because md.thumbnailUri usually deletes the file after import
    pt_md.thumbnailUri = ITS_thumb

    # Assign the Metadata object's content to a target item
    tgt_item_md = md.Metadata(pt_feature_class)
    if not tgt_item_md.isReadOnly:
        tgt_item_md.copy(pt_md)
        tgt_item_md.save()

        print("Point Metadata added successfully.")

def ln_metadata(ln_feature_class): 
    
    # Create a metadata object
    ln_md = md.Metadata(ln_feature_class)
    ln_md.title = 'Interagency Tracking System Lines'
    ln_md.tags = ITS_tags
    ln_md.summary = ITS_summary
    ln_md.description = ITS_description
    ln_md.credits = ITS_credits
    ln_md.accessConstraints = ITS_accessConstraints
    shutil.copy('ITS Logos.jpg','ITS Logos2.jpg') # copy the file because md.thumbnailUri usually deletes the file after import
    ln_md.thumbnailUri = ITS_thumb

    # Assign the Metadata object's content to a target item
    tgt_item_md = md.Metadata(ln_feature_class)
    if not tgt_item_md.isReadOnly:
        tgt_item_md.copy(ln_md)
        tgt_item_md.save()

        print("Line Metadata added successfully.")

def poly_metadata(poly_feature_class):

    # Create a metadata object
    poly_md = md.Metadata(poly_feature_class)
    poly_md.title = 'Interagency Tracking System Polygons'
    poly_md.tags = ITS_tags
    poly_md.summary = ITS_summary
    poly_md.description = ITS_description
    poly_md.credits = ITS_credits
    poly_md.accessConstraints = ITS_accessConstraints
    shutil.copy('ITS Logos.jpg','ITS Logos2.jpg') # copy the file because md.thumbnailUri usually deletes the file after import
    poly_md.thumbnailUri = ITS_thumb

    # Assign the Metadata object's content to a target item
    tgt_item_md = md.Metadata(poly_feature_class)
    if not tgt_item_md.isReadOnly:
        tgt_item_md.copy(poly_md)
        tgt_item_md.save()

        print("Polygon Metadata added successfully.")
