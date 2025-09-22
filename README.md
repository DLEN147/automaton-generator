# Automaton Generator

Generador y simulador de **autómatas finitos deterministas (AFD)** con interfaz gráfica.  
Este proyecto permite **crear, editar, visualizar y exportar autómatas**, proporcionando herramientas educativas e interactivas para estudiantes y docentes de **teoría de autómatas y lenguajes formales**.
---
## Características
- Creación de **estados** y **transiciones** mediante interfaz gráfica.  
- Definición de **estado inicial** y **estados de aceptación**.  
- Validación de cadenas contra el autómata diseñado.  
- Guardado y carga de autómatas en archivos (serialización).  
- Representación gráfica interactiva del autómata.  
- Basado en **Python 3**.
---
## Estructura del proyecto
```bash
automaton-generator/
│── main.py # Punto de entrada principal
│
├── data/
│ └── serializer.py # Manejo de guardado/carga de autómatas
│
├── models/
│ ├── afd.py # Implementación de AFD
│ ├── state.py # Definición de estados
│ └── transition.py # Definición de transiciones
│
└── ui/
├── gui.py # Ventana principal de la aplicación
├── gui_base.py # Componentes base de la GUI
├── gui_dialogs.py # Diálogos interactivos
├── gui_drawing.py # Dibujo de autómatas en la interfaz
└── gui_events.py # Manejo de eventos
```
---
## Instalación
1. Clonar este repositorio:

```bash
git clone https://github.com/DLEN147/automaton-generator.git
cd automaton-generator/automaton-generator
```
## Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv .venv
source .venv/bin/activate   # En Linux/Mac
.venv\Scripts\activate      # En Windows
```
## Ejecutar el programa con:
```bash
python main.py
```
1. Se abrirá la interfaz gráfica, donde se puede:
2. Crear estados y definir el estado inicial.
3. Agregar transiciones con símbolos del alfabeto.
4. Marcar uno o más estados como de aceptación.
5. Dibujar el autómata en pantalla.
6. Guardar o cargar autómatas desde archivo.
7. Probar cadenas para verificar si son aceptadas o rechazadas.

## Reglas de funcionamiento
- Debe existir un único estado inicial.
- Puede haber uno o varios estados de aceptación.
- Cada transición se define con un símbolo válido del alfabeto.
- El autómata debe ser determinista (no se permiten transiciones múltiples con el mismo símbolo desde un mismo estado).
- Una cadena se acepta si, al procesarla desde el estado inicial, el autómata termina en un estado de aceptación.
- Se pueden guardar los autómatas para reutilizarlos en sesiones posteriores.

## Licencia
Este proyecto se distribuye bajo la licencia MIT.

## Créditos
Proyecto desarrollado con fines educativos por DLEN147 y JLCDS.
Inspirado en la enseñanza de autómatas, lenguajes formales y teoría de la computación.
