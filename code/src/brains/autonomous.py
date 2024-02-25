from . import base
import cv2
import numpy as np
# from pynput import keyboard
import time
import curses

class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)
        
        self.state = "forward"
        self.next_state = "forward"
        # self.state = "forward"
        # self.next_state = "forward"
        
    def line_following(self):
        image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('rgb2_image.jpg', image)

        lower_blue = np.array([90, 70, 170])
        upper_blue = np.array([150, 235, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsl_image, lower_blue, upper_blue)
        cv2.imwrite('after_mask.jpg', mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        next_state = None
        if contours:
            # Assume the largest contour is the blue line
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                # Calculate the center of the contour
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                print("LINE DETECTED!")  
                
                img_center = image.shape[1] // 2  # Get the center x-coordinate of the image
                
                if cx < img_center - 40:  # Threshold to avoid minor deviations
                    self.vehicle.pivot_right(0.35)
                elif cx > img_center + 40:
                    self.vehicle.pivot_left(0.35)
                else:
                    self.vehicle.drive_forward(0.5)
                    
                next_state = "forward"
            else:
                print("Contour too small or not detected")  # Default action if contour is too small or not detected
                # self.vehicle.stop()
                next_state = "forward"
                # TODO: do something different maybe
        else:
            print("No blue line detected")  # Default action if no blue line is detected
            next_state = "forward"
            # TODO: do something different maybe
            
        return next_state
            
    # Returns True if the distance to the front is less than 0.25m
    def check_front_distance(self):
        if self.distance_sensors[0].distance < 0.15: #distance sensor0 is the front sensor, 1 is the left 
            return True
        
        return False
    def avoid(self):
        self.vehicle.stop() # stops 
        self.next_state = "stop" # goes to state stop

        self.vehicle.pivot_left(0.4) # whatever number is here (will have to test) Turning right to then go forward and avoid obstacle
        time.sleep(0.2) # whatever number is here (will have to test)  Turning right to then go forward and avoid obstacle

        self.next_state = "stop" #stops 
        while self.distance_sensors[1].distance < 0.6: #while the distance from the left sensor to the obstacle is < 1, move forward
            self.vehicle.drive_forward(0.4) 
        #    # stop when cleared obstacle horizontally 

        self.vehicle.pivot_right(0.4) # Turning left to then go forward and get around obstacle
        time.sleep(0.2) # Turning left to then go forward to get around obstacle 
        
        self.vehicle.drive_forward(0.2)  #creeps forwards a little
        time.sleep(0.2) #creeps forwards a little

        while self.distance_sensors[1].distance != 1: #while the distance from the left sensor to the obstacle is not 0, move forward
            self.vehicle.drive_forward(0.2) 
                        #stop

    def logic(self):
        """
        Find the blue line in the camera feed, and drive the vehicle to follow it
        """
        try:
            # print(self.sample_hz)
            self.state = self.next_state
        
            print(self.state)
            match self.state:
                case "fake_forward":
                    if self.check_front_distance():
                        self.next_state = "avoid"
                        return
                    
                    self.vehicle.drive_forward(0.3)
                    self.next_state = "fake_forward"
                        
                        # self.vehicle.drive_forward(0.8)
                        self.next_state = self.line_following() # should call drive_forward and sets next_state
                        
                    case "avoid":
                        self.vehicle.avoid()
                        self.next_state.forward()
                        # go to state blue line ???
                        

                        
                    case "stop":
                        self.vehicle.stop()
                        self.next_state = "stop"
                        
                    case "kill":
                        self.vehicle.stop()
                        self.next_state = None
                        return False

                    case _:
                        self.vehicle.stop()
                        self.next_state = None
                        return False
                    
                    
                time.sleep(max(0, 1 / self.sample_hz - (time.time() - start_time)))

        # if anything is detected by the sonic sensors, stop the car
        # stop = False
        # for distance_sensor in self.distance_sensors:
        #     if distance_sensor.distance < 0.25:
        #         self.vehicle.stop()
        #         stop = True
                

        #
