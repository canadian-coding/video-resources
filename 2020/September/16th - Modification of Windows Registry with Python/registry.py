import winreg # Allows access to the windows registry
import ctypes # Allows interface with low-level C API's


program_path = f"%USERPROFILE%\\Documents"


with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey: # Get the necessary HKEY
    with winreg.OpenKey(hkey, "Environment", 0, winreg.KEY_ALL_ACCESS) as sub_key: # Go to the environment key
        existing_path_value = winreg.EnumValue(sub_key, 3)[1] # Grab the current path value
        print(f"{existing_path_value=}")
        new_path_value = existing_path_value + program_path + ";" # Takes the current path value and appends the new program path
        print(f"{new_path_value=}")
        winreg.SetValueEx(sub_key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value) # Updated the path with the updated path

        # Tell other processes to update their environment
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_long()
        SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u"Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result),) 
