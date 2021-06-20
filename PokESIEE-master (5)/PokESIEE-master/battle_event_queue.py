import text_box
import selection_box
import config


class BattleEventQueue:

    def __init__(self) -> None:
        self.event_queue = []

    def get_current_event(self):
        if not len(self.event_queue) == 0:
            return self.event_queue[len(self.event_queue) - 1]

    def del_current_event(self) -> None:
        del self.event_queue[-1]

    def have_event(self) -> bool:
        return not len(self.event_queue) == 0

    def add_event(self, animation) -> None:
        self.event_queue.insert(0, animation)

    def clear(self):
        self.event_queue.clear()

class Event:

    def __init__(self):
        self.user_input = ''
        self.isFinished = False


class BattleEventOptionBoxAndTextBox(Event):

    def __init__(self, player):
        super(BattleEventOptionBoxAndTextBox, self).__init__()
        self.current_text_box = text_box.TextBox(["Que va faire ", player.get_current_pokemon().get_name() + " ?"])
        self.current_option_box = selection_box.SelectionBox(int(config.SCREEN_WIDTH / 2) + 30,
                                                             int(config.SCREEN_WIDTH / 2) - 30,
                                                             ["Attaque", "Pokémon", "Capture", "Fuite"], 4, 14)

    def update(self):
        if self.current_option_box.user_have_choose and self.current_option_box.timer > 20:
            self.isFinished = True
        self.current_option_box.update()

    def get_user_input(self) -> int:
        return self.current_option_box.find_user_input()

    def draw(self, surface):
        self.current_text_box.draw(surface)
        self.current_option_box.draw(surface)


class ChooseAttack(Event):

    def __init__(self, pokemon):
        super(ChooseAttack, self).__init__()
        self.option = []
        for moves in pokemon.moves:
            if moves is not None:
                self.option.append(moves.name)

        self.current_option_box = selection_box.SelectionBox(int(config.SCREEN_WIDTH / 2) + 100,
                                                             int(config.SCREEN_WIDTH / 2) - 100,
                                                             self.option,
                                                             len(self.option),
                                                             12)

    def draw(self, surface):
        self.current_option_box.draw(surface)

    def update(self):
        if self.current_option_box.user_have_choose:
            self.isFinished = True
        self.current_option_box.update()

    def get_user_input(self) -> int:
        return self.current_option_box.find_user_input()


class YesNoOptionWithMessage(Event):

    def __init__(self, message: list[str, str]) -> None:
        super(YesNoOptionWithMessage, self).__init__()
        self.current_option_box = selection_box.SelectionBox(80, 350, ["Yes", " ", "No"], 3, 14)
        self.current_text_box = text_box.TextBox(message)

    def draw(self, surface):
        self.current_option_box.draw(surface)
        self.current_text_box.draw(surface)

    def update(self):
        self.current_option_box.update()
