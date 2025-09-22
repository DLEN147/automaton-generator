import os
from models.afd import AFD
from data.serializer import guardar_afd, cargar_afd


class SimuladorAFD:
    """
    Clase principal que maneja la interfaz de usuario del simulador
    """

    def __init__(self):
        self.afd = AFD()

    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("    SIMULADOR DE AUTÓMATAS FINITOS DETERMINISTAS")
        print("="*50)
        print("1. Crear nuevo AFD")
        print("2. Evaluar cadena")
        print("3. Generar cadenas del lenguaje")
        print("4. Mostrar información del AFD")
        print("5. Guardar AFD en archivo")
        print("6. Cargar AFD desde archivo")
        print("7. Salir")
        print("-"*50)

    def crear_afd(self):
        """Permite al usuario crear un nuevo AFD"""
        print("\n=== CREACIÓN DE NUEVO AFD ===")
        self.afd = AFD()

        estados_input = input("Ingrese los estados separados por comas (ej: q0,q1,q2): ").strip()
        estados = [estado.strip() for estado in estados_input.split(",") if estado.strip()]
        for estado in estados:
            self.afd.agregar_estado(estado)

        alfabeto_input = input("Ingrese los símbolos del alfabeto separados por comas (ej: 0,1): ").strip()
        simbolos = [simbolo.strip() for simbolo in alfabeto_input.split(",") if simbolo.strip()]
        for simbolo in simbolos:
            self.afd.agregar_simbolo(simbolo)

        estado_inicial = input("Ingrese el estado inicial: ").strip()
        self.afd.establecer_estado_inicial(estado_inicial)

        aceptacion_input = input("Ingrese los estados de aceptación separados por comas: ").strip()
        estados_aceptacion = [estado.strip() for estado in aceptacion_input.split(",") if estado.strip()]
        for estado in estados_aceptacion:
            self.afd.agregar_estado_aceptacion(estado)

        print("Ingrese las transiciones en el formato: estado_origen,simbolo,estado_destino (fin para terminar)")
        while True:
            transicion = input("Transición: ").strip()
            if transicion.lower() == 'fin':
                break
            partes = transicion.split(',')
            if len(partes) == 3:
                origen, simbolo, destino = [parte.strip() for parte in partes]
                self.afd.agregar_transicion(origen, simbolo, destino)

        print("\n✓ AFD creado exitosamente!")
        self.afd.mostrar_info()

    def evaluar_cadena(self):
        """Evalúa una cadena con el AFD actual"""
        cadena = input("Ingrese la cadena a evaluar: ").strip()
        es_aceptada, recorrido = self.afd.procesar_cadena(cadena)

        print(f"\nEvaluando la cadena: \"{cadena}\"")
        for i, simbolo in enumerate(cadena):
            print(f"{i+1}. Desde ({recorrido[i]}) con '{simbolo}' → ({recorrido[i+1]})")

        print(f"Estado final: {recorrido[-1]}")
        print("Resultado:", "ACEPTADA ✓" if es_aceptada else "RECHAZADA ✗")

    def generar_cadenas(self):
        """Genera las primeras 10 cadenas válidas del lenguaje"""
        cadenas = self.afd.generar_cadenas_validas(10)
        print("Cadenas válidas:", cadenas)

    def guardar_afd(self):
        """Guarda el AFD actual en un archivo"""
        nombre_archivo = input("Ingrese el nombre del archivo (sin extensión): ").strip() + ".json"
        guardar_afd(self.afd, nombre_archivo)

    def cargar_afd(self):
        """Carga un AFD desde un archivo"""
        archivos_json = [f for f in os.listdir('.') if f.endswith('.json')]
        print("Archivos disponibles:", archivos_json)
        nombre_archivo = input("Ingrese el nombre del archivo: ").strip()
        self.afd = cargar_afd(nombre_archivo)

    def ejecutar(self):
        """Ejecuta el simulador"""
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción (1-7): ").strip()
            if opcion == "1":
                self.crear_afd()
            elif opcion == "2":
                self.evaluar_cadena()
            elif opcion == "3":
                self.generar_cadenas()
            elif opcion == "4":
                self.afd.mostrar_info()
            elif opcion == "5":
                self.guardar_afd()
            elif opcion == "6":
                self.cargar_afd()
            elif opcion == "7":
                print("¡Gracias por usar el Simulador de AFD!")
                break
