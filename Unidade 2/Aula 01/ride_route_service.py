import requests
import math

def calcular_corrida(cep_origem, cep_destino):
    url1 = "https://viacep.com.br/ws/" + cep_origem + "/json/"
    r1 = requests.get(url1)
    dados1 = r1.json()
    
    url2 = "https://viacep.com.br/ws/" + cep_destino + "/json/"
    r2 = requests.get(url2)
    dados2 = r2.json()
    
    lat1 = dados1["lat"]
    lon1 = dados1["lng"]
    lat2 = dados2["lat"]
    lon2 = dados2["lng"]
    
    distancia = math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2) * 111
    tarifa = distancia * 2.5 + 5
    print("Tarifa: R$" + str(tarifa))

calcular_corrida("70000000", "01310000")