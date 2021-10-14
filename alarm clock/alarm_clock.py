# Alarm clock using Python Tkinter module by Rajkumar Selvaraj
# https://github.com/rajkumar49/Simple-Alarm-Clock-Python

#Necessary for importing file from parent folder
import os
import sys
currentdirectory_path = os.path.dirname(os.path.abspath(__file__))
parentdirectory_path = os.path.dirname(currentdirectory_path)
sys.path.insert(0, parentdirectory_path)

import fileUtil
import masterUtil

from tkinter import Tk, messagebox, ttk
import time
import random

class my_window():
    def __init__(self, win):
        # Gets the requested values of the height and widht.
        window_width = root.winfo_reqwidth()
        window_height = root.winfo_reqheight()
        
        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth()/2 - window_width/2)
        positionDown = int(root.winfo_screenheight()/2 - window_height/2)
        
        # Positions the window in the center of the page.
        root.geometry("+{}+{}".format(positionRight, positionDown))

        # Defines and places the notebook widget
        self.nb = ttk.Notebook(root)
        self.nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
        
        # Adds tab 1 of the notebook
        self.alarm_settings_page = ttk.Frame(self.nb)
        self.nb.add(self.alarm_settings_page, text='Alarm input')

        self.label_alarm_time = ttk.Label(self.alarm_settings_page, text="Enter the Alarm time:")
        self.label_alarm_time.grid(row = 0, column = 0)

        self.hour_input = ttk.Spinbox(self.alarm_settings_page, from_= 0, to = 24)
        self.hour_input.grid(row = 0, column = 1)
        self.minute_input = ttk.Spinbox(self.alarm_settings_page, from_= 0, to = 59)
        self.minute_input.grid(row = 0, column = 2)
        self.second_input = ttk.Spinbox(self.alarm_settings_page, from_= 0, to = 59)
        self.second_input.grid(row = 0, column = 3)

        self.label_alarm_message = ttk.Label(self.alarm_settings_page, text="Alarm Message:")
        self.label_alarm_message.grid(row = 1, column = 0)

        self.alarm_message = ttk.Entry(self.alarm_settings_page)
        self.alarm_message.grid(row = 1, column = 1)

        self.ringtone_dir = ttk.Button(self.alarm_settings_page, text="Select folder for ringtones", command=self.select_folder)
        self.ringtone_dir.grid(row = 1, column = 2)

        self.label_reps = ttk.Label(self.alarm_settings_page, text = "Number of repetitions for the alarm: ")
        self.label_reps.grid(row = 2, column = 0)
        self.no_reps = ttk.Spinbox(self.alarm_settings_page, from_= 0, to = 5)
        self.no_reps.grid(row = 2, column = 1)

        self.button1 = ttk.Button(self.alarm_settings_page, text="submit", command=self.submit_button)
        self.button1.grid(row = 2, column = 2, sticky = 'nsew')

        # Adds tab 2 of the notebook
        alarm_list_page = ttk.Frame(self.nb)
        self.nb.add(alarm_list_page, text='Alarm list')

    def select_folder(self):
        extension_list = ['mp3', 'wav', 'm4a', 'aac']
        if masterUtil.get_platform() == "Windows":
            extension_list.append('wma')
        self.ringtones = fileUtil.filetypes_path_dir(True, False, extension_list)

    def submit_button(self):
        hour = self.hour_input.get().zfill(2)
        minute = self.minute_input.get().zfill(2)
        second = self.second_input.get().zfill(2)

        alarm_time = hour + ":" + minute + ":" + second
        alarm_time = time.strptime(str(alarm_time), "%H:%M:%S")
        current_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = time.strptime(str(current_time), "%H:%M:%S")

        def input_check(self):
            if self.alarm_message.get() == "":
                return False
            if self.ringtones == None:
                return False
            if alarm_time < current_time:
                return False
            return True

        if (input_check(self) == False):
            messagebox.showerror(title='Alarm Message',
                                message="{}".format("The input is not correct. Aborting ..."))

        reps = self.no_reps.get()
        random_tone = random.choice(self.ringtones)

        while alarm_time != current_time:
            current_time = time.strftime("%H:%M:%S")
            time.sleep(1)

        if alarm_time == current_time:
            messagebox.showinfo(title='Alarm Message',
                                message="{}".format(self.alarm_message.get()))
            cmd = "start " + random_tone
            os.system(cmd)

            # Play alarm no_reps times

root = Tk()
mywin = my_window(root)
root.title('Alarm clock')
root.mainloop()