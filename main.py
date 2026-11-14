import time
import datetime as dt
import os

# Importación de los módulos del equipo (Responsables 1, 2 y 3)
from manageBD import cargarBD, actualizarBD
from geo_validador_parte3 import validar_ubicacion
from modelos import Cliente, Operador, Dron, Envio

# ==============================================================================
# CÓDIGOS DE COLOR ANSI Y UTILIDADES DE CONSOLA
# ==============================================================================
class Color:
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    ROJO = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def limpiar_pantalla():
    """Detecta el sistema operativo y limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa la ejecución para que el usuario lea antes de borrar la pantalla."""
    input(f"\n{Color.AMARILLO}Presiona ENTER para continuar...{Color.RESET}")

# ==============================================================================
# FUNCIONES DE VALIDACIÓN ROBUSTA (A prueba de errores de entrada)
# ==============================================================================
def pedir_entero(mensaje, min_val, max_val):
    while True:
        entrada = input(mensaje).strip()
        if len(entrada) > 50:
            print(f"{Color.ROJO}❌ Error: La entrada excede el límite de 50 caracteres.{Color.RESET}")
            continue
        try:
            numero = int(entrada)
            if min_val <= numero <= max_val:
                return numero
            else:
                print(f"{Color.ROJO}❌ Error: Ingresa un número entre {min_val} y {max_val}.{Color.RESET}")
        except ValueError:
            print(f"{Color.ROJO}❌ Error: Entrada inválida. Usa solo números.{Color.RESET}")

def pedir_cadena(mensaje, max_largo=50):
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print(f"{Color.ROJO}❌ Error: Este campo no puede estar vacío.{Color.RESET}")
        elif len(entrada) > max_largo:
            print(f"{Color.ROJO}❌ Error: El texto es demasiado largo ({len(entrada)} caracteres). Máximo permitido: {max_largo}.{Color.RESET}")
        else:
            return entrada

# ==============================================================================
# ALGORITMO ETA EN CASCADA (RESPONSABLE 5)
# ==============================================================================
def obtener_eta_cascada(data, estado, municipio):
    """
    Calcula el tiempo estimado de llegada (ETA) en 3 niveles jerárquicos:
    1. Promedio del Municipio -> 2. Promedio del Estado -> 3. Valor por defecto (45 min).
    Retorna una tupla: (minutos_eta, nivel_utilizado)
    """
    historial = data.get("historial_eta", {})
    
    # 1. Nivel Municipio
    datos_muni = historial.get("municipios", {}).get(municipio)
    if datos_muni and datos_muni.get("promedio_minutos") is not None:
        return datos_muni["promedio_minutos"], f"Historial del Municipio ({municipio})"

    # 2. Nivel Estado (Fallback)
    datos_edo = historial.get("estados", {}).get(estado)
    if datos_edo and datos_edo.get("promedio_minutos") is not None:
        return datos_edo["promedio_minutos"], f"Promedio General del Estado ({estado})"

    # 3. Valor por defecto de la configuración
    eta_defecto = data.get("config", {}).get("eta_defecto_minutos", 45)
    return eta_defecto, "Valor Estándar por Defecto (Zona Nueva)"

