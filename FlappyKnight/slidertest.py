import tkinter as tk
from tkinter import simpledialog

def open_slider_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    popup = tk.Toplevel(root)
    popup.title("Slider Popup")
    popup.geometry(f"{sliderwidth}x{sliderheight}")

    slider = tk.Scale(popup, from_=0, to=1000, orient=tk.HORIZONTAL, length=slider_length)
    slider.pack(padx=20, pady=10)

    ok_button = tk.Button(popup, text="OK", command=lambda: on_ok_button(slider.get(), popup))
    ok_button.pack(pady=10)

    popup.grab_set()  # Make the popup grab the focus

    popup.mainloop()  # Run the popup's main loop

def on_ok_button(value, popup):
    print("Selected value:", value)
    popup.destroy()



open_slider_popup()