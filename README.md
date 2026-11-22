# Zyrox Announcer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Mensajero comunitario para publicar anuncios formateados en Discord mediante un **webhook oficial**.
Usa la función oficial de webhooks: **no usa tu cuenta, no necesita token y no te puede banear**.

El remitente de los mensajes es **Zyrox**, con su banner animado al abrir.
El crédito `Creado por Norvy`.

---

## Cómo funciona

Los mensajes viven en la carpeta `mensajes/` como archivos `.txt`. No se crean desde el CMD:
tú creas el `.txt` con el Bloc de notas, pegas tu mensaje y Zyrox te muestra un menú para
elegir cuál(es) enviar.

Puedes seleccionar **uno o varios** mensajes en una sola ejecución.

---

## Estructura

```
Zyrox-Announcer/
├── zyrox_announcer.py      <- el script
├── README.md               <- este archivo
├── LICENSE                 <- licencia MIT
├── requirements.txt
├── evidencias/
│   └── ejemplo como se ve en discord.png   <- captura de referencia
└── mensajes/
    ├── actualizacion.txt   <- ejemplo: trivia de los viernes
    ├── bienvenida.txt      <- ejemplo: bienvenida a la comunidad
    └── mantenimiento.txt   <- ejemplo: aviso de mantenimiento
```

> Los `.txt` de ejemplo son solo eso: **ejemplos**. Míralos, cámbialos o bórralos.

---

## Paso 1 - Requisitos

