'''
    Grid Eye UI

    Author: Viki (a) Vignesh Natarajan

    #Python2.7
'''


from tkinter import *
import Tkinter as tk
import random
import time
#pip install pyserial
import serial
from threading import Thread
import serial.tools.list_ports
import tkMessageBox


#Constants
d_list_default="  < Select Serial Port >  "
drop_down_width=35
button_width=20

serial_port_list=[d_list_default]
serial_port_selected=d_list_default
serial_connected=False

ge_x=250
ge_y=100

def update_button_states():
    global btn_connect_handle, btn_disconnect_handle
    global d_list, serial_connected, serial_port_selected

    if serial_connected != True:
        btn_connect_handle["state"] = "normal"
        d_list["state"]="normal"
        btn_disconnect_handle["state"] = "disabled"
        serial_port_selected=d_list_default
    else:
        btn_connect_handle["state"] = "disabled"
        d_list["state"]="disabled"
        btn_disconnect_handle["state"] = "normal"

def btn_disconnect_callback():
    global btn_disconnect_handle, btn_connect_handle, d_list, serial_connected
    close_serial_port()
    update_button_states()


def btn_connect_callback():
    global serial_port_selected
    if serial_port_selected == d_list_default:
        tkMessageBox.showinfo( "Alert!", "Select a valid serial port")
    else:
        open_serial_port()
        update_button_states()

def btn_connect_create(px, py):
    global root, btn_connect_handle, button_width

    btn_connect_handle = Button(root, text ="Connect", width=button_width,
                            command=btn_connect_callback)
    btn_connect_handle.pack()
    btn_connect_handle.place(x=px, y=py)

def btn_disconnect_create(px, py):
    global root, btn_disconnect_handle, button_width
    btn_disconnect_handle = Button(root, text ="Disconnect", width=button_width,
                                   command=btn_disconnect_callback)
    btn_disconnect_handle.pack()
    btn_disconnect_handle.place(x=px, y=py)

def drop_down_callback(selected_value):
    global serial_port_selected
    serial_port_selected=selected_value
    #tkMessageBox.showinfo( "Alert!", serial_port_selected)
    #ui_object_group_port_selector_update(10, 20)
    print serial_port_selected

def ui_object_group_port_selector_create(px, py):
    global drop_down_width, button_width, serial_port_list
    global root, d_list

    #drop down list
    variable = StringVar(root)
    variable.set(serial_port_selected) # default value
    d_list = OptionMenu(root, variable, *serial_port_list, command=drop_down_callback)
    d_list.config(width=drop_down_width)
    d_list.config(anchor='w')
    d_list.place(x=px,y=py)

    #Connect Button
    px=px+drop_down_width+button_width
    btn_connect_create(px+240,py)

    #Disconnect Button
    btn_disconnect_create(px+430,py)

    btn_connect_handle["state"] = "normal"
    d_list["state"]="normal"
    btn_disconnect_handle["state"] = "disabled"

'''
def ui_object_group_port_selector_update(px, py):
    global drop_down_width, button_width, serial_port_list
    global root, d_list

    #drop down list
    variable = StringVar(root)
    d_list['menu'].delete(0, 'end')
    print "selected port:"
    print serial_port_selected
    variable.set(serial_port_selected) # default value
    for element in serial_port_list:
        d_list['menu'].add_command(label=element, command=tk._setit(variable, element, drop_down_callback))
    print "selected port:"
    print serial_port_selected
    update_button_states()
'''

def draw(width, height):
    global root
    dimension=str(width)+'x'+str(height)
    root = Tk()
    root.title('Sensor Fusion')
    root.geometry(dimension)
    root.config(bg='white')

def loop():
    global root
    root.mainloop()

