import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports  

# Function to read data from selected serial port
def read_data():
    try:
        selected_port = port_combobox.get()
        selected_baudrate = int(baudrate_combobox.get())
        ser = serial.Serial(selected_port, selected_baudrate)
        while True:
            data = ser.readline().decode().strip()  # Read a line of data from serial port
            # Process the data here, for now, let's just print it
            print(data)
            # Update the GUI with the received data
            update_plot(data)
    except serial.SerialException as e:
        print("Serial port error:", e)

# Function to update the plot with new data
def update_plot(data):
    # Parse the data and update the plot
    # This is just a placeholder, replace it with your data processing logic
    try:
        values = [float(val) for val in data.split(',')]
        for i, value in enumerate(values):
            x_data[i].append(len(x_data[i]))
            y_data[i].append(value)
            lines[i].set_xdata(x_data[i])
            lines[i].set_ydata(y_data[i])
            axes[i].relim()
            axes[i].autoscale_view()
        canvas.draw()
    except ValueError:
        print("Invalid data received:", data)

# Function to refresh available serial ports
def refresh_ports():
    port_combobox['values'] = [port.device for port in serial.tools.list_ports.comports()]

# Function to handle 'OK' button click event
def ok_button_click():
    # Start reading data from selected serial port
    read_data()


# Function to handle menu item clicks
def menu_click(menu_item):
    messagebox.showinfo("Clicked", f"You clicked {menu_item}.")

#-----------------------

window = tk.Tk()
window.title("My Oscilloscope")
window.resizable(height=False,width=False)
frame = tk.Frame(window)
frame.pack()

#-----------------------

# Menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=lambda: menu_click("New"))
file_menu.add_command(label="Open", command=lambda: menu_click("Open"))
file_menu.add_separator()
file_menu.add_command(label="Save", command=lambda: menu_click("Save"))
file_menu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=lambda: menu_click("Cut"))
edit_menu.add_command(label="Copy", command=lambda: menu_click("Copy"))
edit_menu.add_command(label="Paste", command=lambda: menu_click("Paste"))
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Options menu
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Option1", command=lambda: menu_click("Option 1"))
options_menu.add_command(label="Option2", command=lambda: menu_click("Option 2"))
menu_bar.add_cascade(label="Options", menu=options_menu)

# View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="View1", command=lambda: menu_click("View 1"))
view_menu.add_command(label="View2", command=lambda: menu_click("View 2"))
menu_bar.add_cascade(label="View", menu=view_menu)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=lambda: menu_click("About"))
menu_bar.add_cascade(label="Help", menu=help_menu)

#-----------------------
# Add selection buttons for serial port and baud rate at the top
port_label = ttk.Label(window, text="Select Port:")
port_label.pack(side=tk.LEFT, padx=5, pady=5)

port_combobox = ttk.Combobox(window, width=20, state="readonly")
port_combobox.pack(side=tk.LEFT, padx=5, pady=5)

refresh_ports()  # Populate initial list of available ports
refresh_button = ttk.Button(window, text="Refresh Ports", command=refresh_ports)
refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

baudrate_label = ttk.Label(window, text="Select Baud Rate:")
baudrate_label.pack(side=tk.LEFT, padx=5, pady=5)

baudrate_combobox = ttk.Combobox(window, width=10, state="readonly")
baudrate_combobox['values'] = [9600, 19200, 38400, 57600, 115200]  # You can add more baud rates if needed
baudrate_combobox.current(0)
baudrate_combobox.pack(side=tk.LEFT, padx=5, pady=5)

ok_button = ttk.Button(window, text="Connect", command="")
ok_button.pack(side=tk.LEFT, padx=5, pady=10)

# To center-align horizontally
window.update_idletasks()
x = (window.winfo_width() - port_label.winfo_reqwidth() - port_combobox.winfo_reqwidth() -
     refresh_button.winfo_reqwidth() - baudrate_label.winfo_reqwidth() - baudrate_combobox.winfo_reqwidth() -
     ok_button.winfo_reqwidth()) / 2

