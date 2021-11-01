import sqlite3
from tkinter import filedialog
import shutil

import masterUtil

username = masterUtil.get_user()

def get_history_path():
    """
    Gets the path of the history database in Google Chrome
    :returns: path to file
    """
    file_path = ""
    if masterUtil.get_platform() == 'Windows':
        file_path = "C:/Users/" + username + "/AppData/Local/Google/Chrome/User Data/Default"
    elif masterUtil.get_platform() == 'Mac OS':
        file_path = "/Users/" + username + "/Library/Application Support/Google/Chrome/Default"
    elif masterUtil.get_platform() == 'Linux':
        file_path = "/home/" + username + "/.config/google-chrome/Default"
    
    file_path = file_path + "/History"
    return file_path

def copy_history(file_path):
    copy = filedialog.asksaveasfilename("SQL file", ".sql")
    shutil.copyfile(file_path, copy)

def analyze(dbfile):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM mytable")

history_file = get_history_path()
db_copy = copy_history(history_file)
#analyze(db_copy)