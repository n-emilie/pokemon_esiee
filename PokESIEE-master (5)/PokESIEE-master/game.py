import pygame
import localisation
import warp
from battle import Battle
import config
import pokemon
import trainer
from draw_area import DrawArea
from player import Player
from game_map import GameMap
from direction import Directions as dir
from animation import ScreenAnimationManager
from pokemon import Pokemon
from ability import loadmoves
from copy import deepcopy

class Game:

    # game constructor
    def __init__(self, screen) -> None:
        # load all pokemon in the game
        loadmoves.loadmoves()
        Pokemon.load_pokemons()
        trainer.load_trainer()
        # red variable
        self.screen = screen
        # create the area that gonna be drawn
        self.draw_area = DrawArea(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        player_premier_pokemon = pokemon.get_new_poke(4)
        player_deuxieme_pokemon = pokemon.get_new_poke(25)
        player_premier_pokemon.level = 5
        player_deuxieme_pokemon.level = 5
        player_premier_pokemon.multilearn(['griffe','rugissement'])
        player_deuxieme_pokemon.multilearn(['eclair','double_pied'])
        temp_poke_list = []
        temp_poke_list.append(player_premier_pokemon)
        temp_poke_list.append(player_deuxieme_pokemon)
        self.player_trainer = trainer.Trainer('Player', temp_poke_list, '')
        # print(player_premier_pokemon.all_moves)
        # print(player_premier_pokemon.moves)
        Pokemon.auto_learn_all()

        self.player_save = []

        self.animation_manager = ScreenAnimationManager()
        # dictionary containing all the gameMap
        self.maps = {}
        self.load_map()
        self.localisation_list = {}
        self.localisations_objet = localisation.Localisations(self)
        self.current_localisation = self.localisation_list['ville_1']
        self.next_localisation = localisation.Localisation({}, {}, "test")
        self.current_state = config.GAME_STATE_EXPLORATION
        self.next_state = config.GAME_STATE_EXPLORATION
        self.current_battle = Battle
        self.player = Player(self.draw_area, self)
        self.player_save.append((self.player.current_tile_x, self.player.current_tile_y))
        self.current_localisation.map.map_objects.append(self.player)
        self.option = ''

    def load_map(self):

        pokemon_list = {'route_1': [
            pokemon.get_poke(16),
            pokemon.get_poke(19),
            pokemon.get_poke(25),
            pokemon.get_poke(261),
        ], 'route_2': [
            pokemon.get_poke(58),
            pokemon.get_poke(43),
            pokemon.get_poke(231),
            pokemon.get_poke(29),
            pokemon.get_poke(32),
            pokemon.get_poke(403),
            pokemon.get_poke(276),
            pokemon.get_poke(532)
        ], 'route_3': [
            pokemon.get_poke(246),
            pokemon.get_poke(309),
            pokemon.get_poke(624),
            pokemon.get_poke(626),
            pokemon.get_poke(396),
            pokemon.get_poke(287),
            pokemon.get_poke(179)
        ], 'route_5': [
            pokemon.get_poke(350),
            pokemon.get_poke(437),
            pokemon.get_poke(589),
            pokemon.get_poke(617)
        ], 'desert': [
            pokemon.get_poke(27),
            pokemon.get_poke(111),
            pokemon.get_poke(304),
            pokemon.get_poke(529),
            pokemon.get_poke(551)
        ], 'foret': [
            pokemon.get_poke(92),
            pokemon.get_poke(200),
            pokemon.get_poke(406),
            pokemon.get_poke(543),
            pokemon.get_poke(355),
            pokemon.get_poke(198),
            pokemon.get_poke(451),
        ], 'grotte_2': [
            pokemon.get_poke(614),
            pokemon.get_poke(473),
            pokemon.get_poke(362),
            pokemon.get_poke(76),
            pokemon.get_poke(472)
        ], 'grotte_3': [
            pokemon.get_poke(614),
            pokemon.get_poke(473),
            pokemon.get_poke(362),
            pokemon.get_poke(76),
            pokemon.get_poke(472)
        ]}

        trainers_list = {'route_1': [
            trainer.get_trainer("gamin_farouk"),
            trainer.get_trainer("marin_francois"),
            trainer.get_trainer("jumelle_anne"),
            trainer.get_trainer("jumelle_frank")
        ], 'route_2': [
            trainer.get_trainer("gamin_titouan"),
            trainer.get_trainer("fillette_amelie"),
            trainer.get_trainer("scout_antonin"),
            trainer.get_trainer("fillette_zoe"),
            trainer.get_trainer("gamin_theo")
        ], 'foret': [
            trainer.get_trainer("scout_maxence"),
            trainer.get_trainer("mysti_gertrude"),
            trainer.get_trainer("combat_alexandre"),
            trainer.get_trainer("fillette_anna"),
            trainer.get_trainer("scout_noe")
        ], 'manoir': [
            trainer.get_trainer("homme_etrange")
        ], 'route_3': [
            trainer.get_trainer("ornitho_pierre"),
            trainer.get_trainer("motard_louis"),
            trainer.get_trainer("pecheur_JP"),
            trainer.get_trainer("bandit_arthur")
        ], 'desert': [
            trainer.get_trainer("mont_gilbert"),
            trainer.get_trainer("top_hitomi"),
            trainer.get_trainer("scout_timothe"),
            trainer.get_trainer("mont_jhon")
        ], 'route_4': [
            trainer.get_trainer("mont_matthias"),
            trainer.get_trainer("top_nicholas"),
            trainer.get_trainer("fillette_lucie"),
            trainer.get_trainer("gamin_jordan"),
            trainer.get_trainer("mysti_jeanne")
        ], 'route_5': [
            trainer.get_trainer("top_alain"),
            trainer.get_trainer("combat_arnaud"),
            trainer.get_trainer("gamin_guillaume"),
            trainer.get_trainer("gentleman_pierrot"),
        ], 'grotte_2': [
            trainer.get_trainer("mont_jack"),
            trainer.get_trainer("fillette_aurore"),
            trainer.get_trainer("gamin_florian"),
            trainer.get_trainer("bandit_hugo"),
            trainer.get_trainer("mont_charlie")

        ], 'grotte_3': [
            trainer.get_trainer("mont_jack"),
            trainer.get_trainer("fillette_aurore"),
            trainer.get_trainer("gamin_florian"),
            trainer.get_trainer("bandit_hugo"),
            trainer.get_trainer("mont_charlie")

        ], 'route_6': [
            trainer.get_trainer("scout_alban"),
            trainer.get_trainer("mysti_laure"),
            trainer.get_trainer("top_bastian"),
        ]}

        localisation_name = ['route_1',
                             'route_2',
                             'route_3',
                             'route_5',
                             'ville_1',
                             'ville_2',
                             'ville_3',
                             'ville_4',
                             'ville_5',
                             'desert',
                             'foret',
                             'grotte_2',
                             'grotte_3',
                             'labo',
                             'maison_depart'
                             ]
        localisation_size = [(880, 1760),
                             (800, 320),
                             (1281, 321),
                             (880, 1120),
                             (640, 640),
                             (640, 640),
                             (960, 640),
                             (1280, 640),
                             (1520, 800),
                             (640, 2244),
                             (768, 704),
                             (272, 528),
                             (512, 416),
                             (208, 208),
                             (176, 128)
                             ]

        for i in range(0, len(localisation_name)):
            fichier_text = localisation_name[i] + ".txt"
            fichier_image = "map_image/" + localisation_name[i] + ".png"
            name = localisation_name[i]

            if not name[0] == 'r':
                temp_trainer_list = []
            else:
                temp_trainer_list = trainers_list[localisation_name[i]]

            # if the localisation is a city, there is no pokemon
            if name[0] == 'v' or name[0] == 'l' or name[0] == 'm':
                temp_pokemon_list = []
            else:
                temp_pokemon_list = pokemon_list[localisation_name[i]]

            try:
                self.maps[localisation_name[i]] = GameMap(localisation_size[i][0], localisation_size[i][1],
                                                          fichier_image,
                                                          fichier_text, temp_pokemon_list, localisation_name[i], self, temp_trainer_list)
                self.maps[localisation_name[i]].load_map_array()
            except FileNotFoundError:
                print(fichier_image)

    # update class method
    def update(self) -> None:

        #deplacement
        self.handle_event()

        if self.current_state == config.GAME_STATE_EXPLORATION:
            for map_objects in self.current_localisation.map.map_objects:
                map_objects.update()

        elif self.current_state == config.GAME_STATE_BATTLE:
            if not self.current_battle.has_been_loaded():
                self.current_battle.begin()
            else:
                self.current_battle.update()

        if self.animation_manager.have_animation():
            if self.animation_manager.get_current_animation().isFinished:
                self.animation_manager.pop_current_animation()
                self.update_state()
        else:
            self.update_state()

    # update the current map to the next map
    def update_map(self):
        self.current_localisation = self.next_localisation

    # update the current state to the next state
    def update_state(self):
        self.current_state = self.next_state

    # request a game state change
    def request_state_change(self, state):
        self.next_state = state

    # draw class method
    def draw(self) -> None:

        self.screen.fill((0, 0, 0))
        surface_to_draw = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

        if self.current_state == config.GAME_STATE_EXPLORATION:
            # fill the screen black
            self.current_localisation.map.draw(surface_to_draw, self.draw_area)
            for map_object in self.current_localisation.map.map_objects:
                map_object.draw(surface_to_draw)

        elif self.current_state == config.GAME_STATE_BATTLE:
            if self.current_battle.has_been_loaded():
                self.current_battle.draw(surface_to_draw)

        if self.animation_manager.have_animation():
            current_anim = self.animation_manager.get_current_animation()
            current_anim.update(surface_to_draw)
        self.screen.blit(surface_to_draw, (0, 0))

    def handle_event(self) -> None:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                config.MAIN_LOOP_DOWN = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n and self.player.current_mode == config.PLAYER_MODE_WALK:
                    self.player.next_mode = config.PLAYER_MODE_RUN

                if event.key == pygame.K_DOWN:
                    self.player.directionPressed[dir.SOUTH] = True
                if event.key == pygame.K_UP:
                    self.player.directionPressed[dir.NORTH] = True
                if event.key == pygame.K_LEFT:
                    self.player.directionPressed[dir.WEST] = True
                if event.key == pygame.K_RIGHT:
                    self.player.directionPressed[dir.EAST] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_n and self.player.current_mode == config.PLAYER_MODE_RUN:
                    self.player.next_mode = config.PLAYER_MODE_WALK
                if event.key == pygame.K_DOWN:
                    self.player.release_direction(dir.SOUTH)
                if event.key == pygame.K_UP:
                    self.player.release_direction(dir.NORTH)
                if event.key == pygame.K_LEFT:
                    self.player.release_direction(dir.WEST)
                if event.key == pygame.K_RIGHT:
                    self.player.release_direction(dir.EAST)

    def new_battle(self, battle):
        self.current_battle = battle

    def load_next_localisation(self):
        inverse_option = warp.find_opposite(self.option)
        print(warp.find_opposite(self.option))
        new_player_coordinate = self.next_localisation.warp[inverse_option]
        self.player_save.append(new_player_coordinate)
        self.player.change_current_tile(new_player_coordinate)
        self.player.update_coordinates()
        self.next_localisation.map.map_objects.append(self.player)
        self.player.game_map = self.next_localisation.map
        self.next_localisation.map.load_map_array()
        self.update_map()
        pygame.time.wait(100)

    def change_next_localisation(self):
        self.next_localisation = self.current_localisation.get_exit(self.option)
