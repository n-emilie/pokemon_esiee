import pokemon
import pandas as pd
import os
import inspect
from ability import loadmoves
from typing import List

ALL_TRAINERS: dict[str: 'Trainer'] = {}

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
f = pd.read_csv(os.path.join(scriptDIR, 'data/trainers.csv'), ';')

# this class represent a pokemon trainer
class Trainer:

    def __init__(self, name: str, poke: List[pokemon.Pokemon], message: str) -> None:
        self.name = name
        if len(poke) <= 6:
            self.pokemon_list = poke
        else:
            self.pokemon_list = []
        self.message = message

    def add_pokemon(self, poke: pokemon.Pokemon) -> bool:
        if len(self.pokemon_list) >= 6:
            return False
        else:
            self.pokemon_list.append(poke)
            return True

    def get_current_pokemon(self) -> pokemon.Pokemon:
        poke = None
        for pokemon in self.pokemon_list:
            if not pokemon.is_fainted():
                poke = pokemon
                break
        return poke
    def get_pokemon_list_size(self) -> int:
        return len(self.pokemon_list)

    def get_pokemon_string(self) -> str:
        returnable = ""
        en_vie = []
        fainted = []
        for pokemon in self.pokemon_list:
            if pokemon.is_fainted():
                fainted.append(pokemon)
            else:
                en_vie.append(pokemon)
        for poke in en_vie:
            returnable += " " + poke.name
        for poke in fainted:
            returnable += " " +poke.name + " (K.O)"
        return returnable


    def reset(self):
        for pokemon in self.pokemon_list:
            pokemon.reset_stats()


def load_trainer():
    file = open(os.path.join(scriptDIR,"trainer.py"),'a')
    for i in range(0, 41):
        t = f.loc[i]
        poke: List[pokemon.Pokemon] = []
        # les pokemons
        recup: str = t[3]
        recup: List = recup.split(',', 6)
        for k in recup:
            poke.append(pokemon.get_new_poke(pokemon.get_poke_id(f'{k}')))
        # print(poke)
        #level
        lvl: str = t[4]
        lvl: List[int] = lvl.split(',', len(poke))
        # les compétences
        for p in range(0, len(poke)):
            # print(poke[p].name)
            # print(t[5+p])
            recup: str = t[5 + p]
            recup: List[str] = recup.split(',', 4)
            poke[p].level = lvl[p]

            for m in recup:
                poke[p].learn(m)
                # print(m)
        trainer = Trainer(t[1],poke,t[2])
        ALL_TRAINERS[f"{t[0]}"] = trainer
    # print(ALL_TRAINERS)

def get_trainer(name : str):
    return ALL_TRAINERS[name]



# loadmoves.loadmoves()
# pokemon.Pokemon.load_pokemons()
# load_trainer()

