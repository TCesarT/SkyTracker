import time
from typing import List, Optional

# CLASE PADRE: Usuario
class Usuario:
    """Clase base para todos los usuarios del sistema."""
    def __init__(self, id_usuario: str, nombre: str, contra: str):
        self.id = id_usuario
        self.nombre = nombre
        self.contra = contra

    def autenticar(self, intento_contra: str) -> bool:
        """Método de autenticación común para cualquier usuario."""
        return self.contra == intento_contra

# CLASE HIJA: Cliente
class Cliente(Usuario):
    """Hereda de Usuario e incluye datos de ubicación."""
    def __init__(self, id_usuario: str, nombre: str, contra: str, estado: str, municipio: str, direccion: str):
        super().__init__(id_usuario, nombre, contra)
        self.estado = estado
        self.municipio = municipio
        self.direccion = direccion

    def filtrar_envios_propios(self, todos_los_envios: List['Envio']) -> List['Envio']:
        """Filtra y retorna solo los envíos que pertenecen a este cliente."""
        return [envio for envio in todos_los_envios if envio.cliente_id == self.id]

# CLASE HIJA: Operador
class Operador(Usuario):
    """Hereda de Usuario e incluye validación de seguridad empresarial."""
    # Token extraído de la configuración de la BD y la interfaz de usuario
    TOKEN_EMPRESARIAL = "SKYTRACK2026" 

    def __init__(self, id_usuario: str, nombre: str, contrasena: str):
        super().__init__(id_usuario, nombre, contrasena)

    def validar_token_seguridad(self, token_intento: str) -> bool:
        """Valida el token de seguridad empresarial requerido para operadores."""
        return token_intento == self.TOKEN_EMPRESARIAL

# CLASE: Dron
class Dron:
    """Manejo de la flota de drones y sus estados."""
    ESTADOS_PERMITIDOS = ["Disponible", "En Camino", "Entregado", "Retornando", "Extraviado"]

    def __init__(self, id_dron: str, modelo: str, estado: str = "Disponible", envio_activo_id: Optional[str] = None):
        self.id = id_dron
        self.modelo = modelo
        self.estado = estado
        self.envio_activo_id = envio_activo_id

    def actualizar_estado(self, nuevo_estado: str):
        """Valida y actualiza el estado del dron."""
        if nuevo_estado in self.ESTADOS_PERMITIDOS:
            self.estado = nuevo_estado
        else:
            raise ValueError(f"Estado '{nuevo_estado}' no válido. Opciones: {self.ESTADOS_PERMITIDOS}")

# CLASE: Envio
class Envio:
    """Vinculación de dron, cliente, ubicaciones y marcas de tiempo."""
    def __init__(self, id_envio: str, dron_id: str, cliente_id: str, 
                 estado_destino: str, municipio_destino: str, direccion_destino: str, 
                 operador_id: str, eta_minutos: int):
        
        # Vinculaciones
        self.id = id_envio
        self.dron_id = dron_id
        self.cliente_id = cliente_id
        self.operador_id = operador_id
        
        # Ubicación
        self.estado_destino = estado_destino
        self.municipio_destino = municipio_destino
        self.direccion_destino = direccion_destino
        
        # Manejo de Estados y Marcas de tiempo (Timestamps)
        self.estado_envio = "En Camino"
        self.timestamp_salida = time.time()
        self.timestamp_entrega = None
        self.timestamp_retorno = None
        
        # Métricas de vuelo
        self.eta_minutos = eta_minutos
        self.tiempo_real_vuelo_minutos = None

    def registrar_entrega(self):
        """Registra el momento exacto de la entrega y cambia el estado."""
        self.timestamp_entrega = time.time()
        self.estado_envio = "Entregado"

    def registrar_retorno(self):
        """Registra el momento en que el dron vuelve a la base."""
        self.timestamp_retorno = time.time()
        self.estado_envio = "Retornando"
        if self.timestamp_salida:
            self.tiempo_real_vuelo_minutos = (self.timestamp_retorno - self.timestamp_salida) / 60