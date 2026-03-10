from algoritmes.algoritme_cerca_local import AlgoritmeCercaLocal


class HillClimbing(AlgoritmeCercaLocal):
    """
    Algoritme de Hill Climbing per a problemes de minimització.
    
    L'algoritme parteix d'un estat inicial aleatori i es mou sempre cap al millor veï
    fins que es compleixi algun criteri d'aturada.
    """
    
    def __init__(self, max_iteracions=1000):
        """
        Inicialitza l'algoritme.
        
        :param max_iteracions: nombre màxim d'iteracions
        """
        self.max_iteracions = max_iteracions
    
    def executa(self, problema):
        """
        Executa l'algoritme de hill climbing.
        
        :param problema: instància de ProblemaCercaLocal a resoldre
        :return: (millor_estat, historic_cost)
                 - millor_estat: millor solució trobada
                 - historic_cost: llista de costos en cada iteració
        """
        # Estat inicial aleatori
        estat_actual = problema.estat_inicial()
        cost_actual = problema.cost(estat_actual)
        
        millor_estat = list(estat_actual)
        millor_cost = cost_actual
        
        historic_cost = [cost_actual]
        
        iteracio = 0
        millora_en_iteracio = True
        iteracions_sense_millora = 0
        
        print("\n--- ITERACIÓ 0 (INICIAL) ---")
        print("Estat:", estat_actual)
        print("Cost:", cost_actual)
        print("Nombre de persones seleccionades:", sum(estat_actual))
        print("*" * 50)
        
        while iteracio < self.max_iteracions and millora_en_iteracio and iteracions_sense_millora < 7:
            # Generar els veïns
            veins = problema.veinat(estat_actual)
            
            # Trobar el millor veí
            millor_vei = veins[0]
            millor_cost_vei = problema.cost(millor_vei)
            
            for vei in veins[1:]:
                cost_vei = problema.cost(vei)
                if cost_vei < millor_cost_vei:
                    millor_cost_vei = cost_vei
                    millor_vei = vei
            
            # Criteri d'aturada: si el millor veí no millora l'estat actual (òptim local)
            millora_en_iteracio = problema.es_millor(millor_vei, estat_actual)
            
            if millora_en_iteracio:
                # Moure's al millor veí
                estat_actual = millor_vei
                cost_actual = millor_cost_vei
                historic_cost.append(cost_actual)
                
                # Actualitzar el millor estat global si és necessari
                if problema.es_millor(estat_actual, millor_estat):
                    millor_estat = list(estat_actual)
                    millor_cost = cost_actual
                
                # Imprimir iteració
                iteracio += 1
                print("\n--- ITERACIÓ", iteracio, "---")
                print("Estat:", estat_actual)
                print("Cost:", cost_actual)
                print("Nombre de persones seleccionades:", sum(estat_actual))
                print("*" * 50)
            else:
                iteracio += 1
        
        return millor_estat, historic_cost
