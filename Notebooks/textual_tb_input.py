# https://textual.textualize.io/widgets/label/
# https://textual.textualize.io/widgets/input/
# https://textual.textualize.io/guide/reactivity/#watch-methods


from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, Static


class InputApp(App):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Static("Scan your **card to borrow**, or some **equipment to return**", classes="header"),
                Input(placeholder="ID: ")
            )
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        print("************")
        print("************")
        print(f"  {str(event.value)}")
        print("************")
        print("************")

        self.exit(str(event.value))


if __name__ == "__main__":
    app = InputApp()
    app.run()