import random
import battle_event_queue
import animation
import config
from ability import move
import pokemon
import trainer
from battle_updater import BattleUpdater
import battle_hud


class Battle:

    def __init__(self, animation_manager: animation.ScreenAnimationManager, player: trainer.Trainer,
                 opponent: pokemon.Pokemon, game) -> None:
        self.anim_manager = animation_manager

        self.player_trainer = player
        self.opponent_trainer = trainer.Trainer
        self.player_pokemon = self.player_trainer.get_current_pokemon()
        self.opponent_pokemon = opponent

        self.queue = battle_event_queue.BattleEventQueue()
        self.battle_overlay = battle_hud.BattleHud(self.player_pokemon, self.opponent_pokemon)
        self.battle_updater = BattleUpdater(self)
        self.battle_mech = BattleMechanics()
        self.loaded = False
        self.game = game

    def have_event(self) -> bool:
        return self.queue.have_event()

    def has_been_loaded(self) -> bool:
        return self.loaded

    def begin(self) -> None:
        self.anim_manager.add_animation(animation.RectAnimation())

    def progress(self, user_input):
        # si le pokemo courant du player est plus rapide que pokemon en face
        if self.battle_mech.goes_first(self.player_pokemon, self.opponent_pokemon):

            self.play_turn(config.BATTLE_ACTOR_PLAYER, user_input)
            if self.battle_updater.current_state == config.BATTLE_STATE_READY_TO_PROGRESS:

                self.play_turn(config.BATTLE_ACTOR_OPPONENT, 0)
        else:
            self.play_turn(config.BATTLE_ACTOR_OPPONENT, 0)
            if self.battle_updater.current_state == config.BATTLE_STATE_READY_TO_PROGRESS:
                self.play_turn(config.BATTLE_ACTOR_PLAYER, user_input)


    def play_turn(self, user: int, user_input: int) -> None:

        target = BattleActor.get_opposite(user)
        pokemon_user = None
        pokemon_target = None
        if user == config.BATTLE_ACTOR_PLAYER:
            pokemon_user = self.player_pokemon
            pokemon_target = self.opponent_pokemon
        elif user == config.BATTLE_ACTOR_OPPONENT:
            pokemon_user = self.opponent_pokemon
            pokemon_target = self.player_pokemon

        move = pokemon_user.get_move_index(user_input)

        self.anim_manager.add_animation(animation.ListenableTextDisplay([pokemon_user.get_name() + " Utilise ", move.name]))

        if self.battle_mech.attempt_a_hit(move):
            move.use(self.battle_mech, pokemon_user, pokemon_target)
        else:
            self.anim_manager.add_animation(
                animation.ListenableTextDisplay([pokemon_user.get_name(), " a raté sa cible"]))

        if self.player_pokemon.is_fainted():
            # FAINTING ANIMATION
            nextpoke = self.player_trainer.get_current_pokemon()

            if nextpoke != None:
                self.anim_manager.add_animation(
                    animation.ListenableTextDisplay([self.player_pokemon.get_name(), " est K.O!"]))
                self.battle_updater.current_state = config.BATTLE_STATE_CHOOSE_NEW_POKEMON
                self.player_pokemon = nextpoke

            else:
                self.anim_manager.add_animation(
                    animation.ListenableTextDisplay(["Malheureusement", "vous avez perdu.."]))
                self.battle_updater.current_state = config.BATTLE_STATE_LOOSE
        elif self.opponent_pokemon.is_fainted():
            self.player_trainer.get_current_pokemon().add_exp(self.opponent_pokemon)
            self.anim_manager.add_animation(animation.ListenableTextDisplay(["Félicitation", "vous avez gagné"]))
            self.battle_updater.current_state = config.BATTLE_STATE_WIN
        else:
            self.battle_updater.restart_turn()

    def update(self):
        self.battle_updater.update()

    def draw(self, surface):
        self.battle_updater.draw(surface)


