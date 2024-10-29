import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, Frame
from frames import *


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('CNC Utility')
        self.file_name = ''
        self.content = {'height': '0'   , 'width': '0'  , 'thickness':'0', 'elements':[]}
        self.parent.geometry('800x600')
        self.menu_bar = MenuBar(self)
        self.parent.configure(menu=self.menu_bar)
        self.file_changed = False

        self.frm_dimensions = DimFrame(self, borderwidth=1, relief=tk.GROOVE, padding=[0, 0])
        self.frm_dimensions.pack(anchor=tk.NW, padx=1, pady=1, side=tk.LEFT)
        self.frm_info = Frame(self, borderwidth=1, relief=tk.GROOVE)
        self.frm_info.pack(anchor=tk.NW, padx=1, pady=1, fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.frm_fig = Frame(self, borderwidth=1, relief=tk.GROOVE)
        self.frm_fig.pack(anchor=tk.NW, padx=1, pady=1, fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.content['elements'].append({'type': 'Compartment', 'door': False, 'shelves': 2, 'height': '450'})

        self.redraw_list()


    def redraw_list(self):

        for widget in self.frm_info.winfo_children():
            widget.destroy()
        for element in reversed(self.content['elements']):
            row = ttk.Frame(self.frm_info)
            row.pack(anchor=tk.NW)
            match element['type']:
                case 'box':
                    box_height = ttk.Label(row, text=element['height'], justify='left', font=("Arial", 16))
                    box_height.pack(side=tk.LEFT)
                    lbl = ttk.Label(row, text=f"{element['name']}-{element['width']}.", justify='left')
                    lbl.pack(side=tk.LEFT, padx=5)
                case 'Compartment':
                    cell_height = ttk.Label(row, text=element['height'], justify='left', font=("Arial", 16))
                    cell_height.pack(side=tk.LEFT)
                    lbl = ttk.Label(row, text=f"Compartment {'with' if element['door'] else 'without' } door "
                                              f"and {element['shelves']} shelves.", justify='left')
                    lbl.pack(side=tk.LEFT, padx=5)

    def new_file(self):
        """Clear all fields for a new file."""
        self.content = {'height': '0' , 'width': '0' , 'thickness':'0', 'elements':[]}
        self.redraw_list()


    def open_file(self):
        file = filedialog.askopenfilename()
        with open(file, 'r', encoding='utf-8') as f:
            self.content = json.load(f)
            self.file_name = file
            f.close()
        self.frm_dimensions.clear_data()
        self.frm_dimensions.ent_width.insert(0,self.content['width'])
        self.frm_dimensions.ent_height.insert(0,self.content['height'])
        self.frm_dimensions.ent_thickness.insert(0,self.content['thickness'])
        self.redraw_list()


    def save_file(self):
        if self.file_changed:
            if self.file_name:
                self.content['height'] = self.frm_dimensions.ent_height.get()
                self.content['width'] = self.frm_dimensions.ent_width.get()
                self.content['thickness'] = self.frm_dimensions.ent_thickness.get()
                json_object = json.dumps(self.content, indent=4)
                with open(self.file_name, 'w', encoding='utf-8') as f:
                    f.write(json_object)
            else:
                self.save_as_file()

    def save_as_file(self):
        self.content['height'] = self.frm_dimensions.ent_height.get()
        self.content['width'] = self.frm_dimensions.ent_width.get()
        self.content['thickness'] = self.frm_dimensions.ent_thickness.get()
        file = filedialog.asksaveasfile(filetypes=[('json files', '*.json')], defaultextension='.json')
        json_object = json.dumps(self.content, indent=4)
        if not file:
            return
        with open(file.name, 'w', encoding='utf-8') as f:
            f.write(json_object)

    def quit(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit(0)


class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save as...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def quit(self):
        self.parent.quit()

    def new_file(self):
        self.parent.new_file()

    def open_file(self):
        self.parent.open_file()

    def save_file(self):
        self.parent.save_file()

    def save_as_file(self):
        self.parent.save_as_file()



if __name__ == "__main__":
    root = tk.Tk()
    Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()