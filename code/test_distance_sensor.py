from src import distance_sensor as distance_sensor_module
import time


if __name__ == '__main__':

    total_seconds = 60
    sample_hz = 2

    distance_sensor1 = distance_sensor_module.DistanceSensor({
        "pins": {
            "echo": 23,
            "trigger": 24
        }
    })

    distance_sensor2 = distance_sensor_module.DistanceSensor({
        "pins": {
            "echo": 17,
            "trigger": 27
        }
    })

    start_time = time.time()
    ct = 0
    while time.time() - start_time < total_seconds:
        if ct % 5 == 0: print(f"Loop Counter: {ct}")
        loop_start = time.time()

        print(1, distance_sensor1.distance)
        print(2, distance_sensor2.distance)

        print(1/sample_hz - (time.time() - loop_start))
        time.sleep(max(0, 1/sample_hz -
                       (time.time() - loop_start)))
        
        ct += 1
