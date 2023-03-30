# **************** Developed By: ARIJEET DE ****************
# Last Updated: 30/03/2023

import ctypes
import win32gui
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import ImageGrab


ctypes.windll.shcore.SetProcessDpiAwareness(1)
# root.tk.call('tk', 'scaling', 1.5)


class PaintApp:
    def __init__(self, master, canvas_color, brush_color, brush_size):
        self.root = master
        self.root.title('Paint App')
        self.root.geometry("860x730+530+120")
        self.root.configure(bg="#eab6fc")

        self.canvas_color = canvas_color
        self.brush_color = brush_color
        self.brush_size = brush_size

        self.my_canvas = Canvas(self.root, width=780, height=400, bg="white", cursor="circle")
        self.my_canvas.pack(pady=40)

        # All Frames Frame
        self.all_frame = Frame(self.root, bg="#f6e3fc")
        self.all_frame.pack()

        self.inner_frames_bg_color = "#ffffff"

        # Brush Size Frame
        self.brush_size_frame = LabelFrame(self.all_frame, text="Brush Size", bg=self.inner_frames_bg_color, pady=10)
        self.brush_size_frame.grid(row=0, column=0, pady=5, padx=(10, 60))

        # Elements inside Brush Size Frame
        self.brush_slider = ttk.Scale(self.brush_size_frame, orient=VERTICAL, from_=50, to=2, length=100, value=25,
                                      command=self.change_brush_size)
        self.brush_slider.pack()
        self.brush_label = Label(self.brush_size_frame, text=self.brush_slider.get())
        self.brush_label.pack()

        # Brush Type Frame
        self.brush_type_frame = LabelFrame(self.all_frame, text="Brush Type", bg=self.inner_frames_bg_color, padx=5)
        self.brush_type_frame.grid(row=0, column=1, pady=5, padx=(20, 20))

        self.brush_type = StringVar()
        self.brush_type.set("Round")

        brush_types = [('Round', 'Round'),
                       ('Slash', 'Slash'),
                       ('Diamond', 'Diamond')]

        # Elements Inside Brush Type Frame
        for text, value in brush_types:
            Radiobutton(self.brush_type_frame, text=text, variable=self.brush_type, value=value, bg="#ffffff").pack(anchor=W)

        # Change Colors Frame
        self.change_color_frame = LabelFrame(self.all_frame, text="Change Colors", bg=self.inner_frames_bg_color, padx=10, pady=7)
        self.change_color_frame.grid(row=0, column=2, pady=5, padx=(10, 20))

        # Brush Color Button and its Color Label
        self.brush_color_button = Button(self.change_color_frame, text="Brush Color", command=self.change_brush_color)
        self.brush_color_button.grid(row=0, column=0, pady=(0, 10), sticky=E)
        self.brush_color_label = Label(self.change_color_frame, text="", bg=brush_color, borderwidth=2, padx=12, relief=RAISED)
        self.brush_color_label.grid(row=0, column=1, padx=(8, 0), pady=(0, 10))

        # Canvas Color Button and its Color Label
        self.canvas_color_button = Button(self.change_color_frame, text="Canvas Color", command=self.change_canvas_color)
        self.canvas_color_button.grid(row=1, column=0, sticky=E)
        self.canvas_color_label = Label(self.change_color_frame, text="", bg=canvas_color, borderwidth=2, padx=12, relief=RAISED)
        self.canvas_color_label.grid(row=1, column=1, padx=(8, 0))

        # Program Options Frame
        self.program_options_frame = LabelFrame(self.all_frame, text="Program Options", bg=self.inner_frames_bg_color, padx=10, pady=7)
        self.program_options_frame.grid(row=0, column=3, pady=5, padx=10)

        # Elements inside Program Options Frame
        self.clear_screen_button = Button(self.program_options_frame, text="Clear Screen", command=self.clear_canvas)
        self.clear_screen_button.pack(pady=(0, 10))
        self.save_png_button = Button(self.program_options_frame, text="SAVE Image", command=self.save_image)
        self.save_png_button.pack()

        # Binding the Mouse Button to draw
        self.my_canvas.bind("<B1-Motion>", self.paint)
        self.my_canvas.bind("<Button-1>", self.paint)

    # Function which does the painting
    def paint(self, event):
        color = self.brush_color
        size = self.brush_size // 2

        if self.brush_type.get() == "Round":
            x1, y1 = event.x - size, event.y - size
            x2, y2 = event.x + size, event.y + size
            self.my_canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        elif self.brush_type.get() == "Slash":
            x1, y1 = event.x - size, event.y + size
            x2, y2 = event.x + size, event.y - size
            self.my_canvas.create_line(x1, y1, x2, y2, fill=color, width=4)
        elif self.brush_type.get() == "Diamond":
            x1, y1 = event.x, event.y + size
            x2, y2 = event.x + size, event.y
            x3, y3 = event.x, event.y - size
            x4, y4 = event.x - size, event.y
            self.my_canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=color, outline=color)

    # For changing the brush size
    def change_brush_size(self, size):
        self.brush_label.config(text=str(int(float(size))))
        self.brush_size = int(self.brush_slider.get())

    # For changing the brush color
    def change_brush_color(self):
        temp = colorchooser.askcolor()[1]
        if temp:
            self.brush_color = temp
            self.brush_color_label.config(bg=str(self.brush_color))

    # For changing the background of canvas
    def change_canvas_color(self):
        temp = colorchooser.askcolor()[1]
        if temp:
            self.canvas_color = temp
            self.my_canvas.configure(bg=str(self.canvas_color))
            self.canvas_color_label.config(bg=str(self.canvas_color))

    # Clearing the Canvas
    def clear_canvas(self):
        self.my_canvas.delete("all")
        self.my_canvas.configure(bg="white")

    # Converting Canvas drawing to PNG or JPG File and Saving
    def save_image(self):
        filename = filedialog.asksaveasfile(defaultextension=".*", initialdir="./Images/", title="Save File",
                                            filetypes=(("PNG File", "*.png"), ("JPG File", "*.jpg")))

        if filename:
            # Get the handle of the canvas
            my_canvas_handle = self.my_canvas.winfo_id()
            # Get the boundary of canvas
            my_canvas_boundary = win32gui.GetWindowRect(my_canvas_handle)
            # Saving the screenshot while cropping with the canvas boundary
            ImageGrab.grab().crop(my_canvas_boundary).save(filename.name)


if __name__ == "__main__":
    # Global Variables
    CANVAS_COLOR = 'white'
    BRUSH_COLOR = 'red'
    BRUSH_SIZE = 25

    root = Tk()
    PaintApp(root, CANVAS_COLOR, BRUSH_COLOR, BRUSH_SIZE)

    mainloop()
