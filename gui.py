from tkinter import (
    Tk,
    END,
    Frame,
    BOTH,
    Canvas,
    LEFT,
    Y,
    RIGHT,
    Scrollbar,
    VERTICAL,
    Label,
    Text,
    Button,
    StringVar,
    OptionMenu,
)
import subprocess
from datetime import datetime as dt
import os

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLACK = "#000000"
SMOKE = "#848884"
Glaucous = "#7393B3"
AshGray = "#C0C0C0"
FONT_NAME = "Courier"


def load_module():
    run_command(f"insmod ./src/firewall.ko ip_addr_rule={ip_text.get('1.0','end-1c')}")


def remove_module():
    run_command("rmmod ./src/firewall.ko")


def show_log():
    dmesg_text.delete(1.0, END)
    result = subprocess.run(["dmesg"], capture_output=True, text=True)
    dmesg_lines = result.stdout.splitlines()[
        -10:
    ]  # Get the last 10 lines of dmesg output
    dmesg_output = "\n".join(dmesg_lines)
    dmesg_text.insert(END, f"{dt.now().strftime('%H:%M:%S')}:")
    dmesg_text.insert(END, dmesg_output)


def enter_run():
    run_command()


def select_test():
    test = clicked.get()
    return test


def run_command(command=""):
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )


def run_test():
    type = clicked.get()
    hostname = ip_test_entry.get("1.0", "end-1c")
    cmd = ""
    if type == "ping":
        cmd = "ping -c 5 " + hostname
    elif type == "wget":
        cmd = "wget --timeout=5 --tries=1 " + hostname

    response = subprocess.getoutput(cmd)
    op_text.delete(1.0, END)
    op_text.insert(END, f"Time : {dt.now().strftime('%H:%M:%S')}:", "blue")
    op_text.insert(END, f"\n{os.getcwd()}> $ ", "red")
    op_text.insert(END, f"{cmd}\n", "green")
    op_text.insert(END, response)


window = Tk()
window.title("Netfilter Firewall")
window.geometry("760x900")
# window.config(padx=100, pady=20, bg=Glaucous)

# Create a main frame
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)

# Create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add a scroll bar to the canvas
my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind(
    "<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox("all"))
)
# main_frame.bind_all("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))

# Create a 2nd frame inside canvas
second_frame = Frame(my_canvas)
second_frame.config(padx=50, pady=20, bg=Glaucous)

# Add that new frame to a window inside canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="ne")


title = Label(
    second_frame,
    text="Netfilter Firewall",
    font=(FONT_NAME, 25, "bold"),
    bg=Glaucous,
    fg=GREEN,
)
title.pack(pady=10)


ip_label = Label(
    second_frame,
    text="Enter IP addresses:",
    font=("Arial", 12, "bold"),
    bg=Glaucous,
    fg=BLACK,
)
ip_label.pack()
ip_text = Text(second_frame, height=1, width=30, bg="light cyan")
ip_text.insert("1.0", "142.250.4.103")
ip_text.pack()


kernel_frame = Frame(second_frame)
kernel_frame.config(bg=Glaucous)
kernel_frame.pack()

load_but = Button(kernel_frame, text="Load Module", width=15, command=load_module)
load_but.grid(row=0, column=0, padx=5, pady=10)
remove_but = Button(kernel_frame, text="Remove Module", width=15, command=remove_module)
remove_but.grid(row=0, column=1, padx=5, pady=10)
# list_but = Button(second_frame,text="List Module", width=12, command=list_module)
# list_but.pack(pady=10)

refresh_button = Button(kernel_frame, text="Refresh dmesg logs", command=show_log)
refresh_button.grid(row=0, column=3, padx=5, pady=10)

dmesg_text = Text(second_frame, height=15, width=80, bg=AshGray)
dmesg_text.pack(pady=10)
refresh_button.invoke()

options = ["ping", "wget"]

clicked = StringVar()
clicked.set(options[0])

run_frame = Frame(second_frame)
run_frame.config(bg=Glaucous)
run_frame.pack()

drop = OptionMenu(run_frame, clicked, *options)
drop.config(width=12)
drop.grid(row=0, column=0, padx=5, pady=10)

ip_test_entry = Text(run_frame, height=1, width=30, bg="light cyan")
ip_test_entry.insert("1.0", "142.250.4.103")
ip_test_entry.grid(row=0, column=1, padx=5, pady=10)

test_button = Button(run_frame, text="Run Test", width=12, command=run_test)
test_button.grid(row=0, column=2, padx=5, pady=10)

op_text = Text(second_frame, height=15, width=80, bg=AshGray)
op_text.tag_configure("green", foreground="green")
op_text.tag_configure("blue", foreground="blue")
op_text.tag_configure("red", foreground="red")
op_text.pack(pady=10)


exit = Button(second_frame, text="Exit", width=12, command=window.destroy)
exit.pack(pady=10)

# show_log()
window.mainloop()
