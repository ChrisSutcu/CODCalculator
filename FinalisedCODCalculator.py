import cv2
import numpy as np
import os
import csv
import pandas as pd
import re

# Screen resolution
screen_width = 1920  # Replace with your screen width
screen_height = 1080  # Replace with your screen height

# Global variables to store the starting point coordinates
start_x1, start_y1 = -1, -1  # First COD point
start_x2, start_y2 = -1, -1  # Second COD point
cal_x1, cal_y1 = -1, -1  # First calibration point
cal_x2, cal_y2 = -1, -1  # Second calibration point
point_counter = 0  # Counter to track which point is being selected
calibration_done = False  # Flag to indicate if calibration is complete

# Create lists to store the crack extension data
image_names = []
coordinates = []
crack_extensions_mm = []

pixel_density = None  # Will be calculated dynamically

# Intrinsic camera parameters
fx = 29236.3390294649  # Focal length in the x-direction
fy = 29236.1897370766  # Focal length in the y-direction
cx = 3012.00465642500  # Principal point x-coordinate
cy = 1652.25048297345  # Principal point y-coordinate
s = 35.4395696677326  # Skew

K = np.array([[fx, s, cx],
              [0, fy, cy],
              [0, 0, 1]])

# Distortion Coefficients
rad_disx = 1.99075035363854
rad_disy = -13.6602292104863
tan_disx = -0.00755671321937868
tan_disy = 0.0296836680261452

dist_coeffs = np.array([[rad_disx, rad_disy, tan_disx, tan_disy]])

# Global variables for scaling
scaling_x = 1
scaling_y = 1

# Variable to store the previous image
prev_image = None


def letterbox_image(image, screen_width, screen_height):
    # Calculate the scaling factors for width and height to maintain the image aspect ratio
    scaling_x = screen_width / image.shape[1]
    scaling_y = screen_height / image.shape[0]

    # Use the minimum of the two scaling factors to fit the image on the screen
    min_scaling = min(scaling_x, scaling_y)

    # Calculate the dimensions of the letterboxed image
    new_width = int(image.shape[1] * min_scaling)
    new_height = int(image.shape[0] * min_scaling)

    # Resize the image
    letterboxed_image = cv2.resize(image, (new_width, new_height))

    # Create a blank screen with the specified screen resolution
    screen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    # Calculate the position to paste the letterboxed image
    x_offset = (screen_width - new_width) // 2
    y_offset = (screen_height - new_height) // 2

    # Paste the letterboxed image onto the screen
    screen[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = letterboxed_image

    return screen


def preprocess_image(image_path, screen_width, screen_height):
    image = cv2.imread(image_path)

    # Letterbox the image to maintain aspect ratio
    letterboxed_image = letterbox_image(image, screen_width, screen_height)

    # Undistort the letterboxed image using the camera matrix and dist coefficients
    undistorted = cv2.undistort(letterboxed_image, K, dist_coeffs)

    gray_image = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    smoothed_image = cv2.GaussianBlur(gray_image, (11, 11), 0)  # Adjust the kernel size as needed

    # Adaptive thresholding
    threshold_image = cv2.adaptiveThreshold(
        smoothed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2
    )

    # Dilation to enhance features.
    dilated_image = cv2.dilate(threshold_image, None, iterations=1)

    # Apply erosion to reduce noise.
    eroded_image = cv2.erode(dilated_image, None, iterations=2)

    # Apply the Laplacian of Gaussian (LoG) for edge detection
    edges = cv2.Laplacian(eroded_image, cv2.CV_8U)

    return edges


def calculate_crack_extension(y1, y2, pixel_density):
    # Calculate the difference in y-coordinates in pixels
    y_difference = abs(y2 - y1)

    # Convert the pixel difference to millimeters
    crack_extension_mm = y_difference / pixel_density

    return crack_extension_mm


def get_start_point(event, x, y, flags, param):
    global start_x1, start_y1, start_x2, start_y2, cal_x1, cal_y1, cal_x2, cal_y2, point_counter, calibration_done, pixel_density

    if event == cv2.EVENT_LBUTTONDOWN:
        if not calibration_done:
            if point_counter == 0:
                cal_x1, cal_y1 = x, y
                print(f"Selected first calibration point: ({cal_x1}, {cal_y1})")
                point_counter += 1
            elif point_counter == 1:
                cal_x2, cal_y2 = x, y
                print(f"Selected second calibration point: ({cal_x2}, {cal_y2})")

                # Prompt user for known thickness
                try:
                    known_thickness_mm = float(input("Enter the known thickness of the specimen (in mm): "))
                    thickness_pixels = abs(cal_y2 - cal_y1)
                    pixel_density = thickness_pixels / known_thickness_mm
                    print(f"Calculated pixel density: {pixel_density:.4f} pixels/mm")

                    calibration_done = True
                    point_counter = 0  # Reset for COD selection

                except ValueError:
                    print("Invalid input! Please enter a numeric value for thickness.")
                    point_counter = 1  # Allow retry for second calibration point

        else:
            if point_counter == 0:
                start_x1, start_y1 = x, y
                print(f"Selected first COD point: ({start_x1}, {start_y1})")
                point_counter += 1
            elif point_counter == 1:
                start_x2, start_y2 = x, y
                print(f"Selected second COD point: ({start_x2}, {start_y2})")
                point_counter = 0


def get_image_paths(directory):
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    image_paths = []

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))

    return image_paths


