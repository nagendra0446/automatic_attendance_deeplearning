from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as fd
import time
import shutil
import sys
import os

def get_filename(path_name):
    arr = path_name.split('/')
    return arr[len(arr)-1]

ws = Tk()
ws.title('Automatic Attendance System A2S')
ws.geometry('500x350') 

files = []

ws.rowconfigure(0, weight=1)
ws.columnconfigure(0, weight=1)
ws.rowconfigure(2, weight=1)
ws.columnconfigure(2, weight=1)

heading = Label(
    ws, 
    text='Welcome to A2S',
    justify='center',
    font=('Avenir Book', 27, 'bold'),

)
heading.grid(row=0, columnspan=3)


adhar = Label(
    ws, 
    text='Upload images for training',
    justify='center'
)
adhar.grid(row=3, column=0, padx=5)

menu = StringVar(ws)
menu.set("Student")

drop= OptionMenu(ws, menu, "Student", "Student", "Faculty")

drop.grid(row=3, column=1, pady=5)

def call_main():
    import a2s_core
    a2s_core.main()

def open_file():
    global files
    files = list(fd.askopenfilenames(parent=ws, title='Choose file(s)'))
    Label(ws, text=str([get_filename(f) for f in files]), foreground='green').grid(row=2, columnspan=3, pady=10)
    #print(file_path)

def saveFiles():
    pb1 = Progressbar(
        ws, 
        orient=HORIZONTAL, 
        length=300, 
        mode='determinate'
        )
    pb1.grid(row=4, columnspan=3, pady=5)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()


    Label(ws, text='Images saved Successfully!', foreground='green').grid(row=6, columnspan=3, pady=10)
    #print(file_path.name)

    option = menu.get()
    img_loc = 'faculty_training_imgs' if option=='Faculty' else 'student_training_imgs'
    for f in files:
        src_path = f
        dst_path = './'+img_loc+'/' + get_filename(f)
        shutil.copy(src_path, dst_path)
        
        
adhar = Label(
    ws, 
    text='Upload images for training',
    justify='center'
    )
adhar.grid(row=1, column=0, padx=10)

adharbtn = Button(
    ws, 
    text ='Choose Image(s)', 
    command = open_file
    ) 
adharbtn.grid(row=1, column=1)


upld = Button(
    ws, 
    text='Upload Image(s)', 
    command=saveFiles
    )
upld.grid(row=5, columnspan=3, pady=10)

run = Button(
    ws, 
    text='Run A2S', 
    command=call_main
    )
run.grid(row=7, columnspan=3, pady=10)


def run():
    os.system('code attendance_report.csv')

run = Button(
    ws, 
    text='View Report', 
    command=run
    )
run.grid(row=8, columnspan=3, pady=10)


empty = Label(
    ws, 
    text='',
    justify='center'
    )
empty.grid(row=9, column=0, padx=10)

ws.mainloop()