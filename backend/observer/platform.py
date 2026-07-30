"""Best-effort active-window adapters. They return metadata only and never read input fields."""
import platform, subprocess, shutil

def active_window():
    system=platform.system()
    try:
        if system=='Windows':
            import ctypes
            from ctypes import wintypes
            user32=ctypes.windll.user32; hwnd=user32.GetForegroundWindow()
            length=user32.GetWindowTextLengthW(hwnd); buf=ctypes.create_unicode_buffer(length+1); user32.GetWindowTextW(hwnd,buf,length+1)
            pid=wintypes.DWORD(); user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
            try:
                import psutil; app=psutil.Process(pid.value).name()
            except Exception: app='Windows application'
            return app,buf.value
        if system=='Darwin':
            script='tell application "System Events" to tell (first process whose frontmost is true) to return {name, name of front window}'
            out=subprocess.check_output(['osascript','-e',script],text=True,timeout=2).strip()
            parts=[x.strip() for x in out.split(',')]; return (parts+["",""])[:2]
        if shutil.which('xdotool'):
            wid=subprocess.check_output(['xdotool','getactivewindow'],text=True,timeout=2).strip()
            title=subprocess.check_output(['xdotool','getwindowname',wid],text=True,timeout=2).strip()
            pid=subprocess.check_output(['xdotool','getwindowpid',wid],text=True,timeout=2).strip()
            try:
                import psutil; app=psutil.Process(int(pid)).name()
            except Exception: app='Linux application'
            return app,title
    except Exception: pass
    return '',''
