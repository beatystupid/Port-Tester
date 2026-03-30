import tkinter as tk
from tkinter import filedialog, messagebox

def generate_script():
    raw_ips = ip_text.get("1.0", tk.END).strip().split("\n")
    raw_ports = port_entry.get().split(",")

    # Clean inputs
    ips = [ip.strip() for ip in raw_ips if ip.strip()]
    ports = [p.strip() for p in raw_ports if p.strip().isdigit()]

    if not ips:
        messagebox.showerror("Error", "Enter at least one valid IP")
        return

    if not ports:
        messagebox.showerror("Error", "Enter valid ports (numbers only)")
        return

    show_closed = closed_var.get()

    # Build PowerShell script
    ps_script = "$ips = @(\n"
    ps_script += ",\n".join([f'    "{ip}"' for ip in ips])
    ps_script += "\n)\n\n"

    ps_script += "$ports = @(" + ", ".join(ports) + ")\n\n"

    ps_script += "foreach ($ip in $ips) {\n"
    ps_script += '    Write-Host "Checking $ip..." -ForegroundColor Cyan\n\n'
    ps_script += "    foreach ($port in $ports) {\n"
    ps_script += "        $result = Test-NetConnection -ComputerName $ip -Port $port -WarningAction SilentlyContinue\n\n"

    ps_script += "        if ($result.TcpTestSucceeded) {\n"
    ps_script += '            Write-Host "  Port $port OPEN" -ForegroundColor Green\n'
    ps_script += "        }\n"

    if show_closed:
        ps_script += "        else {\n"
        ps_script += '            Write-Host "  Port $port CLOSED" -ForegroundColor DarkGray\n'
        ps_script += "        }\n"

    ps_script += "    }\n\n    Write-Host \"\"\n}\n"

    # Add pause at the end
    ps_script += 'Read-Host -Prompt "Press Enter to exit"\n'

    # Save file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ps1",
        filetypes=[("PowerShell Script", "*.ps1")]
    )

    if file_path:
        with open(file_path, "w") as f:
            f.write(ps_script)
        messagebox.showinfo("Success", f"Script saved:\n{file_path}")

# GUI setup
root = tk.Tk()
root.title("PS1 Port Scanner Generator")

tk.Label(root, text="Enter IPs (one per line):").pack(pady=(10, 0))
ip_text = tk.Text(root, height=10, width=40)
ip_text.pack(padx=10, pady=(0,10))

tk.Label(root, text="Enter Ports (comma separated):").pack()
port_entry = tk.Entry(root, width=40)
port_entry.pack(padx=10, pady=(0,10))

closed_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show CLOSED ports too", variable=closed_var).pack(pady=(0,10))

generate_button = tk.Button(root, text="Generate .ps1 Script", command=generate_script)
generate_button.pack(pady=(0,15))

root.mainloop()