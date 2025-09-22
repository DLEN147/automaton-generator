from collections import deque
from typing import Set, Dict, List, Tuple, Optional

from .state import State
from .transition import Transition


class AFD:
    """
    Clase que representa un Autómata Finito Determinista
    """

    def __init__(self):
        self.estados: Dict[str, State] = {}                # {nombre: State}
        self.alfabeto: Set[str] = set()
        self.estado_inicial: Optional[str] = None          # nombre del estado inicial
        self.estados_aceptacion: Set[str] = set()          # nombres de estados de aceptación
        self.transiciones: List[Transition] = []           # lista de transiciones

    def agregar_estado(self, estado: str, es_aceptacion: bool = False):
        """Agrega un estado al conjunto de estados"""
        self.estados[estado] = State(estado, es_aceptacion)
        if es_aceptacion:
            self.estados_aceptacion.add(estado)

    def agregar_simbolo(self, simbolo: str):
        """Agrega un símbolo al alfabeto"""
        self.alfabeto.add(simbolo)

    def establecer_estado_inicial(self, estado: str):
        """Establece el estado inicial"""
        if estado not in self.estados:
            raise ValueError(f"El estado '{estado}' no existe en el conjunto de estados")
        self.estado_inicial = estado

    def agregar_estado_aceptacion(self, estado: str):
        """Marca un estado existente como de aceptación"""
        if estado not in self.estados:
            raise ValueError(f"El estado '{estado}' no existe en el conjunto de estados")
        self.estados[estado].is_accepting = True
        self.estados_aceptacion.add(estado)

    def agregar_transicion(self, estado_origen: str, simbolo: str, estado_destino: str):
        """Agrega una transición al AFD"""
        if estado_origen not in self.estados:
            raise ValueError(f"El estado origen '{estado_origen}' no existe")
        if estado_destino not in self.estados:
            raise ValueError(f"El estado destino '{estado_destino}' no existe")
        if simbolo not in self.alfabeto:
            raise ValueError(f"El símbolo '{simbolo}' no pertenece al alfabeto")

        self.transiciones.append(Transition(estado_origen, simbolo, estado_destino))

    def procesar_cadena(self, cadena: str) -> Tuple[bool, List[str]]:
        """
        Procesa una cadena y retorna si es aceptada junto con el recorrido
        """
        if not self.estado_inicial:
            raise ValueError("No se ha definido un estado inicial")

        # Validar que todos los símbolos pertenezcan al alfabeto
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                raise ValueError(f"El símbolo '{simbolo}' no pertenece al alfabeto")

        estado_actual = self.estado_inicial
        recorrido = [estado_actual]

        for simbolo in cadena:
            # Buscar transición válida
            transicion_valida = next(
                (t for t in self.transiciones if t.current_state == estado_actual and t.symbol == simbolo),
                None
            )
            if not transicion_valida:
                return False, recorrido

            estado_actual = transicion_valida.next_state
            recorrido.append(estado_actual)

        # Verificar si el estado final es de aceptación
        es_aceptada = estado_actual in self.estados_aceptacion
        return es_aceptada, recorrido

    def generar_cadenas_validas(self, limite: int = 10) -> List[str]:
        """
        Genera las primeras 'limite' cadenas válidas del lenguaje
        usando búsqueda en amplitud (BFS)
        """
        if not self.estado_inicial:
            return []

        cadenas_validas = []
        cola = deque([(self.estado_inicial, "")])  # (estado_actual, cadena_construida)
        visitados = set()

        while cola and len(cadenas_validas) < limite:
            estado_actual, cadena = cola.popleft()

            if (estado_actual, cadena) in visitados:
                continue
            visitados.add((estado_actual, cadena))

            if estado_actual in self.estados_aceptacion:
                cadenas_validas.append(cadena)

            for simbolo in self.alfabeto:
                for t in self.transiciones:
                    if t.current_state == estado_actual and t.symbol == simbolo:
                        nueva_cadena = cadena + simbolo
                        if len(nueva_cadena) <= 20:
                            cola.append((t.next_state, nueva_cadena))

        return cadenas_validas

    def mostrar_info(self):
        """Muestra información completa del AFD"""
        print("\n=== INFORMACIÓN DEL AUTÓMATA ===")
        print(f"Estados: {sorted(list(self.estados.keys()))}")
        print(f"Alfabeto: {sorted(list(self.alfabeto))}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados de aceptación: {sorted(list(self.estados_aceptacion))}")
        print("Transiciones:")
        for t in self.transiciones:
            print(f"  {t}")
        print("=" * 35)
