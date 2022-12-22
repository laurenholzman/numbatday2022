import os
cd= 'C:\\Users\\hello\\OneDrive\\Documents\\ArcGIS\\Projects\\wow'
PATH = cd
PATH


# Requirements: Spatial Analyst Extension (arcpy.sa in the code below)

# Import system modules
import arcpy as ap
from arcpy import env
from arcpy.sa import * # By explicitly importing all of the spatial analyst extensions tools we don't need to prepend the module name.
import pandas as pd
import numpy as np
import random #unsure what this is for, but doing so makes it work

# Set environment settings
env.workspace = PATH
env.workspace
env.overwriteOutput = True # We need to set this explicitly so that we can easily rerun the code if we change the parameters 
GDB = ap.ListWorkspaces("*", "FileGDB")[1] # returns the geodatabase names and the full address.
GDB # Make sure it is pointing to the right location

env.workspace


# Set the input point layer and the field to normalize
input_layer = "p" #"r"
field_to_normalize = "sum shape_length"

# Create a new field to hold the normalized values
new_field = "lengthNorm"
arcpy.AddField_management(input_layer, new_field, "DOUBLE")

# Get the min and max values of the field to normalize
max_value = 18966.606292

# Normalize the values and update the new field
with arcpy.da.UpdateCursor(input_layer, [field_to_normalize, new_field]) as cursor:
    for row in cursor:
        print(row)
        normalized_value = row[0] / max_value
        row[1] = normalized_value
        cursor.updateRow(row)



# Set the input point layer
point_layer = "points_6"

# Set the field containing the string values
string_field = "NVC_SUBCL"

# Create an empty list to store the unique values
unique_values = []

# Use the SearchCursor to loop through the rows in the point layer and add the values
# of the string field to the list if they are not already in the list
with arcpy.da.SearchCursor(point_layer, string_field) as cursor:
    for row in cursor:
        if row[0] not in unique_values and row[0] != None:
            unique_values.append(row[0])
            
#replace with field name friendly characters:
for i in range(0,14):
    field_name = unique_values[i] 
    field_name =field_name.replace(' ', '_') 
    field_name =field_name.replace('&', '_')
    field_name =field_name.replace('-', '_')
    unique_values[i] =field_name
        

# Loop through the unique values and create a new field for each one

for value in unique_values:
    
    if value != None:
        print(value)
        arcpy.AddField_management(point_layer, value, "SHORT")




# Use the UpdateCursor to loop through the rows in the point layer and assign
# the appropriate value (1 or 0) to the new fields
unique_values[5]="Warm_Desert___Semi_Desert_Woodland__Scrub___Grassland"
with arcpy.da.UpdateCursor(point_layer, unique_values) as cursor:
    for row in cursor:
        for i, value in enumerate(unique_values):
            if row[-1] == value:
                row[i] = 1
            else:
                row[i] = 0
        cursor.updateRow(row)


unique_values

unique_values2 = ['Temperate___Boreal_Grassland___Shrubland', 'Developed___Urban', 'Temperate___Boreal_Forest___Woodland', 'Cool_Semi_Desert_Scrub___Grassland', 'Warm_Desert___Semi_Desert_Woodland__Scrub___Grassland', 'Herbaceous_Agricultural_Vegetation', 'Shrub___Herb_Wetland', 'Open_Water', 'Introduced___Semi_Natural_Vegetation', 'Recently_Disturbed_or_Modified', 'Temperate___Boreal_Open_Rock_Vegetation', 'Barren', 'Current_and_Historic_Mining_Activity', 'Temperate_Alpine_to_Polar_Tundra']

unique_values

print(unique_values[0].replace(' ', '_'))