def main():
    global start_x1, start_y1, start_x2, start_y2, current_image_index, prev_image, point_counter, pixel_density, calibration_done

    try:
        cumulative_extension_total = 0  # Initialize cumulative_extension_total outside the loop
        processed_images = 0  # Initialize the number of processed images

        while processed_images < num_images:
            image_path = image_paths[current_image_index]
            gray_image = preprocess_image(image_path, screen_width, screen_height)

            # Create a named window and display the image in fullscreen mode
            cv2.namedWindow('Select Points', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('Select Points', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('Select Points', gray_image)
            cv2.setMouseCallback('Select Points', get_start_point)

            while True:
                key = cv2.waitKey(1)

                if key == ord('x'):
                    raise KeyboardInterrupt

                if key == ord('z'):
                    current_image_index = (current_image_index + 1) % num_images
                    processed_images += 1
                    image_path = image_paths[current_image_index]
                    gray_image = preprocess_image(image_path, screen_width, screen_height)
                    start_x1, start_y1 = -1, -1
                    start_x2, start_y2 = -1, -1
                    point_counter = 0
                    cv2.imshow('Select Points', gray_image)  # Display the updated image
                    print(f"The current image is {image_path}.")
                    current_image_number = current_image_index

                if calibration_done and start_x1 != -1 and start_y1 != -1 and start_x2 != -1 and start_y2 != -1:
                    break

            cv2.destroyAllWindows()

            if not calibration_done:
                # Calculate pixel density based on calibration points
                thickness_pixels = abs(cal_y2 - cal_y1)
                known_thickness_mm = float(input("Enter the known thickness of the specimen (in mm): "))
                pixel_density = thickness_pixels / known_thickness_mm
                print(f"Calculated pixel density: {pixel_density:.4f} pixels/mm")
                calibration_done = True
                continue  # Skip to the next image after calibration

            if prev_image is None:
                prev_image = gray_image  # Initialize the prev_image on the first iteration

            # Track both points using optical flow
            next_point1, status1, _ = cv2.calcOpticalFlowPyrLK(prev_image, gray_image,
                                                              np.array([[start_x1, start_y1]], dtype=np.float32), None)
            next_point2, status2, _ = cv2.calcOpticalFlowPyrLK(prev_image, gray_image,
                                                              np.array([[start_x2, start_y2]], dtype=np.float32), None)

            if status1[0] == 1 and status2[0] == 1:
                # If optical flow was successful, update the starting points for the next image
                start_x1, start_y1 = next_point1[0].astype(int)
                start_x2, start_y2 = next_point2[0].astype(int)

            # Calculate the crack extension in the y-direction in millimeters
            crack_extension_mm = calculate_crack_extension(start_y1, start_y2, pixel_density)
            print(f"COD for {image_path}: {crack_extension_mm:.3f} mm")

            # Update the previous image for the next iteration
            prev_image = gray_image

            # Calculate the cumulative crack extension from the starting point
            if current_image_index == 0:
                cumulative_extension_total = crack_extension_mm
            else:
                cumulative_extension_total += crack_extension_mm

            # Save the calculated crack extension and associated data
            image_names.append(os.path.basename(image_path))
            coordinates.append(((start_x1, start_y1), (start_x2, start_y2)))
            crack_extensions_mm.append(f"{crack_extension_mm:.3f}")

            # Move to the next image
            current_image_index = (current_image_index + 1) % num_images
            processed_images += 1  # Increment the number of processed images

        # Load the final image from the image directory
        final_image = preprocess_image(image_paths[-1], screen_width, screen_height)

        # Draw the final points and a line between them on the final image
        (x1, y1), (x2, y2) = coordinates[-1]
        cv2.circle(final_image, (x1, y1), 10, (255, 255, 255), -1)
        cv2.circle(final_image, (x2, y2), 10, (255, 255, 255), -1)

        cv2.line(final_image, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.imshow('Final COD Points', final_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        # In case of manual exit (pressing 'x'), save the CSV file before exiting
        pass

    # Create a list of dictionaries to store the crack extension data
    data_list = []

    for name, coord, extension,  in zip(image_names, coordinates, crack_extensions_mm):

        # Extract numeric part and Unix time number using regular expressions
        match = re.match(r'DCB_(\d+)_(\d+)\.JPG', name)

        if match:
            IDs, unix_time = match.groups()
            data_list.append({
                "Image Name": name,
                "IDs": IDs,
                "Unix Time": unix_time,
                "Coordinates": coord,
                "COD (mm)": extension,

            })
        else:
            print(f"Failed to extract parts from image name: {name}")

    # Now, data_list contains the desired information in two separate columns.

    # Create a DataFrame from the data_list
    data = pd.DataFrame(data_list)
    # Specify the output CSV file path
    output_directory = r""
    excel_file_path = os.path.join(output_directory, f"{group_name}COD_data.xlsx")

    # Check if the Excel file already exists
    if os.path.exists(excel_file_path):
        # Load existing Excel file
        try:
            existing_data = pd.read_excel(excel_file_path, sheet_name=None)
        except FileNotFoundError:
            existing_data = {}

        if specimen_name in existing_data:
            existing_data[specimen_name] = pd.concat([existing_data[specimen_name], data], ignore_index=True)
        else:
            existing_data[specimen_name] = data

        # Write the updated data to the Excel file
        with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            for sheet_name, sheet_data in existing_data.items():
                sheet_data.to_excel(writer, index=False, sheet_name=sheet_name)

        print(f"Excel file updated: {excel_file_path}")
    else:
        # Write a new Excel file with the new data
        data.to_excel(excel_file_path, index=False, sheet_name=specimen_name, engine='xlsxwriter')


if __name__ == "__main__":
    image_directory = r""
    specimen_name = os.path.basename(image_directory)
    group_name = specimen_name[0:-1]
    image_paths = get_image_paths(image_directory)
    num_images = len(image_paths)
    current_image_index = 0

    main()
