import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
from models.afd import AFD
from data.serializer import guardar_afd, cargar_afd
import math


class AFDGui:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Simulador de AFD - Diseñador Visual")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # Configurar estilo moderno
        self.setup_styles()
        
        self.afd = AFD()

        # Estados gráficos
        self.estado_counter = 0
        self.estados_graficos = {}   # nombre → (x, y, circle_id, text_id, shadow_id)
        self.estado_inicial = None
        self.transiciones_graficas = []

        # Historial para Ctrl+Z
        self.undo_stack = []
        
        # Variables para drag & drop
        self.dragging = False
        self.drag_estado = None
        self.drag_offset = (0, 0)
        self.drag_threshold = 5  # Umbral mínimo para considerar drag
        self.drag_started = False

        # Variables para selección y modos
        self.estado_seleccionado = None
        self.hover_estado = None
        self.modo_borrador = False

        # Crear interfaz
        self.create_interface()

        # Eventos
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_stop)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Motion>", self.on_hover)

        # Atajos de teclado
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Control-s>", lambda e: self.guardar())
        self.root.bind("<Control-o>", lambda e: self.cargar())
        self.root.bind("<F5>", lambda e: self.evaluar_cadena())
        self.root.bind("<Delete>", self.eliminar_seleccionado)

    # ================== ESTILOS ==================
    def setup_styles(self):
        self.colors = {
            'bg_primary': '#2c3e50',
            'bg_secondary': '#34495e',
            'canvas_bg': '#ecf0f1',
            'estado_normal': '#3498db',
            'estado_inicial': '#e74c3c',
            'estado_final': '#27ae60',
            'estado_seleccionado': '#f39c12',
            'estado_hover': '#9b59b6',
            'transicion': '#7f8c8d',
            'texto': '#2c3e50',
            'boton_primary': '#3498db',
            'boton_success': '#27ae60',
            'boton_warning': '#f39c12',
            'boton_danger': '#e74c3c'
        }

    # ================== CREAR INTERFAZ ==================
    def create_interface(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame superior para botones
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill="x", pady=(0, 10))

        # Botones principales
        tk.Button(button_frame, text="💾 Guardar", command=self.guardar,
                 bg=self.colors['boton_success'], fg='white', 
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="📂 Cargar", command=self.cargar,
                 bg=self.colors['boton_primary'], fg='white',
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="🧪 Evaluar Cadena", command=self.evaluar_cadena,
                 bg=self.colors['boton_warning'], fg='white',
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)

        tk.Button(button_frame, text="🎯 Evaluador Múltiple", command=self.evaluador_multiple,
                 bg='#8e44ad', fg='white',
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)

        tk.Button(button_frame, text="🎲 Generar Cadenas", command=self.generar_cadenas_lenguaje,
                 bg='#16a085', fg='white',
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)

        tk.Button(button_frame, text="📋 Ver Quintupla", command=self.mostrar_quintupla,
                 bg='#d35400', fg='white',
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)

        # Botón borrador (toggle)
        self.boton_borrador = tk.Button(button_frame, text="🗑️ Borrador", command=self.toggle_borrador,
                                       bg=self.colors['bg_secondary'], fg='white',
                                       font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5)
        self.boton_borrador.pack(side="left", padx=5)

        tk.Button(button_frame, text="🔄 Limpiar Todo", command=self.limpiar_canvas,
                 bg=self.colors['boton_danger'], fg='white',
                 font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5).pack(side="left", padx=5)

        # Frame para instrucciones
        info_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief="ridge", bd=1)
        info_frame.pack(fill="x", pady=(0, 10))
        
        self.info_label = tk.Label(info_frame, 
                                  text="💡 Click: crear estado | Drag: mover | Click derecho: menú contextual | Click + Click: crear transición",
                                  bg=self.colors['bg_secondary'], fg='white',
                                  font=('Segoe UI', 9), wraplength=800, justify="center")
        self.info_label.pack(pady=10)

        # Canvas
        canvas_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief="sunken", bd=2)
        canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['canvas_bg'], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

    # ================== EVENTOS ==================
    def on_click(self, event):
        """Click izquierdo: crear estado, seleccionar para transición o borrar"""
        estado = self.get_estado_por_coordenada(event.x, event.y)
        transicion_grafica = self.get_transicion_por_coordenada(event.x, event.y)

        # Modo borrador
        if self.modo_borrador:
            if estado:
                self.eliminar_estado(estado)
            elif transicion_grafica:
                self.eliminar_transicion(transicion_grafica)
            return

        if estado:
            # Preparar drag
            self.dragging = True
            self.drag_estado = estado
            self.drag_started = False
            ex, ey, _, _, _ = self.estados_graficos[estado]
            self.drag_offset = (event.x - ex, event.y - ey)

            # Selección para transición
            if self.estado_seleccionado is None:
                self.estado_seleccionado = estado
                self.highlight_estado(estado, self.colors['estado_seleccionado'])
            else:
                destino = estado
                simbolo = self.pedir_simbolo_transicion(self.estado_seleccionado, destino)
                if simbolo:
                    try:
                        self.afd.agregar_simbolo(simbolo)
                        self.afd.agregar_transicion(self.estado_seleccionado, simbolo, destino)
                        self.dibujar_transicion_mejorada(self.estado_seleccionado, destino, simbolo)
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al crear transición: {str(e)}")
                
                self.unhighlight_estado(self.estado_seleccionado)
                self.estado_seleccionado = None
        else:
            # Crear nuevo estado en espacio vacío
            if not self.modo_borrador:
                nombre = f"q{self.estado_counter}"
                self.estado_counter += 1
                self.afd.agregar_estado(nombre)
                self.dibujar_estado_mejorado(nombre, event.x, event.y)

    def on_drag_motion(self, event):
        """Arrastrar un estado"""
        if self.dragging and self.drag_estado and not self.modo_borrador:
            # Calcular distancia para determinar si es drag real
            if not self.drag_started:
                ex, ey, _, _, _ = self.estados_graficos[self.drag_estado]
                distance = math.sqrt((event.x - ex)**2 + (event.y - ey)**2)
                if distance > self.drag_threshold:
                    self.drag_started = True
                else:
                    return

            x, y = event.x - self.drag_offset[0], event.y - self.drag_offset[1]
            self.mover_estado(self.drag_estado, x, y)

    def on_drag_stop(self, event):
        """Soltar estado arrastrado"""
        if self.dragging and not self.drag_started:
            # Si no hubo drag real, mantener la selección
            pass
        
        self.dragging = False
        self.drag_estado = None
        self.drag_started = False

    def on_right_click(self, event):
        """Menú contextual"""
        estado = self.get_estado_por_coordenada(event.x, event.y)
        if estado:
            menu = tk.Menu(self.root, tearoff=0)
            
            # Opciones para estado inicial
            if estado == self.afd.estado_inicial:
                menu.add_command(label="❌ Quitar como inicial", 
                               command=lambda: self.quitar_inicial(estado))
            else:
                menu.add_command(label="➡️ Marcar como inicial", 
                               command=lambda: self.set_inicial(estado))
            
            # Opciones para estado de aceptación
            if estado in self.afd.estados_aceptacion:
                menu.add_command(label="❌ Quitar aceptación", 
                               command=lambda: self.toggle_aceptacion(estado))
            else:
                menu.add_command(label="⭕ Marcar como aceptación", 
                               command=lambda: self.toggle_aceptacion(estado))
            
            menu.add_separator()
            menu.add_command(label="🔄 Transición a sí mismo", 
                           command=lambda: self.crear_autotransicion(estado))
            menu.add_separator()
            menu.add_command(label="🗑️ Eliminar estado", 
                           command=lambda: self.eliminar_estado(estado))
            menu.tk_popup(event.x_root, event.y_root)

    def on_hover(self, event):
        """Efecto hover sobre estados"""
        if self.modo_borrador:
            # Cambiar cursor en modo borrador
            estado = self.get_estado_por_coordenada(event.x, event.y)
            transicion = self.get_transicion_por_coordenada(event.x, event.y)
            if estado or transicion:
                self.canvas.configure(cursor="dotbox")
                # Mostrar información de lo que se va a borrar
                if estado:
                    self.info_label.config(text=f"🗑️ Click para borrar estado '{estado}'")
                elif transicion:
                    self.info_label.config(text=f"🗑️ Click para borrar transición {transicion['origen']} -{transicion['simbolo']}→ {transicion['destino']}")
            else:
                self.canvas.configure(cursor="")
                self.info_label.config(text="🗑️ MODO BORRADOR: Click en estados o transiciones para eliminar")
            return

        estado = self.get_estado_por_coordenada(event.x, event.y)
        if estado != self.hover_estado:
            # Quitar hover anterior
            if self.hover_estado and self.hover_estado != self.estado_seleccionado:
                self.unhighlight_estado(self.hover_estado)
            
            # Aplicar nuevo hover
            if estado and estado != self.estado_seleccionado:
                self.highlight_estado(estado, self.colors['estado_hover'])
            
            self.hover_estado = estado

    # ================== DIBUJO ==================
    def dibujar_estado_mejorado(self, nombre, x, y):
        r = 30
        # Sombra
        shadow = self.canvas.create_oval(x-r+3, y-r+3, x+r+3, y+r+3, 
                                        fill="#bdc3c7", outline="")
        # Círculo principal
        circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, 
                                        outline="#2c3e50", width=3,
                                        fill=self.colors['estado_normal'])
        # Texto
        text = self.canvas.create_text(x, y, text=nombre, 
                                      font=("Segoe UI", 11, "bold"), 
                                      fill="white")
        
        self.estados_graficos[nombre] = (x, y, circle, text, shadow)

    def redibujar_estado_mejorado(self, nombre, aceptar=None, inicial=None):
        if nombre not in self.estados_graficos:
            return
            
        x, y, old_circle, text_id, shadow = self.estados_graficos[nombre]
        
        # Determinar color basado en los parámetros explícitos o el estado actual del AFD
        if inicial is True or (inicial is None and nombre == self.afd.estado_inicial):
            color = self.colors['estado_inicial']
        elif aceptar is True or (aceptar is None and nombre in self.afd.estados_aceptacion):
            color = self.colors['estado_final']
        elif inicial is False and (aceptar is False or aceptar is None and nombre not in self.afd.estados_aceptacion):
            color = self.colors['estado_normal']
        else:
            # Estado normal por defecto
            color = self.colors['estado_normal']
        
        # Eliminar círculo anterior
        self.canvas.delete(old_circle)
        
        # Crear nuevo círculo
        r = 30
        circle = self.canvas.create_oval(x-r, y-r, x+r, y+r, 
                                        outline="#2c3e50", width=3, 
                                        fill=color)
        
        # Si es estado de aceptación, agregar círculo interior
        es_aceptacion = (aceptar is True or 
                        (aceptar is None and nombre in self.afd.estados_aceptacion))
        if es_aceptacion:
            inner_circle = self.canvas.create_oval(x-r+5, y-r+5, x+r-5, y+r-5, 
                                                  outline="white", width=2, fill="")
        
        # IMPORTANTE: Actualizar la referencia pero conservar el text_id original
        # NO eliminamos ni recreamos el texto, solo actualizamos la referencia del círculo
        self.estados_graficos[nombre] = (x, y, circle, text_id, shadow)
        
        # Asegurarse de que el texto esté visible por encima del círculo
        self.canvas.tag_raise(text_id)

    def dibujar_transicion_mejorada(self, origen, destino, simbolo):
        if origen not in self.estados_graficos or destino not in self.estados_graficos:
            return
            
        x1, y1, _, _, _ = self.estados_graficos[origen]
        x2, y2, _, _, _ = self.estados_graficos[destino]
        
        if origen == destino:  # Auto-transición
            # Dibujar un bucle en la parte superior del estado
            loop_radius = 25
            loop_x = x1
            loop_y = y1 - 30 - loop_radius
            
            # Arco del bucle
            arc = self.canvas.create_arc(loop_x - loop_radius, loop_y - loop_radius,
                                        loop_x + loop_radius, loop_y + loop_radius,
                                        start=30, extent=300, outline=self.colors['transicion'],
                                        width=2, style="arc")
            
            # Flecha al final del bucle
            arrow_x = loop_x + loop_radius * 0.7
            arrow_y = loop_y - loop_radius * 0.3
            arrow = self.canvas.create_polygon(arrow_x, arrow_y,
                                              arrow_x - 5, arrow_y - 8,
                                              arrow_x - 5, arrow_y + 2,
                                              fill=self.colors['transicion'],
                                              outline=self.colors['transicion'])
            
            # Etiqueta
            text_bg = self.canvas.create_rectangle(loop_x - 15, loop_y - 15,
                                                  loop_x + 15, loop_y + 5,
                                                  fill="white", outline="")
            text = self.canvas.create_text(loop_x, loop_y - 5, text=simbolo,
                                          font=("Segoe UI", 10, "bold"),
                                          fill=self.colors['texto'])
            
            trans_info = {
                'elementos': [arc, arrow, text_bg, text],
                'origen': origen,
                'destino': destino,
                'simbolo': simbolo,
                'tipo': 'auto'
            }
            
        else:  # Transición normal
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
            line = self.canvas.create_line(start_x, start_y, end_x, end_y, 
                                          fill=self.colors['transicion'],
                                          width=2, arrow=tk.LAST, 
                                          arrowshape=(16, 20, 6))
            
            # Etiqueta en el centro
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            # Fondo blanco para la etiqueta
            bbox = self.canvas.create_rectangle(mid_x-15, mid_y-10, mid_x+15, mid_y+10,
                                               fill="white", outline="")
            text = self.canvas.create_text(mid_x, mid_y, text=simbolo,
                                          font=("Segoe UI", 10, "bold"), 
                                          fill=self.colors['texto'])
            
            trans_info = {
                'elementos': [line, bbox, text],
                'origen': origen,
                'destino': destino,
                'simbolo': simbolo,
                'tipo': 'normal'
            }
        
        self.transiciones_graficas.append(trans_info)

    def mover_estado(self, nombre, x, y):
        """Actualizar posición de un estado arrastrado"""
        if nombre not in self.estados_graficos:
            return
            
        old_x, old_y, circle, text, shadow = self.estados_graficos[nombre]
        dx, dy = x - old_x, y - old_y
        
        # Mover elementos del estado
        self.canvas.move(circle, dx, dy)
        self.canvas.move(text, dx, dy)
        self.canvas.move(shadow, dx, dy)
        
        # Actualizar posición guardada MANTENIENDO las referencias originales
        self.estados_graficos[nombre] = (x, y, circle, text, shadow)
        
        # Asegurar que el texto esté visible
        self.canvas.tag_raise(text)
        
        # Redibujar transiciones afectadas
        self.redibujar_transiciones_de_estado(nombre)

    def redibujar_transiciones_de_estado(self, estado):
        """Redibuja todas las transiciones que involucran un estado"""
        # Eliminar y redibujar transiciones gráficas del estado
        transiciones_a_redibujar = []
        nuevas_transiciones = []
        
        for trans_info in self.transiciones_graficas:
            if trans_info['origen'] == estado or trans_info['destino'] == estado:
                # Eliminar elementos gráficos
                for elemento in trans_info['elementos']:
                    self.canvas.delete(elemento)
                transiciones_a_redibujar.append(trans_info)
            else:
                nuevas_transiciones.append(trans_info)
        
        self.transiciones_graficas = nuevas_transiciones
        
        # Redibujar las transiciones eliminadas
        for trans_info in transiciones_a_redibujar:
            self.dibujar_transicion_mejorada(trans_info['origen'], 
                                           trans_info['destino'], 
                                           trans_info['simbolo'])

    # ================== AUXILIARES ==================
    def get_estado_por_coordenada(self, x, y):
        """Obtiene el estado en las coordenadas dadas"""
        for nombre, (ex, ey, _, _, _) in self.estados_graficos.items():
            if (x-ex)**2 + (y-ey)**2 <= 30**2:
                return nombre
        return None

    def get_transicion_por_coordenada(self, x, y):
        """Obtiene la transición en las coordenadas dadas"""
        for trans_info in self.transiciones_graficas:
            if trans_info['tipo'] == 'auto':
                # Para auto-transiciones, verificar área del bucle
                origen_x, origen_y, _, _, _ = self.estados_graficos[trans_info['origen']]
                loop_x = origen_x
                loop_y = origen_y - 55  # Centro del bucle
                
                # Verificar si está en el área del bucle (círculo de radio 30)
                if (x - loop_x)**2 + (y - loop_y)**2 <= 30**2:
                    return trans_info
                    
            elif trans_info['tipo'] == 'normal':
                # Para transiciones normales, verificar área de la etiqueta
                if len(trans_info['elementos']) >= 2:
                    try:
                        # Obtener coordenadas del rectángulo de fondo de la etiqueta
                        coords = self.canvas.coords(trans_info['elementos'][1])  # bbox de la etiqueta
                        if len(coords) >= 4:
                            x1, y1, x2, y2 = coords
                            if x1 <= x <= x2 and y1 <= y <= y2:
                                return trans_info
                    except:
                        # Si hay error con las coordenadas, usar método alternativo
                        # Verificar si está cerca de la línea principal
                        try:
                            line_coords = self.canvas.coords(trans_info['elementos'][0])
                            if len(line_coords) >= 4:
                                x1, y1, x2, y2 = line_coords
                                # Calcular distancia del punto a la línea
                                mid_x = (x1 + x2) / 2
                                mid_y = (y1 + y2) / 2
                                if (x - mid_x)**2 + (y - mid_y)**2 <= 25**2:
                                    return trans_info
                        except:
                            continue
        return None

    def highlight_estado(self, nombre, color):
        """Resalta un estado con el color dado"""
        if nombre in self.estados_graficos:
            circle = self.estados_graficos[nombre][2]
            self.canvas.itemconfig(circle, outline=color, width=4)

    def unhighlight_estado(self, nombre):
        """Quita el resaltado de un estado"""
        if nombre in self.estados_graficos:
            circle = self.estados_graficos[nombre][2]
            self.canvas.itemconfig(circle, outline="#2c3e50", width=3)

    # ================== FUNCIONES DE ESTADO ==================
    def quitar_inicial(self, estado):
        """Quita la marca de estado inicial"""
        if estado == self.afd.estado_inicial:
            self.afd.estado_inicial = None
            self.estado_inicial = None
            # Redibujar el estado con color normal o de aceptación si corresponde
            if estado in self.afd.estados_aceptacion:
                self.redibujar_estado_mejorado(estado, aceptar=True)
            else:
                self.redibujar_estado_mejorado(estado, aceptar=False, inicial=False)
            messagebox.showinfo("Estado Inicial", f"Estado '{estado}' ya no es inicial")
        else:
            messagebox.showinfo("Info", f"El estado '{estado}' no era inicial")

    def set_inicial(self, estado):
        """Marca un estado como inicial"""
        try:
            # Verificar si ya hay un estado inicial
            if self.afd.estado_inicial and self.afd.estado_inicial != estado:
                respuesta = messagebox.askyesno("Estado Inicial Existente", 
                                              f"Ya existe un estado inicial '{self.afd.estado_inicial}'.\n"
                                              f"¿Desea cambiarlo a '{estado}'?")
                if not respuesta:
                    return
                
                # Quitar el estado inicial anterior
                estado_anterior = self.afd.estado_inicial
                self.afd.estado_inicial = None
                self.estado_inicial = None
                
                # Redibujar el estado anterior
                if estado_anterior in self.afd.estados_aceptacion:
                    self.redibujar_estado_mejorado(estado_anterior, aceptar=True, inicial=False)
                else:
                    self.redibujar_estado_mejorado(estado_anterior, aceptar=False, inicial=False)
            
            # Establecer el nuevo estado inicial
            self.afd.establecer_estado_inicial(estado)
            self.estado_inicial = estado
            
            # Redibujar el estado como inicial (puede ser inicial Y de aceptación)
            if estado in self.afd.estados_aceptacion:
                self.redibujar_estado_mejorado(estado, aceptar=True, inicial=True)
            else:
                self.redibujar_estado_mejorado(estado, aceptar=False, inicial=True)
                
            messagebox.showinfo("Estado Inicial", f"Estado '{estado}' marcado como inicial")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_aceptacion(self, estado):
        """Alterna el estado de aceptación"""
        try:
            if estado in self.afd.estados_aceptacion:
                self.afd.estados_aceptacion.remove(estado)
                self.afd.estados[estado].is_accepting = False
                self.redibujar_estado_mejorado(estado, aceptar=False)
            else:
                self.afd.agregar_estado_aceptacion(estado)
                self.redibujar_estado_mejorado(estado, aceptar=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def crear_autotransicion(self, estado):
        """Crea una transición del estado a sí mismo"""
        simbolo = self.pedir_simbolo_transicion(estado, estado)
        if simbolo:
            try:
                self.afd.agregar_simbolo(simbolo)
                self.afd.agregar_transicion(estado, simbolo, estado)
                self.dibujar_transicion_mejorada(estado, estado, simbolo)
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear auto-transición: {str(e)}")

    def eliminar_estado(self, estado):
        """Elimina un estado y sus transiciones"""
        if messagebox.askyesno("Confirmar", f"¿Eliminar el estado '{estado}'?"):
            # Eliminar elementos gráficos del estado
            if estado in self.estados_graficos:
                _, _, circle, text, shadow = self.estados_graficos[estado]
                self.canvas.delete(circle)
                self.canvas.delete(text)
                self.canvas.delete(shadow)
                del self.estados_graficos[estado]
            
            # Eliminar transiciones gráficas relacionadas
            self.transiciones_graficas = [
                t for t in self.transiciones_graficas 
                if t['origen'] != estado and t['destino'] != estado
            ]
            
            # Eliminar del AFD
            if estado in self.afd.estados:
                del self.afd.estados[estado]
            if estado in self.afd.estados_aceptacion:
                self.afd.estados_aceptacion.remove(estado)
            if self.afd.estado_inicial == estado:
                self.afd.estado_inicial = None
                self.estado_inicial = None
            
            # Eliminar transiciones del AFD
            self.afd.transiciones = [
                t for t in self.afd.transiciones 
                if t.current_state != estado and t.next_state != estado
            ]
            
            # Redibujar canvas
            self.redibujar_todo()

    def eliminar_transicion(self, trans_info):
        """Elimina una transición específica"""
        if messagebox.askyesno("Confirmar", 
                             f"¿Eliminar transición {trans_info['origen']} -{trans_info['simbolo']}→ {trans_info['destino']}?"):
            # Eliminar elementos gráficos
            for elemento in trans_info['elementos']:
                self.canvas.delete(elemento)
            
            # Eliminar de la lista gráfica
            self.transiciones_graficas.remove(trans_info)
            
            # Eliminar del AFD
            self.afd.transiciones = [
                t for t in self.afd.transiciones 
                if not (t.current_state == trans_info['origen'] and 
                       t.next_state == trans_info['destino'] and 
                       t.symbol == trans_info['simbolo'])
            ]

    def eliminar_seleccionado(self, event=None):
        """Elimina el estado seleccionado (tecla Delete)"""
        if self.estado_seleccionado:
            self.eliminar_estado(self.estado_seleccionado)
            self.estado_seleccionado = None

    def pedir_simbolo_transicion(self, origen, destino):
        """Pide al usuario el símbolo para una transición"""
        if origen == destino:
            prompt = f"Símbolo para auto-transición en {origen}:"
        else:
            prompt = f"Símbolo para transición {origen} → {destino}:"
        
        simbolo = simpledialog.askstring("Transición", prompt)
        return simbolo.strip() if simbolo else None

    def toggle_borrador(self):
        """Activa/desactiva el modo borrador"""
        self.modo_borrador = not self.modo_borrador
        
        if self.modo_borrador:
            self.boton_borrador.config(bg=self.colors['boton_danger'], text="🗑️ Borrador ON")
            self.info_label.config(text="🗑️ MODO BORRADOR: Click en estados o transiciones para eliminar")
            self.canvas.configure(cursor="dotbox")
        else:
            self.boton_borrador.config(bg=self.colors['bg_secondary'], text="🗑️ Borrador")
            self.info_label.config(text="💡 Click: crear estado | Drag: mover | Click derecho: menú contextual | Click + Click: crear transición")
            self.canvas.configure(cursor="")

    def redibujar_todo(self):
        """Redibuja todo el canvas"""
        self.canvas.delete("all")
        self.transiciones_graficas = []
        
        # Redibujar estados
        temp_estados = dict(self.estados_graficos)
        self.estados_graficos = {}
        
        for nombre, (x, y, _, _, _) in temp_estados.items():
            self.dibujar_estado_mejorado(nombre, x, y)
            
            # Aplicar propiedades especiales manteniendo las prioridades correctas
            if nombre == self.afd.estado_inicial and nombre in self.afd.estados_aceptacion:
                # Estado que es TANTO inicial COMO de aceptación - prioridad al inicial
                self.redibujar_estado_mejorado(nombre, aceptar=True, inicial=True)
            elif nombre == self.afd.estado_inicial:
                # Solo inicial
                self.redibujar_estado_mejorado(nombre, aceptar=False, inicial=True)
            elif nombre in self.afd.estados_aceptacion:
                # Solo aceptación
                self.redibujar_estado_mejorado(nombre, aceptar=True, inicial=False)
        
        # Redibujar transiciones
        for transicion in self.afd.transiciones:
            self.dibujar_transicion_mejorada(transicion.current_state, 
                                           transicion.next_state, 
                                           transicion.symbol)

    # ================== FUNCIONES PRINCIPALES ==================
    def evaluador_multiple(self):
        """Permite evaluar múltiples cadenas de forma interactiva"""
        # Verificaciones iniciales
        if not self.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return
        
        if not self.afd.estado_inicial:
            messagebox.showwarning("Advertencia", "Debe definir un estado inicial")
            return
            
        if not self.afd.estados_aceptacion:
            messagebox.showwarning("Advertencia", "Debe definir al menos un estado de aceptación")
            return
            
        if not self.afd.alfabeto:
            messagebox.showwarning("Advertencia", "Debe definir al menos una transición para crear el alfabeto")
            return

        # Crear ventana del evaluador múltiple
        ventana_evaluador = tk.Toplevel(self.root)
        ventana_evaluador.title("🎯 Evaluador Múltiple de Cadenas")
        ventana_evaluador.geometry("700x600")
        ventana_evaluador.configure(bg=self.colors['bg_primary'])

        # Frame principal
        main_frame = tk.Frame(ventana_evaluador, bg=self.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Información del AFD
        info_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief="ridge", bd=2)
        info_frame.pack(fill="x", pady=(0, 15))

        tk.Label(info_frame, text="📊 Información del AFD", 
                font=('Segoe UI', 12, 'bold'), bg=self.colors['bg_secondary'], fg='white').pack(pady=10)

        info_afd = f"Estados: {{{', '.join(sorted(self.afd.estados.keys()))}}}\n"
        info_afd += f"Alfabeto: {{{', '.join(sorted(self.afd.alfabeto))}}}\n"
        info_afd += f"Estado inicial: {self.afd.estado_inicial}\n"
        info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.afd.estados_aceptacion))}}}"

        tk.Label(info_frame, text=info_afd, font=('Consolas', 10),
                bg=self.colors['bg_secondary'], fg='white', justify="left").pack(pady=(0, 10))

        # Frame de entrada
        entrada_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        entrada_frame.pack(fill="x", pady=(0, 10))

        tk.Label(entrada_frame, text="Ingrese cadena a evaluar:", 
                font=('Segoe UI', 11, 'bold'), bg=self.colors['bg_primary'], fg='white').pack(anchor="w")

        entrada_var = tk.StringVar()
        entrada_entry = tk.Entry(entrada_frame, textvariable=entrada_var, font=('Consolas', 12), width=30)
        entrada_entry.pack(side="left", pady=5)

        def evaluar_cadena_actual():
            cadena = entrada_var.get().strip()
            if not cadena:
                return

            try:
                es_aceptada, recorrido = self.afd.procesar_cadena(cadena)
                resultado = "ACEPTADA ✅" if es_aceptada else "RECHAZADA ❌"
                recorrido_str = " → ".join(recorrido)
                
                # Insertar resultado en el área de resultados
                resultado_text.config(state="normal")
                resultado_text.insert(tk.END, f"\n{'='*60}\n")
                resultado_text.insert(tk.END, f"Cadena: '{cadena}'\n")
                resultado_text.insert(tk.END, f"Recorrido: {recorrido_str}\n")
                resultado_text.insert(tk.END, f"Resultado: {resultado}\n")
                resultado_text.config(state="disabled")
                resultado_text.see(tk.END)
                
                # Limpiar entrada
                entrada_var.set("")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al evaluar cadena: {str(e)}")

        tk.Button(entrada_frame, text="Evaluar", command=evaluar_cadena_actual,
                 bg=self.colors['boton_warning'], fg='white',
                 font=('Segoe UI', 10, 'bold'), padx=20).pack(side="left", padx=10)

        # Área de resultados
        tk.Label(main_frame, text="📋 Historial de Evaluaciones:", 
                font=('Segoe UI', 11, 'bold'), bg=self.colors['bg_primary'], fg='white').pack(anchor="w", pady=(10, 5))

        # Frame con scroll para resultados
        resultado_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        resultado_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=('Consolas', 10),
                               bg=self.colors['canvas_bg'], fg=self.colors['texto'],
                               yscrollcommand=scrollbar.set, padx=10, pady=10)
        resultado_text.pack(fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        resultado_text.insert("1.0", "💡 Ingrese cadenas para evaluar. Presione Enter o click en Evaluar.\n")
        resultado_text.config(state="disabled")

        # Botones de control
        control_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        control_frame.pack(fill="x", pady=10)

        tk.Button(control_frame, text="🗑️ Limpiar Historial", 
                 command=lambda: self.limpiar_historial(resultado_text),
                 bg=self.colors['boton_danger'], fg='white',
                 font=('Segoe UI', 10, 'bold')).pack(side="left")

        tk.Button(control_frame, text="❌ Cerrar", command=ventana_evaluador.destroy,
                 bg=self.colors['bg_secondary'], fg='white',
                 font=('Segoe UI', 10, 'bold')).pack(side="right")

        # Bind Enter key
        entrada_entry.bind("<Return>", lambda e: evaluar_cadena_actual())
        entrada_entry.focus()

        # Centrar ventana
        ventana_evaluador.transient(self.root)
        ventana_evaluador.grab_set()

    def limpiar_historial(self, text_widget):
        """Limpia el historial del evaluador múltiple"""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", "💡 Ingrese cadenas para evaluar. Presione Enter o click en Evaluar.\n")
        text_widget.config(state="disabled")

    def generar_cadenas_lenguaje(self):
        """Genera las primeras 10 cadenas del lenguaje"""
        # Verificaciones iniciales
        if not self.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return
        
        if not self.afd.estado_inicial:
            messagebox.showwarning("Advertencia", "Debe definir un estado inicial")
            return
            
        if not self.afd.estados_aceptacion:
            messagebox.showwarning("Advertencia", "Debe definir al menos un estado de aceptación")
            return
            
        if not self.afd.alfabeto:
            messagebox.showwarning("Advertencia", "Debe definir al menos una transición para crear el alfabeto")
            return

        try:
            # Generar cadenas
            cadenas_validas = self.afd.generar_cadenas_validas(10)
            
            # Crear ventana de resultados
            ventana_cadenas = tk.Toplevel(self.root)
            ventana_cadenas.title("🎲 Primeras 10 Cadenas del Lenguaje")
            ventana_cadenas.geometry("600x500")
            ventana_cadenas.configure(bg=self.colors['bg_primary'])

            # Frame principal
            main_frame = tk.Frame(ventana_cadenas, bg=self.colors['bg_primary'])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Título
            tk.Label(main_frame, text="🎲 Cadenas del Lenguaje L(AFD)", 
                    font=('Segoe UI', 14, 'bold'), bg=self.colors['bg_primary'], fg='white').pack(pady=(0, 15))

            # Información del AFD
            info_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief="ridge", bd=2)
            info_frame.pack(fill="x", pady=(0, 15))

            info_afd = f"Estados: {{{', '.join(sorted(self.afd.estados.keys()))}}}\n"
            info_afd += f"Alfabeto: {{{', '.join(sorted(self.afd.alfabeto))}}}\n"
            info_afd += f"Estado inicial: {self.afd.estado_inicial}\n"
            info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.afd.estados_aceptacion))}}}"

            tk.Label(info_frame, text=info_afd, font=('Consolas', 10),
                    bg=self.colors['bg_secondary'], fg='white', justify="left").pack(padx=15, pady=10)

            # Área de cadenas
            cadenas_frame = tk.Frame(main_frame, bg=self.colors['canvas_bg'], relief="sunken", bd=2)
            cadenas_frame.pack(fill="both", expand=True, pady=(0, 15))

            # Scroll para las cadenas
            scrollbar_cadenas = tk.Scrollbar(cadenas_frame)
            scrollbar_cadenas.pack(side="right", fill="y")

            cadenas_text = tk.Text(cadenas_frame, wrap="word", font=('Consolas', 11),
                                  bg=self.colors['canvas_bg'], fg=self.colors['texto'],
                                  yscrollcommand=scrollbar_cadenas.set, padx=15, pady=15)
            cadenas_text.pack(fill="both", expand=True)
            scrollbar_cadenas.config(command=cadenas_text.yview)

            # Contenido de las cadenas
            if cadenas_validas:
                contenido = "Las primeras 10 cadenas del lenguaje son:\n\n"
                for i, cadena in enumerate(cadenas_validas, 1):
                    if cadena == "":
                        contenido += f"{i:2d}. ε (cadena vacía)\n"
                    else:
                        contenido += f"{i:2d}. \"{cadena}\"\n"
                
                if len(cadenas_validas) < 10:
                    contenido += f"\n⚠️  Solo se encontraron {len(cadenas_validas)} cadenas."
                    contenido += "\n    El lenguaje podría ser finito o muy restrictivo."
            else:
                contenido = "❌ No se encontraron cadenas válidas.\n\n"
                contenido += "Posibles causas:\n"
                contenido += "• El lenguaje es vacío (no hay caminos del estado inicial a estados de aceptación)\n"
                contenido += "• Faltan transiciones necesarias\n"
                contenido += "• El AFD está mal configurado"

            cadenas_text.insert("1.0", contenido)
            cadenas_text.config(state="disabled")

            # Botones
            button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
            button_frame.pack(fill="x")

            tk.Button(button_frame, text="🔄 Regenerar", command=lambda: self.regenerar_cadenas(cadenas_text),
                     bg=self.colors['boton_primary'], fg='white',
                     font=('Segoe UI', 10, 'bold')).pack(side="left")

            tk.Button(button_frame, text="❌ Cerrar", command=ventana_cadenas.destroy,
                     bg=self.colors['bg_secondary'], fg='white',
                     font=('Segoe UI', 10, 'bold')).pack(side="right")

            # Centrar ventana
            ventana_cadenas.transient(self.root)
            ventana_cadenas.grab_set()

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar cadenas: {str(e)}")

    def regenerar_cadenas(self, text_widget):
        """Regenera las cadenas en la ventana actual"""
        try:
            cadenas_validas = self.afd.generar_cadenas_validas(10)
            
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            
            if cadenas_validas:
                contenido = "Las primeras 10 cadenas del lenguaje son:\n\n"
                for i, cadena in enumerate(cadenas_validas, 1):
                    if cadena == "":
                        contenido += f"{i:2d}. ε (cadena vacía)\n"
                    else:
                        contenido += f"{i:2d}. \"{cadena}\"\n"
                
                if len(cadenas_validas) < 10:
                    contenido += f"\n⚠️  Solo se encontraron {len(cadenas_validas)} cadenas."
            else:
                contenido = "❌ No se encontraron cadenas válidas."

            text_widget.insert("1.0", contenido)
            text_widget.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al regenerar cadenas: {str(e)}")

    def mostrar_quintupla(self):
        """Muestra la quintupla formal del AFD"""
        if not self.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return

        # Crear ventana de la quintupla
        ventana_quintupla = tk.Toplevel(self.root)
        ventana_quintupla.title("📋 Quintupla del AFD")
        ventana_quintupla.geometry("700x600")
        ventana_quintupla.configure(bg=self.colors['bg_primary'])

        # Frame principal
        main_frame = tk.Frame(ventana_quintupla, bg=self.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text="📋 Definición Formal del AFD", 
                font=('Segoe UI', 14, 'bold'), bg=self.colors['bg_primary'], fg='white').pack(pady=(0, 20))

        # Frame de contenido con scroll
        contenido_frame = tk.Frame(main_frame, bg=self.colors['canvas_bg'], relief="sunken", bd=2)
        contenido_frame.pack(fill="both", expand=True, pady=(0, 15))

        scrollbar_quintupla = tk.Scrollbar(contenido_frame)
        scrollbar_quintupla.pack(side="right", fill="y")

        quintupla_text = tk.Text(contenido_frame, wrap="word", font=('Consolas', 11),
                               bg=self.colors['canvas_bg'], fg=self.colors['texto'],
                               yscrollcommand=scrollbar_quintupla.set, padx=20, pady=20)
        quintupla_text.pack(fill="both", expand=True)
        scrollbar_quintupla.config(command=quintupla_text.yview)

        # Construir contenido de la quintupla
        contenido = "Un Autómata Finito Determinista (AFD) se define formalmente como:\n\n"
        contenido += "AFD = (Q, Σ, δ, q₀, F)\n\n"
        contenido += "Donde:\n\n"

        # Q - Estados
        estados_ordenados = sorted(self.afd.estados.keys())
        contenido += "Q = Conjunto de estados\n"
        contenido += f"Q = {{{', '.join(estados_ordenados)}}}\n"
        contenido += f"   |Q| = {len(estados_ordenados)} estados\n\n"

        # Σ - Alfabeto
        alfabeto_ordenado = sorted(self.afd.alfabeto) if self.afd.alfabeto else []
        contenido += "Σ = Alfabeto de entrada\n"
        if alfabeto_ordenado:
            contenido += f"Σ = {{{', '.join(alfabeto_ordenado)}}}\n"
            contenido += f"   |Σ| = {len(alfabeto_ordenado)} símbolos\n\n"
        else:
            contenido += "Σ = ∅ (vacío - no hay transiciones definidas)\n\n"

        # δ - Función de transición
        contenido += "δ = Función de transición\n"
        contenido += "δ: Q × Σ → Q\n"
        if self.afd.transiciones:
            contenido += "Transiciones definidas:\n"
            transiciones_ordenadas = sorted(self.afd.transiciones, 
                                          key=lambda t: (t.current_state, t.symbol, t.next_state))
            for trans in transiciones_ordenadas:
                contenido += f"   δ({trans.current_state}, '{trans.symbol}') = {trans.next_state}\n"
            contenido += f"\nTotal de transiciones: {len(self.afd.transiciones)}\n\n"
        else:
            contenido += "   No hay transiciones definidas\n\n"

        # q₀ - Estado inicial
        contenido += "q₀ = Estado inicial\n"
        if self.afd.estado_inicial:
            contenido += f"q₀ = {self.afd.estado_inicial}\n\n"
        else:
            contenido += "q₀ = ∅ (no definido)\n\n"

        # F - Estados de aceptación
        estados_finales_ordenados = sorted(self.afd.estados_aceptacion)
        contenido += "F = Conjunto de estados de aceptación\n"
        if estados_finales_ordenados:
            contenido += f"F = {{{', '.join(estados_finales_ordenados)}}}\n"
            contenido += f"   |F| = {len(estados_finales_ordenados)} estados\n\n"
        else:
            contenido += "F = ∅ (vacío - no hay estados de aceptación)\n\n"

        # Análisis del AFD
        contenido += "="*60 + "\n"
        contenido += "ANÁLISIS DEL AFD:\n"
        contenido += "="*60 + "\n\n"

        # Validaciones
        problemas = []
        if not self.afd.estado_inicial:
            problemas.append("❌ No hay estado inicial definido")
        if not self.afd.estados_aceptacion:
            problemas.append("❌ No hay estados de aceptación")
        if not self.afd.alfabeto:
            problemas.append("❌ No hay alfabeto definido (faltan transiciones)")
        if not self.afd.transiciones:
            problemas.append("❌ No hay transiciones definidas")

        # Verificar completitud de la función de transición
        if self.afd.alfabeto and self.afd.estados:
            transiciones_esperadas = len(self.afd.estados) * len(self.afd.alfabeto)
            transiciones_existentes = len(self.afd.transiciones)
            if transiciones_existentes < transiciones_esperadas:
                problemas.append(f"⚠️  Función de transición incompleta: {transiciones_existentes}/{transiciones_esperadas}")

        if problemas:
            contenido += "PROBLEMAS DETECTADOS:\n"
            for problema in problemas:
                contenido += f"   {problema}\n"
            contenido += "\n"
        else:
            contenido += "✅ El AFD está correctamente definido\n\n"

        # Propiedades
        contenido += "PROPIEDADES:\n"
        if self.afd.estado_inicial and self.afd.estados_aceptacion:
            contenido += "✅ Puede reconocer un lenguaje\n"
        if len(self.afd.estados) == 1:
            contenido += "📍 AFD trivial (un solo estado)\n"
        if self.afd.estado_inicial in self.afd.estados_aceptacion:
            contenido += "📍 Acepta la cadena vacía (ε)\n"

        quintupla_text.insert("1.0", contenido)
        quintupla_text.config(state="disabled")

        # Botón cerrar
        tk.Button(main_frame, text="❌ Cerrar", command=ventana_quintupla.destroy,
                 bg=self.colors['bg_secondary'], fg='white',
                 font=('Segoe UI', 12, 'bold'), pady=10).pack()

        # Centrar ventana
        ventana_quintupla.transient(self.root)
        ventana_quintupla.grab_set()

    def evaluar_cadena(self):
        """Evalúa una cadena con el AFD actual"""
        # Verificar que hay estados
        if not self.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return
        
        # Verificar estado inicial
        if not self.afd.estado_inicial:
            messagebox.showwarning("Advertencia", "Debe definir un estado inicial")
            return
            
        # Verificar estados de aceptación
        if not self.afd.estados_aceptacion:
            messagebox.showwarning("Advertencia", "Debe definir al menos un estado de aceptación")
            return
            
        # Verificar que hay alfabeto
        if not self.afd.alfabeto:
            messagebox.showwarning("Advertencia", "Debe definir al menos una transición para crear el alfabeto")
            return
            
        cadena = simpledialog.askstring("Evaluar Cadena", "Ingrese la cadena a evaluar:")
        if cadena is None:
            return
            
        try:
            es_aceptada, recorrido = self.afd.procesar_cadena(cadena)
            
            resultado = "ACEPTADA ✓" if es_aceptada else "RECHAZADA ✗"
            recorrido_str = " → ".join(recorrido)
            
            # Información adicional del AFD
            info_afd = f"Estados: {len(self.afd.estados)}\n"
            info_afd += f"Alfabeto: {{{', '.join(sorted(self.afd.alfabeto))}}}\n"
            info_afd += f"Estado inicial: {self.afd.estado_inicial}\n"
            info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.afd.estados_aceptacion))}}}\n\n"
            
            mensaje = info_afd
            mensaje += f"Cadena evaluada: '{cadena}'\n"
            mensaje += f"Recorrido: {recorrido_str}\n\n"
            mensaje += f"Resultado: {resultado}"
            
            # Mostrar en ventana más grande con scroll si es necesario
            ventana_resultado = tk.Toplevel(self.root)
            ventana_resultado.title("Resultado de Evaluación")
            ventana_resultado.geometry("500x400")
            ventana_resultado.configure(bg=self.colors['bg_primary'])
            
            # Frame con scroll
            frame_scroll = tk.Frame(ventana_resultado, bg=self.colors['bg_primary'])
            frame_scroll.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Texto del resultado
            texto_resultado = tk.Text(frame_scroll, wrap="word", font=("Consolas", 11),
                                    bg=self.colors['canvas_bg'], fg=self.colors['texto'],
                                    padx=15, pady=15)
            texto_resultado.pack(fill="both", expand=True)
            texto_resultado.insert("1.0", mensaje)
            texto_resultado.config(state="disabled")
            
            # Botón cerrar
            tk.Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy,
                     bg=self.colors['boton_primary'], fg='white',
                     font=('Segoe UI', 10, 'bold'), pady=10).pack(pady=(10, 0))
            
            # Centrar ventana
            ventana_resultado.transient(self.root)
            ventana_resultado.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar cadena: {str(e)}")
        """Evalúa una cadena con el AFD actual"""
        # Verificar que hay estados
        if not self.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return
        
        # Verificar estado inicial
        if not self.afd.estado_inicial:
            messagebox.showwarning("Advertencia", "Debe definir un estado inicial")
            return
            
        # Verificar estados de aceptación
        if not self.afd.estados_aceptacion:
            messagebox.showwarning("Advertencia", "Debe definir al menos un estado de aceptación")
            return
            
        # Verificar que hay alfabeto
        if not self.afd.alfabeto:
            messagebox.showwarning("Advertencia", "Debe definir al menos una transición para crear el alfabeto")
            return
            
        cadena = simpledialog.askstring("Evaluar Cadena", "Ingrese la cadena a evaluar:")
        if cadena is None:
            return
            
        try:
            es_aceptada, recorrido = self.afd.procesar_cadena(cadena)
            
            resultado = "ACEPTADA ✓" if es_aceptada else "RECHAZADA ✗"
            recorrido_str = " → ".join(recorrido)
            
            # Información adicional del AFD
            info_afd = f"Estados: {len(self.afd.estados)}\n"
            info_afd += f"Alfabeto: {{{', '.join(sorted(self.afd.alfabeto))}}}\n"
            info_afd += f"Estado inicial: {self.afd.estado_inicial}\n"
            info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.afd.estados_aceptacion))}}}\n\n"
            
            mensaje = info_afd
            mensaje += f"Cadena evaluada: '{cadena}'\n"
            mensaje += f"Recorrido: {recorrido_str}\n\n"
            mensaje += f"Resultado: {resultado}"
            
            # Mostrar en ventana más grande con scroll si es necesario
            ventana_resultado = tk.Toplevel(self.root)
            ventana_resultado.title("Resultado de Evaluación")
            ventana_resultado.geometry("500x400")
            ventana_resultado.configure(bg=self.colors['bg_primary'])
            
            # Frame con scroll
            frame_scroll = tk.Frame(ventana_resultado, bg=self.colors['bg_primary'])
            frame_scroll.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Texto del resultado
            texto_resultado = tk.Text(frame_scroll, wrap="word", font=("Consolas", 11),
                                    bg=self.colors['canvas_bg'], fg=self.colors['texto'],
                                    padx=15, pady=15)
            texto_resultado.pack(fill="both", expand=True)
            texto_resultado.insert("1.0", mensaje)
            texto_resultado.config(state="disabled")
            
            # Botón cerrar
            tk.Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy,
                     bg=self.colors['boton_primary'], fg='white',
                     font=('Segoe UI', 10, 'bold'), pady=10).pack(pady=(10, 0))
            
            # Centrar ventana
            ventana_resultado.transient(self.root)
            ventana_resultado.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar cadena: {str(e)}")

    def guardar(self):
        """Guarda el AFD en un archivo"""
        if not self.estados_graficos:
            messagebox.showwarning("Advertencia", "No hay estados para guardar")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                guardar_afd(self.afd, filename)
                messagebox.showinfo("Éxito", f"AFD guardado en {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def cargar(self):
        """Carga un AFD desde un archivo"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                # Limpiar canvas actual
                self.limpiar_canvas()
                
                # Cargar AFD
                self.afd = cargar_afd(filename)
                
                # Redibujar gráficamente (posiciones automáticas)
                self.generar_layout_automatico()
                
                messagebox.showinfo("Éxito", f"AFD cargado desde {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {str(e)}")

    def generar_layout_automatico(self):
        """Genera posiciones automáticas para los estados cargados"""
        estados = list(self.afd.estados.keys())
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
            if estado == self.afd.estado_inicial:
                self.estado_inicial = estado
                self.redibujar_estado_mejorado(estado, inicial=True)
            if estado in self.afd.estados_aceptacion:
                self.redibujar_estado_mejorado(estado, aceptar=True)
        
        # Actualizar contador para nuevos estados
        numeros = []
        for estado in estados:
            if estado.startswith('q') and estado[1:].isdigit():
                numeros.append(int(estado[1:]))
        if numeros:
            self.estado_counter = max(numeros) + 1
        
        # Dibujar transiciones
        for transicion in self.afd.transiciones:
            self.dibujar_transicion_mejorada(transicion.current_state, 
                                           transicion.next_state, 
                                           transicion.symbol)

    def limpiar_canvas(self):
        """Limpia completamente el canvas"""
        self.canvas.delete("all")
        self.estados_graficos = {}
        self.transiciones_graficas = []
        self.estado_counter = 0
        self.estado_inicial = None
        self.estado_seleccionado = None
        self.hover_estado = None
        self.modo_borrador = False
        self.boton_borrador.config(bg=self.colors['bg_secondary'], text="🗑️ Borrador")
        self.info_label.config(text="💡 Click: crear estado | Drag: mover | Click derecho: menú contextual | Click + Click: crear transición")
        self.canvas.configure(cursor="")
        self.afd = AFD()

    def undo(self, event=None):
        """Función para deshacer (placeholder)"""
        messagebox.showinfo("Info", "Función deshacer no implementada aún")


def run_gui():
    root = tk.Tk()
    app = AFDGui(root)
    root.mainloop()