# ==============================================================================
# REGISTRO Y AUTENTICACIÓN DE USUARIOS (CLIENTES Y OPERADORES)
# ==============================================================================
def registrar_usuario():
    limpiar_pantalla()
    print(f"{Color.CYAN}\n===================================={Color.RESET}")
    print(f"{Color.VERDE}📝 REGISTRO DE NUEVO USUARIO{Color.RESET}")
    print(f"{Color.CYAN}===================================={Color.RESET}")
    print("1. Registrar nuevo Cliente")
    print("2. Registrar nuevo Operador (Requiere Token)")
    print("3. Volver al menú principal")

    opcion = pedir_entero(f"\n{Color.AMARILLO}Selecciona el tipo de cuenta (1-3): {Color.RESET}", 1, 3)
    if opcion == 3:
        return

    data = cargarBD()
    if not data:
        print(f"{Color.ROJO}❌ No se pudo conectar con la base de datos.{Color.RESET}")
        return

    # --- REGISTRO DE CLIENTE ---
    if opcion == 1:
        print(f"\n{Color.CYAN}--- DATOS DEL NUEVO CLIENTE ---{Color.RESET}")
        while True:
            id_cliente = pedir_cadena("Ingresa tu ID de Cliente (ej. CLI-003): ").upper()
            ids_existentes = [c["id"].upper() for c in data["usuarios"]["clientes"]]
            if id_cliente in ids_existentes:
                print(f"{Color.ROJO}❌ Error: El ID '{id_cliente}' ya está registrado. Intenta con otro.{Color.RESET}")
            else:
                break

        nombre = pedir_cadena("Nombre completo: ")
        contrasena = pedir_cadena("Contraseña: ")

        print(f"\n{Color.CYAN}--- UBICACIÓN DE ENTREGA ---{Color.RESET}")
        estado, municipio = validar_ubicacion()
        direccion = pedir_cadena("Dirección exacta (Avenida, Edificio/Casa, Piso/Apto): ")

        nuevo_obj = Cliente(id_cliente, nombre, contrasena, estado, municipio, direccion)
        nuevo_cliente_dict = {
            "id": nuevo_obj.id,
            "nombre": nuevo_obj.nombre,
            "contrasena": nuevo_obj.contra,
            "estado": nuevo_obj.estado,
            "municipio": nuevo_obj.municipio,
            "direccion": nuevo_obj.direccion
        }

        data["usuarios"]["clientes"].append(nuevo_cliente_dict)
        if actualizarBD(data):
            print(f"{Color.VERDE}✅ ¡Cliente '{nombre}' ({id_cliente}) registrado y guardado en la nube!{Color.RESET}")

    # --- REGISTRO DE OPERADOR ---
    elif opcion == 2:
        print(f"\n{Color.CYAN}--- VALIDACIÓN DE SEGURIDAD EMPRESARIAL ---{Color.RESET}")
        token_real = data.get("config", {}).get("token_operador", "SKYTRACK2026")
        intento_token = pedir_cadena("Ingresa el Token de Seguridad Empresarial: ")

        if intento_token != token_real:
            print(f"{Color.ROJO}❌ Token inválido. No tienes permisos para crear cuentas de Operador.{Color.RESET}")
            return

        print(f"{Color.VERDE}🔓 Token verificado correctamente.{Color.RESET}")
        print(f"\n{Color.CYAN}--- DATOS DEL NUEVO OPERADOR ---{Color.RESET}")
        while True:
            id_operador = pedir_cadena("Ingresa el ID de Operador (ej. OPE-003): ").upper()
            ids_existentes = [o["id"].upper() for o in data["usuarios"]["operadores"]]
            if id_operador in ids_existentes:
                print(f"{Color.ROJO}❌ Error: El ID '{id_operador}' ya existe. Elige otro.{Color.RESET}")
            else:
                break

        nombre = pedir_cadena("Nombre completo del Operador: ")
        contrasena = pedir_cadena("Contraseña: ")

        nuevo_op_obj = Operador(id_operador, nombre, contrasena)
        nuevo_operador_dict = {
            "id": nuevo_op_obj.id,
            "nombre": nuevo_op_obj.nombre,
            "contrasena": nuevo_op_obj.contra
        }

        data["usuarios"]["operadores"].append(nuevo_operador_dict)
        if actualizarBD(data):
            print(f"{Color.VERDE}✅ ¡Operador '{nombre}' ({id_operador}) registrado con éxito!{Color.RESET}")

def login_cliente():
    limpiar_pantalla()
    print(f"{Color.CYAN}\n--- 🔐 INICIO DE SESIÓN: CLIENTE ---{Color.RESET}")
    data = cargarBD()
    if not data:
        return None

    id_cli = pedir_cadena("ID de Cliente (ej. CLI-001): ").upper()
    contra_cli = pedir_cadena("Contraseña: ")

    for cli_data in data["usuarios"]["clientes"]:
        if cli_data["id"].upper() == id_cli:
            cliente_obj = Cliente(
                cli_data["id"],
                cli_data["nombre"],
                cli_data["contrasena"],
                cli_data["estado"],
                cli_data["municipio"],
                cli_data["direccion"]
            )
            if cliente_obj.autenticar(contra_cli):
                print(f"{Color.VERDE}✅ ¡Bienvenido/a, {cliente_obj.nombre}!{Color.RESET}")
                time.sleep(1)
                return cliente_obj
            else:
                print(f"{Color.ROJO}❌ Contraseña incorrecta.{Color.RESET}")
                return None

    print(f"{Color.ROJO}❌ No se encontró ningún cliente con el ID '{id_cli}'.{Color.RESET}")
    return None

