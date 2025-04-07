

import platform


def is_linux():
    """Return True if running on Linux."""
    return platform.system() == "Linux"

def is_macos():
    """Return True if running on macOS."""
    return platform.system() == "Darwin"

def is_windows():
    """Return True if running on Windows."""
    return platform.system() == "Windows"

def is_raspberry_pi():
    """Return True if running on a Raspberry Pi."""
    if not is_linux():
        return False

    try:
        # Check the device model from /proc/cpuinfo
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read().lower()
            if "raspberry pi" in cpuinfo:
                return True
    except Exception:
        pass

    try:
        # Check DMI product name (some newer models)
        with open("/sys/firmware/devicetree/base/model", "r") as f:
            model = f.read().lower()
            if "raspberry pi" in model:
                return True
    except Exception:
        pass

    return False
