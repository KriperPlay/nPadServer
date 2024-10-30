# ╱╱╱╭━━━╮╱╱╱╱╭╮
# ╱╱╱┃╭━╮┃╱╱╱╱┃┃
# ╭━╮┃╰━╯┣━━┳━╯┃
# ┃╭╮┫╭━━┫╭╮┃╭╮┃
# ┃┃┃┃┃╱╱┃╭╮┃╰╯┃
# ╰╯╰┻╯╱╱╰╯╰┻━━╯


import asyncio
import os
import random
import vgamepad as vg
import websockets

xbuttons = {
    "up": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    "down": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    'left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    'right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    'a': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'b': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    'select': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    'lt': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'rt': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
}

gamepad = vg.VX360Gamepad()

async def press_xbutton(button):
    await asyncio.sleep(0.1)
    gamepad.press_button(button=button)
    gamepad.update()
    await asyncio.sleep(0.2)
    gamepad.release_button(button=button)
    gamepad.update()
    await asyncio.sleep(0.2)

async def handle_client(websocket, path):
    async for message in websocket:
        button_name = message.lower()
        try:
            await press_xbutton(xbuttons[button_name])
        except KeyError:
            continue

async def main():
    port = random.randint(1023, 65535)
    address = os.popen("hostname -i").read().strip()
    
    print(f"Address: {address}:{port}")

    server = await websockets.serve(handle_client, address, port)    
    await server.wait_closed()

asyncio.run(main())
