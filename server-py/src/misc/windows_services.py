import os

from lib.py.core.traces import println


class WindowsServices:
    def shutdown(self, delay="3600", cancel=False):
        if cancel:
            os.system("shutdown -a")
        else:
            cmd = "shutdown -s -t " + delay
            println(cmd)
            os.system(cmd)

    class registry:
        def bluelight(self):
            """
            Ref: https://superuser.com/questions/1200222/configure-windows-creators-update-night-light-via-registry
            :return:
            """
            key = "Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\Cache\\DefaultAccount\\$$windows.data.bluelightreduction.settings\\Current"
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key,
                                access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as reg_key:
                value, regtype = winreg.QueryValueEx(reg_key, "Data")
                if regtype == winreg.REG_BINARY:
                    print(value)

    def proxy(self, port=None):
        # Ref: https://stackoverflow.com/a/36646749/973425

        path = "c:\windows\system32\drivers\etc\hosts"
        print(path)

        if port:
            print("Add an ip and name to hosts file")
            print("Example:\n127.65.44.45   mysite")
            ip = input("What ip did you use? (example - 127.65.44.45): ")

            # Need to use 443 instead of 80 in case of https
            cmd = "netsh interface portproxy add v4tov4 " \
                  "listenport={{target_port}} listenaddress={ip} " \
                  "connectport={port} connectaddress=127.0.0.1".format_map({
                "ip": ip,
                "port": port
            })

            cmd_80 = cmd.format_map({
                "target_port": "80"
            })
            cmd_443 = cmd.format_map({
                "target_port": "443"
            })

            print("Launching: " + cmd_80)
            os.system(cmd_80)

            print("Launching: " + cmd_443)
            os.system(cmd_443)
