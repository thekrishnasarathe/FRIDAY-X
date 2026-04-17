import os
import psutil
from app.utils.logger import log_error


def get_system_info(command: str = "") -> str:
    """Get system information based on the command."""
    command = command.lower()

    try:
        if "battery" in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "on battery"
                return f"Battery is at {percent}%, {plugged}."
            return "Battery info unavailable."

        if "cpu" in command:
            cpu = psutil.cpu_percent(interval=1)
            return f"CPU usage is at {cpu}%."

        if "ram" in command or "memory usage" in command:
            mem = psutil.virtual_memory()
            used_gb = round(mem.used / (1024 ** 3), 1)
            total_gb = round(mem.total / (1024 ** 3), 1)
            return f"RAM usage: {used_gb}GB / {total_gb}GB ({mem.percent}%)."

        if "disk" in command:
            disk = psutil.disk_usage("C:\\")
            free_gb = round(disk.free / (1024 ** 3), 1)
            total_gb = round(disk.total / (1024 ** 3), 1)
            return f"Disk C: {free_gb}GB free of {total_gb}GB total ({disk.percent}% used)."

        if "wifi" in command:
            import subprocess
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True, text=True
            )
            if "connected" in result.stdout.lower():
                # Find SSID
                for line in result.stdout.split("\n"):
                    if "SSID" in line and "BSSID" not in line:
                        ssid = line.split(":")[1].strip()
                        return f"Connected to WiFi: {ssid}"
                return "WiFi is connected."
            return "WiFi is not connected."

        # Default: give everything
        battery = psutil.sensors_battery()
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        bat_str = f"{battery.percent}%" if battery else "N/A"

        return (
            f"System status — CPU: {cpu}%, "
            f"RAM: {mem.percent}%, "
            f"Battery: {bat_str}."
        )

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
