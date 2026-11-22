"""
ZYROX ANNOUNCER - Mensajero comunitario
Creditos en el CMD: Creado por Norvy.

Los mensajes viven en la carpeta 'mensajes/' como archivos .txt.
El script muestra un menu para elegir cuales enviar y admite un webhook
distinto sin editar el codigo.
"""

import os
import re
import sys
import time

import requests

# ============================================================
# CONFIGURACION - EDITA UNA SOLA VEZ CON UN EDITOR (VS Code)
# ============================================================

# URL del webhook (Ajustes del servidor > Integraciones > Webhooks)
WEBHOOK_URL = "https://discord.com/api/webhooks/1573884453833547867/r-bSRfDd39qZ5Q-ncUSZ-hlCQgeQ7UMWH-m9N5S_3Hhy_P7i_WILIq-P03imt3gg5ONf"

# Nombre que aparecera como remitente del mensaje (reemplaza el del webhook)
NOMBRE_REMITENTE = "ZYROX"

# Si el mensaje trae @everyone / @here, que pinguee de verdad?
PERMITIR_EVERYONE = True

# Segundos entre mensajes cuando envias varios
ENTRE_MENSAJES = 2

# ============================================================

BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_MENSAJES = os.path.join(BASE, "mensajes")

FUENTE = {
    "A": [" ### ", "#   #", "#####", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#### ", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#### ", "#    ", "#####"],
    "F": ["#####", "#    ", "#### ", "#    ", "#    "],
    "G": [" ####", "#    ", "#  ##", "#   #", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["#####", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#  ##", " ## #"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "X": ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "   # ", "  #  ", " #   ", "#####"],
    " ": ["     ", "     ", "     ", "     ", "     "],
}


def make_banner(texto, escala=2):
    filas = ["", "", "", "", ""]
    for ch in texto.upper():
        glifo = FUENTE.get(ch, FUENTE[" "])
        for i in range(5):
            filas[i] += glifo[i] + " "
    resultado = []
    for fila in filas:
        agrandada = "".join(c * escala for c in fila)
        for _ in range(escala):
            resultado.append(agrandada)
    return "\n".join(resultado)


def animar_texto(texto, retardo=0.04):
    """Escribe letra por letra, como maquina de escribir."""
    for ch in texto:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(retardo)
    print()


def animar_banner(banner, retardo=0.004):
    """Dibuja el banner bloque por bloque."""
    for fila in banner.split("\n"):
        for ch in fila:
            sys.stdout.write(ch)
            sys.stdout.flush()
            if ch != " ":
                time.sleep(retardo)
        print()


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def cargar_mensajes():
    """Lee todos los .txt de la carpeta mensajes/."""
    if not os.path.isdir(CARPETA_MENSAJES):
        os.makedirs(CARPETA_MENSAJES)
        return []
    datos = []
    for archivo in sorted(os.listdir(CARPETA_MENSAJES)):
        if archivo.lower().endswith(".txt"):
            ruta = os.path.join(CARPETA_MENSAJES, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                datos.append((archivo[:-4].replace("_", " "), f.read()))
    return datos


def elegir_mensajes(disponibles):
    if not disponibles:
        print("\n  No hay mensajes todavia.")
        print("  Crea un archivo .txt dentro de la carpeta 'mensajes/',")
        print("  pega tu mensaje ahi con el Bloc de notas y vuelve a abrir.\n")
        return []

    seleccionados = []
    primera = True

    while True:
        print("\n  Mensajes disponibles:")
        for i, (nombre, _) in enumerate(disponibles, 1):
            marca = "  (ya agregado)" if disponibles[i - 1] in seleccionados else ""
            print(f"    [{i}] {nombre}{marca}")

        if primera:
            print("\n  Elige el PRIMER mensaje escribiendo su numero y dale Enter.")
            prompt = "  Numero del mensaje: "
        else:
            nombres = ", ".join(n for n, _ in seleccionados)
            print(f"\n  Ya seleccionaste: {nombres}")
            print("  Quieres mandar otro en la misma peticion?")
            print("    - Escribe el numero y dale Enter para agregarlo")
            print("    - O solo dale Enter para terminar y continuar")
            prompt = "  Otro numero (o Enter para terminar): "

        op = input(prompt).strip()
        if not op or op == "0":
            break

        numeros = [int(p) for p in re.split(r"[,\s]+", op) if p.isdigit()]
        validos = [n for n in numeros if 1 <= n <= len(disponibles)]
        if not validos:
            print("  Opcion no valida.")
            continue

        agregados_ahora = []
        for n in validos:
            if disponibles[n - 1] not in seleccionados:
                seleccionados.append(disponibles[n - 1])
                agregados_ahora.append(disponibles[n - 1][0])

        if agregados_ahora:
            print(f"  Agregado: {', '.join(agregados_ahora)}")
        else:
            print("  Ese mensaje ya estaba agregado.")

        primera = False

    print(f"\n  Seleccion final: {len(seleccionados)} mensaje(s). Continuando...")
    return seleccionados


def parsear_ids(texto):
    """'123, 456' o '<@123> <@&456>' -> ['123', '456']."""
    if not texto.strip():
        return []
    limpio = re.sub(r"<@&?(\d+)>", r"\1", texto)
    return [p for p in re.split(r"[,\s]+", limpio.strip()) if p.isdigit()]


def menciones_del_mensaje(mensaje):
    usuarios = re.findall(r"<@!?(\d+)>", mensaje)
    roles = re.findall(r"<@&(\d+)>", mensaje)
    everyone = bool(re.search(r"@(everyone|here)\b", mensaje, re.I))
    return usuarios, roles, everyone


def main():
    limpiar()
    animar_texto("  Bienvenido a ", 0.05)
    animar_texto(NOMBRE_REMITENTE, 0.12)
    print()
    animar_banner(make_banner(NOMBRE_REMITENTE, escala=2))
    print("\n  Mensajero comunitario  |  Creado por Norvy\n")

    # 1) Elegir mensajes
    elegidos = elegir_mensajes(cargar_mensajes())
    if not elegidos:
        return

    # 2) Webhook: Enter para usar el configurado
    print("\n  Webhook")
    if "PEGA_AQUI" in WEBHOOK_URL:
        print("  (Todavia no configuraste WEBHOOK_URL en el codigo)")
        url = ""
        while not url.startswith("https://discord.com/api/webhooks/"):
            url = input("  Pega la URL del webhook: ").strip()
            if not url.startswith("https://discord.com/api/webhooks/"):
                print("  No parece un webhook de Discord. Intenta de nuevo.")
    else:
        print(f"  Configurada: {WEBHOOK_URL[:55]}...")
        url = input("  Pega otra URL o Enter para usar la configurada: ").strip()
        if not url:
            url = WEBHOOK_URL
        elif not url.startswith("https://discord.com/api/webhooks/"):
            print("  URL no valida. Se usara la configurada.")
            url = WEBHOOK_URL

    # 3) Contenidos (sin firma: Norvy solo aparece en el CMD)
    contenidos = []
    for nombre, texto in elegidos:
        contenido = texto.rstrip()
        contenidos.append(contenido)
        if len(contenido) > 2000:
            print(f"  AVISO: '{nombre}' tiene {len(contenido)} caracteres (maximo 2000).")

    # 4) Menciones
    usuarios, roles, everyone = [], [], False
    for c in contenidos:
        u, r, e = menciones_del_mensaje(c)
        usuarios += u
        roles += r
        everyone = everyone or e

    detectadas = []
    if usuarios:
        detectadas.append(f"{len(set(usuarios))} usuario(s)")
    if roles:
        detectadas.append(f"{len(set(roles))} rol(es)")
    if everyone:
        detectadas.append("@everyone/@here")
    print("\n  Menciones ya incluidas en los mensajes: " + (", ".join(detectadas) or "ninguna"))

    entrada_u = input("  IDs de USUARIOS extra (coma; Enter=omitir): ")
    entrada_r = input("  IDs de ROLES extra   (coma; Enter=omitir): ")

    usuarios = list(dict.fromkeys(usuarios + parsear_ids(entrada_u)))
    roles = list(dict.fromkeys(roles + parsear_ids(entrada_r)))

    permitir = {"parse": ["everyone"] if (everyone and PERMITIR_EVERYONE) else []}
    if usuarios:
        permitir["users"] = usuarios
    if roles:
        permitir["roles"] = roles

    # 5) Vista previa
    print("\n  ---------- VISTA PREVIA ----------")
    for i, c in enumerate(contenidos, 1):
        print(f"\n  --- mensaje {i}/{len(contenidos)} ---")
        print(c)
    print("\n  ---------------------------------")

    if input("\nEnter para ENVIAR  |  'n' para cancelar: ").strip().lower() in ("n", "no"):
        print("\nCancelado. No se envio nada.\n")
        return

    # 6) Enviar
    for i, contenido in enumerate(contenidos, 1):
        payload = {
            "content": contenido,
            "username": NOMBRE_REMITENTE,
            "allowed_mentions": permitir,
        }
        print(f"\nEnviando mensaje {i}/{len(contenidos)}...")
        intentos = 0
        while intentos < 2:
            try:
                r = requests.post(url, json=payload, timeout=10)
                if r.status_code in (200, 204):
                    print("  Enviado.")
                    break
                if r.status_code == 429:
                    espera = r.json().get("retry_after", 5)
                    print(f"  Discord pidio esperar {espera} s...")
                    time.sleep(espera)
                    intentos += 1
                    continue
                print(f"  Error {r.status_code}: {r.text[:250]}")
                break
            except requests.RequestException as e:
                print(f"  Error de red: {e}")
                break
        if i < len(contenidos):
            time.sleep(ENTRE_MENSAJES)

    print(f"\nListo. Enviado por {NOMBRE_REMITENTE}.\n")


if __name__ == "__main__":
    main()
