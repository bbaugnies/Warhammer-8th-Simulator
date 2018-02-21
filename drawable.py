
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style

width = 20
length = 20

root = Tk()
root.geometry("300x200+300+300")
root.wm_title("Buttons")

canvas_draw = Frame(root)
frame_menu = Frame(canvas_draw, relief=RAISED, borderwidth=1)
frame_menu.pack(fill=BOTH, expand=True)
canvas_draw.pack(fill=BOTH, expand=True)
        
closeButton = Button(canvas_draw, text="Close")
closeButton.pack(side=RIGHT, padx=5, pady=5)
okButton = Button(canvas_draw, text="OK")
okButton.pack(side=RIGHT)


              

def main():
  
    root.mainloop()  


if __name__ == '__main__':
    main() 
