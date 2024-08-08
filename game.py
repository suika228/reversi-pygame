from literal_types import Type


class Game:

    def __init__(self) -> None:
        self.player: Type.PLAYER = "X"

    def switch_player(self) -> None:
        if self.player == "O":
            self.player = "X"
        else:
            self.player = "O"
