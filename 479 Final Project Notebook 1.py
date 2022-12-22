output_feature_classes


import os
cd= 'C:\\Users\\hello\\OneDrive\\Documents\\ArcGIS\\Projects\\479FinalProjectExploration'
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
GDB = ap.ListWorkspaces("*", "FileGDB")[0] # returns the geodatabase names and the full address.
GDB # Make sure it is pointing to the right location

#clip fire layer by state boundaries
boundary = "boundary"
fire = "C:\Users\hello\OneDrive\Documents\ArcGIS\Projects\479FinalProjectExploration\Fire_Feature_Data.gdb\USGS_Wildland_Fire_Combined_DatasetUSGS_Wildland_Fire_Combined_Dataset"
output = "fire_layer"

arcpy.Clip_analysis(fire, boundary, output)
#then exclude fires from before 2000

#clip bioclimatic rasters
tif_files = arcpy.ListRasters("*.tif")
tif_files

for tif_file in tif_files:
    out_raster = tif_file[:-4] + "_clipped.tif"
    arcpy.Clip_management(tif_file, "#", out_raster, "boundary")


#assign raster values to points
#this is for layers that do not need to be processed further

# Set the point layer and raster layers
point_layer = "randomPointsActual"

tif_files = arcpy.ListRasters("*.tif")

clipped_tif_files = []
for tif_file in tif_files:
    if "_clipped" in tif_file:
        clipped_tif_files.append(tif_file)
        
raster_layers = clipped_tif_files
print(raster_layers)

# Create a list to store the output feature classes from the Extract Values to Points tool
output_feature_classes = []

# Loop through each raster layer
for raster in raster_layers:
    # Use the Extract Values to Points tool to extract values from the raster to the points
    output_feature_class = "hi_raster_values_" + raster
    arcpy.sa.ExtractValuesToPoints(point_layer, raster, output_feature_class)
    output_feature_classes.append(output_feature_class)

# Join the output feature classes to the point layer using the Spatial Join tool
#arcpy.analysis.SpatialJoin(point_layer, output_feature_classes, "points_with_raster_values.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL")

    



output_featureswoot= []

for raster in output_feature_classes:
    current = "bioclimatic\\"+ raster[:-4]
    output_featureswoot.append(current)
  
print(output_featureswoot[0])
arcpy.analysis.SpatialJoin(point_layer, output_featureswoot , "JOIN_ONE_TO_ONE", "KEEP_ALL")

   

for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]:
    # Set the input feature class and the target feature class
    print(i)
    input_fc = "bioclimatic//hi_raster_values_wc2.1_30s_bio_" +i+"_clipped"
    target_fc = "randomPointsActual"

    # Set the spatial join type
    join_type = "KEEP_COMMON"

    # Set the join operation
    join_operation = "JOIN_ONE_TO_ONE"

    # Set the join relationship
    join_relationship = "INTERSECT"

    # Perform the spatial join using the "Add Spatial Join" tool
    arcpy.management.AddSpatialJoin(target_fc, input_fc, "", join_type, join_operation, join_relationship)
    print(i)

        

#split points up into two layers based on whether or not they are in a fire area or not
#do not do this. Binary fire presence is not the independent variable
#I like the idea of doing fire density where the density is contributed to by all fires historically. ie the area of fire could concievably be higher than the area of the circle

#assign a new field to each layer with a binary fire status of 0 for no and 1 for yes

#choose bandwidth based on fire size average in polygons
#create histograms and stuff
#chosen see below

#make raster layer for area burned

# Set the input polygon feature class
in_polygons = "fires"

# Set the output point feature class
out_points = "fires_points.shp"

# Convert the polygons to points
arcpy.FeatureToPoint_management(in_polygons, out_points)

# Set the output raster
out_raster = "fireDensity.tif"

# Set the cell size of the output raster
cell_size = 30

# Set the search radius for the kernel density calculation
search_radius = "500 Meters"

# Set the population field to be used in the kernel density calculation
population_field = "POPULATION_FIELD"

# Run the KernelDensity function
arcpy.sa.KernelDensity(out_points, population_field, out_raster, cell_size, search_radius)

# Save the output raster
out_raster.save("fireDensity.tif")


#KDE for roads and transmision lines
search_radius = "1000 Meters"
population_field = "POPULATION_FIELD"

for layer in ["fire"]:#"roads", "transmissionLines"]:
    out_raster = layer +"Density.tif"
    # Run the KernelDensity function
    arcpy.sa.KernelDensity(layer, population_field, 300,out_raster, search_radius)
    # Save the output raster
    out_raster.save(layer +"Density.tif")
    



#mean layers

# Import necessary modules
import arcpy
import numpy as np

# Set the workspace
arcpy.env.workspace = "C:/workspace"

# Set the point layer and the raster layers
point_layer = "randomPointsActual.shp"
#fire density, roads, transmission lines 
raster_layers = ["fireDensity", "roadDensity", "powerLineDensity.tif"]

# Set the radius for the circle
r = 134 #CALCULATED BASED ON MEDIAN FIRE SIZE 1/2

# Add fields to the attribute table of the point layer to store the mean values
arcpy.AddFields_management(point_layer, [("fireDensity", "DOUBLE"), ("roadDensity", "DOUBLE"), ("powerLineDensity", "DOUBLE")])

# Loop through each point in the point layer
with arcpy.da.UpdateCursor(point_layer, ["SHAPE@XY", "mean1", "mean2", "mean3"]) as cursor:
    for point in cursor:
        x, y = point[0]

        # Create a circle around the point with radius "r" units
        circle = arcpy.PointGeometry(arcpy.Point(x, y), arcpy.SpatialReference(4326)).buffer(r)

        # Create an empty list to store the mean values for the current point
        mean_values = []

        # Loop through each raster layer
        for raster in raster_layers:
            # Extract the values within the circle for the current raster
            result = arcpy.sa.ExtractByMask(raster, circle)

            # Calculate the mean value for the extracted values
            mean = np.mean(arcpy.RasterToNumPyArray(result))
            # Normalize the mean value by dividing it by the maximum value in the raster
            max_value = arcpy.GetRasterProperties_management(raster, "MAXIMUM").getOutput(0)
            normalized_mean = mean / float(max_value)

            # Add the normalized mean value to the list of mean values for the current point
            mean_values.append(normalized_mean)

        # Update the attribute table of the current point with the mean values
        cursor.updateRow([x, y] + mean_values)

# Print a message to confirm that the values have been added to the attribute table
print("Values added to attribute table successfully.")



#IGNORE THIS FOR NOW

#these next few will calculate the features for points that are based on the surrounding area and not just the value at the point
#use bandwidth from above then similar to above

#input variables that need to be transformed
#fires, roads, transmission lines, summary stats for vegetation


#create output variables just for ease of use
#independent variable
burnDensity = ""

#bioclimatic variables
#properties of the surface
roadDensity = ""
tranmissionLineDensity = ""
aspect = ""
elevation = ""
gradient = ""

#other variables that might change in the future (conservative approach might assume no change)
vegetationRisk = ""



