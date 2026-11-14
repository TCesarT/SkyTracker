import time
from typing import List, Optional, Dict, Any

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
        return [envio for envio in todos_los_envios if envio.cliente_id == self.idi]
    
    def desde_dict(cls, d: Dict[str, Any]) -> 'Cliente':
        """Convierte un diccionario de la BD en una instancia de Cliente."""
        return cls(
            id_usuario=d["id"],
            nombre=d["nombre"],
            contrasena=d["contrasena"],
            estado=d["estado"],
            municipio=d["municipio"],
            direccion=d["direccion"]
        )

    def a_dict(self) -> Dict[str, Any]:
        """Convierte la instancia de Cliente en un diccionario para la BD."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "estado": self.estado,
            "municipio": self.municipio,
            "direccion": self.direccion
        }

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

    def desde_dict(cls, d: Dict[str, Any]) -> 'Operador':
        """Convierte un diccionario de la BD en una instancia de Operador."""
        return cls(
            id_usuario=d["id"],
            nombre=d["nombre"],
            contrasena=d["contrasena"]
        )

    def a_dict(self) -> Dict[str, Any]:
        """Convierte la instancia de Operador en un diccionario para la BD."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contrasena": self.contrasena
        }

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

    def desde_dict(cls, d: Dict[str, Any]) -> 'Dron':
        """Convierte un diccionario de la BD en una instancia de Dron."""
        return cls(
            id_dron=d["id"],
            modelo=d["modelo"],
            estado=d.get("estado", "Disponible"),
            envio_activo_id=d.get("envio_activo_id")
        )

    def a_dict(self) -> Dict[str, Any]:
        """Convierte la instancia de Dron en un diccionario para la BD."""
        return {
            "id": self.id,
            "modelo": self.modelo,
            "estado": self.estado,
            "envio_activo_id": self.envio_activo_id
        }

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

    def desde_dict(cls, d: Dict[str, Any]) -> 'Envio':
        """Convierte un diccionario de la BD en una instancia de Envio."""
        return cls(
            id_envio=d["id"],
            dron_id=d["dron_id"],
            cliente_id=d["cliente_id"],
            estado_destino=d["estado_destino"],
            municipio_destino=d["municipio_destino"],
            direccion_destino=d["direccion_destino"],
            operador_id=d["operador_id"],
            eta_minutos=d.get("eta_minutos"),
            estado_envio=d.get("estado_envio", "En Camino"),
            timestamp_salida=d.get("timestamp_salida"),
            timestamp_entrega=d.get("timestamp_entrega"),
            timestamp_retorno=d.get("timestamp_retorno"),
            tiempo_real_vuelo_minutos=d.get("tiempo_real_vuelo_minutos")
        )

    def a_dict(self) -> Dict[str, Any]:
        """Convierte la instancia de Envio en un diccionario para la BD."""
        return {
            "id": self.id,
            "dron_id": self.dron_id,
            "cliente_id": self.cliente_id,
            "estado_destino": self.estado_destino,
            "municipio_destino": self.municipio_destino,
            "direccion_destino": self.direccion_destino,
            "estado_envio": self.estado_envio,
            "timestamp_salida": self.timestamp_salida,
            "timestamp_entrega": self.timestamp_entrega,
            "timestamp_retorno": self.timestamp_retorno,
            "eta_minutos": self.eta_minutos,
            "tiempo_real_vuelo_minutos": self.tiempo_real_vuelo_minutos,
            "operador_id": self.operador_id
        }

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