# Manual de Usuario - Simulador de Autómatas Finitos Deterministas

Una guía completa para usar el simulador visual de AFD, desde los conceptos básicos hasta funciones avanzadas.

## ¿Qué es un AFD?

Un **Autómata Finito Determinista (AFD)** es una máquina matemática que puede estar en uno de varios estados y cambiar de estado según las entradas que recibe. Se usa para reconocer patrones en secuencias de símbolos (como texto o números).

### Ejemplo simple
Imagina un AFD que reconoce si una palabra termina en "ar":
- Lee cada letra de izquierda a derecha
- Cambia de estado según las letras que encuentra
- Al final, decide si la palabra cumple el patrón o no

## Primeros Pasos

### Iniciando el programa
1. Ejecuta el archivo `main.py` o abre el ejecutable
2. Verás una ventana con un área de dibujo grande (canvas)
3. En la parte superior están los botones de funciones

### Tu primer AFD: Reconocedor de palabras que terminan en "a"

#### Paso 1: Crear los estados
1. **Haz click** en cualquier parte vacía del canvas
2. Aparecerá un círculo azul con "q0" (tu primer estado)
3. Haz click en otro lugar para crear "q1"

#### Paso 2: Definir el estado inicial
1. **Click derecho** en q0
2. Selecciona "Marcar como inicial"
3. El estado se volverá rojo (estado inicial)

#### Paso 3: Definir estados de aceptación
1. **Click derecho** en q1
2. Selecciona "Marcar como aceptación"
3. El estado se volverá verde con un círculo doble

#### Paso 4: Crear transiciones
1. **Click** en q0 (estado origen)
2. **Click** en q1 (estado destino)
3. Cuando aparezca la ventana, escribe "a"
4. Verás una flecha de q0 a q1 con la etiqueta "a"

#### Paso 5: Completar el AFD
Para que funcione correctamente, agrega más transiciones:
1. q0 a q0 con símbolo "b,c,d,e..." (cualquier letra que no sea 'a')
2. q1 a q0 con símbolo "b,c,d,e..." 
3. q1 a q1 con símbolo "a"

#### Paso 6: Probar tu AFD
1. Click en "Evaluar Cadena"
2. Escribe "casa" y presiona OK
3. Verás: q0 → q0 → q0 → q0 → q1 (ACEPTADA)
4. Prueba con "perro": q0 → q0 → q0 → q0 → q0 (RECHAZADA)

## Funciones del Programa

### Crear y Editar Estados

**Crear estado nuevo:**
- Click en área vacía del canvas

**Mover estados:**
- Arrastra cualquier estado a nueva posición

**Cambiar propiedades de estados:**
- Click derecho en cualquier estado
- "Marcar como inicial": Solo puede haber uno
- "Marcar como aceptación": Puede haber varios
- "Quitar aceptación": Convierte a estado normal

**Eliminar estados:**
- Activa "Modo Borrador" y click en el estado
- O click derecho → "Eliminar estado"

### Crear Transiciones

**Transición normal:**
1. Click en estado origen
2. Click en estado destino
3. Ingresa el símbolo de transición

**Auto-transición (bucle):**
- Click derecho en estado → "Transición a sí mismo"

**Eliminar transiciones:**
- Modo borrador activado + click en la flecha de transición

### Evaluación de Cadenas

**Evaluador simple:**
1. Click "Evaluar Cadena"
2. Escribe la cadena a probar
3. Ve el resultado y recorrido

**Evaluador múltiple:**
1. Click "Evaluador Múltiple"
2. Prueba varias cadenas seguidas
3. Ve el historial completo

### Otras Funciones

**Ver Quintupla:**
- Muestra la definición matemática formal del AFD
- Útil para verificar que todo esté correcto

**Generar Cadenas:**
- Muestra las primeras 10 cadenas que acepta tu AFD
- Útil para entender qué lenguaje reconoce

**Guardar y Cargar:**
- Guarda tu AFD en archivo JSON
- Carga AFDs previamente guardados

## Consejos y Buenas Prácticas

### Diseño Visual
- **Organiza estados en círculo** para mejor visualización
- **Usa nombres descriptivos** para estados cuando sea posible
- **Evita cruces** entre transiciones para claridad

### Construcción del AFD
- **Planifica antes de dibujar**: Piensa qué estados necesitas
- **Prueba casos límite**: Cadena vacía, un solo carácter
- **Verifica completitud**: Cada estado debe tener transiciones para todos los símbolos del alfabeto

### Depuración
- **Usa "Ver Quintupla"** para verificar la estructura
- **Prueba cadenas conocidas** para validar el comportamiento
- **Genera ejemplos** para entender mejor tu lenguaje

## Resolución de Problemas Comunes

### "Mi AFD no acepta nada"
**Posibles causas:**
- No definiste estado de aceptación
- No hay camino del estado inicial a estados de aceptación
- Faltan transiciones necesarias

**Solución:**
1. Verifica que haya al menos un estado de aceptación (verde)
2. Traza manualmente el camino para una cadena simple
3. Usa "Generar Cadenas" para ver si produce algo

### "Acepta cadenas incorrectas"
**Posibles causas:**
- Estados de aceptación mal definidos
- Transiciones incorrectas

**Solución:**
1. Evalúa paso a paso una cadena problemática
2. Revisa si los estados finales son correctos
3. Verifica cada transición

### "El programa se comporta raro"
**Soluciones:**
1. Usa "Limpiar Todo" y empieza de nuevo
2. Guarda tu trabajo antes de experimentar
3. Reinicia el programa si es necesario

## Atajos Útiles

| Tecla | Función |
|-------|---------|
| Ctrl+S | Guardar AFD |
| Ctrl+O | Cargar AFD |
| F5 | Evaluar cadena rápido |
| Delete | Eliminar elemento seleccionado |

## Conceptos Importantes

### Estados
- **Estado inicial**: Donde comienza el procesamiento (rojo)
- **Estados de aceptación**: Donde el AFD acepta la cadena (verde)
- **Estados normales**: Estados intermedios (azul)

### Transiciones
- **Símbolos**: Las "letras" o "números" que lee el AFD
- **Alfabeto**: Conjunto de todos los símbolos posibles
- **Función de transición**: Las "reglas" que dicen cómo cambiar de estado

### Cadenas y Lenguajes
- **Cadena**: Secuencia de símbolos (ej: "abc", "123")
- **Lenguaje**: Conjunto de todas las cadenas que acepta el AFD
- **Cadena vacía**: La cadena sin símbolos (se escribe ε)

## Limitaciones del Programa

- **Máximo recomendado**: 20 estados para mejor visualización
- **Símbolos**: Solo caracteres individuales (no palabras completas)
- **No soporta epsilon**: Este es un simulador de AFD, no de AFN

---

Creado por:
David Leonardo Espíndola Núñez
Juan Lopez Castro
