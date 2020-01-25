# import os
# from win10toast import ToastNotifier
#
# from lib.py.core.singleton import Singleton
#
# icons_directory = os.path.dirname(os.path.dirname(__file__))
# icons_directory = os.path.join(icons_directory, "app\\static\\images")
# fav_icon = os.path.join(icons_directory, "favicon.ico")
#
#
# class Notification(ToastNotifier):
#     __metaclass__ = Singleton
#
#     def show(self, title="VilokanLabs", message="Server has been started", duration=5, icon=fav_icon):
#         self.show_toast(title,
#                         message,
#                         icon_path=icon,
#                         duration=duration)
#
#     def on_destroy(self, hwnd, msg, wparam, lparam):
#         pass
