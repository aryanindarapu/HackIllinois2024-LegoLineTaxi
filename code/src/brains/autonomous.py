from . import base
import cv2
import numpy as np


class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)

    def logic(self):
        """
        Find the blue line in the camera feed, and drive the vehicle to follow it
        """

        image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        cv2.imwrite('hsv_image.jpg', hsv_image)

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        cv2.imwrite('after_mask.jpg', mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # if contours:
        #     # Assume the largest contour is the blue line
        #     largest_contour = max(contours, key=cv2.contourArea)
        #     M = cv2.moments(largest_contour)
            
        #     if M["m00"] != 0:
        #         # Calculate the center of the contour
        #         cx = int(M["m10"] / M["m00"])
        #         cy = int(M["m01"] / M["m00"])
                
        #         img_center = image.shape[1] // 2  # Get the center x-coordinate of the image
                
        #         if cx < img_center - 10:  # Threshold to avoid minor deviations
        #             self.vehicle.pivot_left(0.5)
        #         elif cx > img_center + 10:
        #             self.vehicle.pivot_right(0.5)
        #         else:
        #             self.vehicle.drive_forward(0.8)
        #     else:
        #         print("Contour too small or not detected")  # Default action if contour is too small or not detected
        #         self.vehicle.stop()
        # else:
        #     print("No blue line detected")  # Default action if no blue line is detected
        #     self.vehicle.stop()

        # # if anything is detected by the sonic sensors, stop the car
        # stop = False
        # for distance_sensor in self.distance_sensors:
        #     if distance_sensor.distance < 0.25:
        #         self.vehicle.stop()
        #         stop = True

        # if not stop:
        #     self.vehicle.drive_forward()
