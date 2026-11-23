import os
import psutil
from app.utils.logger import log_error


import time

_sys_cache = {}
CACHE_TTL = 10  # 10 seconds

def get_system_info(command: str = "") -> str:
    """Get system information based on the command."""
    command = command.lower()
    
    now = time.time()
    if command in _sys_cache:
        cached_data, cached_time = _sys_cache[command]
        if now - cached_time < CACHE_TTL:
            return cached_data

    try:
        result = ""
        if "battery" in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "on battery"
                result = f"Battery is at {percent}%, {plugged}."
            else:
                result = "Battery info unavailable."

        elif "cpu" in command:
            cpu = psutil.cpu_percent(interval=0.1)
            result = f"CPU usage is at {cpu}%."

        elif "ram" in command or "memory usage" in command:
            mem = psutil.virtual_memory()
            used_gb = round(mem.used / (1024 ** 3), 1)
            total_gb = round(mem.total / (1024 ** 3), 1)
            result = f"RAM usage: {used_gb}GB / {total_gb}GB ({mem.percent}%)."

        elif "disk" in command:
            disk_path = "C:\\" if os.name == 'nt' else "/"
            disk = psutil.disk_usage(disk_path)
            free_gb = round(disk.free / (1024 ** 3), 1)
            total_gb = round(disk.total / (1024 ** 3), 1)
            result = f"Disk: {free_gb}GB free of {total_gb}GB total ({disk.percent}% used)."

        elif "wifi" in command:
            if os.name == 'nt':
                import subprocess
                res = subprocess.run(
                    ["netsh", "wlan", "show", "interfaces"],
                    capture_output=True, text=True
                )
                if "connected" in res.stdout.lower():
                    for line in res.stdout.split("\n"):
                        if "SSID" in line and "BSSID" not in line:
                            ssid = line.split(":")[1].strip()
                            result = f"Connected to WiFi: {ssid}"
                            break
                    if not result:
                        result = "WiFi is connected."
                else:
                    result = "WiFi is not connected."
            else:
                result = "Network interface monitoring is active."

        else:
            # Default: give everything
            battery = psutil.sensors_battery()
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            bat_str = f"{battery.percent}%" if battery else "N/A"

            result = (
                f"System status — CPU: {cpu}%, "
                f"RAM: {mem.percent}%, "
                f"Battery: {bat_str}."
            )

        _sys_cache[command] = (result, now)
        return result

    except Exception as e:
        log_error("get_system_info", e)
        return f"Couldn't retrieve system info: {str(e)}"


def control_system(command: str) -> str:
    """Handle system control commands like shutdown, restart, lock."""
    command = command.lower()

    try:
        if "lock" in command:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "Locking the screen now."

        if "shutdown" in command:
            return (
                "Shutdown command received. For safety, please run "
                "'shutdown /s /t 60' manually, or confirm and I'll execute it."
            )

        if "restart" in command:
            return (
                "Restart command received. For safety, please run "
                "'shutdown /r /t 60' manually, or confirm and I'll execute it."
            )

        if "sleep" in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Putting the system to sleep."

        return "System command not recognized."

    except Exception as e:
        log_error("control_system", e)
        return f"System control error: {str(e)}"
