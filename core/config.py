# filepath: e:\www_develop\mud-pi\config.py

# Diccionario de alias para las salidas típicas
COMMAND_ALIASES = {
    "n": "norte",
    "s": "sur",
    "e": "este",
    "o": "oeste",
    "ne": "noreste",
    "no": "noroeste",
    "se": "sudeste",
    "so": "sudoeste",
    "ar": "arriba",
    "ab": "abajo",
    "de": "dentro",
    "fu": "fuera",
    "quitar":"abandonar"
}

# Reversed dictionary for aliases (full name -> alias)
REVERSED_COMMAND_ALIASES = {v: k for k, v in COMMAND_ALIASES.items()}

# Descripción de los niveles: infrarojo, rojo, naranja, amarillo, verde, índigo, morado, ultravioleta, x
NIVEL_DISPLAY = {
    0: "IR",
    1: "R",
    2: "N",
    3: "Y",
    4: "V",
    5: "I",
    6: "M",
    7: "UV",
    8: "X"
}

# Colores ANSI para los niveles
NIVEL_COLOR = {
    0: "\033[90m",  # IR (37)
    1: "\033[91m",  # R
    2: "\033[33m",  # N
    3: "\033[93m",  # Y
    4: "\033[92m",  # V
    5: "\033[96m",  # I (o 94)
    6: "\033[95m",  # M
    7: "\033[35m",  # UV
    8: "\033[97m",   # X
    "reset": "\033[0m"  # Reset color
}
