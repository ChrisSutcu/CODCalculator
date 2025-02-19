# CODCalculator
Crack Opening Displacement Calculator 
README: Crack Opening Displacement (COD) Tracking Script

Overview

This script processes a series of images to track the crack opening displacement (COD) by selecting two points on each image and computing the COD in millimeters. The script also calibrates pixel density based on a known specimen thickness and saves the results to an Excel file.

Requirements

Ensure you have the following Python libraries installed before running the script:

cv2
numpy
os
csv
pandas
re

Features

Undistorts images using intrinsic camera parameters and distortion coefficients, the camera matrix must be found using a calibration step for a given camera and lens setup. This can be done using MATLAB.

Allows manual selection of calibration and COD points.

Tracks COD points across multiple images using optical flow.

Computes COD for each subsequent image in millimeters.

Saves results to an Excel file with specimen-specific sheets.

Experimental Consideration

Ensure that the area of interest from the camera around the COD selection points is as large as possible so that the pixel density can be maximised.

Ensure that the side of the specimen is flat compared to the camera. 

Bright colouring of the specimens helps reflect as much light as possible. 

Use a flash or a torch to illuminate the specimen. 

Select a suitable frequency of image acquisition so that optical flow can work appropriately and there are not large jumps in the COD points between images.

Usage

1. Prepare Your Image Directory

Store all images in a single folder. Supported formats include .jpg, .jpeg, .png, and .bmp.

Update the image_directory variable in the script with the full path of your image folder.


2. Run the Script

Execute the script using:

python script.py


3. Select initiation image

The script will display the first image in the folder.

Press "z" to skip one image in the folder until the image that the crack is initiating (The non-linearity criterion is used to determine this) is displayed.


4. Select Calibration Points

Click on two points that represent the thickness of the specimen.

Enter the actual thickness (in mm) when prompted. The script will compute pixel density automatically.


5. Select COD Points

Click on two points that define the COD measurement.

The script will track the COD points automatically using optical flow.

6. Exit the Script

Press x at any time to exit. There will be a de-bugging step at the end that shows the final tracked COD points, ensure this is representative of the COD you are aiming to capture.

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

The script expects images to follow a naming pattern like DCB_123_45678.JPG to extract ID and timestamp.

If an Excel file already exists, the script appends data to the relevant sheet.

Troubleshooting

The final image will be displayed with the final COD points, ensure that this is representative of the COD measurement.

If COD tracking fails, manually restart the process again selecting new COD pixels.

If images do not display, ensure OpenCV is properly installed.

License

This script is provided as-is without any warranties. Use at your own risk. Please cite the following paper if you use any version of the developed code.

"Transition from Large-Scale Fibre Bridging to Short-Scale via a Thin Plain Weave Interleaf "

For any issues or improvements, feel free to modify the script accordingly! 
This version can adequately calculate COD provided the points are representative of the COD measurement allowing quick and reliable calculation of fibre bridging laws for Fibre reinforced Polmer Composites.
It can also be used outside of composite materials to calculate COD.
