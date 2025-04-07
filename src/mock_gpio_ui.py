
# enhanced_mock_gpio_ui.py — Mock RPi.GPIO with Tkinter UI, tabs, and visual layout

import logging
import tkinter as tk
from tkinter import ttk, scrolledtext
from threading import Thread
from os_utils import is_macos
logging.basicConfig(level=logging.DEBUG, format='[MOCK GPIO] %(message)s')

# Constants
BCM = 'BCM'
BOARD = 'BOARD'
IN = 'IN'
OUT = 'OUT'
PUD_UP = 'PUD_UP'
PUD_DOWN = 'PUD_DOWN'
HIGH = 1
LOW = 0

# State tracking
_pin_states = {}
_pin_modes = {}
_input_pins = []
_output_pins = []
_mode_set = None  # BCM or BOARD

# BOARD to BCM mapping (for Raspberry Pi 3/4 Model B 40-pin header)
BOARD_TO_BCM = {
    3: 2, 5: 3, 7: 4, 8: 14, 10: 15, 11: 17, 12: 18,
    13: 27, 15: 22, 16: 23, 18: 24, 19: 10, 21: 9,
    22: 25, 23: 11, 24: 8, 26: 7, 29: 5, 31: 6,
    32: 12, 33: 13, 35: 19, 36: 16, 37: 26, 38: 20, 40: 21
}

# Logging
logging.basicConfig(level=logging.DEBUG, format='[MOCK GPIO] %(message)s')

# Helper
def _resolve_pin(pin):
    if _mode_set is None:
        raise RuntimeError("Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)")
    if _mode_set == BOARD:
        if pin not in BOARD_TO_BCM:
            raise ValueError(f"Invalid BOARD pin number: {pin}")
        return BOARD_TO_BCM[pin]
    else:
        return pin

def setmode(mode):
    global _mode_set
    if mode not in (BCM, BOARD):
        raise ValueError("Invalid mode. Use GPIO.BCM or GPIO.BOARD")
    _mode_set = mode
    logging.debug(f"GPIO mode set to {mode}")

def setup(pin, mode, pull_up_down=None):
    bcm_pin = _resolve_pin(pin)
    # default to low state
    _pin_states[bcm_pin] = LOW if pull_up_down == PUD_UP else HIGH
    _pin_modes[bcm_pin] = mode
    if mode == IN:
        _input_pins.append(bcm_pin)
    elif mode == OUT:
        _output_pins.append(bcm_pin)
    logging.debug(f"Pin {pin} ({bcm_pin}) set up as {mode}, pull={pull_up_down}")

def input(pin):
    bcm_pin = _resolve_pin(pin)
    state = _pin_states.get(bcm_pin, LOW)
    logging.debug(f"Reading pin {pin} ({bcm_pin}): {state}")
    return state

def output(pin, state):
    bcm_pin = _resolve_pin(pin)
    if _pin_modes.get(bcm_pin) == OUT:
        _pin_states[bcm_pin] = state
        logging.debug(f"Writing to pin {pin} ({bcm_pin}): {state}")
    else:
        raise RuntimeError(f"Pin {pin} is not set as an output")

def cleanup():
    logging.debug("Cleaning up GPIO pins")
    _pin_states.clear()
    _pin_modes.clear()
    _input_pins.clear()
    _output_pins.clear()
    global _mode_set
    _mode_set = None

# GUI
def build_ui():
    root = tk.Tk()
    root.title("Enhanced GPIO Mock UI (macOS Safe)")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Input Tab
    input_frame = ttk.Frame(notebook)
    notebook.add(input_frame, text='Inputs')

    input_label = tk.Label(input_frame, text="Simulate Sensor Inputs", font=("Arial", 12, "bold"))
    input_label.pack(pady=5)

    button_frame = tk.Frame(input_frame)
    button_frame.pack(pady=5)

    input_labels = {}
    input_buttons = {}
    def toggle(pin, event):
        print(event)
        current = _pin_states.get(pin, LOW)
        print(f"current state: {current}")
        new_state = HIGH if current == LOW else LOW
        _pin_states[pin] = new_state
        color = "green" if new_state == LOW else "red"
        input_labels[pin].config(
            text=f"GPIO {pin}: {new_state}",
            bg=color
        )
        logging.debug(f"Toggled GPIO {pin} to {new_state}")

    
    total_length = len(_input_pins)
    max_rows = 20
    columns = 1
    if total_length > max_rows:
        columns = total_length// max_rows + 1

    for idx, pin in enumerate(sorted(set(_input_pins))):
        
        current_state = _pin_states.get(pin, LOW)
        row=idx // columns
        column=idx % columns
        color = "green" if current_state == LOW else "red"
        lbl = tk.Label(button_frame, text=f"GPIO {pin}: {current_state}", width=20,
                    relief="groove", bd=2, bg=color)
        lbl.bind("<Button>", lambda e, p=pin: toggle(p, e))
        lbl.grid(row=row, column=column, padx=5, pady=2, sticky="ew")
        input_labels[pin] = lbl
        _pin_states[pin] = current_state

        
        

    # Output Tab
    output_frame = ttk.Frame(notebook)
    notebook.add(output_frame, text='Outputs')

    output_label = tk.Label(output_frame, text="Output Pin States", font=("Arial", 12, "bold"))
    output_label.pack(pady=5)

    output_box = scrolledtext.ScrolledText(output_frame, width=80, height=15, state='disabled')
    output_box.pack(padx=10, pady=5)

    def update_outputs():
        output_box.config(state='normal')
        output_box.delete(1.0, tk.END)
        for pin in sorted(_output_pins):
            val = _pin_states.get(pin, LOW)
            output_box.insert(tk.END, f"GPIO {pin} = {val}\n")
        output_box.config(state='disabled')
        output_box.after(1000, update_outputs)

    update_outputs()

    # Log Tab
    log_frame = ttk.Frame(notebook)
    notebook.add(log_frame, text='Logs')

    log_label = tk.Label(log_frame, text="GPIO Activity Log", font=("Arial", 12, "bold"))
    log_label.pack(pady=5)

    log_box = scrolledtext.ScrolledText(log_frame, width=80, height=15)
    log_box.pack(padx=10, pady=5)

    class TextHandler(logging.Handler):
        def emit(self, record):
            msg = self.format(record)
            log_box.insert(tk.END, msg + "\n")
            log_box.see(tk.END)

    handler = TextHandler()
    logging.getLogger().addHandler(handler)

    return root

def start_ui():
    root = build_ui()
    root.mainloop()

def start_ui_async():
    # Not recommended on macOS — included for compatibility
    Thread(target=start_ui, daemon=True).start()

def run_ui():
    if is_macos():        
        start_ui()
    else:
        start_ui_async()


