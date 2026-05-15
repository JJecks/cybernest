import os
import sys
import time
import webbrowser
import threading
import tkinter as tk
from tkinter import messagebox


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def open_browser():
    time.sleep(4)
    webbrowser.open('http://127.0.0.1:8000')


def main():
    base_dir = get_base_dir()
    os.chdir(base_dir)
    sys.path.insert(0, base_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        "CyberNest Server",
        "CyberNest Server is starting...\n\nThe dashboard will open in your browser automatically."
    )
    root.destroy()

    threading.Thread(target=open_browser, daemon=True).start()

    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '--noreload'])


if __name__ == '__main__':
    main()