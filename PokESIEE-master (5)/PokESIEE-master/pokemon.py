import json
import os
from copy import deepcopy
from typing import Optional, Dict, List, Any

import pygame

import config
import spritesheet
from ability import move, loadmoves
from element import TYPES, Type
from entity import Entity
from utils import get_args
import random

poke_dos = Entity(2976, 2016, 'spritesheet/poke_dos.png')
poke_face = Entity(2976, 2016, 'spritesheet/poke_face.png')

ID_LIST: List[int] = [4, 5, 6, 252, 253, 254, 393, 394, 395, 16, 17, 18, 25, 26, 19, 20, 261, 262, 143, 29, 30, 31, 32,
                      33, 34, 58, 59, 43, 44, 45,
                      231, 232, 403, 404, 405, 276, 277, 532, 533, 534, 92, 93, 94, 200, 429, 406, 315, 407, 543, 544,
                      545, 355, 356, 477, 198,
                      430, 451, 452, 228, 229, 246, 247, 248, 442, 607, 608, 609, 396, 397, 398, 309, 310, 624, 625,
                      626, 287, 288, 289, 179,
                      180, 181, 27, 28, 111, 112, 464, 304, 305, 306, 529, 530, 551, 552, 553, 322, 323, 449, 450, 115,
                      344, 350, 437, 589, 617,
                      614, 473, 362, 76, 472
                      ]

NB_POKEMON: int = 626
POKEMONS: List[Optional['Pokemon']] = [None for i in range(NB_POKEMON + 1)]


# retourne instance du pokemon correspondant a l ID POKEDEX
def get_poke(num_id: int):
     return POKEMONS[num_id]



# retourne l'index correspondant au nom du pokemon ou 0 s'il est introuvable
def get_poke_id(name: str):
    for poke in POKEMONS:
        if poke != None:
            if poke.name == name:
                return POKEMONS.index(poke)
    return 0

def get_new_poke(poke_id : int):
    id_str = to_3_digit(poke_id)
    try:
        with open(os.path.join(config.scriptDIR, f"pokemon/{id_str}.json"), "r", encoding='utf-8') as file:
            data = json.load(file)
            return Pokemon(poke_id, data)
    except FileNotFoundError:
        print(f'pokemon id : {poke_id}, not found')

def get_moves(dictio: dict):
    vkeys = dictio.keys()
    mydict: dict[move.Move: int] = {}
    for k in vkeys:
        mydict[loadmoves.get_Move(k)] = dictio[k]
    return mydict


def to_3_digit(num: int) -> str:
    if num < 10:
        return "00" + str(num)
    if num < 100:
        return "0" + str(num)
    return str(num)


