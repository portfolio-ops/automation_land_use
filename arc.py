import arcpy
from arcpy.sa import *

# Set workspace
arcpy.env.workspace = "C:\Users\rutow\Downloads\Bomori"

# Load input data
input_raster = "satellite_image.tif"
boundary = "study_area.shp"

# Clip raster to study area
clipped_raster = arcpy.Clip_management(input_raster, "#", "clipped_image.tif", boundary, "#", "ClippingGeometry")

# Calculate NDVI
red_band = arcpy.Raster(clipped_raster + "/Band_4")
nir_band = arcpy.Raster(clipped_raster + "/Band_5")
ndvi = (nir_band - red_band) / (nir_band + red_band)

# Classify land use based on NDVI
land_use = Con(ndvi > 0.4, 1, Con(ndvi > 0.2, 2, 3))  # 1 = Forest, 2 = Grassland, 3 = Other

# Save output
land_use.save("land_use_map.tif")

# Generate a map layout
aprx = arcpy.mp.ArcGISProject("CURRENT")
layout = aprx.listLayouts()[0]
layout.exportToPDF("land_use_map.pdf")

print("Land use mapping completed!")
