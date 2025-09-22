import tkinter as tk
import math


class DrawingManager:
    """Maneja todo lo relacionado con el dibujo en el canvas"""
    
    def __init__(self, gui):
        self.gui = gui

    def dibujar_estado_mejorado(self, nombre, x, y):
        """Dibuja un estado en el canvas"""
        r = 30
        # Sombra
        shadow = self.gui.canvas.create_oval(x-r+3, y-r+3, x+r+3, y+r+3, 
                                            fill="#bdc3c7", outline="")
        # Círculo principal
        circle = self.gui.canvas.create_oval(x-r, y-r, x+r, y+r, 
                                            outline="#2c3e50", width=3,
                                            fill=self.gui.colors['estado_normal'])
        # Texto
        text = self.gui.canvas.create_text(x, y, text=nombre, 
                                          font=("Segoe UI", 11, "bold"), 
                                          fill="white")
        
        self.gui.estados_graficos[nombre] = (x, y, circle, text, shadow)

    def redibujar_estado_mejorado(self, nombre, aceptar=None, inicial=None):
        """Redibuja un estado con nuevos atributos"""
        if nombre not in self.gui.estados_graficos:
            return
            
        x, y, old_circle, text_id, shadow = self.gui.estados_graficos[nombre]
        
        # Determinar color basado en los parámetros explícitos o el estado actual del AFD
        if inicial is True or (inicial is None and nombre == self.gui.afd.estado_inicial):
            color = self.gui.colors['estado_inicial']
        elif aceptar is True or (aceptar is None and nombre in self.gui.afd.estados_aceptacion):
            color = self.gui.colors['estado_final']
        elif inicial is False and (aceptar is False or aceptar is None and nombre not in self.gui.afd.estados_aceptacion):
            color = self.gui.colors['estado_normal']
        else:
            color = self.gui.colors['estado_normal']
        
        # Eliminar círculo anterior
        self.gui.canvas.delete(old_circle)
        
        # Crear nuevo círculo
        r = 30
        circle = self.gui.canvas.create_oval(x-r, y-r, x+r, y+r, 
                                            outline="#2c3e50", width=3, 
                                            fill=color)
        
        # Si es estado de aceptación, agregar círculo interior
        es_aceptacion = (aceptar is True or 
                        (aceptar is None and nombre in self.gui.afd.estados_aceptacion))
        if es_aceptacion:
            inner_circle = self.gui.canvas.create_oval(x-r+5, y-r+5, x+r-5, y+r-5, 
                                                      outline="white", width=2, fill="")
        
        # Actualizar referencia del círculo y asegurar que el texto esté visible
        self.gui.estados_graficos[nombre] = (x, y, circle, text_id, shadow)
        self.gui.canvas.tag_raise(text_id)

    def dibujar_transicion_mejorada(self, origen, destino, simbolo):
        """Dibuja una transición entre estados"""
        if origen not in self.gui.estados_graficos or destino not in self.gui.estados_graficos:
            return
            
        x1, y1, _, _, _ = self.gui.estados_graficos[origen]
        x2, y2, _, _, _ = self.gui.estados_graficos[destino]
        
        if origen == destino:  # Auto-transición
            self._dibujar_autotransicion(x1, y1, simbolo, origen, destino)
        else:  # Transición normal
            self._dibujar_transicion_normal(x1, y1, x2, y2, simbolo, origen, destino)

    def _dibujar_autotransicion(self, x, y, simbolo, origen, destino):
        """Dibuja una auto-transición (bucle)"""
        loop_radius = 25
        loop_x = x
        loop_y = y - 30 - loop_radius
        
        # Arco del bucle
        arc = self.gui.canvas.create_arc(loop_x - loop_radius, loop_y - loop_radius,
                                        loop_x + loop_radius, loop_y + loop_radius,
                                        start=30, extent=300, 
                                        outline=self.gui.colors['transicion'],
                                        width=2, style="arc")
        
        # Flecha al final del bucle
        arrow_x = loop_x + loop_radius * 0.7
        arrow_y = loop_y - loop_radius * 0.3
        arrow = self.gui.canvas.create_polygon(arrow_x, arrow_y,
                                              arrow_x - 5, arrow_y - 8,
                                              arrow_x - 5, arrow_y + 2,
                                              fill=self.gui.colors['transicion'],
                                              outline=self.gui.colors['transicion'])
        
        # Etiqueta
        text_bg = self.gui.canvas.create_rectangle(loop_x - 15, loop_y - 15,
                                                  loop_x + 15, loop_y + 5,
                                                  fill="white", outline="")
        text = self.gui.canvas.create_text(loop_x, loop_y - 5, text=simbolo,
                                          font=("Segoe UI", 10, "bold"),
                                          fill=self.gui.colors['texto'])
        
        trans_info = {
            'elementos': [arc, arrow, text_bg, text],
            'origen': origen,
            'destino': destino,
            'simbolo': simbolo,
            'tipo': 'auto'
        }
        
        self.gui.transiciones_graficas.append(trans_info)

    def _dibujar_transicion_normal(self, x1, y1, x2, y2, simbolo, origen, destino):
        """Dibuja una transición normal entre dos estados diferentes"""
        # Calcular puntos en el borde de los círculos
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Normalizar vector
        unit_x = dx / distance
        unit_y = dy / distance
        
        # Puntos en el borde
        start_x = x1 + 30 * unit_x
        start_y = y1 + 30 * unit_y
        end_x = x2 - 30 * unit_x
        end_y = y2 - 30 * unit_y
        
        # Línea con flecha
        line = self.gui.canvas.create_line(start_x, start_y, end_x, end_y, 
                                          fill=self.gui.colors['transicion'],
                                          width=2, arrow=tk.LAST, 
                                          arrowshape=(16, 20, 6))
        
        # Etiqueta en el centro
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Fondo blanco para la etiqueta
        bbox = self.gui.canvas.create_rectangle(mid_x-15, mid_y-10, mid_x+15, mid_y+10,
                                               fill="white", outline="")
        text = self.gui.canvas.create_text(mid_x, mid_y, text=simbolo,
                                          font=("Segoe UI", 10, "bold"), 
                                          fill=self.gui.colors['texto'])
        
        trans_info = {
            'elementos': [line, bbox, text],
            'origen': origen,
            'destino': destino,
            'simbolo': simbolo,
            'tipo': 'normal'
        }
        
        self.gui.transiciones_graficas.append(trans_info)

    def mover_estado(self, nombre, x, y):
        """Actualizar posición de un estado arrastrado"""
        if nombre not in self.gui.estados_graficos:
            return
            
        old_x, old_y, circle, text, shadow = self.gui.estados_graficos[nombre]
        dx, dy = x - old_x, y - old_y
        
        # Mover elementos del estado
        self.gui.canvas.move(circle, dx, dy)
        self.gui.canvas.move(text, dx, dy)
        self.gui.canvas.move(shadow, dx, dy)
        
        # Actualizar posición guardada MANTENIENDO las referencias originales
        self.gui.estados_graficos[nombre] = (x, y, circle, text, shadow)
        
        # Asegurar que el texto esté visible
        self.gui.canvas.tag_raise(text)
        
        # Redibujar transiciones afectadas
        self.redibujar_transiciones_de_estado(nombre)

    def redibujar_transiciones_de_estado(self, estado):
        """Redibuja todas las transiciones que involucran un estado"""
        # Eliminar y redibujar transiciones gráficas del estado
        transiciones_a_redibujar = []
        nuevas_transiciones = []
        
        for trans_info in self.gui.transiciones_graficas:
            if trans_info['origen'] == estado or trans_info['destino'] == estado:
                # Eliminar elementos gráficos
                for elemento in trans_info['elementos']:
                    self.gui.canvas.delete(elemento)
                transiciones_a_redibujar.append(trans_info)
            else:
                nuevas_transiciones.append(trans_info)
        
        self.gui.transiciones_graficas = nuevas_transiciones
        
        # Redibujar las transiciones eliminadas
        for trans_info in transiciones_a_redibujar:
            self.dibujar_transicion_mejorada(trans_info['origen'], 
                                           trans_info['destino'], 
                                           trans_info['simbolo'])

    def highlight_estado(self, nombre, color):
        """Resalta un estado con el color dado"""
        if nombre in self.gui.estados_graficos:
            circle = self.gui.estados_graficos[nombre][2]
            self.gui.canvas.itemconfig(circle, outline=color, width=4)

    def unhighlight_estado(self, nombre):
        """Quita el resaltado de un estado"""
        if nombre in self.gui.estados_graficos:
            circle = self.gui.estados_graficos[nombre][2]
            self.gui.canvas.itemconfig(circle, outline="#2c3e50", width=3)

    def redibujar_todo(self):
        """Redibuja todo el canvas"""
        self.gui.canvas.delete("all")
        self.gui.transiciones_graficas = []
        
        # Redibujar estados
        temp_estados = dict(self.gui.estados_graficos)
        self.gui.estados_graficos = {}
        
        for nombre, (x, y, _, _, _) in temp_estados.items():
            self.dibujar_estado_mejorado(nombre, x, y)
            
            # Aplicar propiedades especiales manteniendo las prioridades correctas
            if nombre == self.gui.afd.estado_inicial and nombre in self.gui.afd.estados_aceptacion:
                # Estado que es TANTO inicial COMO de aceptación - prioridad al inicial
                self.redibujar_estado_mejorado(nombre, aceptar=True, inicial=True)
            elif nombre == self.gui.afd.estado_inicial:
                # Solo inicial
                self.redibujar_estado_mejorado(nombre, aceptar=False, inicial=True)
            elif nombre in self.gui.afd.estados_aceptacion:
                # Solo aceptación
                self.redibujar_estado_mejorado(nombre, aceptar=True, inicial=False)
        
        # Redibujar transiciones
        for transicion in self.gui.afd.transiciones:
            self.dibujar_transicion_mejorada(transicion.current_state, 
                                           transicion.next_state, 
                                           transicion.symbol)

    def generar_layout_automatico(self):
        """Genera posiciones automáticas para los estados cargados"""
        estados = list(self.gui.afd.estados.keys())
        if not estados:
            return
            
        # Disposición circular
        center_x, center_y = 400, 300
        radius = 150
        
        for i, estado in enumerate(estados):
            angle = 2 * math.pi * i / len(estados)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            self.dibujar_estado_mejorado(estado, x, y)
            
            # Aplicar propiedades especiales
            if estado == self.gui.afd.estado_inicial:
                self.gui.estado_inicial = estado
                self.redibujar_estado_mejorado(estado, inicial=True)
            if estado in self.gui.afd.estados_aceptacion:
                self.redibujar_estado_mejorado(estado, aceptar=True)
        
        # Actualizar contador para nuevos estados
        numeros = []
        for estado in estados:
            if estado.startswith('q') and estado[1:].isdigit():
                numeros.append(int(estado[1:]))
        if numeros:
            self.gui.estado_counter = max(numeros) + 1
        
        # Dibujar transiciones
        for transicion in self.gui.afd.transiciones:
            self.dibujar_transicion_mejorada(transicion.current_state, 
                                           transicion.next_state, 
                                           transicion.symbol)