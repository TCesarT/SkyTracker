# Diccionario con los estados y sus principales municipios
estados = {
    "Amazonas": ["Atabapo", "Atures", "Autana", "Maroa"],
    "Anzoátegui": ["Anaco", "Bruzual", "Guanipa", "Guanta", "Simón Bolívar", "Simón Rodríguez"],
    "Apure": ["Achaguas", "Biruaca", "Páez", "San Fernando"],
    "Aragua": ["Girardot", "Linares Alcántara", "Ribas", "Mariño", "Zamora"],
    "Barinas": ["Barinas", "Barinitas", "Sosa"],
    "Bolívar": ["Caroní", "Heres", "Piar", "Gran Sabana"],
    "Carabobo": ["Valencia", "Guacara", "Naguanagua", "San Diego", "Puerto Cabello"],
    "Cojedes": ["Ezequiel Zamora", "Tinaco"],
    "Delta Amacuro": ["Tucupita", "Casacoima"],
    "Distrito Capital": ["Libertador"],
    "Falcón": ["Carirubana", "Miranda", "Los Taques"],
    "Guárico": ["Juan Germán Roscio", "Miranda", "Infante"],
    "Lara": ["Iribarren", "Palavecino", "Torres", "Jiménez"],
    "Mérida": ["Libertador", "Alberto Adriani", "Campo Elías"],
    "Miranda": ["Chacao", "Baruta", "Sucre", "El Hatillo", "Guicaipuro", "Plaza"],
    "Monagas": ["Maturín", "Caripe", "Piar"],
    "Nueva Esparta": ["Mariño", "Maneiro", "Arismendi"],
    "Portuguesa": ["Guanare", "Araure"],
    "Sucre": ["Bermúdez", "Sucre", "Montes"],
    "Táchira": ["San Cristóbal", "Junín", "Cárdenas", "Bolívar"],
    "Trujillo": ["Valera", "Trujillo", "Boconó"],
    "Vargas": ["Vargas"],
    "Yaracuy": ["San Felipe", "Bruzual", "Nirgua"],
    "Zulia": ["Maracaibo", "San Francisco", "Cabimas", "Colón", "Lagunillas"]
}

def validar_ubicacion():
    print("Validación de ubicación:")
    
    # Bucle para pedir y verificar el estado
    while True:
        entrada = input("Estado (escriba LISTAR para ver opciones): ").strip()
        
        # Si está vacío, se le avisa y se reinicia el ciclo
        if not entrada:
            print("Error: No puedes dejar el campo vacío.")
            continue
        
        # Si el usuario escribe listar (en cualquier combinación de mayúsculas/minúsculas)
        if entrada.upper() == "LISTAR":
            print("Estados disponibles:")
            for e in estados:
                print("-", e)
            continue
            
        # Limpia espacios dobles en el medio y pone la primera letra de cada palabra en mayúscula
        edo = " ".join(entrada.split()).title()
        
        # Si el estado existe en el diccionario, salimos de este bucle
        if edo in estados:
            break
        print("Error: Estado no válido.")

    # Bucle para pedir el municipio y verificar que pertenezca al estado seleccionado
    while True:
        municipios_validos = estados[edo]
        entrada_muni = input(f"Municipio para {edo} (escriba LISTAR para ver): ").strip()
        
        # Si está vacío, se le avisa y se reinicia
        if not entrada_muni:
            print("Error: No puedes dejar el campo vacío.")
            continue
        
        # Si pide listar, mostramos solo los municipios de este estado en específico
        if entrada_muni.upper() == "LISTAR":
            print(f"Municipios de {edo}:")
            for m in municipios_validos:
                print("-", m)
            continue
            
        # Limpiamos espacios y capitalizamos el municipio
        muni = " ".join(entrada_muni.split()).title()
        
        # Validamos que el municipio esté dentro de la lista de ese estado
        if muni in municipios_validos:
            print(f"Ubicación aceptada: {muni}, {edo}")
            return edo, muni
        print("Error: El municipio no pertenece a este estado.")

if __name__ == "__main__":
    validar_ubicacion()