class Pokemon(Entity):

    def __init__(self, id: int, data: Dict[str, Any], ):
        super(Pokemon, self).__init__(96, 96, 'misc_sprite/empty.png')
        self.name: str = get_args(data, "name", id)
        self.id: int = id
        self.level: int = get_args(data, "level", id)
        self.exp: int = 0
        self.exp_max: int = self.level ** 3
        self.exp_points: int = get_args(data, "exp_points", id)
        self.types: List[Type] = [TYPES[t] for t in get_args(data, "type", id)]
        self.base_health: int = get_args(data, "base_health", id)
        self.health: int = int((2 * self.base_health * self.level) / 100 + self.level + 10)
        self.health_max: int = self.health

        self.base_attack: int = get_args(data, "stats", id)["attack"]
        self.base_defense: int = get_args(data, "stats", id)["defense"]
        self.base_attack_spe: int = get_args(data, "stats", id)["attack_spe"]
        self.base_defense_spe: int = get_args(data, "stats", id)["defense_spe"]
        self.base_speed: int = get_args(data, "stats", id)["speed"]

        self.attack = self.base_attack
        self.defense = self.base_defense
        self.attack_spe = self.base_attack_spe
        self.defense_spe = self.base_defense_spe
        self.speed = self.base_speed

        self.all_moves: Dict[move.Move: int] = get_moves(get_args(data, "ability", id))
        self.moves = []
        self.front_image = spritesheet.pick_image(poke_face.image, (((id - 1) % 31) * 96), int((id -1) / 31) * 96,
                                                  self.width, self.height)
        self.back_image = spritesheet.pick_image(poke_dos.image, (((id - 1) % 31) * 96), int((id -1) / 31) * 96, self.width,
                                                 self.height)
        self.evolution: List[Optional[int]] = get_args(data, "evolution", id)
        self.status: Optional[Effect] = None
        self.calc_health_max()
        self.calc_good_stat_per_level()



    # methode pour les calcul d'evolution etc
    def calc_exp_max(self) -> None:  # calcul de l'exp max (formule de progression moyenne choisie)
        self.exp_max = self.level ** 3

    # calcul des PV sans tenir compte des EV et IV
    def calc_health_max(self) -> None:
        self.health_max = (2 * self.base_health * self.level) / 100 + self.level + 10
        self.health = self.health_max

    def calc_good_stat_per_level(self) -> None:
        self.attack = (2 * self.base_attack * self.level) / 100 + self.level + 5
        self.attack_spe = (2 * self.base_attack_spe * self.level) / 100 + self.level + 5
        self.defense = (2 * self.base_defense * self.level) / 100 + self.level + 5
        self.defense_spe = (2 * self.base_defense_spe * self.level) / 100 + self.level + 5
        self.speed = (2 * self.base_speed * self.level) / 100 + self.level + 5

    # test si le pokemon possède une evolution
    def has_evolve(self) -> bool:
        if len(self.evolution) == 0:
            return False
        else:
            return True

    def get_name(self) -> str:
        return self.name

    # test si le pokemon peut evoluer
    def can_evolve(self) -> bool:
        if not self.has_evolve() or self.evolution[1] > self.level:
            return False
        return True

    # fait evoluer un pokemon s'il possède une évolutione t qu'il a le niveau requis
    def evolve(self) -> None:
        if self.can_evolve():
            evol_poke: Pokemon = POKEMONS[self.evolution[0]]
            moves = self.moves
            self = evol_poke
            self.moves = moves

    def can_up(self) -> bool:
        return self.exp >= self.exp_max

    def get_move_index(self, index: int) -> move.Move:
        return self.moves[index]

    def get_move_with_name(self, name: str) -> move.Move:
        for vMove in self.moves:
            if vMove is not None:
                if vMove.name == name:
                    return vMove

    # augmente le niv d'un pokemon
    def level_up(self) -> None:
        if self.can_up():
            self.level += 1
            self.exp = self.exp - self.exp_max
            self.calc_exp_max()
            self.calc_health_max()
            self.calc_good_stat_per_level()

    # ajoute l'exp à un pokemon s'i ln'est pas mort et que le pokemon en param est bien KO
    def add_exp(self, ennemies: Optional['Pokemon']) -> None:
        self.exp += ennemies.exp_points * (int(ennemies.level) / 7)

    # automatisation fin de combat pour un pokemon si manque de temps
    def auto_fight_end(self, ennemies: Optional['Pokemon']):
        if self.health > 0:
            self.add_exp(ennemies)
            if self.can_up(): self.level_up()
            if self.can_evolve(): self.evolve()

    def reset_stats(self) -> None:
        poke = POKEMONS[self.id]
        self.attack = poke.attack
        self.attack_spe = poke.attack_spe
        self.defense = poke.defense
        self.defense_spe = poke.defense_spe
        self.speed = poke.speed
        self.health = self.health_max

    def can_learn(self, move_name: str) -> bool:
        vMove: move.Move = loadmoves.get_Move(move_name)
        if vMove not in self.all_moves:
            return False
        else:
            return int(self.level) >= self.all_moves[vMove]

    def can_learn_move(self, ability: move.Move) -> bool:
        if ability not in self.all_moves:
            return False
        else:
            return int(self.level) >= self.all_moves[ability]

    def learn(self, move_name: str):
        if self.can_learn(move_name):
            self.moves.append(loadmoves.get_Move(move_name))
            del self.all_moves[loadmoves.get_Move(move_name)]

    def learn_move(self, move: move.Move):
        if self.can_learn_move(move):
            self.moves.append(move)
            del self.all_moves[move]

    # retourne un boolean True si la ocmpétence à été supprimé sinon False
    def forget(self, index) -> bool:
        if self.moves[index] is None:
            return False
        else:
            del self.moves[index]
            return True

    def auto_learn(self):
        learnable = []
        for k in self.all_moves:
            if self.can_learn_move(k):
                learnable.append(k)
        if len(learnable) < 4:
            for i in range(0, len(learnable)):
                self.learn_move(learnable[i])
        else:
            while len(self.moves) < 4:
                number = random.randint(0, len(learnable) - 1)
                self.learn_move((learnable[number]))
                del learnable[number]

    def multilearn(self, abilitys: List[str]):
        for skill in abilitys:
            self.learn(skill)

    def apply_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_fainted(self) -> bool:
        return self.health == 0

    @staticmethod
    def auto_learn_all():
        for i in range(0, len(ID_LIST)):
            poke_id: int = ID_LIST[i]
            POKEMONS[poke_id].auto_learn()

    @staticmethod
    def load_pokemons():
        global POKEMONS, NB_POKEMON
        for i in range(0, len(ID_LIST)):
            poke_id: int = ID_LIST[i]
            # print([(((poke_id-1) % 31)* 96), int(poke_id / 31) * 96 , poke_id])
            id_str = to_3_digit(poke_id)
            try:
                with open(os.path.join(config.scriptDIR, f"pokemon/{id_str}.json"), "r", encoding='utf-8') as file:
                    data = json.load(file)
                    POKEMONS[poke_id] = Pokemon(poke_id, data)
            except FileNotFoundError:
                print(f'pokemon id : {poke_id}, not found')
                break
        # while POKEMONS[-1] is None:
        #      del POKEMONS[-1]
        NB_POKEMON = len(POKEMONS) - 1