def login_operador():
    limpiar_pantalla()
    print(f"{Color.CYAN}\n--- 🔐 INICIO DE SESIÓN: OPERADOR ---{Color.RESET}")
    data = cargarBD()
    if not data:
        return None

    id_op = pedir_cadena("ID de Operador (ej. OPE-001): ").upper()
    contra_op = pedir_cadena("Contraseña: ")
    token_intento = pedir_cadena("Token de Seguridad Empresarial: ")

    token_real = data.get("config", {}).get("token_operador", "SKYTRACK2026")
    if token_intento != token_real:
        print(f"{Color.ROJO}❌ Acceso denegado: Token empresarial incorrecto.{Color.RESET}")
        return None

    for op_data in data["usuarios"]["operadores"]:
        if op_data["id"].upper() == id_op:
            operador_obj = Operador(op_data["id"], op_data["nombre"], op_data["contrasena"])
            if operador_obj.autenticar(contra_op):
                print(f"{Color.VERDE}✅ ¡Bienvenido/a, {operador_obj.nombre}!{Color.RESET}")
                time.sleep(1)
                return operador_obj
            else:
                print(f"{Color.ROJO}❌ Contraseña incorrecta.{Color.RESET}")
                return None

    print(f"{Color.ROJO}❌ No se encontró ningún operador con el ID '{id_op}'.{Color.RESET}")
    return None

# ==============================================================================
# FUNCIONES DEL PANEL DEL CLIENTE (RESPONSABLE 5)
# ==============================================================================
def ver_mis_envios(cliente_actual):
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    print(f"{Color.CYAN}\n--- 📦 MIS ENVÍOS ({cliente_actual.nombre}) ---{Color.RESET}")
    # Aislamiento de datos: solo filtramos los envíos asociados al ID de este cliente
    mis_envios = [e for e in data.get("envios", []) if e["cliente_id"].upper() == cliente_actual.id.upper()]

    if not mis_envios:
        print(f"{Color.AMARILLO}Aún no tienes envíos registrados a tu nombre.{Color.RESET}")
        return

    print(f"{'ID ENVÍO':<10} | {'DRON':<9} | {'ESTADO':<13} | {'ETA ESTIMADO':<14} | {'TIEMPO TRANSCURRIDO / REAL'}")
    print("-" * 80)

    for e in mis_envios:
        estado = e["estado_envio"]
        eta_str = f"{e['eta_minutos']} min" if e.get("eta_minutos") else "N/A"

        if estado == "Entregado":
            color_est = Color.VERDE
            tiempo_info = f"Entregado en {e.get('tiempo_real_vuelo_minutos', 0):.1f} min"
        elif estado == "En Camino":
            color_est = Color.AMARILLO
            if e.get("timestamp_salida"):
                transcurrido = (time.time() - e["timestamp_salida"]) / 60
                restante = max(0, (e.get("eta_minutos") or 45) - transcurrido)
                tiempo_info = f"Volando: {transcurrido:.1f} min (Faltan ~{restante:.1f} min)"
            else:
                tiempo_info = "En preparación"
        else:
            color_est = Color.ROJO
            tiempo_info = estado

        print(f"{e['id']:<10} | {e['dron_id']:<9} | {color_est}{estado:<13}{Color.RESET} | {eta_str:<14} | {tiempo_info}")
    print("-" * 80)

def consultar_mi_eta(cliente_actual):
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    print(f"{Color.CYAN}\n--- ⏱️ ESTIMACIÓN INTELIGENTE DE TIEMPO (ALGORITMO ETA) ---{Color.RESET}")
    eta_min, criterio = obtener_eta_cascada(data, cliente_actual.estado, cliente_actual.municipio)

    print(f"📍 Tu ubicación registrada:")
    print(f"   - Estado:    {cliente_actual.estado}")
    print(f"   - Municipio: {cliente_actual.municipio}")
    print(f"   - Dirección: {cliente_actual.direccion}")
    print("-" * 55)
    print(f"🔍 Criterio aplicado en cascada: {Color.AMARILLO}{criterio}{Color.RESET}")
    print(f"🚁 Tiempo estimado de entrega (ETA): {Color.VERDE}{eta_min} minutos{Color.RESET}")

