import requests
import urllib.parse

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_status = replydata.status_code
    print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200:
        json_data = replydata.json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        region = json_data["hits"][0].get("state", "")
        country = json_data["hits"][0].get("country", "")
        print("Ciudad:", name)
        print("Región/Estado:", region)
        print("País:", country)
        print("Latitud:", lat)
        print("Longitud:", lng)
        print()

        return lat, lng, country, region, name
    else:
        return "null", "null", "null", "null", "null"

def get_route(orig, dest, key):
    route_url = "https://graphhopper.com/api/1/route?"
    op = "&point=" + str(orig[0]) + "%2C" + str(orig[1])
    dp = "&point=" + str(dest[0]) + "%2C" + str(dest[1])

    paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": medio_eng}) + op + dp
    paths_response = requests.get(paths_url)

    paths_status = paths_response.status_code
    print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)

    if paths_status == 200:
        paths_data = paths_response.json()
        distance = paths_data["paths"][0]["distance"] / 1000 #Kilometros
        distance_mile = distance * 0.621371 #Millas
        time = paths_data["paths"][0]["time"] / 1000 #Segundos
        horas = int(time // 3600)
        minutos = int((time % 3600) // 60)
        segundos = int(time % 60)
        print("Desde " + orig[3] + " hasta " + dest[3] + " en " + medio + " son ")
        print(f"Distancia: {distance:.1f} km ({distance_mile:.1f} millas)")
        print(f"Tiempo estimado: {horas:02d}:{minutos:02d}:{segundos:02d}")
    else:
        return "null", "null"

key = "fe320ff2-6393-40d1-a72d-cc9e7030812a"

print("Ingrese Ubicaciones de Origen y Destino")
print("Si desea terminar con el proceso, escriba 'Salir'")

while True:
    loc1 = input("#- Ingrese Origen > ")
    if loc1 == "Salir" or loc1 == "salir" or loc1 == "s" or loc1 == "S":
        break

    loc2 = input("#- Ingrese Destino > ")
    if loc2 == "Salir" or loc2 == "salir" or loc2 == "s" or loc2 == "S":
        break

    orig = geocoding(loc1, key)
    dest = geocoding(loc2, key)
    
    print("Elige el medio de transporte \n auto, bicicleta, pie \n")
    medio = input("elige tu medio de transporte:  ")
    
    if medio == "auto":
        medio_eng = "car"

    elif medio == "bicicleta" or medio == "bici":
        medio_eng = "bike"
    elif medio == "pie":
        medio_eng = "foot"
    else:
        print("Porfavor selecciona una opcion valida")
        continue



    if orig[0] and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        op = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":medio_eng}) + op + dp

    if orig != ("null", "null") and dest != ("null", "null"):
        dist = get_route(orig, dest, key)
        if dist:
            print(dist)
