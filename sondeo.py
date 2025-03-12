'''
Herramienta de escaneo de red en Python con Nmap.

Este script obtiene las IPs de las interfaces del equipo y permite al usuario:
1. Escanear la red en busca de dispositivos activos (ping sweep).
2. Guardar las IPs activas en una lista.

Requisitos:
- Python 3
- Tener instalado `nmap`, 
    -por ejemplo: sudo apt update && sudo apt install nmap -y
    -introduciendo la contraseña de sudo
- Ejecutar con permisos adecuados para acceder a la información de red.

'''

# Importamos las librerías necesarias
from subprocess import run  # Para ejecutar comandos del sistema
import re  # Para trabajar con expresiones regulares

# ==============================================
#           MENSAJE DE PRESENTACIÓN
# ==============================================

print("=" * 60)
print(r"""
     _______.  ______   .__   __.  _______   _______   ______   
    /       | /  __  \  |  \ |  | |       \ |   ____| /  __  \  
   |   (----`|  |  |  | |   \|  | |  .--.  ||  |__   |  |  |  | 
    \   \    |  |  |  | |  . `  | |  |  |  ||   __|  |  |  |  | 
.----)   |   |  `--'  | |  |\   | |  '--'  ||  |____ |  `--'  | 
|_______/     \______/  |__| \__| |_______/ |_______| \______/  
                                                                
""")
print("=" * 60)

# ==============================================
#           OBTENER IPs DE LAS INTERFACES
# ==============================================

# Lista para almacenar las interfaces de red y sus direcciones IP
interfaces_list = []

# Lista para almacenar las IPs activas encontradas en el ping sweep
pingsweep_list = []

print("🚀 Ejecutando comando: ip -br -c a")

# Ejecutamos el comando para obtener las direcciones IP de las interfaces del sistema.
comando_ip = ["ip", "-br", "-c", "a"]
resultado_ip = run(comando_ip, capture_output=True, text=True)

# Mostramos la salida del comando en pantalla.
print(resultado_ip.stdout)

# Verificamos si el comando se ejecutó con éxito (código de retorno 0).
if resultado_ip.returncode == 0:
    # Dividimos la salida en líneas para analizarla.
    lineas = resultado_ip.stdout.split('\n')

    # Procesamos cada línea para extraer la información relevante.
    for linea in lineas:
        if linea.strip():  # Ignoramos líneas vacías.
            # Eliminamos secuencias de escape ANSI (colores en la salida de la terminal).
            linea_limpia = re.sub(r'\x1b\[[0-9;]*[mK]', '', linea)
            componentes = linea_limpia.split()

            # Verificamos que la línea tenga al menos 3 elementos antes de continuar.
            if len(componentes) >= 3:
                interfaz = componentes[0]  # Nombre de la interfaz (ejemplo: eth0, wlan0)
                ip = componentes[2]  # Dirección IP con máscara (ejemplo: 192.168.1.10/24)
                interfaces_list.append((interfaz, ip))  # Almacenamos en la lista como tupla
            else:
                print(f"⚠️ Error al procesar la línea: {linea}")

    # ==============================================
    #           SELECCIÓN DE INTERFAZ PARA ESCANEO
    # ==============================================

    # Mostramos las interfaces y sus IPs detectadas.
    print("🖥️  Nuestro ordenador tiene las siguientes IPs e interfaces:")
    for inter, ip in interfaces_list:
        print(f"   ✅ {inter} → {ip}")
    while True:
 
        # Solicitamos al usuario que elija una interfaz para el escaneo de red.
        interfaz_elegida = input("Introduce una interfaz para hacer un ping sweep con nmap: \n")

        # Buscar si la interfaz elegida está en la lista
        ip_nmap = None
        for inter, ip in interfaces_list:
            if inter == interfaz_elegida:
                ip_nmap = ip
                break

        # Si la interfaz es válida, realizamos el escaneo con Nmap
        if ip_nmap:
            print("=" * 60)
            print("🚀 Ejecutando comando: nmap -sn ", ip_nmap)

            try:
                # Ejecutamos Nmap para hacer un ping sweep en la red especificada.
                resultado_ping_sweep = run(["nmap", "-sn", ip_nmap], capture_output=True, text=True)

                # Verificamos si el comando se ejecutó correctamente.
                if resultado_ping_sweep.returncode == 0:
                    # Extraemos las direcciones IP detectadas en la salida de Nmap.
                    ips_encontradas = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', resultado_ping_sweep.stdout)

                    # Guardamos las IPs encontradas en la lista de dispositivos activos.
                    pingsweep_list.extend(ips_encontradas)

                    # Mostramos las IPs encontradas en la red.
                    print("🌐 Las IPs activas en la red son:")
                    print("   📌 ", pingsweep_list)

            except:
                print("⚠️ Se ha producido un error al ejecutar el escaneo.")

            # Mostramos la IP de la interfaz utilizada para el escaneo.
            print("🔍 Escaneo realizado en la red de: ", ip_nmap)
            print("=" * 60)
            break  # Salimos del bucle porque el escaneo ha sido exitoso.

        else:
            # Mensaje de error y explicación
            print("=" * 60)
            print("⚠️ Interfaz no encontrada. Debes escoger una de las siguientes:")
            for inter, _ in interfaces_list:
                print(f"   ✅ {inter}")
            print("🔁 Inténtalo de nuevo.")
            print("=" * 60)
            continue  # Volvemos a pedir al usuario una interfaz válida.

# ==============================================
#           ERROR AL OBTENER LAS IPs
# ==============================================

else:
    # Mostramos un mensaje de error si la ejecución del comando falla.
    print(f"⚠️ Se ha producido un error al obtener las IPs: {resultado_ip.stderr}")