def recibir_paquete(cliente_actual):
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    print(f"{Color.CYAN}\n--- 📬 CONFIRMAR RECEPCIÓN DE PAQUETE ---{Color.RESET}")
    # Filtramos solo los envíos de este cliente que estén "En Camino"
    envios_en_camino = [
        e for e in data.get("envios", [])
        if e["cliente_id"].upper() == cliente_actual.id.upper() and e["estado_envio"] == "En Camino"
    ]

    if not envios_en_camino:
        print(f"{Color.AMARILLO}No tienes ningún paquete 'En Camino' pendiente por recibir en este momento.{Color.RESET}")
        return

    print("Envíos actualmente en camino hacia tu ubicación:")
    for idx, env in enumerate(envios_en_camino, start=1):
        minutos_vuelo = (time.time() - env["timestamp_salida"]) / 60 if env.get("timestamp_salida") else 0
        print(f"{idx}. Envío {env['id']} | Dron: {env['dron_id']} | Tiempo de vuelo actual: {minutos_vuelo:.1f} min")

    seleccion = pedir_entero(f"\n{Color.AMARILLO}Selecciona el número del envío que acabas de recibir (1-{len(envios_en_camino)}): {Color.RESET}", 1, len(envios_en_camino))
    envio_elegido = envios_en_camino[seleccion - 1]

    # 1. Calcular el tiempo real de vuelo en minutos
    ahora = time.time()
    salida = envio_elegido.get("timestamp_salida") or ahora
    tiempo_real_min = round(max(0.1, (ahora - salida) / 60), 2)

    # 2. Actualizar los datos del envío en el JSON
    envio_elegido["timestamp_entrega"] = ahora
    envio_elegido["tiempo_real_vuelo_minutos"] = tiempo_real_min
    envio_elegido["estado_envio"] = "Entregado"

    # 3. Cambiar el estado del dron a "Retornando" (Retornando a base)
    for dron in data.get("drones", []):
        if dron["id"] == envio_elegido["dron_id"]:
            dron_obj = Dron(dron["id"], dron["modelo"], dron["estado"], dron["envio_activo_id"])
            dron_obj.actualizar_estado("Retornando")
            dron["estado"] = dron_obj.estado
            break

    # 4. Actualizar los promedios geográficos en historial_eta (Municipio y Estado)
    edo = envio_elegido["estado_destino"]
    muni = envio_elegido["municipio_destino"]

    if "historial_eta" not in data:
        data["historial_eta"] = {"municipios": {}, "estados": {}}

    # 4.1 Actualizar Historial del Municipio (según plantilla en baseD.json)
    hist_municipios = data["historial_eta"].setdefault("municipios", {})
    if muni not in hist_municipios:
        hist_municipios[muni] = {
            "estado": edo,
            "tiempos_minutos": [],
            "promedio_minutos": None
        }
    hist_municipios[muni]["tiempos_minutos"].append(tiempo_real_min)
    lista_muni = hist_municipios[muni]["tiempos_minutos"]
    hist_municipios[muni]["promedio_minutos"] = round(sum(lista_muni) / len(lista_muni), 2)

    # 4.2 Actualizar Historial del Estado (según plantilla en baseD.json)
    hist_estados = data["historial_eta"].setdefault("estados", {})
    if edo not in hist_estados:
        hist_estados[edo] = {
            "tiempos_minutos": [],
            "promedio_minutos": None
        }
    hist_estados[edo]["tiempos_minutos"].append(tiempo_real_min)
    lista_edo = hist_estados[edo]["tiempos_minutos"]
    hist_estados[edo]["promedio_minutos"] = round(sum(lista_edo) / len(lista_edo), 2)

    # 5. Guardar todos los cambios en JSONBin.io
    if actualizarBD(data):
        print(f"\n{Color.VERDE}✅ ¡Paquete {envio_elegido['id']} recibido con éxito!{Color.RESET}")
        print(f"   ⏱️  Tiempo real de vuelo registrado: {tiempo_real_min} minutos")
        print(f"   📈 Nuevo promedio ETA en {muni}: {hist_municipios[muni]['promedio_minutos']} min")
        print(f"   📈 Nuevo promedio ETA en {edo}: {hist_estados[edo]['promedio_minutos']} min")
        print(f"   🚁 El dron {envio_elegido['dron_id']} ha cambiado su estado a: 'Retornando' (Retornando a base).")

