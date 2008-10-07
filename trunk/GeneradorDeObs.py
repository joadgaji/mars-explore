
class GeneradorDeObs:        

    def __init__(self):
        pass
    
    def generarObs(x):
        opciones =[(0,0), (11,13), (11,12)]
        obs = []
        
        while (x > 0):
            if x < 3:
                figuras = 0
            else:
                figuras  = random.randint(0,3)
                
            if figuras == 0:
                obs = obs + generarRand()
                x = x - 1
            else:
                obs = obs + generarRandParaTes(opciones[figuras][0], opciones[figuras][1])        
                x = x - 3 
        return obs
            
    def generarRand():
            rand = random.randint(0,120)
            while mapa.has_key(rand):
                  rand = random.randint(0,120)
            return rand

    def generarRandParaTres(uno, dos):
            rand1 = random.randint(0,120)
            rand2 = rand1 + uno
            rand3 = rand2 + dos
            if (mapa.has_key(rand2) or mapa.has_key(rand3) or mapa.has_key(rand1)):
                generarRandParaTres(uno, dos)
            return [rand1, rand2, rand3]
           
