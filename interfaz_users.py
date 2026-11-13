import time
import datetime as dt
import os 
# ==============================================================================
# CÓDIGOS DE COLOR ANSI (El maquillaje de la consola)
# ==============================================================================
class Color:
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'  

def limpiar_pantalla():
    """Detecta tu sistema operativo y limpia la consola."""
    # 'nt' es Windows (usa cls), el resto (Mac/Linux) usa 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Hace una pausa para que el usuario pueda leer antes de limpiar la pantalla."""
    input(f"\n{Color.AMARILLO}Presiona ENTER para continuar...{Color.RESET}")

# ==============================================================================
# DATOS SIMULADOS (MOCKS)
# ==============================================================================
TOKEN_EMPRESARIAL = "SKYTRACK_2026"

db_simulada = {
    "flota": [
        {"id": "DRN-001", "estado": "Disponible", "hora_salida": None},
        {"id": "DRN-002", "estado": "En Camino", "hora_salida": time.time() - 3600}, 
        {"id": "DRN-003", "estado": "Retornando", "hora_salida": None}
    ],
    "envios": [],
    "clientes": [{"id": "CLI-001", "nombre": "Juan Pérez", "municipio": "Chacao"}]
}

# ==============================================================================
# FUNCIONES DE VALIDACIÓN ROBUSTA
# ==============================================================================
def pedir_entero(mensaje, min_val, max_val):
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            if min_val <= numero <= max_val:
                return numero
            else:
                print(f"{Color.ROJO}❌ Error: Ingresa un número entre {min_val} y {max_val}.{Color.RESET}")
        except ValueError:
            print(f"{Color.ROJO}❌ Error: Entrada inválida. Usa solo números.{Color.RESET}")

def pedir_cadena(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print(f"{Color.ROJO}❌ Error: Este campo no puede estar vacío.{Color.RESET}")

# ==============================================================================
# FUNCIONES DEL PANEL DE OPERADOR
# ==============================================================================
def ver_flota():
    limpiar_pantalla()
    print(f"{Color.CYAN}\n--- 🚁 ESTADO DE LA FLOTA EN TIEMPO REAL ---{Color.RESET}")
    print(f"{'ID DRON':<10} | {'ESTADO':<15} | {'TIEMPO DE VUELO'}")
    print("-" * 45)
    
    for dron in db_simulada["flota"]:
        tiempo_vuelo = "N/A"
        color_estado = Color.VERDE if dron["estado"] == "Disponible" else Color.AMARILLO
        
        if dron["hora_salida"]:
            minutos = (time.time() - dron["hora_salida"]) / 60
            tiempo_vuelo = f"{minutos:.1f} min"
            if minutos > 45: # Si lleva mucho tiempo, se pinta de rojo
                color_estado = Color.ROJO
            
        print(f"{dron['id']:<10} | {color_estado}{dron['estado']:<15}{Color.RESET} | {tiempo_vuelo}")
    print("-" * 45)

def despachar_envio():
    limpiar_pantalla()
    print(f"{Color.CYAN}\n--- 📦 DESPACHAR NUEVO ENVÍO ---{Color.RESET}")
    drones_disponibles = [d for d in db_simulada["flota"] if d["estado"] == "Disponible"]
    
    if not drones_disponibles:
        print(f"{Color.ROJO}⚠️ No hay drones disponibles en este momento.{Color.RESET}")
        return

    dron_asignado = drones_disponibles[0]
    cliente_id = pedir_cadena("Ingresa el ID del Cliente a despachar (ej. CLI-001): ")
    
    dron_asignado["estado"] = "En Camino"
    dron_asignado["hora_salida"] = time.time()
    
    nuevo_envio = {
        "id_envio": f"ENV-{len(db_simulada['envios']) + 1}",
        "dron": dron_asignado["id"],
        "cliente": cliente_id,
        "salida_str": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db_simulada["envios"].append(nuevo_envio)
    
    print(f"{Color.VERDE}✅ ¡Envío {nuevo_envio['id_envio']} despachado con éxito en el {dron_asignado['id']}!{Color.RESET}")

def verificar_extraviados():
    limpiar_pantalla()
    print(f"{Color.CYAN}\n--- 🚨 VERIFICACIÓN DE SEGURIDAD ---{Color.RESET}")
    LIMITE_MINUTOS = 45 
    alertas = 0
    
    for dron in db_simulada["flota"]:
        if dron["estado"] in ["En Camino", "Retornando"] and dron["hora_salida"]:
            minutos_volando = (time.time() - dron["hora_salida"]) / 60
            if minutos_volando > LIMITE_MINUTOS:
                dron["estado"] = "Extraviado"
                print(f"{Color.ROJO}❌ ¡ALERTA! Dron {dron['id']} marcado como EXTRAVIADO. (Tiempo: {minutos_volando:.1f} min){Color.RESET}")
                alertas += 1
                
    if alertas == 0:
        print(f"{Color.VERDE}✅ Toda la flota operando dentro de los tiempos seguros.{Color.RESET}")

# ==============================================================================
# MENÚS DE NAVEGACIÓN
# ==============================================================================
def menu_operador():
    while True:
        limpiar_pantalla()
        print(f"{Color.CYAN}\n=============================={Color.RESET}")
        print(f"{Color.VERDE}👨‍💻 PANEL DE CONTROL OPERADOR{Color.RESET}")
        print(f"{Color.CYAN}=============================={Color.RESET}")
        print("1. Ver estado de la flota")
        print("2. Despachar un envío")
        print("3. Verificar drones extraviados")
        print("4. Cerrar Sesión")
        
        opcion = pedir_entero(f"\n{Color.AMARILLO}Selecciona una opción (1-4): {Color.RESET}", 1, 4)
        
        if opcion == 1:
            ver_flota()
            pausar()
        elif opcion == 2:
            despachar_envio()
            pausar()
        elif opcion == 3:
            verificar_extraviados()
            pausar()
        elif opcion == 4:
            print(f"{Color.AMARILLO}Cerrando sesión de operador...{Color.RESET}")
            time.sleep(1) # Pequeña pausa dramática antes de volver al menú principal
            break

def menu_principal():
    while True:
        limpiar_pantalla()
        print(f"{Color.CYAN}\n=============================={Color.RESET}")
        print(f"{Color.VERDE}🚁 BIENVENIDO A SKYTRACK CLI{Color.RESET}")
        print(f"{Color.CYAN}=============================={Color.RESET}")
        print("1. Iniciar sesión como Cliente")
        print("2. Iniciar sesión como Operador")
        print("3. Salir del sistema")
        
        opcion = pedir_entero(f"\n{Color.AMARILLO}Selecciona tu rol (1-3): {Color.RESET}", 1, 3)
        
        if opcion == 1:
            print("\nEn construcción...")
            pausar()
        elif opcion == 2:
            print(f"\n{Color.CYAN}--- SEGURIDAD EMPRESARIAL ---{Color.RESET}")
            intento_token = pedir_cadena("Ingresa el Token de Seguridad: ")
            
            if intento_token == TOKEN_EMPRESARIAL:
                menu_operador()
            else:
                print(f"{Color.ROJO}❌ Acceso denegado. Token incorrecto.{Color.RESET}")
                pausar()
                
        elif opcion == 3:
            print(f"{Color.VERDE}¡Gracias por usar SkyTrack! Apagando sistemas...{Color.RESET}")
            break

if __name__ == "__main__":
    menu_principal()