import win32api as wapi

"""
  0x26: "up Arrow",
  0x28: "Down Arrow"}
"""

key_list = [0x26, 0x28]
no_of_classes = len(key_list) + 1


def key_check():
    pressed = []
    for key in key_list:
        if wapi.GetAsyncKeyState(key):
            pressed.append(key)
    return pressed
