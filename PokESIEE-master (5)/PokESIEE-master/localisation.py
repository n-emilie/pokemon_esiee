from warp import Warp


class Localisation:

    def __init__(self, warp, map, name):
        self.exit = {}
        self.warp = warp
        self.map = map
        self.name = name

    def set_exit(self, direction, voisin: object) -> None:
        self.exit[direction] = voisin

    def get_exit(self, option) -> None:
        return self.exit[option]


class Localisations:

    def __init__(self, game):
        self.game = game
        self.create()

    def create(self):
        warp_foret = {'South': (16, 37), 'North': (15, 6)}
        warp_ville_1 = {'North': (20, 10), 'Up': (17, 27), 'Up1': (15, 17)}
        warp_ville_2 = {'North': (20, 6), 'South': (21, 33), 'West': (6, 17), 'East': (33, 22)}
        warp_ville_3 = {'East': (50, 15)}
        warp_ville_4 = {"West": (7, 16)}
        warp_ville_5 = {"South": (32, 40)}
        warp_route1 = {"North": (17, 6), "South": (19, 54)}
        warp_route_2 = {'North': (10, 5), 'East': (42, 13)}
        warp_route3 = {'South': (72, 12), 'West': (5, 8)}
        warp_route_5 = {"North": (35, 11), "South": (24, 57)}
        warp_desert = {"West": (7, 9), 'East': (30, 135)}
        warp_grotte2 = {"North": (4, 1), "South": (8, 28)}
        warp_grotte3 = {"North": (4, 1), "South": (27, 16)}

        warp_labo = {'Down': (7, 11)}
        warp_maison_depart = {'Down1': (3, 6)}


        # create all the different localisation and set the relation between another
        VILLE1 = Localisation(warp_ville_1, self.game.maps['ville_1'], "Bourg-en-vol")
        VILLE2 = Localisation(warp_ville_2, self.game.maps['ville_2'], 'ville_2')
        VILLE3 = Localisation(warp_ville_3, self.game.maps['ville_3'], 'ville_3')
        VILLE4 = Localisation(warp_ville_4, self.game.maps['ville_4'], 'ville_4')
        VILLE5 = Localisation(warp_ville_5, self.game.maps['ville_5'], 'ville_5')

        ROUTE1 = Localisation(warp_route1, self.game.maps['route_1'], 'route1')
        ROUTE2 = Localisation(warp_route_2, self.game.maps['route_2'], "route_2")
        ROUTE3 = Localisation(warp_route3, self.game.maps['route_3'], 'route3')
        ROUTE5 = Localisation(warp_route_5, self.game.maps['route_5'], 'route5')

        FORET = Localisation(warp_foret, self.game.maps['foret'], "foret_maudite")
        DESERT = Localisation(warp_desert, self.game.maps['desert'], "Desert Delassant")
        GROTTE2 = Localisation(warp_grotte2, self.game.maps['grotte_2'], "Grotte_2")
        GROTTE3 = Localisation(warp_grotte3, self.game.maps['grotte_3'], "grotte3")

        LABO = Localisation(warp_labo, self.game.maps['labo'], "labo")
        MAISON_DEPART = Localisation(warp_maison_depart, self.game.maps['maison_depart'], "maison_depart")


        VILLE1.set_exit('North', ROUTE1)
        VILLE1.set_exit('Up', LABO)
        VILLE1.set_exit('Up1', MAISON_DEPART)

        MAISON_DEPART.set_exit('Down1', VILLE1)

        LABO.set_exit('Down', VILLE1)

        ROUTE1.set_exit('South', VILLE1)
        ROUTE1.set_exit('North', VILLE2)

        VILLE2.set_exit('South', ROUTE1)
        VILLE2.set_exit('West', ROUTE2)
        VILLE2.set_exit('East', DESERT)
        VILLE2.set_exit('North', ROUTE5)

        ROUTE2.set_exit('East', VILLE2)
        ROUTE2.set_exit('North', FORET)

        FORET.set_exit('South', ROUTE2)
        FORET.set_exit('North', ROUTE3)

        VILLE3.set_exit('East', ROUTE3)

        ROUTE3.set_exit('South', FORET)
        ROUTE3.set_exit('West', VILLE3)

        DESERT.set_exit('West', VILLE2)
        DESERT.set_exit('East', VILLE4)

        ROUTE5.set_exit('South', VILLE2)
        ROUTE5.set_exit('North', GROTTE2)

        GROTTE2.set_exit('South', ROUTE5)
        GROTTE2.set_exit('North', GROTTE3)

        GROTTE3.set_exit('South', GROTTE2)
        GROTTE3.set_exit('North', VILLE5)

        VILLE4.set_exit('West', DESERT)
        VILLE5.set_exit('South', GROTTE3)

        self.game.localisation_list['route_1'] = ROUTE1
        self.game.localisation_list['route_2'] = ROUTE2
        self.game.localisation_list['route_3'] = ROUTE3
        self.game.localisation_list['route_5'] = ROUTE5
        self.game.localisation_list['ville_1'] = VILLE1
        self.game.localisation_list['ville_2'] = VILLE2
        self.game.localisation_list['ville_3'] = VILLE3
        self.game.localisation_list['ville_4'] = VILLE4
        self.game.localisation_list['ville_5'] = VILLE5
        self.game.localisation_list['foret'] = FORET
        self.game.localisation_list['desert'] = DESERT
        self.game.localisation_list['grotte_2'] = GROTTE2
        self.game.localisation_list['grotte_3'] = GROTTE3




















