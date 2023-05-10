from pynput import keyboard

def get_key():
    with keyboard.Events() as events:
        for event in events:
            return str(event.key)