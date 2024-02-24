from pynput import keyboard

def stop_motors():
    # Your code to stop the motors goes here
    print("Motors stopped")

def on_press(key):
    try:
        if key.char == 'q':  # If 'q' is pressed
            stop_motors()
            # Stop listener
            return False
    except AttributeError:
        pass  # Handle special key presses that don't involve characters here if needed

# Collect events until released
with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
