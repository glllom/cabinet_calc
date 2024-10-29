from classes import EntryDigits
from dialog import *
class DimFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.lbl_width = ttk.Label(self, text="Width: ")
        self.lbl_width.grid(row=0, column=0)
        self.ent_width = EntryDigits(self)
        self.ent_width.grid(row=0, column=1, padx=5, pady=5)
        self.lbl_height = ttk.Label(self, text="Height: ")
        self.lbl_height.grid(row=1, column=0)
        self.ent_height = EntryDigits(self)
        self.ent_height.grid(row=1, column=1, padx=5, pady=5)
        self.lbl_thickness = ttk.Label(self, text="Thickness: ")
        self.lbl_thickness.grid(row=2, column=0)
        self.ent_thickness = EntryDigits(self)
        self.ent_thickness.grid(row=2, column=1, padx=5, pady=5)

        self.btn_add_shelves = ttk.Button(self, text="Add Shelves", command=self.add_shelves)
        self.btn_add_shelves.grid(row=3, column=0, padx=5, pady=5)

        self.btn_add_boxes = ttk.Button(self, text="Add Boxes", command=self.add_boxes)
        self.btn_add_boxes.grid(row=4, column=0, padx=5, pady=5)

    def clear_data(self):
        self.ent_width.delete(0, tk.END)
        self.ent_height.delete(0, tk.END)
        self.ent_thickness.delete(0, tk.END)

    def add_shelves(self):
        print("shelf added")

    def add_boxes(self):
        box_window = BoxesWindow(self, self.parent.redraw_list, elements=self.parent.content['elements'])
        # print(f"data={box_window}")
        # self.parent.redraw_list()
        print("box added2")

        box_window.grab_set()
        print("box added3")


