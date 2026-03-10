from algoritmes.algoritme_cerca_local import AlgoritmeCercaLocal


class HillClimbing(AlgoritmeCercaLocal):

    # Algoritme de Hill Climbing per a minimitzar cost de persones  
      
    def __init__(self, max_iteracions=1000, num_reinicios=1):

        # Paràmetre per limitar el nombre d'iteracions en cas de no trobar un òptim local 
        self.max_iteracions = max_iteracions
        # Nombre de vegades que es reinicia l'algoritme amb estat inicial aleatori
        self.num_reinicios = num_reinicios
    
    def executa(self, problema):
        """
        Executa Hill Climbing amb múltiples reinicios aleatoris.
        Retorna la millor solució trobada entre tots els reinicios.
        """
        millor_estat_global = [1] * problema.n  # "Millor estat" inicial: inicialment totes les persones seleccionades
        millor_cost_global = 999999  # "Millor cost": inicialment un valor molt alt
        historic_cost_total = []  # Llista de histórics de costos per cada reinicio
        
        # Executar Hill Climbing múltiples vegades
        for reinici in range(self.num_reinicios):
            print("\n" + "=" * 60)
            print(f"REINICI ",reinici + 1,self.num_reinicios)
            print("=" * 60)
            
            # Executar una iteració de Hill Climbing
            millor_estat, historic_cost = self._hill_climbing_una_vegada(problema)
            cost_final = historic_cost[-1]
            
            # Registrar l'historial d'aquest reinicio
            historic_cost_total.append(historic_cost)
            
            # Comprovar si és millor que el global
            if cost_final < millor_cost_global:
                millor_cost_global = cost_final
                millor_estat_global = list(millor_estat)
                print(f"\nMillor solució actualitzada: cost = ",cost_final," (millora respecte al millor global anterior)")
            else:
                print(f"\nSolució d'aquest reinici: cost = ",cost_final)
        
        return millor_estat_global, historic_cost_total
    
    def _hill_climbing_una_vegada(self, problema):

        # Executa una iteració de Hill Climbing a partir d'un estat inicial generat pel problema.
        estat_actual = problema.estat_inicial()
        cost_actual = problema.cost(estat_actual)

        # Inicialitzar millor estat i cost amb l'estat inicial
        millor_estat = list(estat_actual)
        millor_cost = cost_actual

        historic_cost = [cost_actual] # Històric de costos per aquesta iteració de Hill Climbing

        iteracio = 0 # Contador d'iteracions
        hi_ha_millora = True   # Controla si seguimos iterando (cas de no millora o si)

        print("\n--- ITERACIÓ 0 (INICIAL) ---")
        print("Estat:", estat_actual)
        print("Cost:", cost_actual)
        print("Nombre de persones seleccionades:", sum(estat_actual))
        print("*" * 50)

        while iteracio < self.max_iteracions and hi_ha_millora: # Limitar el nombre d'iteracions per evitar bucles infinits en casos de no trobar un òptim local

            veins = problema.veinat(estat_actual) # Generar tots els veïns de l'estat actual

            millor_vei = veins[0] # Inicialitzar el millor veí amb el primer de la llista
            millor_cost_vei = problema.cost(millor_vei) # Calcular el cost del millor veí inicial

            for vei in veins[1:]: # Iterar per cada veí (comencem des del segon perquè el primer ja l'hem considerat)
                cost_vei = problema.cost(vei) # Calcular el cost del veí actual
                if cost_vei < millor_cost_vei: # Si el cost es millor que el millor cost del veí actual
                    millor_cost_vei = cost_vei # Actualitzar el millor cost del veí
                    millor_vei = vei # Actualitzar el millor veí

            # Comprovar si el millor veí és millor que l'estat actual
            hi_ha_millora = problema.es_millor(millor_vei, estat_actual)

            if hi_ha_millora:

                estat_actual = millor_vei # Moure's al millor veí
                cost_actual = millor_cost_vei # Actualitzar el cost actual al cost del millor veí
                historic_cost.append(cost_actual) # Registrar el cost actual al històric de costos

                if problema.es_millor(estat_actual, millor_estat): # Comprovar si el nou estat actual és millor que el millor estat registrat
                    millor_estat = list(estat_actual) # Actualitzar el millor estat registrat
                    millor_cost = cost_actual # Actualitzar el millor cost registrat

                iteracio += 1

                # Imprimir informació de la iteració actual
                print("\n--- ITERACIÓ", iteracio, "---")
                print("Estat:", estat_actual)
                print("Cost:", cost_actual)
                print("Nombre de persones seleccionades:", sum(estat_actual))
                print("*" * 50)

            else:
                print("\nÒptim local assolit. No hi ha millora.")
                print("*" * 50)

        return millor_estat, historic_cost
