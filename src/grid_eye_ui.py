'''
    Grid Eye UI

    Author: Viki (a) Vignesh Natarajan

    #Python2.7
'''


from tkinter import *
import random
import time
#pip install pyserial
import serial
from threading import Thread
import serial.tools.list_ports


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

def grid_eye_draw(cx, cy, pixel):
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
            value=pixel[(r+1)*c]

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
        pixel[i] = random.randrange(0,255)

    print pixel

def init_serial(serial_port):
    global serial_mon
    serial_mon = serial.Serial(serial_port)
    serial_mon.flushInput()

def read_serial():
    global serial_mon
    serial_data = serial_mon.readline()
    #print serial_data
    return serial_data

def parse_serial_data(serial_data):
    global pixel, pixel_ready
    s = str(serial_data)
    e1 = s.split("#")
    if(len(e1) >= 2):
        e2 = e1[1]

        #grid eye pixel values are here
        e3 = e2.split(",")
        #print(e3)
        for i in range(0, 64):
            pixel[i] = int(e3[i])
            print pixel
            pixel_ready=True

    return 1

def list_serial_ports():
    serial_port_list = serial.tools.list_ports.comports()
    serial_ports = []
    for element in serial_port_list:
        serial_ports.append(element.device)

    print serial_ports
    return serial_ports

def serial_monitor_thread():
    global quit_called, root, pixel
    serial_ports = list_serial_ports()
    init_serial(serial_ports[1])
    #init_serial('/dev/cu.usbmodem14201')

    while True:
        if quit_called == False:
            serial_data = read_serial()
            parse_serial_data(serial_data)
            ui_update()
            time.sleep(0.1)
        else:
            break

def serial_monitor_thread_begin():
    global smon_thread
    try:
        smon_thread=Thread(target=serial_monitor_thread,args=())
        smon_thread.start()
    except:
        print "error: creating thread"

def serial_monitor_thread_end():
    global serial_mon, smon_thread
    serial_mon.close()
    print "EXIT: Serial Monitor"
    smon_thread.join()
    print "Exit: Serial Monitor Thread"

def ui_update():
    global pixel, root, pixel_ready

    if pixel_ready == True:
        grid_eye_draw(10,10, pixel)
        pixel_ready=False

    #fill other sensors update routine here
    root.update()

def ui_thread_begin():
    global pixel
    draw(280,280)
    init_pixels()
    grid_eye_draw(10,10, pixel)
    loop()

def ui_thread_end():
    global root, quit_called
    root.quit()
    quit_called=True
    print "EXIT: UI THREAD"

def main():
    global quit_called, pixel_ready
    quit_called=False
    pixel_ready = False
    serial_monitor_thread_begin()
    ui_thread_begin()
    ui_thread_end()
    serial_monitor_thread_end()


main()