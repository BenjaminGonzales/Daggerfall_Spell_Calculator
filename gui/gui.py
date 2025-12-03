from tkinter import *
from tkinter import ttk

class dsc_gui(Tk):
    def __init__(self):
        super().__init__()
        self.title("daggerfall spell calculator")

        self.frame = ttk.Frame()
        self.frame.grid(column=0, row=0, sticky=NSEW)

        self.spell_selector = top_level(self.frame)
        self.spell_selector.grid(column=0, row=1, sticky=EW)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def start_gui(self):
        self.mainloop()

    def set_spells(self, spells):
        self.spell_selector.set_spells(spells)

class top_level(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.feedback = StringVar()
        self.feedback.set("nothing yet!")

        self.spell_select = ttk.Combobox(self)
        self.spell_select.grid(column=0, row=0, sticky=EW)

        self.character_path_request_button = ttk.Button(self, text="Import Character", command=self.import_character)
        self.character_path_request_button.grid(column=2, row=0, sticky=EW)

        self.character_select = ttk.Entry(self)
        self.character_select.grid(column=1, row=0, sticky=EW)

        ttk.Label(self, textvariable=self.feedback).grid(column=0, row=1, sticky=EW, columnspan=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        self.columnconfigure(1, weight=1)
        
    def import_character(self):
        try:
            self.feedback.set("feedback set!~")
        except:
            pass

    def set_spells(self, args):
        try:
            print(f"setting spells: {args}")
            self.spell_select['values'] = args
        except:
            pass        

if __name__ == "__main__":
    # main_frame()
    dsc_gui().start_gui()