# ==============================================================================
# FUNCIONES DEL PANEL DE OPERADOR (RESPONSABLE 4)
# ==============================================================================
def ver_flota():
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    umbral_extravio = data.get("config", {}).get("umbral_extravío_minutos", 180)
    envios_por_id = {e["id"]: e for e in data.get("envios", [])}

    print(f"{Color.CYAN}\n--- 🚁 ESTADO DE LA FLOTA EN TIEMPO REAL ---{Color.RESET}")
    print(f"{'ID DRON':<10} | {'MODELO':<18} | {'ESTADO':<15} | {'ENVÍO ACTIVO':<12} | {'TIEMPO VUELO'}")
    print("-" * 78)

    for d in data.get("drones", []):
        tiempo_vuelo = "N/A"
        envio_id = d.get("envio_activo_id") or "Ninguno"
        estado = d["estado"]

        if estado == "Disponible":
            color_estado = Color.VERDE
        elif estado == "Extraviado":
            color_estado = Color.ROJO
        else:
            color_estado = Color.AMARILLO

        if d.get("envio_activo_id") and d["envio_activo_id"] in envios_por_id:
            envio_actual = envios_por_id[d["envio_activo_id"]]
            if envio_actual.get("timestamp_salida"):
                minutos = (time.time() - envio_actual["timestamp_salida"]) / 60
                tiempo_vuelo = f"{minutos:.1f} min"
                if minutos > umbral_extravio:
                    color_estado = Color.ROJO

        print(f"{d['id']:<10} | {d['modelo']:<18} | {color_estado}{estado:<15}{Color.RESET} | {envio_id:<12} | {tiempo_vuelo}")
    print("-" * 78)

    # Opción rápida para que el operador reciba en base a los drones que están "Retornando"
    drones_retornando = [d for d in data.get("drones", []) if d["estado"] == "Retornando"]
    if drones_retornando:
        print(f"\n{Color.AMARILLO}💡 Hay {len(drones_retornando)} dron(es) 'Retornando' a la base tras entregar su paquete.{Color.RESET}")
        resp = input("¿Deseas confirmar su llegada a la base y ponerlos 'Disponible'? (S/N): ").strip().upper()
        if resp == "S":
            envios_dict = {e["id"]: e for e in data.get("envios", [])}
            for d in drones_retornando:
                if d.get("envio_activo_id") and d["envio_activo_id"] in envios_dict:
                    envios_dict[d["envio_activo_id"]]["timestamp_retorno"] = time.time()
                d["estado"] = "Disponible"
                d["envio_activo_id"] = None
            if actualizarBD(data):
                print(f"{Color.VERDE}✅ Drones recibidos en base y listos para nuevos envíos.{Color.RESET}")

def despachar_envio(operador_actual):
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    print(f"{Color.CYAN}\n--- 📦 DESPACHAR NUEVO ENVÍO ---{Color.RESET}")
    drones_disponibles = [d for d in data.get("drones", []) if d["estado"] == "Disponible"]

    if not drones_disponibles:
        print(f"{Color.ROJO}⚠️ No hay drones disponibles en este momento.{Color.RESET}")
        return

    clientes = data.get("usuarios", {}).get("clientes", [])
    if not clientes:
        print(f"{Color.ROJO}⚠️ No hay clientes registrados en el sistema.{Color.RESET}")
        return

    print("\nClientes registrados:")
    for c in clientes:
        print(f" - {c['id']}: {c['nombre']} ({c['estado']}, {c['municipio']})")

    cliente_id = pedir_cadena("\nIngresa el ID del Cliente a despachar (ej. CLI-001): ").upper()
    cliente_seleccionado = next((c for c in clientes if c["id"].upper() == cliente_id), None)

    if not cliente_seleccionado:
        print(f"{Color.ROJO}❌ Error: El cliente '{cliente_id}' no existe en la base de datos.{Color.RESET}")
        return

    dron_asignado = drones_disponibles[0]
    nuevo_id_envio = f"ENV-{len(data.get('envios', [])) + 1:03d}"
    eta_estimado, criterio_eta = obtener_eta_cascada(
        data, cliente_seleccionado["estado"], cliente_seleccionado["municipio"]
    )

    envio_obj = Envio(
        id_envio=nuevo_id_envio,
        dron_id=dron_asignado["id"],
        cliente_id=cliente_seleccionado["id"],
        estado_destino=cliente_seleccionado["estado"],
        municipio_destino=cliente_seleccionado["municipio"],
        direccion_destino=cliente_seleccionado["direccion"],
        operador_id=operador_actual.id,
        eta_minutos=eta_estimado
    )

    nuevo_envio_dict = {
        "id": envio_obj.id,
        "dron_id": envio_obj.dron_id,
        "cliente_id": envio_obj.cliente_id,
        "estado_destino": envio_obj.estado_destino,
        "municipio_destino": envio_obj.municipio_destino,
        "direccion_destino": envio_obj.direccion_destino,
        "estado_envio": envio_obj.estado_envio,
        "timestamp_salida": envio_obj.timestamp_salida,
        "timestamp_entrega": envio_obj.timestamp_entrega,
        "timestamp_retorno": envio_obj.timestamp_retorno,
        "eta_minutos": envio_obj.eta_minutos,
        "tiempo_real_vuelo_minutos": envio_obj.tiempo_real_vuelo_minutos,
        "operador_id": envio_obj.operador_id
    }

    dron_asignado["estado"] = "En Camino"
    dron_asignado["envio_activo_id"] = nuevo_id_envio
    data["envios"].append(nuevo_envio_dict)

    if actualizarBD(data):
        print(f"\n{Color.VERDE}✅ ¡Envío {nuevo_id_envio} despachado con éxito!{Color.RESET}")
        print(f"   🚁 Dron asignado: {dron_asignado['id']} ({dron_asignado['modelo']})")
        print(f"   📍 Destino: {cliente_seleccionado['municipio']}, {cliente_seleccionado['estado']} - {cliente_seleccionado['direccion']}")
        print(f"   ⏱️  ETA estimado: {eta_estimado} minutos ({criterio_eta})")

