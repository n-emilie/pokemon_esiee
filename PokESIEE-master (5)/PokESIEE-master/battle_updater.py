import random

import animation
import pygame

import battle
import battle_hud
import battle_event_queue
import config
import os


class BattleUpdater:

    def __init__(self, battle):
        self.battle = battle
        self.image_path = "ui/pokemon_battle_background.png"
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(config.image, self.image_path)),
                                            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.user_input = -1
        self.current_state = config.BATTLE_STATE_READY_TO_PROGRESS
        self.next_state = config.BATTLE_STATE_READY_TO_PROGRESS
        self.queue = self.battle.queue
        self.anim_manager = self.battle.anim_manager
        self.need_to_draw_wild_pokemon = False
        self.need_to_draw_player_pokemon = False
        self.battle_overlay = self.battle.battle_overlay
        self.user_input = int

        self.tryna_restart = False

        self.need_listen_moves = False
        self.need_listen_options = True

        self.need_event_move = True
        self.need_event_option = True

    def update(self):
        if not self.anim_manager.have_animation():
            if self.battle.queue.have_event():
                self.current_state = config.BATTLE_STATE_WAIT_FOR_USER_INPUT
                self.battle.queue.get_current_event().update()
            else:
                if self.current_state == config.BATTLE_STATE_RUN:
                    self.want_to_quit_fight(config.GAME_STATE_EXPLORATION)
                elif self.current_state == config.BATTLE_STATE_WIN:
                    self.want_to_quit_fight(config.GAME_STATE_EXPLORATION)
                elif self.current_state == config.BATTLE_STATE_LOOSE:
                    self.battle.game.player.change_current_tile(
                        self.battle.game.player_save[len(self.battle.game.player_save) - 1])
                    self.battle.game.player.update_coordinates()
                    self.want_to_quit_fight(config.GAME_STATE_EXPLORATION)

        if self.battle.queue.have_event() and self.battle.queue.get_current_event().isFinished:
            self.current_state = config.BATTLE_STATE_READY_TO_PROGRESS
            self.user_input = self.queue.get_current_event().get_user_input()
            self.queue.del_current_event()

        if self.current_state == config.BATTLE_STATE_CHOOSE_NEW_POKEMON:
            self.anim_manager.add_animation(
                animation.ListenableTextDisplay(["un pokémon de votre équipe", "a été envoyé au combat", ""]))
            self.current_state = config.BATTLE_STATE_READY_TO_PROGRESS
            self.restart_turn()

        self.battle_overlay.update(self.battle.player_trainer.get_current_pokemon(), self.battle.opponent_pokemon)
        # print(self.battle.queue.event_queue)
        # print(self.current_state)
        if self.current_state == config.BATTLE_STATE_READY_TO_PROGRESS:
            if self.need_listen_options:
                self.listen_option()
            elif self.need_listen_moves:
                self.listen_moves()
        if self.tryna_restart:
            self.restart_turn()


    def restart_turn(self):
        if not self.anim_manager.have_animation():
            self.need_listen_options = True
            self.queue.add_event(battle_event_queue.BattleEventOptionBoxAndTextBox(self.battle.player_trainer))
            self.queue.add_event(battle_event_queue.ChooseAttack(self.battle.player_trainer.get_current_pokemon()))
            self.current_state = config.BATTLE_STATE_WAIT_FOR_USER_INPUT
            self.tryna_restart = False
        else:
            self.tryna_restart = True

    def listen_option(self):
        #attaque
        if self.user_input == 0:
            self.need_listen_moves = True
            self.need_listen_options = False
        #capture
        elif self.user_input == 2:
            self.queue.clear()
            if isinstance(self.battle, battle.TrainerBattle):
                self.anim_manager.add_animation(animation.ListenableTextDisplay(
                    ["On ne capture pas le pokémon ", " d'un dresseur adverse!!!!"]))
                self.restart_turn()
            else:
                self.anim_manager.add_animation(animation.ListenableTextDisplay(
                    ["Vous essayez de capturer ", self.battle.opponent_pokemon.get_name()]))
                if self.battle.battle_mech.can_catch():
                    self.anim_manager.add_animation(animation.ListenableTextDisplay(
                        ["Vous avez capturé ", self.battle.opponent_pokemon.get_name() + " !"]))
                    self.battle.player_trainer.pokemon_list.append(self.battle.opponent_pokemon)
                    self.current_state = config.BATTLE_STATE_WIN
                else:
                    self.anim_manager.add_animation(animation.ListenableTextDisplay(
                        ["Vous n'avez pas reussi a capturer ", self.battle.opponent_pokemon.get_name() + "..."]))
                    self.restart_turn()
            self.need_listen_options = False
            self.need_listen_moves = False
        #fuite
        elif self.user_input == 3:
            self.queue.clear()
            if isinstance(self.battle, battle.TrainerBattle):
                self.anim_manager.add_animation(
                    animation.ListenableTextDisplay(["On ne fuit pas d'un combat de dresseur! ", ""]))
                self.restart_turn()
            else:
                self.anim_manager.add_animation(animation.ListenableTextDisplay(["vous fuyez ! (lache)", ""]))
                self.current_state = config.BATTLE_STATE_RUN
            self.need_listen_moves = False
            self.need_listen_options = False
        #pokemon
        elif self.user_input == 1:
            self.queue.clear()
            # anim.set_font_size(12)
            self.anim_manager.add_animation(animation.ListenableTextDisplay(["Vos pokémons sont :",
                                                                             self.battle.player_trainer.get_pokemon_string()]))
            self.restart_turn()

    def want_to_quit_fight(self, state: int) -> None:
        self.battle.game.player.can_move = True
        self.battle.game.request_state_change(state)

    def listen_moves(self):
        self.battle.progress(self.user_input)
        self.need_listen_moves = False
        self.need_listen_options = False

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (0, 0))
        self.draw_opponent_pokemon(surface)
        self.draw_player_pokemon(surface)
        if not self.anim_manager.have_animation():
            if self.queue.have_event():
                self.queue.get_current_event().draw(surface)
        self.battle_overlay.draw(surface)

    def draw_opponent_pokemon(self, surface: pygame.Surface) -> None:
        self.need_to_draw_wild_pokemon = True
        for anim in self.anim_manager.animation_queue:
            if isinstance(anim, animation.OpponentEnterBattle) or isinstance(anim, animation.OpponentPokemonFaint):
                self.need_to_draw_wild_pokemon = False
        if self.need_to_draw_wild_pokemon:
            surface.blit(self.battle.opponent_pokemon.front_image, (325, 40))

    def draw_player_pokemon(self, surface: pygame.Surface) -> None:
        self.need_to_draw_player_pokemon = True
        for anim in self.anim_manager.animation_queue:
            if isinstance(anim, animation.PlayerPokemonEnterBattle) or isinstance(anim, animation.OpponentPokemonFaint):
                self.need_to_draw_player_pokemon = False
        if self.need_to_draw_player_pokemon:
            if self.battle.player_trainer.get_current_pokemon() == None :

            surface.blit(pygame.transform.scale(self.battle.player_trainer.get_current_pokemon().back_image,
                                                (int(1.5*self.battle.player_pokemon.back_image.get_width()), int(1.5*self.battle.player_trainer.get_current_pokemon().back_image.get_height())))
                         , (60, 120))