port_label.pack_configure(padx=(x, 5))
port_combobox.pack_configure(padx=5)
refresh_button.pack_configure(padx=5)
baudrate_label.pack_configure(padx=5)
baudrate_combobox.pack_configure(padx=5)
ok_button.pack_configure(padx=5)


#-----------------------

# Graph 
terms_frame_0 = tk.LabelFrame(frame, text="", width=500, height=400)
terms_frame_0.grid(row=1, columnspan=4, padx=5, pady=5)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
lines = []
x_data = []
y_data = []
line, = ax.plot(x_data, y_data)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.set_title('')
lines.append(line)

# Embed the plots into the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=terms_frame_0)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#-----------------------

#Time/DIV Menu
terms_frame_1 = tk.LabelFrame(frame, text="Time/DIV",)
terms_frame_1.grid(row=2, column=0, padx=5, pady=5)

time_div_buttons = [
    "100ms", "40ms", "20ms", "10ms", "4ms", "2ms", "1ms", "0.4ms", "0.2ms", "0.1ms",
    "40us", "20us", "10us", "4us", "2us", "1us", "0.4us", "0.2us", "0.1us", "0.05us"]

for i, button_name in enumerate(time_div_buttons):
    button = tk.Button(terms_frame_1, text=button_name, width=5, height=1)
    button.grid(row=i // 5, column=i % 5, padx=5, pady=5)

#-----------------------

#Volts/DIV Menu
terms_frame_2 = tk.LabelFrame(frame, text="Volts/DIV")
terms_frame_2.grid(row=2, column=1, pady=5)

volts_div_labels = ["3V", "1V", "0.3V", "0.1V", "30mV", "10mV"]

for i, label_name in enumerate(volts_div_labels):
    button = tk.Button(terms_frame_2, text=label_name, width=4, height=1)
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

coupling_label = tk.Label(terms_frame_2, text="Coupling:")
coupling_label.grid(row=len(volts_div_labels), column=0, padx=5, pady=5)

ac_button = tk.Button(terms_frame_2, text="AC")
ac_button.grid(row=len(volts_div_labels), column=1, padx=5, pady=5)

dc_button = tk.Button(terms_frame_2, text="DC")
dc_button.grid(row=len(volts_div_labels), column=2, padx=5, pady=5)

#-----------------------

#Trigger Menu
terms_frame_3 = tk.LabelFrame(frame, text="Trigger", width=200, height=100)
terms_frame_3.grid(row=2, column=2, pady=5)

coupling_on_off_label = tk.Label(terms_frame_3, text="On/Off:")
coupling_on_off_label.grid(row=0, column=0, padx=5, pady=5)

coupling_on_button = tk.Button(terms_frame_3, text="On", width=5, height=1)
coupling_on_button.grid(row=0, column=1, padx=5, pady=5)

coupling_off_button = tk.Button(terms_frame_3, text="Off", width=5, height=1)
coupling_off_button.grid(row=0, column=2, padx=5, pady=5)

edge_label = tk.Label(terms_frame_3, text="Edge:")
edge_label.grid(row=1, column=0, padx=5, pady=5)

edge_left_button = tk.Button(terms_frame_3, text="<-", width=4, height=1)
edge_left_button.grid(row=1, column=1, padx=5, pady=5)

edge_right_button = tk.Button(terms_frame_3, text="->", width=4, height=1)
edge_right_button.grid(row=1, column=2, padx=5, pady=5)

#-----------------------

#Start and Stop frame
frame_4 = tk.LabelFrame(frame, text="", width=200, height=100)
frame_4.grid(row=2, column=3,padx=10, pady=5)

start_button = tk.Button(frame_4, text="Start", width=8, height=2)
start_button.grid(row=0, column=0, padx=5, pady=5)

stop_button = tk.Button(frame_4, text="Stop", width=8, height=2)
stop_button.grid(row=1, column=0, padx=5, pady=5)

auto_set_button = tk.Button(frame_4, text="AutoSet", width=8, height=2)
auto_set_button.grid(row=2, column=0, padx=5, pady=5)

#-----------------------

window.mainloop()
