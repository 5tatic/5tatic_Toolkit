import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageEnhance

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image OGRE")

        self.canvas = Canvas(root, cursor="cross")
        self.canvas.pack(fill=BOTH, expand=True)

        self.image = None
        self.photo = None
        self.rect = None
        self.start_x = self.start_y = None
    
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<buttonRelease-1>", self.on_release)

        menu = Menu(root)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image...", command=self.open_image)
        file_menu.add_command(label="Apply Edit", command=self.apply_edit)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        self.image = cv2.imread(file_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.show_image()

    def show_image(self, img=None):
        if img is None:
            img = self.image
        self.photo - ImageTk.PhotoImage(image=Image.formarray(img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.start_x, self.start_y, outline='green')

    def on_release(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.delete(self.rect)
        self.rect = None
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='green')

    def apply_edit(self):
        if self.image is None or self.start_x is None:
            return
        # Example edit: Convert selected region to grayscale
        roi = cv2.cvtColor(self.image[self.start_y:self.end_y:self.start_x:self.end_x], cv2.COLOR_RGB2GRAY)
        color_roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
        self.image[self.start_y:self.end_y, self.start_x:self.end_x] = color_roi
        self.show_image()

    def draw(self, event):
        if not self.drawing:
            return
        self.canvas.create_line(self.prev_x, self.prev_y, event_x, event_y, fill="green", width=2)
        cv2.line(self.mask, (self.prev_x, self.prev_y), (event.x, event.y). 255, thickness=2)
        self.prev_x = event.x
        self.prev_y = event.y

    def stop_draw(self, event):
        self.drawing = False
    
    def apply_edit(self):
        if self.image is None or self.start_x is None:
            return
        # Example edit: Convert selected region to grayscale
        roi = cv2.cvtColor(self.image[self.start_y:self.end_y:self.start_x:self.end_x], cv2.COLOR_RGB2GRAY)
        color_roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
        self.image[self.start_y:self.end_y, self.start_x:self.end_x] = color_roi
        self.show_image()

    def adjust_brightness(self):
        # Example: Adjust brightness
        factor = simpledialog.askfloat("Brightness", "Enter brightness factor (.05 for darker, 2 for brighter):", minvalue=0.1, maxvalue=3.0)
        if factor is not None:
            self.apply_edit(self.brightness_adjustment, factor)

    def brightness_adjustment(self, image, factor):
        enhancer = ImageEnhace.Brightness(Image.fromarray(image))
        enhanced_im = enhancer.enhance(factor)
        return np.array(enganced_im)
    
    def apply_grayscale_filter(self):
        self.apply_edit(self.grayscale_filter)

    def grayscale_filter(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        colored_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        # Apply the mask
        masked_image = np.where(self.mask[:, :, None] > 0, colored_image, image)
        

if __name__ == "__main__":
    root = Tk()
    app = ImageEditor(root)
    root.mainloop()
    