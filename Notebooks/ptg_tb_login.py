# https://github.com/bczsalba/pytermgui/blob/master/utils/readme_scripts/contact.py

import pytermgui as ptg
from db import Database

db = Database()

OUTPUT = {}
def submitLogin(manager: ptg.WindowManager, window: ptg.Window) -> None:
    for widget in window:
        if isinstance(widget, ptg.InputField):
            OUTPUT[widget.prompt] = widget.value
            continue

        if isinstance(widget, ptg.Container):
            label, field = iter(widget)
            OUTPUT[label.value] = field.value
    manager.stop()

with ptg.WindowManager() as manager:
    window = (
        ptg.Window(
            "",
            ptg.InputField("", prompt="Scan card to log in: "),
            "",
            ptg.Window(db.getPartsString(), multiline=True, box="EMPTY_VERTICAL"),
            "",
            ["Submit", lambda *_: submitLogin(manager, window)],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]Home Page")
        .center()
    )

    manager.add(window)
