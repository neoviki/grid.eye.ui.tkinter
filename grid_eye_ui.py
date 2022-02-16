from tkinter import *
import random

def draw(width, height):
    global ws
    dimension=str(width)+'x'+str(height)
    ws = Tk()
    ws.title('Sensor Fusion')
    ws.geometry(dimension)
    ws.config(bg='white')

def loop():
    global ws
    ws.mainloop()

def grid_eye_draw(cx, cy, pixel):
    grid_width=30
    grid_height=30
    n_grid_rows=8
    n_grid_cols=8

    canvas_height=n_grid_rows*grid_height+15
    canvas_width = n_grid_cols*grid_width+15
    c1 = Canvas(ws,height=canvas_height,width=canvas_width,bg='black')
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

def main():
    global pixel
    draw(280,280)
    init_pixels()
    grid_eye_draw(10,10, pixel)
    loop()

main()