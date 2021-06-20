import pygame
import os
import pokemon
import config
import spritesheet
import trainer


class BattleHud:

    def __init__(self, trainer_pokemon: pokemon.Pokemon, opponent_pokemon: pokemon.Pokemon) -> None:

        self.sprite = pygame.image.load((os.path.join(config.image, "misc_sprite/hud_battle_each_pokemon.png")))
        self.opponent_hud = pygame.transform.scale(spritesheet.pick_image(self.sprite, 0, 0, 140, 45), (int(1.9 * 140), int(1.9 * 45)))
        self.player_hud = pygame.transform.scale(spritesheet.pick_image(self.sprite, 0, 45, 140, 45), (int(1.9 * 140), int(1.9 * 45)))
        self.color_bar_green = spritesheet.pick_image(self.sprite, 56, 187, 4, 1)
        self.color_bar_orange = spritesheet.pick_image(self.sprite, 56 + 4, 187, 1, 3)
        self.color_bar_red = spritesheet.pick_image(self.sprite, 56 + 4 + 4, 187, 1, 3)

        self.player_pokemon = trainer_pokemon
        self.opponent_pokemon = opponent_pokemon

        self.hp_bar_render_width_player = (96 * self.player_pokemon.health) / self.player_pokemon.health_max
        self.hp_bar_render_width_opponent = (96 * self.opponent_pokemon.health) / self.opponent_pokemon.health_max

        self.need_to_update_player_hp_bar = True
        self.need_to_update_opponent_hp_bar = True

        self.right_color_opponent = self.color_bar_green
        self.right_color_player = self.color_bar_green

        # font
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join(config.font, "game_font.ttf"), 12)

    def draw_hud(self, surface: pygame.Surface) -> None:
        surface.blit(self.player_hud, (0 + self.player_hud.get_width() - 45, int(1.35*self.player_hud.get_height())))
        surface.blit(self.opponent_hud, (-20, 10))

    def draw_player_hp_bar(self, surface: pygame.Surface) -> None:
        current_surface_hp_bar_player = pygame.transform.scale(self.right_color_player,
                                                                    (int(self.hp_bar_render_width_player), 3))
        surface.blit(current_surface_hp_bar_player, (375, 164))

    def draw_opponent_hp_bar(self, surface: pygame.Surface) -> None:
        current_surface_hp_bar_opponent = pygame.transform.scale(self.right_color_opponent,
                                                                      (int(self.hp_bar_render_width_opponent), 3))
        surface.blit(current_surface_hp_bar_opponent, (93, 75))

    def update_pokemon(self, trainer_pokemon: pokemon.Pokemon, opponent_pokemon: pokemon.Pokemon):
        self.player_pokemon = trainer_pokemon
        self.opponent_pokemon = opponent_pokemon

    def draw(self, surface: pygame.Surface) -> None:
        self.draw_hud(surface)
        self.draw_opponent_hp_bar(surface)
        self.draw_player_hp_bar(surface)
        self.draw_font(surface)

    def update(self, player_pokemon: pokemon.Pokemon, opponent_pokemon: pokemon.Pokemon):

        if self.need_to_update_player_hp_bar:
            self.hp_bar_render_width_player = (96 * self.player_pokemon.health) / self.player_pokemon.health_max

        if self.need_to_update_opponent_hp_bar:
            self.hp_bar_render_width_opponent = (96 * self.opponent_pokemon.health) / self.opponent_pokemon.health_max

        if self.hp_bar_render_width_player < 0:
            self.hp_bar_render_width_player = 0
        if self.hp_bar_render_width_opponent < 0:
            self.hp_bar_render_width_opponent = 0

        if self.player_pokemon.health <= (1/5 * self.player_pokemon.health_max):
            self.right_color_player = self.color_bar_red
        elif self.player_pokemon.health <= 1/3 + 1/5 * self.player_pokemon.health_max:
            self.right_color_player = self.color_bar_orange
        else:
            self.right_color_player = self.color_bar_green

        if self.opponent_pokemon.health <= (1/5 * self.opponent_pokemon.health_max):
            self.right_color_opponent = self.color_bar_red
        elif self.opponent_pokemon.health <= 1/3 + 1/5 * self.opponent_pokemon.health_max:
            self.right_color_opponent = self.color_bar_orange
        else:
            self.right_color_opponent = self.color_bar_green

        self.update_pokemon(player_pokemon, opponent_pokemon)



    def render_player_exp_level(self) -> pygame.Surface:
        return self.font.render(str(self.player_pokemon.level), False, (0, 0, 0))

    def render_opponent_exp_lvl(self) -> pygame.Surface:
        return self.font.render(str(self.opponent_pokemon.level), False, (0, 0, 0))

    def render_opponent_name(self) -> pygame.Surface:
        return self.font.render(self.opponent_pokemon.name, False, (0, 0, 0))

    def render_player_name(self) -> pygame.Surface:
        return self.font.render(self.player_pokemon.name, False, (0, 0, 0))

    def render_player_max_health(self) -> pygame.Surface:
        return self.font.render(str(int(self.player_pokemon.health_max)), False, (0, 0, 0))

    def render_player_current_health(self) -> pygame.Surface:
        return self.font.render(str(int(self.player_pokemon.health)), False, (0, 0, 0))


    def draw_font(self, surface) -> None:
        player_level_surface = self.render_player_exp_level()
        opponent_level_surface = self.render_opponent_exp_lvl()
        player_name = self.render_player_name()
        opponent_name = self.render_opponent_name()
        player_max_health = self.render_player_max_health()
        player_current_health = self.render_player_current_health()
        surface.blit(player_name, ((self.player_hud.get_width() + 40), int(1.62*self.player_hud.get_height())))
        surface.blit(opponent_name, (45, 49))
        surface.blit(player_level_surface, (0 + self.player_hud.get_width() + 172, int(1.62*self.player_hud.get_height())))
        surface.blit(opponent_level_surface, (157, 48))
        surface.blit(player_current_health, ((self.player_hud.get_width() + 105), int(2.05*self.player_hud.get_height())))
        surface.blit(player_max_health, ((self.player_hud.get_width() + 155), int(2.05*self.player_hud.get_height())))


