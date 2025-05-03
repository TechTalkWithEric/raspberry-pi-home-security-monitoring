import sys
import os
import site
import platform
from pathlib import Path


def print_env_info():
    print("🔎 Python Environment Info")
    print("=" * 30)

    print(f"📦 Python Version     : {platform.python_version()}")
    print(f"🐍 Python Executable  : {sys.executable}")
    print(f"📂 sys.prefix         : {sys.prefix}")
    print(f"📂 Base Prefix        : {getattr(sys, 'base_prefix', sys.prefix)}")
    print(
        f"🧠 site-packages path : {site.getsitepackages()[0] if hasattr(site, 'getsitepackages') else 'N/A'}"
    )

    in_venv = is_virtual_environment()
    print(f"✅ In Virtual Env     : {'Yes' if in_venv else 'No'}")

    if in_venv:
        venv_name = Path(sys.prefix).name
        print(f"📁 Virtual Env Name   : {venv_name}")


def is_virtual_environment():
    # Works in Python 3.3+
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


if __name__ == "__main__":
    print_env_info()
