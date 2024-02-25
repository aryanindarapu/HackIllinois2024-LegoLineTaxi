from src import camera as camera_module
import time
import cv2
import numpy as np

if __name__ == '__main__':

    total_seconds = 60
    sample_hz = 10

    camera = camera_module.Camera({
        "show_preview": False
    })
    start_time = time.time()

    while time.time() - start_time < total_seconds:
        camera.capture()
        # print(camera.image_array)
        # image = cv2.cvtColor(camera.image_array, cv2.COLOR_BGR2RGB)
        # image = cv2.rotate(image, cv2.ROTATE_180)
        # cv2.imwrite("rbg_picture.jpg", image)
        image = cv2.rotate(camera.image_array, cv2.ROTATE_180)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('rgb2_image.jpg', image)

        lower_blue = np.array([90, 60, 60])
        upper_blue = np.array([150, 190, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsl_image, lower_blue, upper_blue)
        cv2.imwrite('after_mask.jpg', mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        next_state = None
        # print(len(contours))
        if contours:
            # Assume the largest contour is the blue line
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] > 50.0:
                # Calculate the center of the contour
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                print("LINE DETECTED!")  
                
                img_center = image.shape[1] // 2  # Get the center x-coordinate of the image
                
                # if cx < img_center - 50:  # Threshold to avoid minor deviations
                #     self.vehicle.pivot_left(0.45)
                #     print("Pivoting left")
                # elif cx > img_center + 50:
                #     self.vehicle.pivot_right(0.45)
                #     print("Pivoting right")
                # else:
                #     self.vehicle.drive_forward(0.5) # TODO: tune
                #     print("Driving forward")
            else:
                print("Contour too small or not detected")  # Default action if contour is too small or not detected
                next_state = "forward"
                # TODO: do something different maybe
        else:
            print("No blue line detected")  # Default action if no blue line is detected
            next_state = "forward"
            # TODO: do something different maybe

        time.sleep(max(0, 1/sample_hz -
                       (time.time() - start_time)))
