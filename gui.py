import tkinter as tk
from tkinter import *
import subprocess
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
    run_command()

def remove_module():
    run_command("ls -l")

# def list_module():
#     pass


def show_log():
    result = subprocess.run(['dmesg'], capture_output=True, text=True)
    dmesg_lines = result.stdout.splitlines()[-10:]  # Get the last 10 lines of dmesg output
    dmesg_output = "\n".join(dmesg_lines)
    dmesg_text.delete(1.0, tk.END)
    dmesg_text.insert(tk.END, dmesg_output)

def enter_run(event):
    run_command()
    
    
def run_command(command=""):
    sudo_password = "1212"  # Replace with the actual sudo password

    if command=="":
        command = command_entry.get()
        
    if command == "clear":
        terminal_output.delete('1.0', tk.END)
        
    if command.startswith("cd "):
        
        try:
            directory = command.split("cd ")[1]
            os.chdir(directory)
            terminal_output.insert(tk.END, f"\nDirectory changed to: {directory}\n", "blue")  # Provide a message to confirm directory change
            
        except FileNotFoundError:
            terminal_output.insert(tk.END, f"\nDirectory not found: {directory}\n",'brown')

        
    else:
        
        # if command.startswith("sudo"):
        #     # Handle sudo command securely
        #     command = f'echo {sudo_password} | sudo -S {command[5:]}'  # Modify the command to include sudo password input
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
            
        terminal_output.insert(tk.END, f"\n{os.getcwd()}>$ ","red")
        terminal_output.insert(tk.END, f"{command}\n","green")
        for line in process.stdout:
            # terminal_output.insert(tk.END, line)  # Update the terminal output with new lines
            terminal_output.insert(tk.END, f"{line}")
            terminal_output.see(tk.END)  # Scroll to the end to show the latest output
    command_entry.delete(0, "end")


    # def run_command(command=""):
        
    #     if command=="":
    #         command = command_entry.get()
            
    #     if command == "clear":
    #         terminal_output.delete('1.0', tk.END)
    #     else:
    #         result = subprocess.run(command, shell=True, capture_output=True, text=True)
    #         # Insert and color text
    #         terminal_output.insert(tk.END, f"\n$ ","red")
    #         terminal_output.insert(tk.END, f"{command}","green")
    #         terminal_output.insert(tk.END, f"\n{result.stdout}")
    #     command_entry.delete(0, "end")

window = Tk()
window.title("Netfilter Firewall")
window.geometry('900x1200')
window.config(padx=100, pady=20, bg=Glaucous)

# Label
title = Label(text="Netfilter Firewall", font=(FONT_NAME, 25, "bold"), bg=Glaucous, fg=GREEN)
title.pack(pady=10)
ip_label = Label(window, text="Enter IP addresses:",font=("Arial", 12, "bold"), bg=Glaucous, fg=BLACK)
ip_label.pack()


# Entry
ip_text = Text(window, height = 1, width = 30, bg = "light cyan")
ip_text.pack()

# Buttons
load_but = Button(text="Load Module", width=12, command=load_module)
load_but.pack(pady=10)
remove_but = Button(text="Remove Module", width=12,command=remove_module)
remove_but.pack(pady=10)
# list_but = Button(text="List Module", width=12, command=list_module)
# list_but.pack(pady=10)
log_but = Button(text="Show log", width=12,command=show_log)
log_but.pack(pady=10)

refresh_button = Button(window, text="Refresh dmesg Logs", command=show_log)
refresh_button.pack(pady=10)

# dmesg_text = Text(window, height=15, width=100,bg = AshGray)
# dmesg_text.pack(pady=10)

# Terminal Section
command_entry = Entry(window, width=50,bg = AshGray)
command_entry.bind('<Return>', enter_run)
command_entry.pack(pady=10)


run_button = Button(window, text="Run Command", command=run_command)
run_button.pack(pady=10)

terminal_output = Text(window, height=10, width=100,bg = AshGray)
terminal_output.tag_configure("green", foreground="green")
terminal_output.tag_configure("blue", foreground="blue")
terminal_output.tag_configure("red", foreground="red")
terminal_output.pack(pady=10)


exit = Button(window, text = "Exit", width = 12, command = window.destroy)
exit.pack(pady=10)

# show_log()
window.mainloop()