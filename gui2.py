import pytermgui as ptg
from db import Database

db = Database()

with ptg.WindowManager() as manager:
    window = (
        ptg.Window(
            "",
            ptg.InputField("", prompt="Scan card to log in: "),
            "",
            ptg.Window("", multiline=True, box="EMPTY_VERTICAL")
            "",
            ["Submit", lambda *_: submit(manager, window)],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]New contact")
        .center()
    )

    manager.add(window)
