import json
from models.afd import AFD
from models.transition import Transition


def guardar_afd(afd: AFD, nombre_archivo: str):
    """Guarda el AFD en un archivo JSON"""
    datos = {
        "estados": list(afd.estados.keys()),
        "alfabeto": list(afd.alfabeto),
        "estado_inicial": afd.estado_inicial,
        "estados_aceptacion": list(afd.estados_aceptacion),
        "transiciones": [
            {
                "origen": t.current_state,
                "simbolo": t.symbol,
                "destino": t.next_state
            }
            for t in afd.transiciones
        ]
    }

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
    print(f"AFD guardado exitosamente en '{nombre_archivo}'")


def cargar_afd(nombre_archivo: str) -> AFD:
    """Carga un AFD desde un archivo JSON"""
    afd = AFD()
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        # Cargar estados
        for estado in datos["estados"]:
            afd.agregar_estado(estado)

        # Cargar alfabeto
        for simbolo in datos["alfabeto"]:
            afd.agregar_simbolo(simbolo)

        # Cargar estado inicial
        if datos["estado_inicial"]:
            afd.establecer_estado_inicial(datos["estado_inicial"])

        # Cargar estados de aceptación
        for estado in datos["estados_aceptacion"]:
            afd.agregar_estado_aceptacion(estado)

        # Cargar transiciones
        for transicion in datos["transiciones"]:
            afd.agregar_transicion(
                transicion["origen"],
                transicion["simbolo"],
                transicion["destino"]
            )

        print(f"AFD cargado exitosamente desde '{nombre_archivo}'")
        return afd

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe")
    except json.JSONDecodeError:
        print(f"Error: El archivo '{nombre_archivo}' no tiene un formato JSON válido")
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")

    return afd
