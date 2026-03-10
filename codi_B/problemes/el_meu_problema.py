import random
from problemes.problema import ProblemaCercaLocal


class ElMeuProblema(ProblemaCercaLocal):
    """
    Problema d'optimització de formació d'equips de treball.
    
    Estat: vector binari de n elements on 1 indica persona seleccionada, 0 no seleccionada
    Objectiu: minimitzar el cost total considerant:
    - Cost individual de cada persona seleccionada
    - Penalització per incompatibilitats entre persones
    - Penalització per desviació respecte a la mida ideal de l'equip
    """
    
    def __init__(self, n, costs_unitaris, penal_parelles, nombre_ideal, alpha):
        """
        Inicialitza el problema.
        
        :param n: nombre de persones disponibles
        :param costs_unitaris: llista de costos individuals de cada persona
        :param penal_parelles: diccionari de penalitzacions per parelles incompatibles
                              format: {(i, j): penalitzacio}
        :param nombre_ideal: mida ideal de l'equip
        :param alpha: factor de ponderació per la desviació de mida
        """
        self.n = n
        self.costs_unitaris = costs_unitaris
        self.penal_parelles = penal_parelles
        self.nombre_ideal = nombre_ideal
        self.alpha = alpha
    
    def estat_inicial(self):
        """
        Genera un estat inicial amb totes les persones seleccionades.
        :return: vector binari de n elements (tots 1)
        """
        return [1] * self.n
    
    def veinat(self, estat):
        """
        Genera el vecindari d'un estat.
        El vecindari consisteix en tots els estats que es difereixen en exactament un bit
        (afegir o treure una persona).
        
        :param estat: estat actual
        :return: llista de tots els veïns possibles
        """
        veins = []
        for i in range(self.n):
            # Crear un nou estat canviant el bit i
            nou_estat = [estat[j] if j != i else 1 - estat[j] for j in range(self.n)]
            veins.append(nou_estat)
        return veins
    
    def cost(self, estat):
        """
        Calcula el cost total d'un estat.
        Cost = cost individual + cost incompatibilitats + cost desviació mida
        
        :param estat: estat actual
        :return: cost total
        """
        # 1. Cost individual: suma dels costos de les persones seleccionades
        cost_individual = 0
        for i in range(self.n):
            if estat[i] == 1:
                cost_individual += self.costs_unitaris[i]
        
        # 2. Cost per incompatibilitats
        cost_incompatibilitats = 0
        for (i, j), penalitzacio in self.penal_parelles.items():
            # Si les dues persones estan seleccionades
            if estat[i] == 1 and estat[j] == 1:
                cost_incompatibilitats += penalitzacio
        
        # 3. Cost per desviació de mida
        nombre_seleccionats = sum(estat)
        desviacio = abs(nombre_seleccionats - self.nombre_ideal)
        cost_desviacio = self.alpha * desviacio
        
        # Cost total
        cost_total = cost_individual + cost_incompatibilitats + cost_desviacio
        
        return cost_total