def verificar_extraviados():
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    print(f"{Color.CYAN}\n--- 🚨 VERIFICACIÓN DE SEGURIDAD (DRONES EXTRAVIADOS) ---{Color.RESET}")
    umbral_minutos = data.get("config", {}).get("umbral_extravío_minutos", 180)
    envios_por_id = {e["id"]: e for e in data.get("envios", [])}
    alertas = 0

    for dron in data.get("drones", []):
        if dron["estado"] in ["En Camino", "Retornando"] and dron.get("envio_activo_id"):
            envio_act = envios_por_id.get(dron["envio_activo_id"])
            if envio_act and envio_act.get("timestamp_salida"):
                minutos_volando = (time.time() - envio_act["timestamp_salida"]) / 60
                if minutos_volando > umbral_minutos:
                    dron["estado"] = "Extraviado"
                    envio_act["estado_envio"] = "Extraviado"
                    print(f"{Color.ROJO}❌ ¡ALERTA! Dron {dron['id']} (Envío {envio_act['id']}) marcado como EXTRAVIADO ({minutos_volando:.1f} min > {umbral_minutos} min).{Color.RESET}")
                    alertas += 1

    if alertas > 0:
        actualizarBD(data)
    else:
        print(f"{Color.VERDE}✅ Toda la flota opera dentro del límite seguro ({umbral_minutos} min).{Color.RESET}")

def ver_reportes_historicos():
    limpiar_pantalla()
    data = cargarBD()
    if not data:
        return

    print(f"{Color.CYAN}\n--- 📊 REPORTES HISTÓRICOS Y RENDIMIENTO ---{Color.RESET}")
    envios = data.get("envios", [])
    print(f"Total de envíos registrados: {len(envios)}")

    if envios:
        print(f"\n{'ID ENVÍO':<10} | {'CLIENTE':<10} | {'DRON':<10} | {'DESTINO':<22} | {'ESTADO':<12} | {'TIEMPO REAL'}")
        print("-" * 88)
        for e in envios:
            destino = f"{e['municipio_destino']} ({e['estado_destino']})"
            t_real = f"{e['tiempo_real_vuelo_minutos']} min" if e.get("tiempo_real_vuelo_minutos") else "En curso"
            print(f"{e['id']:<10} | {e['cliente_id']:<10} | {e['dron_id']:<10} | {destino:<22} | {e['estado_envio']:<12} | {t_real}")
        print("-" * 88)

    print(f"\n{Color.CYAN}Promedios Históricos por Estado:{Color.RESET}")
    estados_hist = data.get("historial_eta", {}).get("estados", {})
    if not estados_hist:
        print(" - Aún no hay entregas finalizadas para calcular promedios por Estado.")
    else:
        for edo, info in estados_hist.items():
            print(f" - {edo}: {info.get('promedio_minutos', 'N/A')} min ({len(info.get('tiempos_minutos', []))} entregas)")

    print(f"\n{Color.CYAN}Promedios Históricos por Municipio:{Color.RESET}")
    munis_hist = data.get("historial_eta", {}).get("municipios", {})
    if not munis_hist:
        print(" - Aún no hay entregas finalizadas para calcular promedios por Municipio.")
    else:
        for muni, info in munis_hist.items():
            print(f" - {muni} ({info.get('estado')}): {info.get('promedio_minutos', 'N/A')} min ({len(info.get('tiempos_minutos', []))} entregas)")

