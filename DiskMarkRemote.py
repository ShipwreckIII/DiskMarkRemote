import tkinter as tk
from tkinter import messagebox
import requests

session = requests.Session()

def connect():
    global session
    ip = entry_ip.get()
    user = entry_user.get()
    password = entry_pass.get()
    session.auth = (user, password)
    session.base_url = f"http://{ip}/api/v2.0"
    try:
        r = session.get(f"{session.base_url}/system/info")
        r.raise_for_status()
        version = r.json().get("version")
        messagebox.showinfo("Connected", f"TrueNAS Version: {version}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def list_pools():
    try:
        r = session.get(f"{session.base_url}/pool")
        r.raise_for_status()
        pools = [p["name"] for p in r.json()]
        messagebox.showinfo("Pools", "\n".join(pools) if pools else "No pools found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("DiskMarkRemote")

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
tk.Button(root, text="List Pools", command=list_pools).grid(row=4, columnspan=2)

root.mainloop()
