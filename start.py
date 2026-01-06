import pydivert
import threading
import time
import keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key

# =====================================================
# SPEED CONTROL (MACRO A)
# =====================================================
SPEED = 2.5   # same as your original

# =====================================================
# CONTROLLERS
# =====================================================
mouse = MouseController()
kb = KeyboardController()

# =====================================================
# NETWORK FREEZE (F8)
# =====================================================
FILTER = "true"
network_running = False
network_thread = None
last_toggle = 0

def network_blocker():
    global network_running
    print("[❌] NETWORK FROZEN (packets dropped)")
    with pydivert.WinDivert(FILTER) as w:
        for packet in w:
            if not network_running:
                break
    print("[✅] NETWORK RESTORED")

def toggle_network():
    global network_running, network_thread, last_toggle

    now = time.time()
    if now - last_toggle < 0.4:
        return
    last_toggle = now

    if not network_running:
        network_running = True
        network_thread = threading.Thread(
            target=network_blocker,
            daemon=True
        )
        network_thread.start()
    else:
        network_running = False

# =====================================================
# MACRO A (FULL – FAST MACRO, UNCHANGED)
# =====================================================
macro_a_events = [
    {"time": 0.55213, "type": "key_press", "key": "q"},
    {"time": 1.055171, "type": "key_release", "key": "q"},

    {"time": 1.54583, "type": "mouse_click", "button": Button.left, "action": "pressed", "x": 981, "y": 455},
    {"time": 2.454857, "type": "mouse_click", "button": Button.right, "action": "pressed", "x": 981, "y": 455},
    {"time": 2.611821, "type": "mouse_click", "button": Button.left, "action": "released", "x": 981, "y": 455},
    {"time": 2.651844, "type": "mouse_click", "button": Button.right, "action": "released", "x": 981, "y": 455},

    {"time": 2.900000, "type": "key_press", "key": Key.f8},
    {"time": 2.970000, "type": "key_release", "key": Key.f8},

    {"time": 3.069828, "type": "key_press", "key": Key.tab},
    {"time": 3.15291,  "type": "key_release", "key": Key.tab},

    {"time": 3.786779, "type": "mouse_click", "button": Button.left, "action": "pressed", "x": 1500, "y": 352},
    {"time": 3.798635, "type": "mouse_move", "x": 1500, "y": 352},
    {"time": 3.820652, "type": "mouse_move", "x": 1500, "y": 352},
    {"time": 3.831582, "type": "mouse_move", "x": 1493, "y": 351},
    {"time": 3.841645, "type": "mouse_move", "x": 1473, "y": 350},
    {"time": 3.852613, "type": "mouse_move", "x": 1426, "y": 345},
    {"time": 3.863581, "type": "mouse_move", "x": 1344, "y": 338},
    {"time": 3.874591, "type": "mouse_move", "x": 1239, "y": 331},
    {"time": 3.884636, "type": "mouse_move", "x": 1130, "y": 325},
    {"time": 3.895584, "type": "mouse_move", "x": 1005, "y": 322},
    {"time": 3.905603, "type": "mouse_move", "x": 891,  "y": 322},
    {"time": 3.915603, "type": "mouse_move", "x": 783,  "y": 332},
    {"time": 3.926576, "type": "mouse_move", "x": 681,  "y": 346},
    {"time": 3.936588, "type": "mouse_move", "x": 611,  "y": 359},
    {"time": 3.946595, "type": "mouse_move", "x": 559,  "y": 368},
    {"time": 3.957601, "type": "mouse_move", "x": 519,  "y": 374},
    {"time": 3.968573, "type": "mouse_move", "x": 490,  "y": 377},
    {"time": 3.978608, "type": "mouse_move", "x": 471,  "y": 379},
    {"time": 3.989574, "type": "mouse_move", "x": 457,  "y": 379},
    {"time": 4.00062,  "type": "mouse_move", "x": 450,  "y": 379},
    {"time": 4.012648, "type": "mouse_move", "x": 447,  "y": 379},

    {"time": 4.295903, "type": "mouse_click", "button": Button.left, "action": "released", "x": 447, "y": 379},

    {"time": 4.723861, "type": "key_press", "key": Key.tab},
    {"time": 4.793927, "type": "key_release", "key": Key.tab},
]