# this class is a child class of a general Battle, it represent a battle between the player and a Trainer with multiple pokemon
class TrainerBattle(Battle):

    def __init__(self, screen_manager, player, opponent: trainer.Trainer, game):
        super(TrainerBattle, self).__init__(screen_manager, player, opponent.get_current_pokemon(), game)
        self.opponent_sprite = opponent.get_current_pokemon().back_image
        self.player_pokemon_sprite = player.get_current_pokemon().front_image

    def begin(self):
        self.anim_manager.add_animation(animation.OpponentEnterBattle(self.opponent_pokemon))
        self.anim_manager.add_animation(
            animation.ListenableTextDisplay(["En avant ", self.player_trainer.get_current_pokemon().get_name() + " !"]))
        self.anim_manager.add_animation(animation.PlayerEnterBattle())
        self.anim_manager.add_animation(animation.PlayerPokemonEnterBattle(self.player_trainer.get_current_pokemon()))

        self.battle_updater.queue.add_event(battle_event_queue.BattleEventOptionBoxAndTextBox(self.player_trainer))
        self.battle_updater.queue.add_event(battle_event_queue.ChooseAttack(self.player_trainer.get_current_pokemon()))
        self.battle_updater.current_state = config.BATTLE_STATE_WAIT_FOR_USER_INPUT

        self.loaded = True




# this class is a child class of a general Battle, it represent a battle between the player and a wild pokemon
class WildBattle(Battle):

    def __init__(self, animation_manager: animation.ScreenAnimationManager, player: trainer.Trainer,
                 wild_pokemon: pokemon.Pokemon, game) -> None:
        super(WildBattle, self).__init__(animation_manager, player, wild_pokemon, game)
        self.opponent_sprite = wild_pokemon.front_image
        self.player_pokemon_sprite = player.get_current_pokemon().front_image

    # play the starting animation
    def begin(self) -> None:
        super().begin()
        self.anim_manager.add_animation(animation.OpponentEnterBattle(self.opponent_pokemon))
        self.anim_manager.add_animation(
            animation.ListenableTextDisplay(["Un " + self.opponent_pokemon.get_name() + " apparait ! ", ""]))
        self.anim_manager.add_animation(
            animation.ListenableTextDisplay(["En avant ", self.player_trainer.get_current_pokemon().get_name() + " !"]))
        self.anim_manager.add_animation(animation.PlayerEnterBattle())
        self.anim_manager.add_animation(animation.PlayerPokemonEnterBattle(self.player_trainer.get_current_pokemon()))
        self.battle_updater.queue.add_event(battle_event_queue.BattleEventOptionBoxAndTextBox(self.player_trainer))
        self.battle_updater.queue.add_event(battle_event_queue.ChooseAttack(self.player_trainer.get_current_pokemon()))
        self.battle_updater.current_state = config.BATTLE_STATE_WAIT_FOR_USER_INPUT

        self.loaded = True

    def chose_new_pokemon(self, pokemon: pokemon.Pokemon):
        pass

class BattleActor:

    @staticmethod
    def get_opposite(actor):
        if actor == config.BATTLE_ACTOR_PLAYER:
            return config.BATTLE_ACTOR_OPPONENT
        else:
            return config.BATTLE_ACTOR_PLAYER


class BattleMechanics:

    def __init(self):
        self.message = ""

    # return true if the player go first else False


    def goes_first(self, player: pokemon.Pokemon, opponent: pokemon.Pokemon) -> bool:
        if player.speed > opponent.speed:
            return True
        elif opponent.speed > player.speed:
            return False
        else:
            # same speed, speedTie
            return bool(random.getrandbits(1))

    def attempt_a_hit(self, move: move.Move) -> bool:
        random_float = random.randint(0, 1)
        if move.accuracy >= random_float:
            return True
        else:
            return False

    def critical_hit(self) -> bool:
        probability = 1 / 16
        if probability > random.randint(0, 1):
            return True
        else:
            return False

    def can_catch(self):
        probability = 0.5
        if probability > random.uniform(0, 1):
            return True
        else:
            return False

    def calculate_damage(self, move: move.Move, user: pokemon.Pokemon, target: pokemon.Pokemon):
        if move.category == "SPECIAL":
            attack = user.attack_spe
            defense = target.defense_spe
        else:
            attack = user.attack
            defense = target.defense

        critical_hit = self.critical_hit()
        level = user.level
        base = move.power
        modifier = random.uniform(0.85, 1)
        if critical_hit:
            modifier = modifier * 2
            self.message = "Coup Critique!"

        damage: int = int((((2 * int(level) + 10) / 250) * ((attack / defense) * base) + 2) * modifier)
        return damage
