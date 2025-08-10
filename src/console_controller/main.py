# src/console_controller/main.py
import json
import logging
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import vgamepad as vg

app = FastAPI()

logger = logging.getLogger("uvicorn.error")

# Keep track of connected clients and their virtual gamepads
clients: Dict[str, vg.VX360Gamepad] = {}
next_player = 1

# Utility: map simple string button ids to vgamepad constants
BUTTON_MAP = {
    "A": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    "B": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    "X": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    "Y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    "UP": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    "DOWN": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    "LEFT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    "RIGHT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    "LB": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    "RB": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    "START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    "BACK": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
}

def create_gamepad() -> vg.VX360Gamepad:
    """Create and return a connected virtual Xbox360 gamepad."""
    gp = vg.VX360Gamepad()
    # No explicit connect() call required — creating the object hooks into ViGEm.
    return gp

async def handle_ws(websocket: WebSocket):
    global next_player
    await websocket.accept()
    client_id = f"{websocket.client.host}:{websocket.client.port}"
    logger.info(f"Client connected: {client_id}")

    # create virtual pad for this connection
    pad = create_gamepad()
    player_id = next_player
    next_player += 1
    clients[client_id] = pad

    # send welcome with assigned player id
    await websocket.send_text(json.dumps({"type": "hello", "player": player_id}))

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                continue

            # button message: { "type":"button", "id":"A", "state": true }
            if msg.get("type") == "button":
                btn = msg.get("id")
                state = bool(msg.get("state"))
                const = BUTTON_MAP.get(btn)
                if const is not None:
                    if state:
                        pad.press_button(button=const)
                    else:
                        pad.release_button(button=const)
                    pad.update()  # send state to system

            # axis message: { "type":"axis", "id":"lx", "value": -1..1 }
            elif msg.get("type") == "axis":
                axis = msg.get("id")
                val = float(msg.get("value", 0.0))
                # left stick
                if axis == "lx" or axis == "ly":
                    # vgamepad expects floats for left_joystick_float(x_value_float, y_value_float)
                    # We'll maintain temporary state: easiest is to call both each time.
                    # For simplicity, we accept messages with both coords, or single-axis updates.
                    # Caller can send {id:"lx", value:0.5} and we merge; here we assume full pairs.
                    pass
                # for this simple example, allow direct left/right stick pair updates:
                if axis == "lstick":
                    x = float(msg.get("x", 0.0))
                    y = float(msg.get("y", 0.0))
                    pad.left_joystick_float(x_value_float=x, y_value_float=y)
                    pad.update()
                elif axis == "rstick":
                    x = float(msg.get("x", 0.0))
                    y = float(msg.get("y", 0.0))
                    pad.right_joystick_float(x_value_float=x, y_value_float=y)
                    pad.update()

            # trigger message: { "type":"trigger", "id":"lt", "value": 0..1 }
            elif msg.get("type") == "trigger":
                which = msg.get("id")
                v = float(msg.get("value", 0.0))
                if which == "lt":
                    pad.left_trigger_float(value_float=v)
                    pad.update()
                elif which == "rt":
                    pad.right_trigger_float(value_float=v)
                    pad.update()

    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {client_id}")
    finally:
        try:
            pad.reset()  # reset before cleanup
            del clients[client_id]
        except Exception:
            pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_ws(websocket)
    
app.mount("/", StaticFiles(directory="public", html=True), name="static")