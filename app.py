# https://textual.textualize.io/widgets/label/
# https://textual.textualize.io/widgets/input/
# https://textual.textualize.io/guide/reactivity/#watch-methods


import tkinter as tk
from tkinter import ttk
from db import Database
from threading import Thread
import time
import logzero
import toml
from usbUpdater import Updater


class GUI:
    LoggedInId = ""
    bgColour = "#292F36"
    headerColour = "#4ECDC4"
    header2Colour = "#FF6B6B"
    header3Colour = "#FFE66D"
    textColour = "#F7FFF7"

    def __init__(self):
        self._loadConfig()
        self.db = Database()
        self.externalDbUpdater = Updater()
        self.externalDbUpdater.run()
        self.compose()
        self.startBackground()
        self.run()

    def _loadConfig(self):
        with open("config.toml", "r") as f:
            self.config = toml.load(f)["gui"]
        logzero.logfile(self.config["logFilename"])
        logzero.loglevel(int(self.config["logLevel"]))

    def run(self):
        self.root.mainloop()

    def startBackground(self):
        self.lastInput = self._getNow()
        t = Thread(target=self._thread)
        t.start()

    def _thread(self):
        while True:
            time.sleep(1)
            # Move the focus back to the input box
            self.entry.focus_set()
            # If somebody is logged in
            if self.LoggedInId:
                # If it's been 20 seconds of inactivity
                autoLogoutTime = int(self.config["autoLogoutTime"])
                if self.lastInput + autoLogoutTime < self._getNow():
                    # Log out
                    logzero.logger.debug("Running auto log-out")
                    self.sv.set(str(self.LoggedInId))
                    self.processInput(None)

    def _getNow(self):
        return time.time()

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
        # self.root.attributes('-fullscreen', True)
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
        self.entry.focus_set()
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
            self.frame, yscrollcommand=self.scroller.set, height=20
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
        partsListSorted = sorted(partsList, key=lambda e: e[0])
        partsListSorted = sorted(partsListSorted, key=lambda e: e[1], reverse=True)
        for index, part in enumerate(partsListSorted):
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
        # Log the last input
        self.lastInput = self._getNow()
        # Lookup the ID in the database
        id = str(self.sv.get().strip())
        dbItem = self.db.getId(id)
        # If it doesn't match anything
        if not dbItem:
            logzero.logger.warning(f"Invalid Barcode:\t{id}")
            self._clear()
            return
        # If it's a user ID
        if dbItem["dataType"] == "user":
            # If they're already logged in as that user, log them out
            if self.LoggedInId == id:
                logzero.logger.info(f"Logging out:\t{dbItem['name']}")
                self.LoggedInId = ""
            # Log in as the user & update the screen.
            else:
                logzero.logger.info(f"Logging in:\t{dbItem['name']}")
                self.LoggedInId = id
        # If it's a piece of equipment
        else:
            # Change the equipment to whoever is logged in
            user = self.db.getId(self.LoggedInId)
            if user:
                logzero.logger.info(
                    f"{user['name']}\tborrowing\t{dbItem['id']}\t{dbItem['name']}"
                )
            else:
                user = self.db.getId(dbItem["status"])
                if user:
                    logzero.logger.info(
                        f"{user['name']}\tReturning\t{dbItem['id']}\t{dbItem['name']}"
                    )
            self.db.changeStatus(id, self.LoggedInId)
        # Update the list of parts shown
        if self.LoggedInId:
            parts = self.db.getBorrowedEquipment(self.LoggedInId)
        else:
            parts = self.db.getParts()
        # Update the GUI
        self.fillTable(parts)
        self._clear()
        return True


if __name__ == "__main__":
    app = GUI()
    app.run()
