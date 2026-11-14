# SKYTRACK - SISTEMA DE ENTREGAS CON DRONES
=========================================

Programa de consola para simular y gestionar la logística de una empresa de reparto de paquetes utilizando drones autónomos.

El sistema funciona con dos roles principales:
- **Los Operadores:** Gestionan la flota de drones desde la base, despachan los paquetes y vigilan que ningún dron se pierda.
- **Los Clientes:** Consultan los envíos que van hacia su dirección, ven en tiempo real cuántos minutos faltan para la entrega y confirman la recepción del paquete.

Todos los datos se sincronizan por internet en tiempo real: cualquier acción realizada por un usuario se refleja al instante para los demás.


REQUISITOS
----------

1. **Tener Python 3 instalado.** Se descarga gratuitamente desde:

       https://www.python.org/downloads/

   Al instalar en Windows, es importante marcar la casilla **"Add Python to PATH"**.

   Para verificar si ya está instalado, abrir una terminal (cmd o PowerShell) y escribir:

       python --version

   Si aparece algo como `Python 3.x.x`, ya está listo.

2. **Conexión a internet.** El programa se conecta a una base de datos centralizada en la nube para guardar y sincronizar los datos de los drones y envíos.


COMO EJECUTAR
-------------

Abrir una terminal en la carpeta donde están los archivos del proyecto y escribir:

    python main.py

Si no reconoce el comando, probar con:

    py main.py


USO DEL PROGRAMA
----------------

Al abrir el programa aparece el menú principal con 4 opciones. Se escribe el número y se presiona Enter:

    Opcion 1 - Iniciar sesion como Cliente.
               Permite a los usuarios consultar sus paquetes en camino y
               confirmar cuando hayan recibido su entrega.

    Opcion 2 - Iniciar sesion como Operador.
               Requiere el codigo de seguridad empresarial. Da acceso al panel
               de control para ver toda la flota y despachar drones.

    Opcion 3 - Registrar nuevo usuario (Cliente / Operador).
               Permite crear una cuenta nueva. Al registrar un cliente, el
               sistema valida que el municipio ingresado pertenezca a su estado.

    Opcion 4 - Salir del sistema.


PANEL DEL OPERADOR (OPCION 2)
-----------------------------

Para ingresar como operador se solicita el código empresarial: `SKYTRACK2026`.
Una vez adentro, se cuenta con estas opciones:

  - **Ver estado de la flota:** Muestra una tabla con todos los drones, su estado actual y el paquete que llevan asignado.
  - **Despachar un nuevo envio:** Permite elegir un dron disponible de la base y asignarlo a un cliente para que despegue de inmediato.
  - **Verificar seguridad (Extraviados):** Escanea los drones en vuelo y alerta en color rojo si alguno supera el límite de vuelo seguro (180 minutos).


PANEL DEL CLIENTE (OPCION 1)
----------------------------

Cada cliente solo puede ver la información de sus propios paquetes:

  - **Ver mis pedidos y tiempo estimado:** Muestra los paquetes que vienen en camino, qué dron los transporta, cuántos minutos llevan volando y el tiempo estimado que falta para llegar.
  - **Confirmar "Recibi mi paquete":** Cuando el dron llega a la casa, el cliente confirma la entrega. El sistema detiene el cronómetro y envía al dron de regreso a la base.
  - **Consultar mi tiempo estimado (ETA):** Informa de antemano cuántos minutos tardaría un envío hacia la zona del cliente.


COSAS A TENER EN CUENTA
-----------------------

- **Los datos sí se guardan:** A diferencia de programas locales, aquí todos los despachos, registros y entregas se guardan en la nube al instante.
- **Código secreto de Operador:** El token de seguridad empresarial es `SKYTRACK2026`.
- **Colores de los drones:**
  - 🟢 **Verde (Disponible):** El dron está en la base listo para salir.
  - 🟡 **Amarillo (En Camino / Retornando):** El dron está volando en una misión.
  - 🔴 **Rojo (Extraviado):** El dron tardó demasiado y el sistema activó la alerta.
- **Cálculo inteligente de tiempos (ETA):**
  - Si ya se han hecho entregas en ese municipio, usa el promedio de viajes anteriores.
  - Si es la primera vez que va a ese municipio, usa el promedio general del estado.
  - Si es una zona totalmente nueva, calcula 45 minutos por defecto.
- **El sistema aprende solo:** Cada vez que se confirma la recepción de un paquete, el sistema guarda el tiempo real que duró el vuelo y ajusta los promedios futuros automáticamente.


EJEMPLO DE USO (PASO A PASO)
----------------------------

1. Se abre el programa con `python main.py`.

2. Se escribe **2** para entrar como Operador.
   - Pide el código: se ingresa `SKYTRACK2026`.
   - Pide el usuario y clave: se ingresa `OPE-001` y contraseña `op_andres01`.

3. Se elige la opción de **Despachar un nuevo envio**.
   - El programa muestra los drones libres (por ejemplo `DRN-001`).
   - Se escribe el ID del dron y luego el del cliente (por ejemplo `CLI-001`).
   - El programa calcula el tiempo estimado de llegada, anota la hora de salida y confirma que el dron despegó.

4. Se sale al menú principal y ahora se escribe **1** para entrar como Cliente.
   - Se ingresa el nombre `María González` y la clave `maria123`.
   - Al seleccionar **Ver mis pedidos**, se observa el paquete con los minutos transcurridos en tiempo real.

5. Cuando se elige **Confirmar recepcion de paquete**:
   - El cliente confirma que lo recibió.
   - El programa calcula los minutos reales de viaje, cambia el dron a "Retornando" hacia la base y actualiza el promedio de tiempo para esa zona.


CUENTAS DE PRUEBA YA CREADAS
----------------------------

Para probar el programa de inmediato sin tener que registrarse:

- **Operador:**
  - Código empresarial: `SKYTRACK2026`
  - Usuario: `OPE-001`  |  Contraseña: `op_andres01`

- **Cliente 1:**
  - Nombre: `María González`  |  Contraseña: `maria123`
  - Ubicación: Chacao, Miranda.

- **Cliente 2:**
  - Nombre: `Carlos Pérez`  |  Contraseña: `carlos456`
  - Ubicación: Libertador, Distrito Capital.


PROBLEMAS COMUNES
-----------------

- **Si aparece "'python' no se reconoce como un comando":**
  Reinstalar Python asegurándose de marcar la casilla "Add Python to PATH".

- **Si dice "Error de conexión: verifica tu conexión a internet":**
  Revisar que la computadora tenga acceso a internet para comunicarse con la base de datos en la nube.

- **Si dice "Token empresarial incorrecto":**
  Verificar que el código esté escrito exactamente como `SKYTRACK2026` (en mayúsculas y sin espacios).

- **Si al registrar un cliente dice "El municipio no pertenece a este estado":**
  El sistema valida la geografía real. Puedes escribir `LISTAR` para ver en pantalla todos los municipios válidos para ese estado.
