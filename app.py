# https://textual.textualize.io/widgets/label/
# https://textual.textualize.io/widgets/input/
# https://textual.textualize.io/guide/reactivity/#watch-methods


from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, Static, DataTable
from db import Database

db = Database()


class Homepage(App):
    CSS_PATH = "app.css"
    LoggedInId = ""
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Static("", classes="header", id="Username"),
                Input(placeholder="Scan your **card to borrow**, or some equipment to return"),
                DataTable(show_cursor=False)
            )
        )

    def _setTableRows(self, rows) -> None:
        table = self.query_one(DataTable)
        table.clear()
        if not table.columns:
            table.add_columns(*["      Equipment      ", "      Borrowed By      "])
        table.add_rows(rows)

    def on_mount(self) -> None:
        parts = db.getParts()
        self._setTableRows(parts)
    
    def _clear(self) -> None:
        self.query_one(Input).value = ""
        dbItem = db.getId(self.LoggedInId)
        loggedInString = ''
        if dbItem:
            loggedInString = f"Logged in as {dbItem['name']}"
        self.query_one("#Username").update(loggedInString)
        


    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Lookup the ID in the database
        id = str(event.value)
        dbItem = db.getId(id)
        # If it doesn't match anything
        if not dbItem:
            self._clear()
            return
        # If it's a users ID
        if dbItem["dataType"] == 'user':
            # If they're already logged in as that user, log them out
            if self.LoggedInId == id:
                self.LoggedInId = ""
                parts = db.getParts()
                self._setTableRows(parts)
            # Log in as the user & update the screen.
            else:
                self.LoggedInId = id
                parts = db.getBorrowedEquipment(id)
                self._setTableRows(parts)
            pass
        # If it's a piece of equipment
        else:
            # Change the equipment to whoever it logged in
            db.changeStatus(id, self.LoggedInId)
            # Update the list of parts shown
            if self.LoggedInId:
                parts = db.getBorrowedEquipment(self.LoggedInId)
            else:
                parts = db.getParts()
            self._setTableRows(parts)
        self._clear()
        return dbItem


if __name__ == "__main__":
    app = Homepage()
    app.run()