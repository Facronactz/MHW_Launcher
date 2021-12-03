import os
from pathlib import Path
import shutil
import time
import PySimpleGUI as sg
import base64 as secret
import psutil
import subprocess

sg.theme('Dark Grey 5')

layout = [[sg.Text('MHW(I) Executable File'), sg.Input(readonly=True, expand_x=True, expand_y=True), sg.FileBrowse(file_types=(("Monster Hunter World", "MonsterHunterWorld.exe"),))],
         [sg.OK(), sg.Cancel()] ]

def cancel(i):
    if (i == 1):
        sg.PopupAnnoying("Operation Canceled", auto_close=True, auto_close_duration=2)
    elif (i == 2):
        return sg.popup_yes_no("Username or Password is incorrect, do you want to sign up?")
    elif (i == 0):
        sg.PopupAnnoying("Operation Completed and Succeeded", auto_close=True, auto_close_duration=2)
    else:
        sg.PopupAnnoying("Something went wrong most likely the data is incorrect or not have been filled", auto_close=True, auto_close_duration=2)

def meter(i, str):
    sg.one_line_progress_meter('Processing', i, 3, str, orientation='h', key='meter')

def isRunning(str):
    return (str in (p.name() for p in psutil.process_iter()))

def changeSaveArchive():
    appdata = os.getenv('APPDATA')
    appdata = os.path.join(appdata, "MHW.txt")

    with open(appdata, "r") as file:
        data = file.readlines()

    with open(appdata, "w+") as file:
        if data[1] == 'r\n':
            data[1] = 's\n'
        else:
            data[1] = 'r\n'
        file.writelines(data)

def MHW(file, i):
    while True:
        meter(1, 'Archiving your save data')

        save_path = Path("C:\\Users\\Public\\Documents\\OnlineFix\\582010")
        save_path2 = save_path.with_name('582010_2')

        if(i=='r\n'):
            shutil.make_archive(save_path,"zip",save_path)
            changeSaveArchive()
        elif(i=='s\n'):
            shutil.make_archive(save_path2,"zip",save_path)
            changeSaveArchive()
        else:
            changeSaveArchive()
        # if(rar_path.is_file and not rar_path2.is_file):
        #     shutil.make_archive(save_path2,"zip",save_path)
        # elif(rar_path2.is_file):
        #     shutil.make_archive(save_path,"zip",save_path)
        # else:
        #     shutil.make_archive(save_path,"zip",save_path)
            
        meter(2, 'Archiving executable')
        file = Path(file)
        shutil.make_archive(file.with_name("MonsterHunterWorld"),"zip",file.parent,"MonsterHunterWorld.exe")

        meter(3, 'Done')
        if not (isRunning("MonsterHunterWorld.exe")):
            break
        time.sleep(1200)

def windows(appdata):
    mainWindows = sg.Window('Monster Hunter World (Iceborne) Launcher', layout, element_justification="center")
    event, values = mainWindows.read()
    mainWindows.close()

    if event == "OK":
        if (values[0] != ""):

            data = [""]*3
            with open(appdata, "w+") as file:
                # f = open(appdata, "w")
                value = values[0].encode('ASCII')
                value = secret.b85encode(value)
                data[0] = "Please dont modify this file!!! We are not responsible for any data damage!!!!\n"
                data[1] = 'r\n'
                data[2] = value.decode('ASCII')
                file.writelines(data)
                # file.write(value.decode('ASCII'))
                # f.close()

            if(sg.popup_yes_no("Do you want to start Monster Hunter World (Iceborne)?") == 'Yes'):
                os.startfile(values[0])
                MHW(values[0], data[1])
            else:
                cancel(0)
        else:
            cancel(3)
    else:
        cancel(1)

def main():
    appdata = os.getenv('APPDATA')
    appdata = os.path.join(appdata, "MHW.txt")
    try:
        with open(appdata, "r") as file:
            data = file.readlines()
        loc = Path(secret.b85decode(data[2]).decode('ASCII'))
        
        # f = open(appdata, "r")
        # a = f.read()
        # f.close()
        # loc = Path(secret.b85decode(a).decode('ASCII'))
        # print(loc)
        os.startfile(loc)
        MHW(loc, data[1])
    except:
        if (Path(appdata).is_file()):
            if(sg.popup_yes_no("There is something wrong with the launcher save data, either the data corupt or you move the MHW(I) installation folder or you simply cancel the operation. Do you want to update launcher data?") == 'Yes'):
                windows(appdata)
            else:
                cancel(1)
        else:
            windows(appdata)


if __name__ == '__main__':
    main()