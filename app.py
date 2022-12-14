# https://textual.textualize.io/widgets/label/
# https://textual.textualize.io/widgets/input/
# https://textual.textualize.io/guide/reactivity/#watch-methods


import tkinter as tk
from tkinter import ttk
from db import Database


class GUI:
    LoggedInId = ""
    bgColour = "#292F36"
    headerColour = "#4ECDC4"
    header2Colour = "#FF6B6B"
    header3Colour = "#FFE66D"
    textColour = "#F7FFF7"

    def __init__(self):
        self.db = Database()
        self.compose()
        self.run()

    def run(self):
        self.root.mainloop()

    def compose(self):
        self.__genRoot()
        self.__genFrame()
        self.__genHeader()
        self.__genInput()
        self.__genTable()

    def __genRoot(self):
        self.root = tk.Tk()
        self.root.title("Equipment Library")
        self.root.geometry("640x480")
        self.root["bg"] = self.bgColour

    def __genFrame(self):
        self.frame = tk.Frame(self.root, background=self.bgColour)
        self.frame.grid(pady=20, padx=20)
        self.frame.pack()

    def __genHeader(self, username: str = ""):
        # Header
        text = "Scan your card to log in"
        if username:
            text = "Logged in as " + str(username)
        self.header = tk.Label(
            self.frame,
            text=text,
            background=self.headerColour,
            foreground=self.textColour,
            width="100",
            height="2",
            font="Helvetica 14 bold",
        )
        self.header.pack()

    def __genInput(self):
        # entry
        self.sv = tk.StringVar()
        self.entry = ttk.Entry(self.frame, width=30, textvariable=self.sv)
        self.entry.bind("<Return>", self.processInput)
        self.entry.pack()

    def __genTable(self):
        ttk.Style().configure(
            "Treeview",
            background=self.bgColour,
            foreground=self.textColour,
            fieldbackground=self.bgColour,
        )
        # scrollbar
        self.scroller = tk.Scrollbar(self.frame, orient="vertical")
        self.scroller.pack(side=tk.RIGHT, fill=tk.Y)
        self.table = ttk.Treeview(
            self.frame, yscrollcommand=self.scroller.set, height=15
        )
        self.table.pack()
        self.scroller.config(command=self.table.yview)
        # Define our columns
        cols = {"ID": "ID", "Borrowed_By": "Borrowed By:"}
        self.table["columns"] = tuple(cols.keys())
        # format our columns & headers
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.heading("#0", text="", anchor=tk.CENTER)
        for ref, text in cols.items():
            self.table.column(ref, anchor=tk.CENTER, width=300)
            self.table.heading(ref, text=text, anchor=tk.CENTER)
        # Add the data to the table
        self.fillTable()
        self.table.pack()

    def fillTable(self, partsList: list = None):
        # Clear the old values:
        self.table.delete(*self.table.get_children())
        if partsList == None:
            partsList = self.db.getParts()
        for index, part in enumerate(partsList):
            self.table.insert(
                parent="", index="end", iid=index, text="", values=tuple(part)
            )

    def _clear(self) -> None:
        self.sv.set("")
        dbItem = self.db.getId(self.LoggedInId)
        loggedInString = "Scan your card to log in"
        if dbItem:
            loggedInString = f"Logged in as {dbItem['name']}"
        self.header.config(text=loggedInString)
        # print(loggedInString)
        self.root.update()

    def processInput(self, event):
        # Lookup the ID in the database
        id = str(self.sv.get().strip())
        dbItem = self.db.getId(id)
        # If it doesn't match anything
        if not dbItem:
            self._clear()
            return
        # If it's a user ID
        if dbItem["dataType"] == "user":
            # If they're already logged in as that user, log them out
            if self.LoggedInId == id:
                self.LoggedInId = ""
                parts = self.db.getParts()
            # Log in as the user & update the screen.
            else:
                self.LoggedInId = id
                parts = self.db.getBorrowedEquipment(id)
        # If it's a piece of equipment
        else:
            # Change the equipment to whoever it logged in
            self.db.changeStatus(id, self.LoggedInId)
            # Update the list of parts shown
            if self.LoggedInId:
                parts = self.db.getBorrowedEquipment(self.LoggedInId)
            else:
                parts = self.db.getParts()
        self.fillTable(parts)
        self._clear()
        return True


if __name__ == "__main__":
    app = GUI()
    app.run()
