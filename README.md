# CODCalculator
README: Crack Opening Displacement (COD) Tracking Script

Overview

This script processes a series of images to track the crack opening displacement (COD) by selecting two points on the crack initiation image which are tracked using optical flow.This allows for computing COD in millimeters. The script also calibrates pixel density based on a known specimen thickness and saves the results to an Excel file.

Requirements

Ensure you have the following Python libraries installed before running the script:

cv2
numpy
os
csv
pandas
re

Features

Undistorts images using intrinsic camera parameters and distortion coefficients, the camera matrix must be found using a calibration process for a given camera, lens and focal length setup. This can be done using MATLAB.

Allows manual selection of calibration and COD points.

Tracks COD points across multiple images using optical flow.

Computes COD for each successive image in millimeters.

Saves results to an Excel file with specimen-specific sheets.

Experimental Consideration

Ensure that the area of interest from the camera around the COD selection points is as large as possible so that the pixel density can be maximised.

Ensure that the side of the specimen is flat as much as possible compared to the camera. 

Ensure the specimen is in focus at all times.

Brightly colour the side of the specimens as it helps reflect as much light as possible. 

Use a flash or a torch to illuminate the specimen. 

Select a suitable frequency of image acquisition so that optical flow can work appropriately and there are no large jumps in the COD points between images.

Please note that this particular image processing chain was appropriate for the experimental conditions I faced, and may not be generally applied to all variable experimental conditions, i.e. lighting and specimen configurations. The image processing chain was adequate for my experimental conditions, but it may require some tweaking for other experimental conditions. The goal is to make the edges as continuous and visible as possible so that optical flow can track the pixels between images. Stability in testing conditions is essential.

Usage

1. Prepare Your Image Directory

Store all images in a single folder. Supported formats include .jpg, .jpeg, .png, and .bmp.

Update the image_directory variable in the script with the full path of your image folder.


2. Run the Script

Execute the script using:

python script.py


3. Select initiation image

The script will display the first image in the folder.

Press "z" to skip one image in the folder until the image corresponding to crack initiation is displayed (The non-linearity criterion is used to determine this).


4. Select Calibration Points

Click on two points that represent the thickness of the specimen.

Enter the actual thickness (in mm) when prompted. The script will compute pixel density automatically.


5. Select COD Points

Click on two points that define the COD measurement.

The script will track the COD points automatically using optical flow.

6. Exit the Script

Press x at any time to exit. There will be a de-bugging image at the end that shows the final tracked COD points, ensure this is representative of the COD you are aiming to capture.

The script will save the results before closing.

7. Output

Results are saved in an Excel file named {group_name}COD_data.xlsx 

Change the output_directory variable to change the location of this output file.

The Excel file contains:

Image Name: Name of the processed image.

IDs: Extracted numeric ID from the filename.

Unix Time: Extracted timestamp from the filename.

Coordinates: Selected COD points.

COD (mm): Computed COD in millimeters.

Notes

The script expects images to follow a naming pattern like DCB_0001_1705676782.JPG to extract ID and timestamp.

If an Excel file already exists, the script appends data to the relevant sheet.

Troubleshooting

The final image will be displayed with the final COD points, ensure that this is representative of the COD measurement.

If COD tracking fails, manually restart the process again selecting new COD pixels.

If images do not display, ensure OpenCV is properly installed.

License

This script is provided as-is without any warranties. Use at your own risk. Please cite the following paper if you use any version of the developed code.

Sutcu, C., Aravand, A., Kazancı, Z., 2024. Transition from large-scale fibre bridging to short-scale via a thin plain weave interleaf. Eng. Fract. Mech. [DOI or Volume/Issue to follow if published].

For any issues or improvements, feel free to modify the script accordingly! 

This version can adequately calculate COD provided the points are representative of the COD measurement allowing quick and reliable calculation of fibre bridging laws for fibre-reinforced Polmer (FRP) Composites.

It can also be used outside of composite materials to calculate COD.

Potential updates include;

Automatic method for COD selection points.

A magnified region around the cursor to allow for more accurate pixel selection.

Automatic crack extension calculator to work alongside this to calculate R-curve automatically as well as fibre bridging laws. 

Anything else that can make the code better! 

This can become a tool used for streamlined Mode I fracture toughness and bridging law characterisation of FRP composite materials, but more generally it can become a fracture mechanics measurement tool.




