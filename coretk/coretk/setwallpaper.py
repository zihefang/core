"""
set wallpaper
"""
import enum
import logging
import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

PATH = os.path.abspath(os.path.dirname(__file__))
WALLPAPER_DIR = os.path.join(PATH, "wallpaper")


class ScaleOption(enum.Enum):
    UPPER_LEFT = 1
    CENTERED = 2
    SCALED = 3
    TILED = 4


class CanvasWallpaper:
    def __init__(self, application):
        self.application = application
        self.canvas = self.application.canvas

        self.top = tk.Toplevel()
        self.top.title("Set Canvas Wallpaper")
        self.radiovar = tk.IntVar()
        self.show_grid_var = tk.IntVar()
        self.adjust_to_dim_var = tk.IntVar()
        self.wallpaper = None

        self.create_image_label()
        self.create_text_label()
        self.open_image()
        self.display_options()
        self.additional_options()
        self.apply_cancel()

    def create_image_label(self):
        image_label = tk.Label(
            self.top, text="(image preview)", height=8, width=32, bg="white"
        )
        image_label.grid(pady=5)

    def create_text_label(self):
        text_label = tk.Label(self.top, text="Image filename: ")
        text_label.grid()

    def open_image_link(self):
        filename = filedialog.askopenfilename(
            initialdir=WALLPAPER_DIR,
            title="Open",
            filetypes=(
                ("images", "*.gif *.jpg *.png *.bmp *pcx *.tga ..."),
                ("All Files", "*"),
            ),
        )

        # fill the file name into the file name entry
        img_open_frame = self.top.grid_slaves(2, 0)[0]
        filename_entry = img_open_frame.grid_slaves(0, 0)[0]
        filename_entry.delete(0, tk.END)
        filename_entry.insert(tk.END, filename)

        # display that onto the label
        img_label = self.top.grid_slaves(0, 0)[0]
        if filename:
            img = Image.open(filename)
            img = img.resize((250, 135), Image.ANTIALIAS)
            tk_img = ImageTk.PhotoImage(img)
            img_label.config(image=tk_img, width=250, height=135)
            img_label.image = tk_img

    def clear_link(self):
        # delete entry
        img_open_frame = self.top.grid_slaves(2, 0)[0]
        filename_entry = img_open_frame.grid_slaves(0, 0)[0]
        filename_entry.delete(0, tk.END)

        # delete display image
        img_label = self.top.grid_slaves(0, 0)[0]
        img_label.config(image="", width=32, height=8)

    def open_image(self):
        f = tk.Frame(self.top)

        var = tk.StringVar(f, value="")
        e = tk.Entry(f, textvariable=var)
        e.focus()
        e.grid()

        b = tk.Button(f, text="...", command=self.open_image_link)
        b.grid(row=0, column=1)

        b = tk.Button(f, text="Clear", command=self.clear_link)
        b.grid(row=0, column=2)

        f.grid()

    def display_options(self):
        f = tk.Frame(self.top)

        b1 = tk.Radiobutton(f, text="upper-left", value=1, variable=self.radiovar)
        b1.grid(row=0, column=0)

        b2 = tk.Radiobutton(f, text="centered", value=2, variable=self.radiovar)
        b2.grid(row=0, column=1)

        b3 = tk.Radiobutton(f, text="scaled", value=3, variable=self.radiovar)
        b3.grid(row=0, column=2)

        b4 = tk.Radiobutton(f, text="titled", value=4, variable=self.radiovar)
        b4.grid(row=0, column=3)

        self.radiovar.set(1)

        f.grid()

    def additional_options(self):
        b = tk.Checkbutton(self.top, text="Show grid", variable=self.show_grid_var)
        b.grid(sticky=tk.W, padx=5)
        b = tk.Checkbutton(
            self.top,
            text="Adjust canvas size to image dimensions",
            variable=self.adjust_to_dim_var,
        )
        b.grid(sticky=tk.W, padx=5)
        self.show_grid_var.set(1)
        self.adjust_to_dim_var.set(0)

    def delete_previous_wallpaper(self):
        prev_wallpaper = self.canvas.find_withtag("wallpaper")
        if prev_wallpaper:
            for i in prev_wallpaper:
                self.canvas.delete(i)

    def get_canvas_width_and_height(self):
        """
        retrieve canvas width and height in pixels

        :return: nothing
        """
        canvas = self.application.canvas
        grid = canvas.find_withtag("rectangle")[0]
        x0, y0, x1, y1 = canvas.coords(grid)
        canvas_w = abs(x0 - x1)
        canvas_h = abs(y0 - y1)
        return canvas_w, canvas_h

    def determine_cropped_image_dimension(self):
        """
        determine the dimension of the image after being cropped

        :return: nothing
        """
        return

    def upper_left(self, img):
        tk_img = ImageTk.PhotoImage(img)

        # crop image if it is bigger than canvas
        canvas_w, canvas_h = self.get_canvas_width_and_height()

        cropx = img_w = tk_img.width()
        cropy = img_h = tk_img.height()

        if img_w > canvas_w:

            cropx -= img_w - canvas_w
        if img_h > canvas_h:
            cropy -= img_h - canvas_h
        cropped = img.crop((0, 0, cropx, cropy))
        cropped_tk = ImageTk.PhotoImage(cropped)

        # place left corner of image to the left corner of the canvas
        self.application.croppedwallpaper = cropped_tk

        self.delete_previous_wallpaper()

        wid = self.canvas.create_image(
            (cropx / 2, cropy / 2), image=cropped_tk, tags="wallpaper"
        )
        self.application.wallpaper_id = wid

    def center(self, img):
        """
        place the image at the center of canvas

        :param Image img: image object
        :return: nothing
        """
        tk_img = ImageTk.PhotoImage(img)
        canvas_w, canvas_h = self.get_canvas_width_and_height()

        cropx = img_w = tk_img.width()
        cropy = img_h = tk_img.height()

        # dimension of the cropped image
        if img_w > canvas_w:
            cropx -= img_w - canvas_w
        if img_h > canvas_h:
            cropy -= img_h - canvas_h

        x0 = (img_w - cropx) / 2
        y0 = (img_h - cropy) / 2
        x1 = x0 + cropx
        y1 = y0 + cropy
        cropped = img.crop((x0, y0, x1, y1))
        cropped_tk = ImageTk.PhotoImage(cropped)

        # place the center of the image at the center of the canvas
        self.application.croppedwallpaper = cropped_tk
        self.delete_previous_wallpaper()
        wid = self.canvas.create_image(
            (canvas_w / 2, canvas_h / 2), image=cropped_tk, tags="wallpaper"
        )
        self.application.wallpaper_id = wid

    def scaled(self, img):
        """
        scale image based on canvas dimension

        :param Image img: image object
        :return: nothing
        """
        canvas_w, canvas_h = self.get_canvas_width_and_height()
        resized_image = img.resize((int(canvas_w), int(canvas_h)), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(resized_image)
        self.application.croppedwallpaper = image_tk

        self.delete_previous_wallpaper()

        wid = self.canvas.create_image(
            (canvas_w / 2, canvas_h / 2), image=image_tk, tags="wallpaper"
        )
        self.application.wallpaper_id = wid

    def tiled(self, img):
        return

    def show_grid(self):
        """

        :return: nothing
        """
        if self.show_grid_var.get() == 0:
            for i in self.canvas.find_withtag("gridline"):
                self.canvas.itemconfig(i, state=tk.HIDDEN)
        elif self.show_grid_var.get() == 1:
            for i in self.canvas.find_withtag("gridline"):
                self.canvas.itemconfig(i, state=tk.NORMAL)
                self.canvas.lift(i)
        else:
            logging.error("setwallpaper.py show_grid invalid value")

    def click_apply(self):
        img_link_frame = self.top.grid_slaves(2, 0)[0]
        filename = img_link_frame.grid_slaves(0, 0)[0].get()
        if not filename:
            self.top.destroy()
            return
        try:
            img = Image.open(filename)
        except FileNotFoundError:
            print("invalid filename, draw original white plot")
            if self.application.wallpaper_id:
                self.canvas.delete(self.application.wallpaper_id)
            self.top.destroy()
            return
        if self.radiovar.get() == ScaleOption.UPPER_LEFT.value:
            self.upper_left(img)
        elif self.radiovar.get() == ScaleOption.CENTERED.value:
            self.center(img)
        elif self.radiovar.get() == ScaleOption.SCALED.value:
            self.scaled(img)
        elif self.radiovar.get() == ScaleOption.TILED.value:
            print("not implemented yet")

        self.show_grid()
        self.top.destroy()

    def apply_cancel(self):
        f = tk.Frame(self.top)

        b = tk.Button(f, text="Apply", command=self.click_apply)
        b.grid(row=0, column=0)

        b = tk.Button(f, text="Cancel", command=self.top.destroy)
        b.grid(row=0, column=1)

        f.grid(pady=5)
