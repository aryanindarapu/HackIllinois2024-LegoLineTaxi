from src import vehicle as vehicle_module
import time

if __name__ == '__main__':

    vehicle = vehicle_module.Vehicle(
        {
            "motors": {
                "left": {
                    "pins": {
                        "speed": 13,
                        "control1": 5,
                        "control2": 6
                    }
                },
                "right": {
                    "pins": {
                        "speed": 12,
                        "control1": 7,
                        "control2": 8
                    }
                }
            }
        }
    )

    vehicle.stop()
    # vehicle.pivot_left(0.6)
    # time.sleep(0.69)
    
    # vehicle.stop()
    # time.sleep(1)
    
    # vehicle.pivot_right(0.6)
    # time.sleep(0.63)
    
    # vehicle.rotate_left()
    # time.sleep(1)
    # vehicle.rotate_right()
    
    
    # vehicle.stop()
    # vehicle.drive_forward(1)    
    



    # print('Forward')
    # vehicle.drive_forward(1)
    # time.sleep(3)

    # print('Stop')
    # vehicle.stop()
    # time.sleep(1)

    # print('Pivot Left')
    # vehicle.pivot_left(1)
    # time.sleep(2)

    # print('Pivot Right')
    # vehicle.pivot_right(1)
    # time.sleep(2)

    # print('Stop')
    # vehicle.stop()
    # time.sleep(1)

    # print('Backward')
    # vehicle.drive_backward(1)
    # time.sleep(2)

    # print('Stop')
    # vehicle.stop()
    # time.sleep(1)

    # print('Driving Figure 8')
    # vehicle.drive_forward(1)
    # time.sleep(1.5)
    # vehicle.drive(0.5, True, 1, True)
    # time.sleep(5)
    # vehicle.drive_forward(1)
    # time.sleep(3)
    # vehicle.drive(1, True, 0.5, True)
    # time.sleep(5)
    # vehicle.drive_forward(1)
    # time.sleep(1.5)
    # vehicle.stop()







