import copy

import networkx as nx

from database.dao import DAO
from geopy import distance

class Model:
    def __init__(self):
        self.state = None
        self.G = nx.Graph()
        self.pesi = None
        self.vicini = None

        self.years = None
        self.shapes = None

        #ricorsione
        self.sol_ottimale = []
        self.sol_ottimale_archi = []
        self.d_max = []
        self.peso_max = []

    def build_graph(self,year,shape):
        self.G.clear()
        self.state = DAO.read_all_states()

        self.G.add_nodes_from(self.state.values())

        self.pesi = DAO.read_all_avvistamenti()
        self.vicini = DAO.read_all_negh()

        for id_stato in self.state:
            stato = self.state[id_stato]

            if stato.neighbors:
                neigh = stato.neighbors.split(' ')
                for id_stato2 in neigh:
                    if id_stato2 in self.state:
                        stato2 = self.state[id_stato2]
                        peso_tot = 0
                        if (id_stato,year,shape) in self.pesi:
                            peso_tot += self.pesi[(id_stato,year,shape)]
                        if (id_stato2,year,shape) in self.pesi:
                            peso_tot += self.pesi[(id_stato2,year,shape)]

                        if sorted((id_stato,id_stato2)) in self.vicini:
                            self.G.add_edge(stato,stato2, weight = peso_tot)




    def get_all_years(self):
        self.years = DAO.read_all_years()
        return self.years

    def get_all_shapes(self):
        self.shapes = DAO.read_all_shapes()
        return self.shapes

    def pesi_adiacenti(self):
        risultato = {}
        for nodo in self.G.nodes():

            adiacenti = self.G[nodo]


            peso_tot = 0
            if adiacenti:
                for adiacente in adiacenti:
                    peso_tot += self.G[nodo][adiacente]['weight']
            risultato[nodo.id] = peso_tot
        return  risultato

    def ricerca_percorso_max(self):


        for nodo in self.G.nodes():
            parziale = [nodo]
            self.ricorsione(parziale,[],[],[])

        return self.sol_ottimale_archi, self.d_max,self.peso_max



    def ricorsione(self,sol_corrente,archi,d,peso):

        ultimo = sol_corrente[-1]
        vicini_amissibili = self.vicini_amissibili(ultimo, archi,sol_corrente)
        if len(vicini_amissibili) == 0:
            if  sum(d)>sum(self.d_max):
                self._sol_ottimale = copy.deepcopy(sol_corrente)
                self.sol_ottimale_archi = copy.deepcopy(archi)
                self.d_max = copy.deepcopy(d)
                self.peso_max = copy.deepcopy(peso)



        for vicino in vicini_amissibili:
            sol_corrente.append(vicino)
            archi.append((ultimo,vicino))
            peso.append(self.G[vicino][ultimo]['weight'])
            (lat1,lng1) = (ultimo.lat,ultimo.lng)
            (lat2,lng2) = (vicino.lat,vicino.lng)
            d.append(distance.geodesic((lat1, lng1), (lat2, lng2)).km)

            self.ricorsione(sol_corrente,archi,d,peso)
            sol_corrente.pop()
            peso.pop()
            d.pop()
            archi.pop()

    def vicini_amissibili(self,nodo,archi, sol_corrente):
        neigh = self.G.neighbors(nodo)
        result = []
        for vicino in neigh:
            if archi:
                if self.G[nodo][vicino]['weight'] > self.G[archi[-1][0]][archi[-1][1]]['weight'] and vicino not in sol_corrente:
                    result.append(vicino)
            else:
                result.append(vicino)
        return result









