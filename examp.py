import tkinter as tk

class Main(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        lbl = tk.Label(self, text="this is the main frame\n")
        lbl.pack()

        btn = tk.Button(self, text='click me', command=self.open_popup)
        btn.pack()

        self.output = tk.Label(self)
        self.output.pack()

    def open_popup(self):
        print("runs before the popup")
        p = Popup(self)
        print("runs after the popup closes")
        self.output.config(text=f"Got data returned:\n {p.result!r}")

class Popup(tk.Toplevel):
    """modal window requires a master"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        lbl = tk.Label(self, text="this is the modal window popup\ntype something")
        lbl.pack()

        self.ent = tk.Entry(self)
        self.ent.insert(0, "Hello world")
        self.ent.pack()

        btn = tk.Button(self, text="OK", command=self.on_ok)
        btn.pack()

        # The following commands keep the popup on top.
        # Remove these if you want a program with 2 responding windows.
        # These commands must be at the end of __init__
        self.transient(master) # set to be on top of the main window
        self.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self) # pause anything on the main window until this one closes

    def on_ok(self):
        self.result = self.ent.get() # save the return value to an instance variable.
        self.destroy()

def main():
    root = tk.Tk()
    window = Main(root)
    window.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
