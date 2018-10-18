import win32api as wapi

key_list = [0x26, 0x28]

key_pressed = {	0x26: "up Arrow",
                0x28: "Down Arrow"}

def key_check():
  pressed = []
  for key in key_list:
    if(wapi.GetAsyncKeyState(key)):
      pressed.append(key)
  return pressed