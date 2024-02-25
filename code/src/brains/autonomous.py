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
        
        # self.state = "fake_forward"
        # self.next_state = "fake_forward"
        
        self.state = "forward"
        self.next_state = "forward"
        
    def line_following(self):
        image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)
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
        self.vehicle.stop()
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
                
                if cx < img_center - 75:  # Threshold to avoid minor deviations
                    self.vehicle.turn_left(0.45)
                    print("Turning left")
                elif cx > img_center + 75:
                    self.vehicle.turn_right(0.45)
                    print("Turning right")
                else:
                    self.vehicle.drive_forward(0.6) # TODO: tune
                    print("Driving forward")
                    
                next_state = "forward"
            else:
                print("Contour too small or not detected")  # Default action if contour is too small or not detected
                self.vehicle.stop()
                next_state = "forward"
                # TODO: do something different maybe
        else:
            print("No blue line detected")  # Default action if no blue line is detected
            self.vehicle.stop()
            next_state = "forward"
            # TODO: do something different maybe
            
        return next_state
            
    # Returns True if the distance to the front is less than 0.25m
    def check_front_distance(self):
        if self.distance_sensors[0].distance < 0.15: #distance sensor0 is the front sensor, 1 is the left 
            print("front distance low")
            return True
        
        return False
    
    def avoid(self):
        # self.vehicle.pivot_left(0.4) # TODO: tune # whatever number is here (will have to test) Turning right to then go forward and avoid obstacle
        # time.sleep(1) # TODO: tune # whatever number is here (will have to test)  Turning right to then go forward and avoid obstacle
        # print("avoiding obstacle")
        self.vehicle.rotate_right()
        start_time = time.time()
        while time.time() - start_time < 25:
            self.vehicle.stop()
            time.sleep(0.1)
            print(self.distance_sensors[1].distance)
            if self.distance_sensors[1].distance > 0.16:
                self.vehicle.turn_left(0.7)

            elif self.distance_sensors[1].distance < 0.1:
                self.vehicle.turn_right(0.7)
            
            else: # 0.1 < dist < 0.9
                self.vehicle.drive_forward(0.7)

                # image = self.camera.capture()
                # image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
                # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # cv2.imwrite('rgb2_image.jpg', image)

                # lower_blue = np.array([90, 70, 170])
                # upper_blue = np.array([150, 235, 255])

                # # Threshold the HSV image to get only blue colors
                # mask = cv2.inRange(hsl_image, lower_blue, upper_blue)
                # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # print(len(contours))
                # if contours:
                #     largest_contour = max(contours, key=cv2.contourArea)
                #     M = cv2.moments(largest_contour)
                #     if M and M["m00"] > 50.0:
                #         print("contours here", contours)
                #         self.vehicle.turn_right(0.7)
                #         time.sleep(0.35)
                #         self.next_state = 'forward'
                #         return
            
            time.sleep(0.15)
        
        self.gun_it_to_blue_line()

        # while self.distance_sensors[1].distance != 1.0: # TODO: tune # while the distance from the left sensor to the obstacle is < 0.6, move forward
        #     print(self.distance_sensors[1].distance)
        #     self.vehicle.stop()
        #     if self.distance_sensors[1].distance < 0.06:
        #         # self.vehicle.pivot_right(0.4)
        #         self.vehicle.turn_right(0.6)
        #         time.sleep(0.15)
        #     elif 0.05 <= self.distance_sensors[1].distance < 0.22:
        #         self.vehicle.drive_forward(0.6)
        #         time.sleep(0.15)
        #     elif self.distance_sensors[1].distance == 1.0:
        #         while self.distance_sensors[1].distance == 1.0:
        #             self.vehicle.turn_left(0.6)
        #             time.sleep(0.15)
        #             self.vehicle.stop()
        #             time.sleep(0.1)
        #     else:
        #         # self.vehicle.pivot_left(0.4)
        #         self.vehicle.turn_left(0.45)
        #         time.sleep(0.15)
        #     # self.vehicle.drive_forward(0.8) # TODO: tune
        #     # self.vehicle.drive(0.5, True, 0.5, True)
            
        # # while self.distance_sensors[1].distance > 0.6:
        # #     self.vehicle.pivot_left(0.6)
            
            
        # print(self.distance_sensors[1].distance)
        # self.vehicle.stop()
        # time.sleep(0.1)
        
        # # print("turning left")
        # while self.distance_sensors[1].distance == 1.0:
        #     self.vehicle.turn_left(0.6)
        #     time.sleep(0.15)
        #     self.vehicle.stop()
        #     time.sleep(0.1)
        # # self.vehicle.turn_left(0.6)
        # # time.sleep(0.45)
        # # self.vehicle.stop()
        # # time.sleep(0.1)
        
        # print("driving forward")
        # self.vehicle.drive_forward(0.6)
        # time.sleep(0.6)
        # self.vehicle.stop()
        # time.sleep(0.1)
        
        # while self.distance_sensors[1].distance == 1.0:
        #     self.vehicle.turn_left(0.6)
        #     time.sleep(0.15)
        #     self.vehicle.stop()
        #     time.sleep(0.1)
        
        # print(self.distance_sensors[1].distance)
        # while self.distance_sensors[1].distance != 1.0:
        #     print("starting on right edge")
        #     print(self.distance_sensors[1].distance)
        #     self.vehicle.stop()
        #     if self.distance_sensors[1].distance < 0.05:
        #         # self.vehicle.pivot_right(0.4)
        #         self.vehicle.turn_right(0.6)
        #         time.sleep(0.15)
        #     elif 0.05 <= self.distance_sensors[1].distance < 0.25:
        #         self.vehicle.drive_forward(0.6)
        #         time.sleep(0.15)
        #     else:
        #         # self.vehicle.pivot_left(0.4)
        #         self.vehicle.turn_left(0.6)
        #         time.sleep(0.15)
        
        
        # # # while self.distance_sensors[1].distance > 0.6:
        # # # self.vehicle.rotate_left() # TODO: tune # whatever number is here (will have to test)  Turning left to then go forward and avoid obstacle
        
        # # print(self.distance_sensors[1].distance)
        # # while self.distance_sensors[1].distance != 1.0: # TODO: tune # while the distance from the left sensor to the obstacle is < 0.6, move forward
        # #     self.vehicle.drive_forward(1) # TODO: tune
            
        # # print(self.distance_sensors[1].distance)
        # # self.vehicle.stop()
        # # self.vehicle.rotate_left() 
        
        
        
        # self.vehicle.rotate_left() 

        # # see if blue line reappears and then follow it
        # image = self.camera.capture()
        # image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # cv2.imwrite('rgb2_image.jpg', image)

        # lower_blue = np.array([90, 70, 170])
        # upper_blue = np.array([150, 235, 255])

        # # Threshold the HSV image to get only blue colors
        # mask = cv2.inRange(hsl_image, lower_blue, upper_blue)
        # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # while not contours:
        #     self.vehicle.drive_forward(1)
        #     image = self.camera.capture()
        #     image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)
        #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #     hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        #     rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #     cv2.imwrite('rgb2_image.jpg', image)

        #     lower_blue = np.array([90, 70, 170])
        #     upper_blue = np.array([150, 235, 255])

        #     # Threshold the HSV image to get only blue colors
        #     mask = cv2.inRange(hsl_image, lower_blue, upper_blue)
        #     contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # if contours :
        #     self.vehicle.turn_right(0.5)
        #     time.sleep(0.35)
        #     self.next_state = 'forward'
        

        # stop when cleared obstacle horizontally 
        # self.vehicle.pivot_right(0.4) # Turning left to then go forward and get around obstacle
        # time.sleep(0.2) # Turning left to then go forward to get around obstacle 
        
        # self.vehicle.drive_forward(0.4)  #creeps forwards a little
        # time.sleep(0.2) #creeps forwards a little

        # while self.distance_sensors[1].distance != 1: #while the distance from the left sensor to the obstacle is not 0, move forward
        #     self.vehicle.drive_forward(0.2) 
                        #stop
                        
    def gun_it_to_blue_line(self):
        # image = self.camera.capture()
        # image = cv2.rotate(self.camera.image_array, cv2.ROTATE_180)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # cv2.imwrite('rgb2_image.jpg', image)

        # lower_blue = np.array([90, 70, 170])
        # upper_blue = np.array([150, 235, 255])

        # # Threshold the HSV image to get only blue colors
        # mask = cv2.inRange(hsl_image, lower_blue, upper_blue)
        # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # if contours:
        #     largest_contour = max(contours, key=cv2.contourArea)
        #     M = cv2.moments(largest_contour)
        #     if M and M["m00"] > 50.0:
                # print("contours here", contours)
                self.vehicle.drive_forward(1)
                time.sleep(1)
                self.vehicle.rotate_right()
                self.next_state = 'forward'
                return
        

    def logic(self):
        """
        Find the blue line in the camera feed, and drive the vehicle to follow it
        """
        try:
            # print(self.sample_hz)
            self.state = self.next_state
        
            match self.state:
                case "fake_forward":
                    if self.check_front_distance():
                        self.next_state = "avoid"
                        return
                    
                    self.vehicle.drive_forward(0.5)
                    self.next_state = "fake_forward"
                        
                case "forward":
                    if self.check_front_distance():
                        self.next_state = "avoid"
                        return
                    
                    # print("line following")
                    self.next_state = self.line_following() # should call drive_forward and sets next_state
                    
                case "avoid":
                    self.vehicle.stop()
                    time.sleep(1)
                    
                    self.avoid()
                    
                    # self.next_state = "forward"
                    
                case "stop":
                    self.vehicle.stop()
                    self.next_state = "stop"
                    
                case "kill":
                    self.vehicle.stop()
                    self.next_state = "kill"
                    return False

                case _:
                    self.vehicle.stop()
                    self.next_state = None
                    return False
                
        except KeyboardInterrupt:
            print("Dying State:", self.state)
            self.vehicle.stop()
            self.next_state = None
            return False