def grid_eye_draw(cx, cy, lpixel):
    global root
    grid_width=30
    grid_height=30
    n_grid_rows=8
    n_grid_cols=8

    canvas_height=n_grid_rows*grid_height+15
    canvas_width = n_grid_cols*grid_width+15
    c1 = Canvas(root,height=canvas_height,width=canvas_width,bg='black')
    c1.pack()
    c1.place(x=cx,y=cy)

    x=0
    y=0
    for r in range(0,8):
        y=r*grid_height+10
        for c in range(0,8):
            x=c*grid_width+10
            value=lpixel[(r+1)*c]

            if(value <= 50):
                c1.create_rectangle(x,y,x+grid_width,y+grid_height, outline='grey', fill='#3440eb')
            if(value > 50):
                c1.create_rectangle(x,y,x+grid_width,y+grid_height, outline='grey', fill='#34eb6e')
            if(value > 100):
                c1.create_rectangle(x,y,x+grid_width,y+grid_height, outline='grey', fill='#ebeb34')
            if(value > 150):
                c1.create_rectangle(x,y,x+grid_width,y+grid_height, outline='grey', fill='#eb9334')
            if(value > 200):
                c1.create_rectangle(x,y,x+grid_width,y+grid_height, outline='grey', fill='#eb4934')

            c1.create_text(x+15, y+15, fill='black', text=str(value))


def init_pixels():
    global pixel
    pixel = [0]*64
    for i in range(0,64):
        #pixel[i] = random.randrange(0,255)
        pixel[i] = 0

def open_serial_port():
    global serial_handle, serial_connected, d_list_default

    if serial_port_selected == d_list_default:
        return

    try:
        serial_handle = serial.Serial(serial_port_selected, 9600)
        serial_connected=True
    except:
        serial_connected=False

    if serial_connected == True:
        serial_handle.flushInput()

def close_serial_port():
    global serial_handle, serial_connected
    if serial_connected == True:
        serial_handle.close()
        serial_connected = False


def read_serial():
    global serial_handle, serial_connected

    if serial_connected == True:
        serial_data = serial_handle.readline()
        #print serial_data
        return serial_data
    else:
        return None

def parse_serial_data(serial_data):
    global pixel, pixel_ready
    s = str(serial_data)
    e1 = s.split("#")
    if(len(e1) >= 2):
        e2 = e1[1]

        #grid eye pixel values are here
        e3 = e2.split(",")
        #print(e3)

        if pixel_ready == True:
            return 0

        for i in range(0, 64):
            pixel[i] = int(e3[i])
            print pixel
            pixel_ready=True

    return 1

def scan_serial_ports():
    global serial_port_list
    s_list = serial.tools.list_ports.comports()
    serial_port_list=[d_list_default]
    for element in s_list:
        serial_port_list.append(str(element.device))

    print serial_port_list

def serial_handler_thread():
    global quit_called, root, pixel, serial_port_list, serial_port_selected, serial_connected

    while True:
        time.sleep(0.2)
        scan_serial_ports()
        if len(serial_port_list) > 1:
            break

    #ui_object_group_port_selector_update(10, 20)

    while True:
        print "serial_handler_thread"
        if quit_called == True:
            break

        if serial_connected == True:
            time.sleep(0.1)
            serial_data = read_serial()
            if serial_data != None:
                parse_serial_data(serial_data)
                ui_update()
        else:
            time.sleep(3)



def serial_main_thread_begin():
    global smon_thread
    try:
        smon_thread=Thread(target=serial_handler_thread,args=())
        smon_thread.start()
    except:
        print "error: creating thread"

def serial_main_thread_end():
    global serial_handle, smon_thread, serial_connected

    if serial_connected == True:
        close_serial_port()

    print "EXIT: Serial Monitor"
    smon_thread.join()
    print "Exit: Serial Monitor Thread"

def ui_update():
    global pixel, root, pixel_ready, serial_port_list

    # Port List Update
    #ui_object_group_port_selector_update(10, 20)

    #Grid Eye Update
    if serial_connected == True:
        if pixel_ready == True:
            grid_eye_draw(ge_x, ge_y, pixel)
            pixel_ready=False

    #fill other sensors update routine here
    root.update()

def ui_main_thread_begin():
    global pixel, serial_port_list, serial_connected
    #draw(280,280)
    draw(700,500)
    init_pixels()

    ui_object_group_port_selector_create(10, 20)

    #if serial_connected == True:
    grid_eye_draw(ge_x, ge_y, pixel)


def ui_main_thread_end():
    global root, quit_called
    loop()
    root.quit()
    quit_called=True
    print "EXIT: UI THREAD"

def main():
    global quit_called, pixel_ready
    quit_called=False
    pixel_ready = False
    serial_main_thread_begin()
    time.sleep(5)
    ui_main_thread_begin()
    ui_main_thread_end()
    serial_main_thread_end()

main()
