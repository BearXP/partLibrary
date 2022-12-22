try:
    import Tkinter as Tk
    from Tkinter import ttk
except ModuleNotFoundError:
    import tkinter as Tk
    from tkinter import ttk

if __name__ == '__main__':
    root = Tk.Tk()
    frame = Tk.Frame(root)

    tree = ttk.Treeview(frame.master, columns=("Name", "Hex Code"), show="headings")
    tree.heading('Name', text="Name")
    tree.heading('Hex Code', text="Hex Code")

    tree.pack()
    dct = {"red":"#ff0000",
           "green":"#00ff00",
           "pink":"#ff1493",
           "teal":"#00cece"}

    for key, value in dct.items():
        tree.insert("", "end",tag=key, values=(key,value))
        tree.tag_configure(tagname=key, background=value)
        

    root.mainloop()