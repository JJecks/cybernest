import time
import sqlite3
import shutil
import os
import requests
import ctypes
import ctypes.wintypes
import subprocess
import json
from datetime import datetime, timezone

# ── CONFIG ───────────────────────────────────────────────────────────────────
SERVER_URL = "http://127.0.0.1:8000/api"
POLL_INTERVAL = 5
BROWSER_SYNC_INTERVAL = 60
PRINT_SYNC_INTERVAL = 30
HEARTBEAT_INTERVAL = 15
CONFIG_FILE = "agent_config.json"
# ─────────────────────────────────────────────────────────────────────────────

machine_id = None


# ── CONFIG LOAD / SAVE ───────────────────────────────────────────────────────
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f)


def get_machine_name():
    config = load_config()
    if 'machine_name' in config:
        return config['machine_name']

    # Show a GUI dialog instead of terminal input
    import tkinter as tk
    from tkinter import simpledialog, messagebox

    root = tk.Tk()
    root.withdraw()  # hide the main window

    name = simpledialog.askstring(
        "CyberNest Setup",
        "Welcome to CyberNest!\n\nEnter a name for this PC:\n(e.g. PC-01, Cashier-PC, Reception)",
        initialvalue="PC-01"
    )

    if not name or not name.strip():
        messagebox.showerror("CyberNest", "PC name cannot be empty. Using 'PC-Unknown'.")
        name = "PC-Unknown"

    name = name.strip()
    config['machine_name'] = name
    save_config(config)

    messagebox.showinfo("CyberNest", f"PC registered as '{name}'.\nThe agent will now start tracking.")
    root.destroy()
    return name


# ── MACHINE REGISTRATION ─────────────────────────────────────────────────────
def get_mac_address():
    import uuid
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))


def register_machine(machine_name):
    global machine_id
    config = load_config()

    # Already registered before — use saved ID
    if 'machine_id' in config:
        machine_id = config['machine_id']
        print(f"[+] Using saved machine ID {machine_id} ({machine_name})")
        return

    mac = get_mac_address()
    try:
        res = requests.post(f"{SERVER_URL}/machines/", json={
            "name": machine_name,
            "mac_address": mac,
            "location": ""
        })
        if res.status_code in (200, 201):
            machine_id = res.json().get("id")
        elif res.status_code == 400:
            machines = requests.get(f"{SERVER_URL}/machines/all/").json()
            for m in machines:
                if m["mac_address"] == mac:
                    machine_id = m["id"]
                    break
        if machine_id:
            config['machine_id'] = machine_id
            save_config(config)
            print(f"[+] Registered as '{machine_name}' (ID {machine_id})")
    except Exception as e:
        print(f"[!] Could not reach server: {e}")


# ── HEARTBEAT ────────────────────────────────────────────────────────────────
def send_heartbeats():
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        if not machine_id:
            continue
        try:
            requests.post(f"{SERVER_URL}/machines/{machine_id}/heartbeat/")
        except:
            pass


# ── WINDOW TRACKING ──────────────────────────────────────────────────────────
user32 = ctypes.windll.user32
psapi = ctypes.windll.psapi
kernel32 = ctypes.windll.kernel32


def get_active_window():
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    title_buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, title_buf, length + 1)
    title = title_buf.value
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    handle = kernel32.OpenProcess(0x0410, False, pid)
    buf = ctypes.create_unicode_buffer(260)
    psapi.GetModuleFileNameExW(handle, None, buf, 260)
    kernel32.CloseHandle(handle)
    exe = os.path.basename(buf.value) if buf.value else "unknown"
    return exe, title


def send_app_log(app_name, window_title, started_at, ended_at, duration):
    try:
        requests.post(f"{SERVER_URL}/logs/app/", json={
            "machine": machine_id,
            "app_name": app_name,
            "window_title": window_title,
            "started_at": started_at,
            "ended_at": ended_at,
            "duration_seconds": duration
        })
    except Exception as e:
        print(f"[!] Failed to send app log: {e}")


def track_windows():
    print("[*] Window tracking started")
    current_app, current_title = get_active_window()
    session_start = datetime.now(timezone.utc)
    while True:
        time.sleep(POLL_INTERVAL)
        app, title = get_active_window()
        if app != current_app or title != current_title:
            ended_at = datetime.now(timezone.utc)
            duration = int((ended_at - session_start).total_seconds())
            if machine_id and duration > 1:
                send_app_log(current_app, current_title,
                             session_start.isoformat(),
                             ended_at.isoformat(), duration)
                print(f"  [app] {current_app} | {duration}s")
            current_app, current_title = app, title
            session_start = datetime.now(timezone.utc)


