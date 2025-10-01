import tkinter as tk
from tkinter import messagebox, simpledialog
import math


#Maneja todos los eventos de la interfaz
class EventHandler:
    
    def __init__(self, gui):
        self.gui = gui
        self.drawing = gui.drawing_manager

     #Click izquierdo: crear estado, seleccionar para transición o borrar
    def on_click(self, event):
        estado = self.gui.get_estado_por_coordenada(event.x, event.y)
        transicion_grafica = self.gui.get_transicion_por_coordenada(event.x, event.y)

        # Modo borrador
        if self.gui.modo_borrador:
            if estado:
                self.gui.save_state_for_undo()  # Guardar antes de eliminar
                self.eliminar_estado(estado)
            elif transicion_grafica:
                self.gui.save_state_for_undo()  # Guardar antes de eliminar
                self.eliminar_transicion(transicion_grafica)
            return

        if estado:
            # Preparar drag
            self.gui.dragging = True
            self.gui.drag_estado = estado
            self.gui.drag_started = False
            ex, ey, _, _, _ = self.gui.estados_graficos[estado]
            self.gui.drag_offset = (event.x - ex, event.y - ey)

            # Selección para transición
            if self.gui.estado_seleccionado is None:
                self.gui.estado_seleccionado = estado
                self.drawing.highlight_estado(estado, self.gui.colors['estado_seleccionado'])
            else:
                destino = estado
                simbolo = self.pedir_simbolo_transicion(self.gui.estado_seleccionado, destino)
                if simbolo:
                    try:
                        self.gui.save_state_for_undo()  # Guardar antes de crear transición
                        self.gui.afd.agregar_simbolo(simbolo)
                        self.gui.afd.agregar_transicion(self.gui.estado_seleccionado, simbolo, destino)
                        self.drawing.dibujar_transicion_mejorada(self.gui.estado_seleccionado, destino, simbolo)
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al crear transición: {str(e)}")
                
                self.drawing.unhighlight_estado(self.gui.estado_seleccionado)
                self.gui.estado_seleccionado = None
        else:
            # Crear nuevo estado en espacio vacío
            if not self.gui.modo_borrador:
                self.gui.save_state_for_undo()  # Guardar antes de crear estado
                nombre = f"q{self.gui.estado_counter}"
                self.gui.estado_counter += 1
                self.gui.afd.agregar_estado(nombre)
                self.drawing.dibujar_estado_mejorado(nombre, event.x, event.y)

    #Arrastrar un estado
    def on_drag_motion(self, event):
        if self.gui.dragging and self.gui.drag_estado and not self.gui.modo_borrador:
            # Calcular distancia para determinar si es drag real
            if not self.gui.drag_started:
                ex, ey, _, _, _ = self.gui.estados_graficos[self.gui.drag_estado]
                distance = math.sqrt((event.x - ex)**2 + (event.y - ey)**2)
                if distance > self.gui.drag_threshold:
                    self.gui.drag_started = True
                    # Guardar estado antes del primer movimiento significativo
                    self.gui.save_state_for_undo()
                else:
                    return

            x, y = event.x - self.gui.drag_offset[0], event.y - self.gui.drag_offset[1]
            self.drawing.mover_estado(self.gui.drag_estado, x, y)

    #Soltar estado arrastrado
    def on_drag_stop(self, event):
        self.gui.dragging = False
        self.gui.drag_estado = None
        self.gui.drag_started = False

    #Menú contextual
    def on_right_click(self, event):
        estado = self.gui.get_estado_por_coordenada(event.x, event.y)
        if estado:
            menu = tk.Menu(self.gui.root, tearoff=0)
            
            # Opciones para estado inicial
            if estado == self.gui.afd.estado_inicial:
                menu.add_command(label="❌ Quitar como inicial", 
                               command=lambda: self.quitar_inicial(estado))
            else:
                menu.add_command(label="➡️ Marcar como inicial", 
                               command=lambda: self.set_inicial(estado))
            
            # Opciones para estado de aceptación
            if estado in self.gui.afd.estados_aceptacion:
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

    #Efecto hover sobre estados
    def on_hover(self, event):
        if self.gui.modo_borrador:
            # Cambiar cursor en modo borrador
            estado = self.gui.get_estado_por_coordenada(event.x, event.y)
            transicion = self.gui.get_transicion_por_coordenada(event.x, event.y)
            if estado or transicion:
                self.gui.canvas.configure(cursor="dotbox")
                # Mostrar información de lo que se va a borrar
                if estado:
                    self.gui.info_label.config(text=f"🗑️ Click para borrar estado '{estado}'")
                elif transicion:
                    self.gui.info_label.config(text=f"🗑️ Click para borrar transición {transicion['origen']} -{transicion['simbolo']}→ {transicion['destino']}")
            else:
                self.gui.canvas.configure(cursor="")
                self.gui.info_label.config(text="🗑️ MODO BORRADOR: Click en estados o transiciones para eliminar")
            return

        estado = self.gui.get_estado_por_coordenada(event.x, event.y)
        if estado != self.gui.hover_estado:
            # Quitar hover anterior
            if self.gui.hover_estado and self.gui.hover_estado != self.gui.estado_seleccionado:
                self.drawing.unhighlight_estado(self.gui.hover_estado)
            
            # Aplicar nuevo hover
            if estado and estado != self.gui.estado_seleccionado:
                self.drawing.highlight_estado(estado, self.gui.colors['estado_hover'])
            
            self.gui.hover_estado = estado

    #FUNCIONES DE ESTADO

    #Marca un estado como inicial
    def set_inicial(self, estado):
        try:
            # Guardar estado antes de cambiar
            self.gui.save_state_for_undo()
            
            # Verificar si ya hay un estado inicial
            if self.gui.afd.estado_inicial and self.gui.afd.estado_inicial != estado:
                respuesta = messagebox.askyesno("Estado Inicial Existente", 
                                              f"Ya existe un estado inicial '{self.gui.afd.estado_inicial}'.\n"
                                              f"¿Desea cambiarlo a '{estado}'?")
                if not respuesta:
                    return
                
                # Quitar el estado inicial anterior
                estado_anterior = self.gui.afd.estado_inicial
                self.gui.afd.estado_inicial = None
                self.gui.estado_inicial = None
                
                # Redibujar el estado anterior
                if estado_anterior in self.gui.afd.estados_aceptacion:
                    self.drawing.redibujar_estado_mejorado(estado_anterior, aceptar=True, inicial=False)
                else:
                    self.drawing.redibujar_estado_mejorado(estado_anterior, aceptar=False, inicial=False)
            
            # Establecer el nuevo estado inicial
            self.gui.afd.establecer_estado_inicial(estado)
            self.gui.estado_inicial = estado
            
            # Redibujar el estado como inicial (puede ser inicial Y de aceptación)
            if estado in self.gui.afd.estados_aceptacion:
                self.drawing.redibujar_estado_mejorado(estado, aceptar=True, inicial=True)
            else:
                self.drawing.redibujar_estado_mejorado(estado, aceptar=False, inicial=True)
                
            messagebox.showinfo("Estado Inicial", f"Estado '{estado}' marcado como inicial")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #Quita la marca de estado inicial
    def quitar_inicial(self, estado):
        if estado == self.gui.afd.estado_inicial:
            self.gui.save_state_for_undo()  # Guardar antes de cambiar
            self.gui.afd.estado_inicial = None
            self.gui.estado_inicial = None
            # Redibujar el estado con color normal o de aceptación si corresponde
            if estado in self.gui.afd.estados_aceptacion:
                self.drawing.redibujar_estado_mejorado(estado, aceptar=True)
            else:
                self.drawing.redibujar_estado_mejorado(estado, aceptar=False, inicial=False)
            messagebox.showinfo("Estado Inicial", f"Estado '{estado}' ya no es inicial")
        else:
            messagebox.showinfo("Info", f"El estado '{estado}' no era inicial")

    #Alterna el estado de aceptación
    def toggle_aceptacion(self, estado):
        try:
            self.gui.save_state_for_undo()  # Guardar antes de cambiar
            if estado in self.gui.afd.estados_aceptacion:
                self.gui.afd.estados_aceptacion.remove(estado)
                self.gui.afd.estados[estado].is_accepting = False
                self.drawing.redibujar_estado_mejorado(estado, aceptar=False)
            else:
                self.gui.afd.agregar_estado_aceptacion(estado)
                self.drawing.redibujar_estado_mejorado(estado, aceptar=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #Crea una transición del estado a sí mismo
    def crear_autotransicion(self, estado):
        simbolo = self.pedir_simbolo_transicion(estado, estado)
        if simbolo:
            try:
                self.gui.save_state_for_undo()  # Guardar antes de crear
                self.gui.afd.agregar_simbolo(simbolo)
                self.gui.afd.agregar_transicion(estado, simbolo, estado)
                self.drawing.dibujar_transicion_mejorada(estado, estado, simbolo)
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear auto-transición: {str(e)}")

    #Elimina un estado y sus transiciones
    def eliminar_estado(self, estado):
        if messagebox.askyesno("Confirmar", f"¿Eliminar el estado '{estado}'?"):
            # Eliminar elementos gráficos del estado
            if estado in self.gui.estados_graficos:
                _, _, circle, text, shadow = self.gui.estados_graficos[estado]
                self.gui.canvas.delete(circle)
                self.gui.canvas.delete(text)
                self.gui.canvas.delete(shadow)
                del self.gui.estados_graficos[estado]
            
            # Eliminar transiciones gráficas relacionadas
            self.gui.transiciones_graficas = [
                t for t in self.gui.transiciones_graficas 
                if t['origen'] != estado and t['destino'] != estado
            ]
            
            # Eliminar del AFD
            if estado in self.gui.afd.estados:
                del self.gui.afd.estados[estado]
            if estado in self.gui.afd.estados_aceptacion:
                self.gui.afd.estados_aceptacion.remove(estado)
            if self.gui.afd.estado_inicial == estado:
                self.gui.afd.estado_inicial = None
                self.gui.estado_inicial = None
            
            # Eliminar transiciones del AFD
            self.gui.afd.transiciones = [
                t for t in self.gui.afd.transiciones 
                if t.current_state != estado and t.next_state != estado
            ]
            
            # Redibujar canvas
            self.drawing.redibujar_todo()

    #Elimina una transición específica
    def eliminar_transicion(self, trans_info):
        if messagebox.askyesno("Confirmar", 
                             f"¿Eliminar transición {trans_info['origen']} -{trans_info['simbolo']}→ {trans_info['destino']}?"):
            # Eliminar elementos gráficos
            for elemento in trans_info['elementos']:
                self.gui.canvas.delete(elemento)
            
            # Eliminar de la lista gráfica
            self.gui.transiciones_graficas.remove(trans_info)
            
            # Eliminar del AFD
            self.gui.afd.transiciones = [
                t for t in self.gui.afd.transiciones 
                if not (t.current_state == trans_info['origen'] and 
                       t.next_state == trans_info['destino'] and 
                       t.symbol == trans_info['simbolo'])
            ]

    #Elimina el estado seleccionado
    def eliminar_seleccionado(self, event=None):
        if self.gui.estado_seleccionado:
            self.gui.save_state_for_undo()  # Guardar antes de eliminar
            self.eliminar_estado(self.gui.estado_seleccionado)
            self.gui.estado_seleccionado = None

    #Pide al usuario el símbolo para una transición
    def pedir_simbolo_transicion(self, origen, destino):
        if origen == destino:
            prompt = f"Símbolo para auto-transición en {origen}:"
        else:
            prompt = f"Símbolo para transición {origen} → {destino}:"
        
        simbolo = simpledialog.askstring("Transición", prompt)

        return simbolo.strip() if simbolo else None


