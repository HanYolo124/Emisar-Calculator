import tkinter as tk
from tkinter import ttk

def calculate_aux_led_runtime(led_colors_quantities, brightness, battery_capacity_mah):
    low_brightness_current = {
        "red": 0.01,
        "green": 0.0075,
        "blue": 0.0075,
        "cyan": 0.0125,
        "purple": 0.015,
        "yellow": 0.016,
        "white": 0.021,
    }

    high_brightness_current = {
        "red": 0.375,
        "green": 0.158,
        "blue": 0.169,
        "cyan": 0.315,
        "purple": 0.525,
        "yellow": 0.516,
        "white": 0.661,
    }

    if brightness == "low":
        currents = low_brightness_current
    elif brightness == "high":
        currents = high_brightness_current
    else:
        raise ValueError("Invalid brightness level. Choose 'low' or 'high'.")

    total_current_draw = sum(currents[color] * num_leds for color, num_leds in led_colors_quantities.items())
    runtime_hours = (battery_capacity_mah / total_current_draw) * 1000 / 1000

    return runtime_hours

def calculate_runtime():
    # Get user input
    battery_capacity_mah = int(battery_capacity_var.get())
    brightness = brightness_var.get()

    led_colors_quantities = {}
    for color, num_leds_var in leds_vars.items():
        num_leds_str = num_leds_var.get().strip()
        if num_leds_str:
            num_leds = int(num_leds_str)
            if num_leds > 0:
                led_colors_quantities[color] = num_leds

    # Calculate runtime
    runtime_hours = calculate_aux_led_runtime(led_colors_quantities, brightness, battery_capacity_mah)
    runtime_days = runtime_hours / 24
    runtime_years = runtime_days / 365.25

    if runtime_years < 1:
        result_var.set(f"Total runtime for the given LED configuration: {runtime_days:.2f} days")
    else:
        result_var.set(f"Total runtime for the given LED configuration: {runtime_years:.2f} years")

root = tk.Tk()
root.title("Emisar Aux LED Runtime Calculator")

# Variables
battery_capacity_var = tk.StringVar()
brightness_var = tk.StringVar()
leds_vars = {color: tk.StringVar() for color in ["red", "green", "blue", "cyan", "purple", "yellow", "white"]}
result_var = tk.StringVar()

# Create widgets
battery_capacity_label = ttk.Label(root, text="Battery Capacity (mAh):")
battery_capacity_entry = ttk.Entry(root, textvariable=battery_capacity_var)

brightness_label = ttk.Label(root, text="Brightness Level:")
brightness_combobox = ttk.Combobox(root, textvariable=brightness_var, values=["low", "high"], state="readonly")

leds_labels_entries = []
for i, color in enumerate(leds_vars.keys()):
    color_label = ttk.Label(root, text=f"{color.capitalize()} LEDs:")
    color_entry = ttk.Entry(root, textvariable=leds_vars[color])
    leds_labels_entries.append((color_label, color_entry))

calculate_button = ttk.Button(root, text="Calculate", command=calculate_runtime)
result_label = ttk.Label(root, textvariable=result_var)

# Place widgets
battery_capacity_label.grid(row=0, column=0, sticky="e")
battery_capacity_entry.grid(row=0, column=1, sticky="w")

brightness_label.grid(row=1, column=0, sticky="e")
brightness_combobox.grid(row=1, column=1, sticky="w")

for i, (color_label, color_entry) in enumerate(leds_labels_entries):
    color_label.grid(row=2+i, column=0, sticky="e")
    color_entry.grid(row=2+i, column=1, sticky="w")

calculate_button.grid(row=10, column=0, sticky="e")
result_label.grid(row=10, column=1, sticky="w")

# Add credit label
credit_label = ttk.Label(root, text="Developed by Chat GPT-4 & u/HanYolo124")

# Place the credit label
credit_label.grid(row=11, column=0, columnspan=2, pady=(10, 0))

root.mainloop()
