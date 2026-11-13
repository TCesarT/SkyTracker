import requests

BIN_ID = "6af532f4ac6210605a81442a"
API_KEY = "$2a$10$rVFbLYYZTDCzwxvNdE8N7O1Ua0gBD6NOO.TW2R0wXnbtfjwhA1WaO"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"

headers = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

def cargarBD(): #Funcion para cargar los datos de la base de datos
    try:
        respuesta = requests.get(URL, headers=headers)
        #Si la peticion es exitosa retorna la data
        if respuesta.status_code == 200:
            data = respuesta.json()["record"]
            return data
        
        else: 
            print(f"Error al cargar la base de datos: {respuesta.status_code}")
            return None
        
    except requests.exceptions.ConnectionError:
            print("Error de connexion: verifica tu conexion a internet")
            return None
    
def actualizarBD(datos_actualizados):
    try:
        respuesta = requests.put(URL, json = datos_actualizados, headers = headers)
        if respuesta.status_code == 200:
            print("Base de datos actualizada correctamente")
            return True
        else:
            print(f"Error al actualizar la base de datos: {respuesta.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
            print("Error de conexion: verifica tu conexion a internet")
            return False