# ==============================================================================
# MENÚS DE NAVEGACIÓN PRINCIPAL Y SUBMENÚS
# ==============================================================================
def menu_cliente(cliente_actual):
    while True:
        limpiar_pantalla()
        print(f"{Color.CYAN}\n=============================================={Color.RESET}")
        print(f"{Color.VERDE}👤 PANEL DEL CLIENTE: {cliente_actual.nombre} ({cliente_actual.id}){Color.RESET}")
        print(f"{Color.CYAN}=============================================={Color.RESET}")
        print("1. Ver estado de mis envíos")
        print("2. Consultar tiempo estimado (ETA) hacia mi ubicación")
        print("3. Confirmar 'Recibí mi paquete'")
        print("4. Cerrar Sesión")

        opcion = pedir_entero(f"\n{Color.AMARILLO}Selecciona una opción (1-4): {Color.RESET}", 1, 4)

        if opcion == 1:
            ver_mis_envios(cliente_actual)
            pausar()
        elif opcion == 2:
            consultar_mi_eta(cliente_actual)
            pausar()
        elif opcion == 3:
            recibir_paquete(cliente_actual)
            pausar()
        elif opcion == 4:
            print(f"{Color.AMARILLO}Cerrando sesión de cliente...{Color.RESET}")
            time.sleep(1)
            break

def menu_operador(operador_actual):
    while True:
        limpiar_pantalla()
        print(f"{Color.CYAN}\n========================================{Color.RESET}")
        print(f"{Color.VERDE}👨‍💻 PANEL DE OPERADOR: {operador_actual.nombre} ({operador_actual.id}){Color.RESET}")
        print(f"{Color.CYAN}========================================{Color.RESET}")
        print("1. Ver estado de la flota en tiempo real")
        print("2. Despachar un envío a un cliente")
        print("3. Verificar alerta de drones extraviados")
        print("4. Visualizar reportes históricos")
        print("5. Cerrar Sesión")

        opcion = pedir_entero(f"\n{Color.AMARILLO}Selecciona una opción (1-5): {Color.RESET}", 1, 5)

        if opcion == 1:
            ver_flota()
            pausar()
        elif opcion == 2:
            despachar_envio(operador_actual)
            pausar()
        elif opcion == 3:
            verificar_extraviados()
            pausar()
        elif opcion == 4:
            ver_reportes_historicos()
            pausar()
        elif opcion == 5:
            print(f"{Color.AMARILLO}Cerrando sesión de operador...{Color.RESET}")
            time.sleep(1)
            break

def menu_principal():
    while True:
        limpiar_pantalla()
        print(f"{Color.CYAN}\n===================================={Color.RESET}")
        print(f"{Color.VERDE}🚁 BIENVENIDO A SKYTRACK CLI{Color.RESET}")
        print(f"{Color.CYAN}===================================={Color.RESET}")
        print("1. Iniciar sesión como Cliente")
        print("2. Iniciar sesión como Operador")
        print("3. Registrar nuevo usuario (Cliente / Operador)")
        print("4. Salir del sistema")

        opcion = pedir_entero(f"\n{Color.AMARILLO}Selecciona una opción (1-4): {Color.RESET}", 1, 4)

        if opcion == 1:
            cliente_logueado = login_cliente()
            if cliente_logueado:
                menu_cliente(cliente_logueado)
            else:
                pausar()
        elif opcion == 2:
            operador_logueado = login_operador()
            if operador_logueado:
                menu_operador(operador_logueado)
            else:
                pausar()
        elif opcion == 3:
            registrar_usuario()
            pausar()
        elif opcion == 4:
            print(f"{Color.VERDE}¡Gracias por usar SkyTrack! Apagando sistemas...{Color.RESET}")
            break

if __name__ == "__main__":
    menu_principal()