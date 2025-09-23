# Manual de Usuario - AFDGedit

## Información del Proyecto

### Desarrollado por:
- **David Leonardo Espíndola Núñez** - Cod. 202128390
- **Juan Lopez Castro** - Cod. 

#### Universidad Pedagógica y Tecnológica de Colombia
**Facultad de Ingeniería**  
**Ingeniería en Sistemas y Computación**
**Lenguajes Formales**

---

## Iniciando el Simulador

### Ejecución del programa
1. Ejecuta el archivo `main.py` o abre el ejecutable
2. Interfaz principal con canvas de dibujo
3. Botones de funciones en la parte superior
4. Barra de instrucciones contextual en la parte inferior

## Construcción del AFD

### Creación de Estados

**Crear estado:**
- Click en área vacía del canvas
- Aparece círculo azul numerado automáticamente (q0, q1, q2...)

**Mover estados:**
- Arrastra clickeando y manteniendo presionado
- Las transiciones se actualizan automáticamente

### Configuración de Estados

**Estado inicial:**
1. Click derecho en el estado deseado
2. Seleccionar "Marcar como inicial"
3. El estado se marca en rojo
4. Solo puede existir uno por AFD

**Estados de aceptación:**
1. Click derecho en cualquier estado
2. Seleccionar "Marcar como aceptación"
3. El estado se marca en verde con círculo doble
4. Pueden existir múltiples estados de aceptación

**Quitar propiedades:**
- Click derecho → "Quitar como inicial" / "Quitar aceptación"

### Creación de Transiciones

**Transición entre estados:**
1. Click en estado origen (se resalta en naranja)
2. Click en estado destino
3. Ingresar símbolo de transición en la ventana emergente
4. Aparece flecha etiquetada

**Auto-transición:**
1. Click derecho en estado
2. "Transición a sí mismo"
3. Ingresar símbolo para el bucle
4. Aparece arco curvado sobre el estado

**Cancelar selección:**
- Click en área vacía cancela la selección activa

## Herramientas de Edición

### Modo Borrador
1. Click en botón "Borrador" (cambia a rojo)
2. Click en estados o transiciones para eliminar
3. Click nuevamente para desactivar

### Limpieza Completa
- "Limpiar Todo" elimina el AFD completo
- Reinicia el canvas para nuevo diseño

## Evaluación y Análisis

### Evaluación de Cadenas

**Evaluador simple:**
1. "Evaluar Cadena" → ingresar secuencia
2. Resultado: ACEPTADA/RECHAZADA con recorrido

**Evaluador múltiple:**
1. "Evaluador Múltiple" → ventana interactiva
2. Probar múltiples cadenas con historial
3. Enter o "Evaluar" para procesar cada cadena

### Generación de Lenguaje
- "Generar Cadenas" muestra las primeras 10 cadenas válidas
- Útil para verificar funcionamiento del AFD

### Análisis Formal
- "Ver Quintupla" muestra definición matemática completa
- Incluye análisis de completitud y validación

## Persistencia

### Guardar
1. "Guardar" → seleccionar ubicación y nombre
2. Formato JSON legible

### Cargar
1. "Cargar" → seleccionar archivo JSON
2. Redibuja automáticamente con layout circular

## Controles y Navegación

### Atajos de Teclado
| Tecla | Función |
|-------|---------|
| `Ctrl+S` | Guardar AFD |
| `Ctrl+O` | Cargar AFD |
| `F5` | Evaluar cadena |
| `Delete` | Eliminar elemento seleccionado |

### Indicadores Visuales

**Estados:**
- Azul: Estado normal
- Rojo: Estado inicial
- Verde: Estado de aceptación
- Naranja: Estado seleccionado
- Morado: Hover del cursor

**Transiciones:**
- Flecha recta: Entre estados diferentes
- Arco curvado: Auto-transición
- Etiqueta blanca: Símbolo de transición

### Menús Contextuales
**Click derecho en estado:**
- Marcar/quitar como inicial
- Marcar/quitar como aceptación
- Crear auto-transición
- Eliminar estado

## Validaciones del Sistema

### Verificaciones Automáticas
- Existencia de estado inicial antes de evaluar
- Existencia de estados de aceptación
- Validez de símbolos de transición
- Conexiones válidas entre estados

### Mensajes de Error
- "Debe definir un estado inicial"
- "Debe definir al menos un estado de aceptación"
- "El símbolo 'X' no pertenece al alfabeto"
- "Error al crear transición"

## Limitaciones Técnicas

- Visualización óptima: hasta 20 estados
- Símbolos: caracteres individuales únicamente
- Tipo: AFD exclusivamente (no AFN)
- Plataforma: Python 3.7+ o ejecutable

## Resolución de Problemas

### Problemas Técnicos
**Programa no inicia:**
- Verificar Python 3.7+
- Comprobar tkinter: `python -m tkinter`

**Elementos no se dibujan:**
- Reiniciar programa
- Usar "Limpiar Todo"

**Error al cargar archivo:**
- Verificar formato JSON válido
- Comprobar referencias de estados correctas

### Problemas de Uso
**AFD no acepta cadenas esperadas:**
- Verificar estados de aceptación definidos
- Revisar completitud de transiciones
- Usar "Ver Quintupla" para análisis

**Transiciones no aparecen:**
- Verificar que ambos estados existan
- Comprobar que el símbolo no esté vacío
- Intentar recrear la transición

---

**AFDGedit**