# ── BROWSER HISTORY ──────────────────────────────────────────────────────────
BROWSER_PATHS = {
    "Chrome": os.path.expandvars(
        r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History"),
    "Edge": os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History"),
}
seen_urls = set()


def read_browser_history(browser, db_path):
    if not os.path.exists(db_path):
        return []
    tmp = db_path + ".tmp"
    shutil.copy2(db_path, tmp)
    results = []
    try:
        conn = sqlite3.connect(tmp)
        cur = conn.cursor()
        cur.execute("""
            SELECT url, title, visit_count,
                   datetime((last_visit_time/1000000)-11644473600, 'unixepoch') as visited
            FROM urls ORDER BY last_visit_time DESC LIMIT 100
        """)
        for row in cur.fetchall():
            url, title, count, visited = row
            key = f"{browser}:{url}"
            if key not in seen_urls:
                seen_urls.add(key)
                results.append({
                    "machine": machine_id,
                    "browser": browser,
                    "url": url,
                    "page_title": title or "",
                    "visited_at": visited or datetime.now(timezone.utc).isoformat(),
                    "visit_count": count
                })
        conn.close()
    except Exception as e:
        print(f"[!] Browser read error ({browser}): {e}")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return results


def sync_browser_history():
    while True:
        time.sleep(BROWSER_SYNC_INTERVAL)
        if not machine_id:
            continue
        for browser, path in BROWSER_PATHS.items():
            entries = read_browser_history(browser, path)
            for entry in entries:
                try:
                    requests.post(f"{SERVER_URL}/logs/browser/", json=entry)
                except:
                    pass
            if entries:
                print(f"  [browser] Synced {len(entries)} {browser} URLs")


# ── PRINT TRACKING ───────────────────────────────────────────────────────────
seen_print_events = set()


def get_print_jobs():
    results = []
    try:
        ps_cmd = """
        Get-WinEvent -LogName 'Microsoft-Windows-PrintService/Operational' -MaxEvents 50 |
        Where-Object { $_.Id -eq 307 } |
        ForEach-Object {
            [PSCustomObject]@{
                TimeCreated = $_.TimeCreated.ToString('o')
                Document    = $_.Properties[1].Value
                Printer     = $_.Properties[4].Value
                Pages       = $_.Properties[7].Value
            }
        } | ConvertTo-Json
        """
        output = subprocess.check_output(
            ["powershell", "-Command", ps_cmd],
            stderr=subprocess.DEVNULL, timeout=10
        )
        jobs = json.loads(output.decode("utf-8", errors="ignore"))
        if isinstance(jobs, dict):
            jobs = [jobs]
        for job in jobs:
            key = f"{job['TimeCreated']}:{job['Document']}"
            if key not in seen_print_events:
                seen_print_events.add(key)
                results.append({
                    "machine": machine_id,
                    "printer_name": job.get("Printer", "Unknown"),
                    "document_name": job.get("Document", "Unknown"),
                    "pages": int(job.get("Pages", 0)),
                    "printed_at": job.get("TimeCreated")
                })
    except Exception as e:
        print(f"[!] Print log error: {e}")
    return results


def enable_print_log():
    try:
        subprocess.run([
            "powershell", "-Command",
            "wevtutil sl Microsoft-Windows-PrintService/Operational /e:true"
        ], check=True, stderr=subprocess.DEVNULL)
        print("[+] Print event log enabled")
    except Exception as e:
        print(f"[!] Could not enable print log (run as Admin): {e}")


def sync_print_logs():
    enable_print_log()
    while True:
        time.sleep(PRINT_SYNC_INTERVAL)
        if not machine_id:
            continue
        jobs = get_print_jobs()
        for job in jobs:
            try:
                requests.post(f"{SERVER_URL}/logs/print/", json=job)
                print(f"  [print] {job['document_name']} | {job['pages']} pages")
            except:
                pass


# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import threading

    print("=== CyberNest Agent ===")
    machine_name = get_machine_name()
    register_machine(machine_name)

    threads = [
        threading.Thread(target=send_heartbeats, daemon=True),
        threading.Thread(target=track_windows, daemon=True),
        threading.Thread(target=sync_browser_history, daemon=True),
        threading.Thread(target=sync_print_logs, daemon=True),
    ]
    for t in threads:
        t.start()

    print("[*] All trackers running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Agent stopped.")