# --- pre-scale Macro A ---
scaled_a = []
prev = macro_a_events[0]["time"]
for e in macro_a_events:
    scaled_a.append(((e["time"] - prev) / SPEED, e))
    prev = e["time"]

def run_macro_a():
    print("[▶] Macro A started")
    for delay, e in scaled_a:
        if delay > 0:
            time.sleep(delay)

        if e["type"] == "mouse_move":
            mouse.position = (e["x"], e["y"])
        elif e["type"] == "mouse_click":
            mouse.position = (e["x"], e["y"])
            mouse.press(e["button"]) if e["action"] == "pressed" else mouse.release(e["button"])
        elif e["type"] == "key_press":
            kb.press(e["key"])
        elif e["type"] == "key_release":
            kb.release(e["key"])
    print("[■] Macro A finished")

# =====================================================
# MACRO B (FULL – NETWORK + CLICK SPAM, UNCHANGED)
# =====================================================
macro_b_events = [
    (7.924503, "mouse_press"),
    (8.020676, "mouse_release"),
    (8.056484, "mouse_press"),
    (8.152533, "mouse_release"),
    (8.195481, "mouse_press"),

    (8.267641, "f8_press"),
    (8.280489, "mouse_release"),

    (8.331510, "mouse_press"),
    (8.334621, "f8_release"),

    (8.421673, "f8_press"),
    (8.424594, "mouse_release"),

    (8.464511, "mouse_press"),
    (8.478775, "f8_release"),

    (8.565165, "mouse_release"),
    (8.569746, "f8_press"),

    (8.601484, "mouse_press"),
    (8.616657, "f8_release"),

    (8.701561, "mouse_release"),
    (8.706651, "f8_press"),

    (8.732472, "mouse_press"),
    (8.738609, "f8_release"),

    (8.760614, "f8_press"),
    (8.783597, "f8_release"),

    (8.827462, "mouse_release"),
    (8.863482, "mouse_press"),
    (8.956488, "mouse_release"),
    (9.003550, "mouse_press"),
    (9.094495, "mouse_release"),
    (9.250000, "f8_press"),
    (9.320000, "f8_release"),
]

def run_macro_b():
    print("[▶] Macro B started")
    base = macro_b_events[0][0]
    for t, action in macro_b_events:
        time.sleep(t - base)
        base = t

        if action == "mouse_press":
            mouse.press(Button.left)
        elif action == "mouse_release":
            mouse.release(Button.left)
        elif action == "f8_press":
            kb.press(Key.f8)
        elif action == "f8_release":
            kb.release(Key.f8)

    print("[■] Macro B finished")

# =====================================================
# COMBINED EXECUTION
# =====================================================
macro_running = False

def run_both():
    global macro_running
    if macro_running:
        return
    macro_running = True
    try:
        run_macro_a()
        time.sleep(0.1)  # 🔥 EXACT 100 ms delay
        run_macro_b()
    finally:
        macro_running = False

# =====================================================
# KEY HOOKS
# =====================================================
def on_key(event):
    if event.event_type != "down":
        return

    if event.name == "f8":
        toggle_network()

    elif event.name == "f5":
        threading.Thread(target=run_both, daemon=True).start()

keyboard.hook(on_key)

# =====================================================
# INFO
# =====================================================
print("======================================")
print("🔥 FULL COMBINED MACRO READY")
print("F5 → Macro A → 100ms → Macro B")
print("F8 → Toggle Network Freeze")
print("RUN AS ADMINISTRATOR")
print("CTRL + C → Exit")
print("======================================")

keyboard.wait()
