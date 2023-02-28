import networkx as nx
import matplotlib.pyplot as plt

class Sommet:
    def __init__(self, id):
        self.id = id
        self.voisins = []
        self.visite = False
        self.pere = None
        self.distance = float('inf')
        
    def ajouter_voisin(self, v, p):
        if v not in self.voisins:
            self.voisins.append([v, p])
            
class Graphique:
    def __init__(self):
        self.G = nx.Graph()
        self.sommets = {}
        
    def afficher_graphique(self):
        pos = nx.layout.spring_layout(self.G)
        nx.draw_networkx(self.G, pos)
        labels = nx.get_edge_attributes(self.G, "weigth")
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        plt.show()
        
    def ajouter_sommet(self, id):
        if id not in self.sommets:
            self.sommets[id] = Sommet(id)
            
    def ajouter_arete(self, sommet_a, sommet_b, poids):
        if sommet_a in self.sommets and sommet_b in self.sommets:
            self.sommets[sommet_a].ajouter_voisin(sommet_b, poids)
            self.sommets[sommet_b].ajouter_voisin(sommet_a, poids)
            
            self.G.add_edge(sommet_a, sommet_b, weigth=poids)
            
    def obtenir_chemin(self, sommet_b):
        chemin = []
        encours = sommet_b
        while(encours != None):
            chemin.insert(0, encours)
            encours = self.sommets[encours].pere
        return [chemin, self.sommets[sommet_b].distance]
    
    def minimum(self, liste):
        if len(liste) > 0:
            m = self.sommets[liste[0]].distance
            v = liste[0]
            
            for e in liste:
                if m > self.sommets[e].distance:
                    m = self.sommets[e].distance
                    v = e
                    
            return v
        
    def dijkstra(self, sommet_a):
        if sommet_a in self.sommets:
            self.sommets[sommet_a].distance = 0
            encours = sommet_a
            non_visites = []
            
            # on ajoute tous a non visites
            for v in self.sommets:
                if v != sommet_a:
                    self.sommets[v].distance = float ('inf')
                self.sommets[v].pere = None
                non_visites.append(v)
                
            while(len(non_visites) > 0):
                #on evalue les sommets voisins et on prend le plus petit
                for voisin in self.sommets[encours].voisins:
                    if self.sommets[voisin[0]].visite == False:
                        if self.sommets[encours].distance + voisin[1] < self.sommets[voisin[0]].distance:
                            self.sommets[voisin[0]].distance = self.sommets[encours].distance + voisin[1]
                            self.sommets[voisin[0]].pere = encours
                        
                self.sommets[encours].visite = True
                non_visites.remove(encours)
                
                encours = self.minimum(non_visites)
        else:
            return False 
            
            
            
#exemple d'utilisation
if __name__ == '__main__':
    gr = Graphique()
    gr.ajouter_sommet('a')
    gr.ajouter_sommet('b')
    gr.ajouter_sommet('c')
    gr.ajouter_sommet('d')
    
    gr.ajouter_arete('a', 'b', 3)
    gr.ajouter_arete('a', 'c', 4)
    gr.ajouter_arete('b', 'd', 2)
    gr.ajouter_arete('c', 'd', 1)

        
    print("Le chemin plus rapide pour Dijkstra est: ")
    #node initial a
    gr.dijkstra('a') 
    #node final d
    print(gr.obtenir_chemin('d'))
    
    gr.afficher_graphique()
