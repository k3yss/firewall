import tkinter as tk
from tkinter import *
import subprocess
from datetime import datetime as dt
import os

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLACK = "#000000"
SMOKE= "#848884"
Glaucous="#7393B3"
AshGray="#C0C0C0"
FONT_NAME = "Courier"

def load_module():
    run_command("insmod ./src/firewall.ko ip_addr_rule=127.0.0.1")

def remove_module():
    run_command("rmmod ./src/firewall.ko")

# def list_module():
#     pass


def show_log():
    dmesg_text.delete(1.0, tk.END)
    result = subprocess.run(['dmesg'], capture_output=True, text=True)
    dmesg_lines = result.stdout.splitlines()[-10:]  # Get the last 10 lines of dmesg output
    dmesg_output = "\n".join(dmesg_lines)
    dmesg_text.insert(tk.END, f"{dt.now().strftime('%H:%M:%S')}:")
    dmesg_text.insert(tk.END, dmesg_output)

def enter_run(event):
    run_command()
    
def select_test(event):
    test = clicked.get()
    return test
    
    
def run_command(command=""):
    # sudo_password = "1212"  # Replace with the actual sudo password

    # if command=="":
    #     command = command_entry.get()
        
    # if command == "clear":
    #     terminal_output.delete("1.0", tk.END)
        
    # if command.startswith("cd "):
        
    #     try:
    #         directory = command.split("cd ")[1]
    #         os.chdir(directory)
    #         terminal_output.insert(tk.END, f"\nDirectory changed to: {directory}\n", "blue")  # Provide a message to confirm directory change
            
    #     except FileNotFoundError:
    #         terminal_output.insert(tk.END, f"\nDirectory not found: {directory}\n",'brown')

        
    # else:
        
    #     # if command.startswith("sudo"):
    #     #     # Handle sudo command securely
    #     #     command = f'echo {sudo_password} | sudo -S {command[5:]}'  # Modify the command to include sudo password input
        
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
            
    #     terminal_output.insert(tk.END, f"\n{os.getcwd()}>$ ","red")
    #     terminal_output.insert(tk.END, f"{command}\n","green")
    #     for line in process.stdout:
    #         # terminal_output.insert(tk.END, line)  # Update the terminal output with new lines
    #         terminal_output.insert(tk.END, f"{line}")
    #         terminal_output.see(tk.END)  # Scroll to the end to show the latest output
    # command_entry.delete(0, "end")
    
    
def run_test():
    type = clicked.get()
    hostname = ip_test_entry.get("1.0", "end-1c")
    if type == "ping":   
        cmd = 'ping -c 5 ' + hostname
    elif type == "wget":
        cmd = 'wget ' + hostname
        
    response = subprocess.getoutput(cmd)
    op_text.delete(1.0, tk.END)
    op_text.insert(tk.END, f"Time : {dt.now().strftime('%H:%M:%S')}:","blue")
    op_text.insert(tk.END, f"\n{os.getcwd()}> $ ","red")
    op_text.insert(tk.END, f"{cmd}\n","green")
    op_text.insert(tk.END, response)
    

window = Tk()
window.title("Netfilter Firewall")
window.geometry('760x900')
# window.config(padx=100, pady=20, bg=Glaucous)

#Create a main frame
main_frame = Frame(window)
main_frame.pack(fill=BOTH,expand=1)

#Create a canvas 
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

#Add a scroll bar to the canvas
my_scrollbar = Scrollbar(main_frame,orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

#Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion=my_canvas.bbox("all")))
# main_frame.bind_all("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))

#Create a 2nd frame inside canvas
second_frame = Frame(my_canvas)
second_frame.config(padx=50, pady=20, bg=Glaucous)

#Add that new frame to a window inside canvas
my_canvas.create_window((0,0),window=second_frame,anchor="ne")


title = Label(second_frame,text="Netfilter Firewall", font=(FONT_NAME, 25, "bold"), bg=Glaucous, fg=GREEN)
title.pack(pady=10)


ip_label = Label(second_frame, text="Enter IP addresses:",font=("Arial", 12, "bold"), bg=Glaucous, fg=BLACK)
ip_label.pack()
ip_text = Text(second_frame, height = 1, width = 30, bg = "light cyan")
ip_text.insert("1.0", "142.250.4.103")
ip_text.pack()


kernel_frame = Frame(second_frame)
kernel_frame.config(bg=Glaucous)
kernel_frame.pack()

load_but = Button(kernel_frame,text="Load Module", width=15, command=load_module)
load_but.grid(row=0,column=0,padx=5,pady=10)
remove_but = Button(kernel_frame,text="Remove Module", width=15,command=remove_module)
remove_but.grid(row=0,column=1,padx=5,pady=10)
# list_but = Button(second_frame,text="List Module", width=12, command=list_module)
# list_but.pack(pady=10)

refresh_button = Button(kernel_frame, text="Refresh dmesg logs", command=show_log)
refresh_button.grid(row=0,column=3,padx=5,pady=10)

dmesg_text = Text(second_frame, height=15, width=80,bg = AshGray)
dmesg_text.pack(pady=10)
refresh_button.invoke()

# # Terminal Section
# command_entry = Entry(second_frame, width=50,bg = AshGray)
# command_entry.bind('<Return>', enter_run)
# command_entry.pack(pady=10)


# run_button = Button(second_frame, text="Run Command", command=run_command)
# run_button.pack(pady=10)

# terminal_output = Text(second_frame, height=10, width=80,bg = AshGray)
# terminal_output.tag_configure("green", foreground="green")
# terminal_output.tag_configure("blue", foreground="blue")
# terminal_output.tag_configure("red", foreground="red")
# terminal_output.pack(pady=10)

options = ["ping", "wget"]

clicked = StringVar()
clicked.set(options[0])

run_frame = Frame(second_frame)
run_frame.config(bg=Glaucous)
run_frame.pack()

drop = OptionMenu(run_frame,clicked,*options,command=select_test)
drop.config(width = 12)
drop.grid(row=0,column=0,padx=5,pady=10)

ip_test_entry = Text(run_frame, height = 1, width = 30, bg = "light cyan")
ip_test_entry.insert("1.0", "142.250.4.103")
ip_test_entry.grid(row=0,column=1,padx=5,pady=10)

test_button = Button(run_frame,text = "Run Test", width = 12, command = run_test)
test_button.grid(row=0,column=2,padx=5,pady=10)

op_text = Text(second_frame, height=15, width=80,bg = AshGray)
op_text.tag_configure("green", foreground="green")
op_text.tag_configure("blue", foreground="blue")
op_text.tag_configure("red", foreground="red")
op_text.pack(pady=10)


exit = Button(second_frame, text = "Exit", width = 12, command = window.destroy)
exit.pack(pady=10)

# show_log()
window.mainloop()