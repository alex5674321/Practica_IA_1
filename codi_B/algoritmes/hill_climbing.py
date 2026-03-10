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

        estat_actual = problema.estat_inicial()
        cost_actual = problema.cost(estat_actual)

        millor_estat = list(estat_actual)
        millor_cost = cost_actual

        historic_cost = [cost_actual]

        iteracio = 0
        hi_ha_millora = True   # Controla si seguimos iterando

        print("\n--- ITERACIÓ 0 (INICIAL) ---")
        print("Estat:", estat_actual)
        print("Cost:", cost_actual)
        print("Nombre de persones seleccionades:", sum(estat_actual))
        print("*" * 50)

        while iteracio < self.max_iteracions and hi_ha_millora:

            veins = problema.veinat(estat_actual)

            millor_vei = veins[0]
            millor_cost_vei = problema.cost(millor_vei)

            for vei in veins[1:]:
                cost_vei = problema.cost(vei)
                if cost_vei < millor_cost_vei:
                    millor_cost_vei = cost_vei
                    millor_vei = vei

            # comprobar si mejora
            hi_ha_millora = problema.es_millor(millor_vei, estat_actual)

            if hi_ha_millora:

                estat_actual = millor_vei
                cost_actual = millor_cost_vei
                historic_cost.append(cost_actual)

                if problema.es_millor(estat_actual, millor_estat):
                    millor_estat = list(estat_actual)
                    millor_cost = cost_actual

                iteracio += 1

                print("\n--- ITERACIÓ", iteracio, "---")
                print("Estat:", estat_actual)
                print("Cost:", cost_actual)
                print("Nombre de persones seleccionades:", sum(estat_actual))
                print("*" * 50)

            else:
                print("\nÒptim local assolit. No hi ha millora.")
                print("*" * 50)

        return millor_estat, historic_cost
