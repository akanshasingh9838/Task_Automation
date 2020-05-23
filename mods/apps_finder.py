import winreg



# take care run only in windows

def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            try:
                software['path'] = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
                if software['path'] == '':
                    software['path'] ='undefined'
            except EnvironmentError:
                software['path'] ='undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

if __name__ == "__main__":
    software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)
    for software in software_list:
        print('Name=%s, Version=%s, Publisher=%s' % (software['name'], software['version'], software['publisher']))
    print('Number of installed apps: %s' % len(software_list))