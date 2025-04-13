import tkinter as tk
from tkinter import messagebox
import requests

def connect():
    ip = entry_ip.get()
    user = entry_user.get()
    password = entry_pass.get()

    try:
        r = requests.get(f"http://{ip}/api/v2.0/system/info", auth=(user, password))
        data = r.json()
        messagebox.showinfo("Connected", f"TrueNAS Version: {data.get('version')}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("TrueNAS Connect")

tk.Label(root, text="TrueNAS IP:").grid(row=0)
tk.Label(root, text="Username:").grid(row=1)
tk.Label(root, text="Password:").grid(row=2)

entry_ip = tk.Entry(root)
entry_user = tk.Entry(root)
entry_pass = tk.Entry(root, show="*")

entry_ip.grid(row=0, column=1)
entry_user.grid(row=1, column=1)
entry_pass.grid(row=2, column=1)

tk.Button(root, text="Connect", command=connect).grid(row=3, columnspan=2)

root.mainloop()
