"""
Various helper functions
Created: 25/07/2021
"""

import sys
import platform
import string
import getpass


def get_platform():
    """
    Gets the operating system currently running
    :returns: name of operating system
    """
    if platform.system() == 'Darwin':
        return 'Mac OS'
    return sys.platform


def get_user():
    """
    Gets the current user using environment variables
    :returns: current username
    """
    return getpass.getuser()


def create_key_list():
    """
    Creates a list of keys that are used on an European keyboard
    """
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase)
    shift_number_chars = ['!', '"', '§', '$', '&', '/', '(', ')', '=']
    other_chars = ['+', '*', '~', '#', '\'', '-', '–',
                   ',', ';', '.', ':', '^', '°', '<', '>', '|']
    key_array = lowercase + uppercase + shift_number_chars + other_chars
    return key_array


def list_fcts_file():
    """
    Returns a list of all top level functions in current file (to be used within target file)
    :returns: list of functions
    """
    lst = []
    for key, value in locals().items():
        if callable(value) and value.__module__ == __name__:
            lst.append(key)
    return lst


def get_active_window():
    """
    Get the currently active window.

    Returns
    -------
    string :
        Name of the currently active window.
    """
    active_window_name = None
    if sys.platform in ['linux', 'linux2']:
        # Alternatives: https://unix.stackexchange.com/q/38867/4784
        try:
            import wnck
        except ImportError:
            wnck = None
            raise ImportError("wnck not installed")
        if wnck is not None:
            screen = wnck.screen_get_default()
            screen.force_update()
            window = screen.get_active_window()
            if window is not None:
                pid = window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    active_window_name = f.read()
        else:
            try:
                from gi.repository import Gtk, Wnck
                gi = "Installed"
            except ImportError:
                gi = None
                raise ImportError("gi.repository not installed")
            if gi is not None:
                Gtk.init([])  # necessary if not using a Gtk.main() loop
                screen = Wnck.Screen.get_default()
                screen.force_update()  # recommended per Wnck documentation
                active_window = screen.get_active_window()
                pid = active_window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    active_window_name = f.read()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        # https://stackoverflow.com/a/608814/562769
        import win32gui
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        # https://stackoverflow.com/a/373310/562769
        from AppKit import NSWorkspace
        active_window_name = (NSWorkspace.sharedWorkspace()
                              .activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is unknown. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    return active_window_name


def get_active_window_repeatedly():
    window = get_active_window()
    print(window)
    while True:
        new_window = get_active_window()
        if new_window != window and new_window != "":
            print(new_window)
            window = new_window