# IMAGE = pygame.image.load(os.path.join(config.spritesheet, "effects.png"))
#
#
# class Effect:
#     def __init__(self, image_y, damage: int, counter: List[str]):
#         self.image = spritesheet.pick_image(IMAGE, 0, image_y * 60, 116, 50)
#         self.damage = damage
#         self.counter_types: List[Type] = [TYPES[t] for t in counter]
#
#     # need to apply the effect by using for example Burn().apply(salameche)
#     def apply(self, poke: Pokemon):
#         pass
#
#     # get the effect of the status for each turn
#     def get_effect(self, poke: Pokemon):
#         pass
#
#     # stop the effect on the pokemon
#     def stop_effect(self, poke: Pokemon):
#         pass
#
#
# class Burn(Effect):
#     def __init__(self):
#         super.__init__(0, int(1 / 16), ["FIRE"])
#
#     def apply(self, poke: Pokemon):
#         if self.counter_types[0] not in poke.types:
#             poke.attack /= 2
#             poke.health -= poke.health_max / 16
#
#     def get_effect(self, poke: Pokemon):
#         poke.health -= poke.health_max / 16
#
#
# class Freeze(Effect):
#     def __init__(self):
#         super.__init__(1, 0, ["ICE"])
#         self.memory_moves: List[move.AbstractMove] = []
#
#     def apply(self, poke: Pokemon):
#         if self.counter_types[0] not in poke.types:
#             self.memory_moves = poke.moves
#             poke.moves = []

    # def get_effect(self, poke: Pokemon):

# Pokemon.load_pokemons()
# poketest = get_poke(4)
# done = False
# screenWidth = 100
# screenHeight = 100
# screen = pygame.display.set_mode((screenWidth, screenHeight))
# clock = pygame.time.Clock()
# pygame.display.set_caption("My Game")
#
# while not done:
#    event = pygame.event.Event(pygame.USEREVENT)  # Remise à zero de la variable event
#
#      # récupère la liste des touches claviers appuyeées sous la forme liste bool
#    pygame.event.pump()
#
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            done = True
#    screen.blit(poketest.front_image, (0, 0))
#    pygame.display.flip()
#
#     # Limit frames per second
#    clock.tick(30)
#
# # Close the window and quit.
# pygame.quit()
