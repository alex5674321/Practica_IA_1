import random
from problemes.problema import ProblemaCercaLocal


class ElMeuProblema(ProblemaCercaLocal):
    
    # Problema d'optimització de formació d'equips de treball.
    
    # Estat: vector binari de n elements on 1 indica persona seleccionada, 0 no seleccionada
    # Objectiu: minimitzar el cost total considerant:
    # - Cost individual de cada persona seleccionada
    # - Penalització per incompatibilitats entre persones
    # - Penalització per desviació respecte a la mida ideal de l'equip
        
    def __init__(self, n, costs_unitaris, penal_parelles, nombre_ideal, alpha):  # Inicialitzador amb paràmetres
        
        # Inicialitza el problema.

        self.n = n  # Nombre de persones disponibles
        self.costs_unitaris = costs_unitaris  # Costos individuals de cada persona
        self.penal_parelles = penal_parelles  # Penalitzacions per incompatibilitats
        self.nombre_ideal = nombre_ideal  # Mida ideal de l'equip
        self.alpha = alpha  # Pes de la desviació de mida
    
    def estat_inicial(self):  # Genera l'estat inicial

        # return [1] * self.n  # Retorna vector amb les persones seleccionades (inicialment totes seleccionades)
        return [random.randint(0, 1) for _ in range(self.n)]  # Alternativa: estat inicial aleatori
    
    def veinat(self, estat):  # Genera tots els estats veïns

        veins = []  # Llista per guardar els estats veïns
        for i in range(self.n):  # Iterar per cada posició
            # Crear un nou estat copiant l'actual
            nou_estat = list(estat)  # Copiar l'estat actual
            # Invertir el bit en la posició i (0 a 1 y viceversa) (apliquem un canvi simple, com fem amb el cas de pastís)
            nou_estat[i] = 1 - nou_estat[i]  # Si era 1 passa a 0, si era 0 passa a 1
            veins.append(nou_estat)  # Afegir el nou veí a la llista
        return veins  # Retornar tots els veïns
    
    def cost(self, estat):  # Calcula el cost total d'un estat

        # 1. Cost individual: suma dels costos de les persones seleccionades
        cost_individual = 0  # Inicialitzar cost individual
        for i in range(self.n):  # Recórrer totes les persones
            if estat[i] == 1:  # Si la persona està seleccionada
                cost_individual += self.costs_unitaris[i]  # Afegir el seu cost
        
        # 2. Cost per incompatibilitats
        cost_incompatibilitats = 0  # Inicialitzar cost d'incompatibilitats
        for (i, j), penalitzacio in self.penal_parelles.items():  # Per cada parella incompatible
            if estat[i] == 1 and estat[j] == 1:  # Si les dues estan seleccionades
                cost_incompatibilitats += penalitzacio  # Aplicar penalització
        
        # 3. Cost per desviació de mida
        nombre_seleccionats = sum(estat)  # Contar persones seleccionades
        desviacio = abs(nombre_seleccionats - self.nombre_ideal)  # Calcular desviació respecte la mida ideal
        cost_desviacio = self.alpha * desviacio  # Penalitzar la desviació
        
        # Cost total
        cost_total = cost_individual + cost_incompatibilitats + cost_desviacio  # Sumar tots els costos
        
        return cost_total  # Retornar el cost total
