import pytermgui as ptg

with ptg.WindowManager() as manager:
    window = (
        ptg.Window(
            "",
            ptg.InputField("Balazs", prompt="Name: "),
            ptg.InputField("Some street", prompt="Address: "),
            ptg.InputField("+11 0 123 456", prompt="Phone number: "),
            "",
            ptg.Container(
                "Additional notes:",
                ptg.InputField(
                    "A whole bunch of\nMeaningful notes\nand stuff", multiline=True
                ),
                box="EMPTY_VERTICAL",
            ),
            "",
            ["Submit", lambda *_: submit(manager, window)],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]New contact")
        .center()
    )

    manager.add(window)