Python instalado (https://python.org, marca **Add Python to PATH**).

```
pip install requests
```

O desde esta carpeta: `pip install -r requirements.txt`

---

## Paso 2 - Crear el webhook

1. Activa el **Modo desarrollador** en *Ajustes de usuario > Avanzado*.
2. En tu servidor: **Ajustes del servidor > Integraciones > Webhooks > Nuevo webhook**.
3. Elige el canal y copia la **URL del webhook**.
4. En la configuración del webhook puedes ponerle **nombre y foto (avatar)**. Esa foto es la
   que se verá en Discord: **el script no la cambia**.

> El canal **no** se configura en el script: la URL del webhook ya apunta al canal que elegiste.
> Si solo vas a usar **un canal**, pega la URL una sola vez en `WEBHOOK_URL` (Paso 3) y
> después solo das **Enter** cuando te la pida. Si usas varios canales, pega la URL que
> corresponda en el momento y no toques nada más.

---

## Paso 3 - Editar el código con un editor (recomendado)

**Usa un editor de código como Visual Studio Code** (https://code.visualstudio.com) con la
extensión de Python. Es mucho más cómodo que el Bloc de notas. Abre esta carpeta en VS Code:

```
Archivo > Abrir carpeta... > Zyrox-Announcer
```

Edita solo la parte de arriba de `zyrox_announcer.py`:

```python
WEBHOOK_URL = "PEGA_AQUI_LA_URL_DEL_WEBHOOK"   # tu URL del paso 2
NOMBRE_REMITENTE = "ZYROX"                     # nombre del remitente (el banner lo dibuja en mayusculas)
PERMITIR_EVERYONE = True                       # si @everyone notifica o solo se ve
ENTRE_MENSAJES = 2                             # pausa entre mensajes
```

- `NOMBRE_REMITENTE` define el **nombre** que se ve en Discord. El banner del inicio se
  dibuja con ese mismo nombre (en mayúsculas). Es el equivalente a "cambiarle el tema".
- La **foto/avatar NO se configura acá**: se pone en el webhook desde Discord
  (*Ajustes del servidor > Integraciones > Webhooks > editar webhook > Avatar*).
  Zyrox respeta esa foto automáticamente.
- Si prefieres usar el **nombre que le pusiste al webhook en Discord**, borra o comenta la
  línea `"username": NOMBRE_REMITENTE,` dentro del `payload` en el script.
- Si dejas `WEBHOOK_URL` sin pegar, Zyrox te la pide al abrirlo.

---

## Paso 4 - Crear tus mensajes (sin tocar el código)

1. Entra a la carpeta `mensajes/`.
2. Crea un **Nuevo documento de texto** con el Bloc de notas.
3. Pega tu mensaje adentro y guárdalo como `nombre.txt`
   (ej. `mantenimiento.txt`, `noche_de_juegos.txt`). El nombre del archivo es el que
   aparecerá en el menú (se muestran sin guiones bajos).

### Tu mensaje debe verse bonito y organizado

Prepara el `.txt` **exactamente como quieres que se vea en tu Discord**. Respeta los
símbolos, los espacios y los saltos de línea:

- Títulos con `#`, `##`, `###`
- Negritas `**texto**`, cursivas `*texto*`, subrayado `__texto__`, tachado `~~texto~~`
- Listas con `- item` y numeradas con `1. item`
- Spoilers `||texto||` y citas `> texto`
- Enlaces: Discord los convierte en link/embed automáticamente
- Menciones: `<@ID_USUARIO>`, `<@&ID_ROL>`, `<#ID_CANAL>`, `@everyone`
- Emojis: **caso avanzado**, ver la sección más abajo

> Límite de Discord: **2000 caracteres** por mensaje. Zyrox avisa si te pasas.

> **Lo más funcional:** mensajes organizaditos con títulos, negritas, listas, citas y enlaces,
> **sin emojis**. Los emojis requieren saber el ID exacto y son más propensos a no mostrarse.

### Así se ve en Discord

Esta es una captura de un mensaje armado en un `.txt` y enviado con Zyrox:

![Ejemplo de mensaje en Discord](evidencias/ejemplo%20como%20se%20ve%20en%20discord.png)

El resultado es idéntico a lo que escribiste en el `.txt`: respeta saltos de línea,
espacios, títulos, listas y citas. Si el mensaje tiene emojis, también se verán, pero para
eso hay que saber sus IDs (sección siguiente).

### Emojis (solo si sabes los IDs)

Los emojis son la parte más complicada. No alcanza con escribir `:nombre:`: necesitas
**el ID numérico del emoji** y pegarlo en el formato exacto:

- Normal: `<:nombre:ID>`
- Animado: `<a:nombre:ID>`

El `nombre` es solo decorativo; lo que Discord usa es el **ID** (18-19 dígitos). Para sacarlo:
**Modo desarrollador** activado → clic derecho sobre el emoji → **Copiar ID**. Ojo: lleva
**dos** dos-puntos, no tres. Si el emoji es de otro servidor, puede que no se muestre salvo
que tu servidor tenga Nitro.

Ejemplo de mensaje con emojis y sus IDs (los IDs son de ejemplo, cámbialos por los reales):

```
## Evento de la comunidad

Nos vemos el viernes a las 20:00 <:clock:987654321098765432>

### Premios
- 1 lugar: <:trophy:987654321098765431> <@&123456789012345679>
- 2 lugar: <a:confetti:987654321098765430>

Reacciona con <:party:123456789012345678> para sumarte.
```

Si te parece mucho lío, **usa el mismo mensaje sin emojis**: queda igual de organizado y
funciona siempre.

### No sabes redactarlo? Usa una IA

Puedes pedirle a una IA que te arme el mensaje con el formato listo. Por ejemplo:

> "Escribe un anuncio para mi servidor de Discord sobre un mantenimiento el sábado a las 03:00.
> Usa markdown de Discord con título `##`, lista con `-`, una cita `>` y un spoiler `||@everyone||`.
> Devuélveme solo el texto listo para pegar en un .txt, sin explicaciones."

Luego pegas lo que te devuelva en tu `.txt` y listo. Los mensajes de ejemplo de esta
carpeta fueron preparados con ayuda de **Big Pickle**, la IA de OpenCode.

Si ya no vas a usar un mensaje, **borra el `.txt`**. Si quieres mejorarlo, **edita el `.txt`**
y vuelve a abrir Zyrox. No hace falta tocar el código.

---

## Paso 5 - Ejecutar y elegir mensajes

```
python zyrox_announcer.py
```

En VS Code: abre la carpeta, elige el intérprete y dale al botón **▶ Run**.

Al abrir sale la animación:

```
  Bienvenido a ZYROX

##########  ...   (banner gigante dibujándose bloque por bloque)

  Mensajero comunitario  |  Creado por Norvy
```

Luego aparece el menú. **La primera vez** te pide el primer mensaje:

```
  Mensajes disponibles:
    [1] actualizacion
    [2] bienvenida
    [3] mantenimiento

  Elige el PRIMER mensaje escribiendo su numero y dale Enter.
  Numero del mensaje: 1
  Agregado: actualizacion
```

Después de esa primera elección, Zyrox te pregunta **explícitamente** si quieres mandar otro
en la misma petición:

```
  Mensajes disponibles:
    [1] actualizacion  (ya agregado)
    [2] bienvenida
    [3] mantenimiento

  Ya seleccionaste: actualizacion
  Quieres mandar otro en la misma peticion?
    - Escribe el numero y dale Enter para agregarlo
    - O solo dale Enter para terminar y continuar
  Otro numero (o Enter para terminar):
```

### Cómo funciona la selección

- Eliges el **primer mensaje** escribiendo su número (ej. `1`) y das Enter.
- Zyrox te dice lo que ya seleccionaste y te pregunta si quieres **otro en la misma petición**.
- Si quieres **agregar más**, escribes otro número (o varios separados por coma, ej. `2,3`)
  y das Enter. Los que ya elegiste aparecen marcados como `(ya agregado)`.
- Si **no quieres más mensajes**, simplemente **das otro Enter sin escribir ningún número**.
  Ahí Zyrox termina la selección y sigue con el envío.

Ejemplo: elegir `1`, dar Enter, y luego dar Enter otra vez = se enviará solo el mensaje 1.
Ejemplo: elegir `1`, Enter, elegir `3`, Enter, Enter = se enviarán los mensajes 1 y 3.

### Después de la selección

1. Te pregunta la URL del webhook: pega otra o **Enter** para usar la configurada.
2. Detecta menciones que ya estén en los mensajes (`<@ID>`, `<@&ID>`, `@everyone`) y te dice
   cuáles encontró.
3. Te pide **IDs extra de usuarios y roles**. Si el mensaje ya los trae, das **Enter** en
   ambas. Acepta varios separados por coma: `1234220113515778108, 9876543210987654321`.
4. Muestra la **vista previa** de cada mensaje con el formato intacto.
5. **Enter para enviar** / `n` para cancelar. Si elegiste varios, van con `ENTRE_MENSAJES`
   segundos de pausa entre ellos.

---

## Opciones de la configuración

| Variable | Qué hace |
|---|---|
| `WEBHOOK_URL` | Webhook por defecto (Enter lo usa; pegar otro lo reemplaza) |
| `NOMBRE_REMITENTE` | Nombre con el que se ve el mensaje en Discord |
| `PERMITIR_EVERYONE` | `True` = `@everyone` notifica; `False` = solo se ve |
| `ENTRE_MENSAJES` | Pausa entre mensajes cuando envías varios |

---

## Funciona sin Discord abierto

Sí. Zyrox hace una petición HTTP a Discord; no necesita que tengas el cliente abierto.
Solo internet y que el webhook siga existiendo.

---

## Licencia

Distribuido bajo la licencia **MIT**. Puedes usar, modificar y compartir el proyecto
incluso en usos comerciales, manteniendo el aviso de copyright. Ver [LICENSE](LICENSE).

---

## Subir a GitHub

Cuando tengas el repo listo:

```
git init
git add .
git commit -m "Zyrox Announcer - mensajero comunitario por webhook"
git remote add origin TU_URL_DE_GITHUB
git branch -M main
git push -u origin main
```

---

**Creado por Norvy** · Ejemplos y documentación con ayuda de **Big Pickle** (IA de OpenCode) · Licencia MIT.
