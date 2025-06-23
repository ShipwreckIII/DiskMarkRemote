import tkinter as tk
from tkinter import messagebox, ttk
import requests
import subprocess
import os

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

        # Get pools
        r = session.get(f"{session.base_url}/pool")
        r.raise_for_status()
        pool_list = [p["name"] for p in r.json()]
        pool_dropdown["values"] = pool_list
        if pool_list:
            pool_dropdown.set(pool_list[0])
        messagebox.showinfo("Connected", f"TrueNAS Version: {version}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def list_datasets():
    selected_pool = pool_dropdown.get()
    if not selected_pool:
        messagebox.showwarning("No Pool", "Select a pool first.")
        return

    try:
        r = session.get(f"{session.base_url}/pool/dataset?name={selected_pool}")
        r.raise_for_status()
        datasets = [d["name"] for d in r.json()]
        messagebox.showinfo("Datasets", "\n".join(datasets) if datasets else "No datasets found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_fio_local():
    try:
        # Check if fio is available
        result = subprocess.run(["fio", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Error", "fio is not installed or not in PATH.")
            return

        # Run simple benchmark on C: drive (you can change this)
        fio_cmd = [
            "fio",
            "--name=randread",
            "--ioengine=windowsaio",
            "--filename=C:\\fio_test_file",
            "--bs=4k",
            "--size=128M",
            "--readwrite=randread",
            "--iodepth=8",
            "--runtime=10",
            "--time_based"
        ]

        result = subprocess.run(fio_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Benchmark Done", result.stdout)
        else:
            messagebox.showerror("Benchmark Failed", result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_results():
    filepath = "fio_test_file"
    if os.path.exists(filepath):
        os.remove(filepath)
    messagebox.showinfo("Note", "Results are shown directly after benchmark for now.\nYou can extend this to save CSV.")

# GUI setup
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

tk.Button(root, text="Connect", command=connect).grid(row=3, columnspan=2, pady=4)

tk.Label(root, text="Pool:").grid(row=4)
pool_dropdown = ttk.Combobox(root, state="readonly")
pool_dropdown.grid(row=4, column=1)

tk.Button(root, text="List Datasets", command=list_datasets).grid(row=5, columnspan=2, pady=4)
tk.Button(root, text="Run Benchmark (Local)", command=run_fio_local).grid(row=6, columnspan=2, pady=4)
tk.Button(root, text="Show Results", command=show_results).grid(row=7, columnspan=2, pady=4)

root.mainloop()
