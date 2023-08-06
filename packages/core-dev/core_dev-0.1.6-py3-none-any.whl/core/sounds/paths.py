

# core package (pip install python-core)
from core.system import get_operating_system

op_sys = get_operating_system()

if op_sys == "windows":
    sounds_remote_path = "C:/Users/{username}/sounds/{type}"
elif op_sys == "linux":
    sounds_remote_path = "/home/{username}/sounds/{type}"
elif op_sys == "darwin":
    sounds_remote_path = "/Users/{username}/sounds/{type}"

del op_sys