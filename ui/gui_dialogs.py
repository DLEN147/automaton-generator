import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from data.serializer import guardar_afd, cargar_afd

#Maneja todas las ventanas de diálogo y funcionalidades avanzadas
class DialogManager:
    def __init__(self, gui):
        self.gui = gui

    #Verifica que el AFD esté completo para evaluación
    def _verificar_afd_completo(self):
        if not self.gui.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return False
        
        if not self.gui.afd.estado_inicial:
            messagebox.showwarning("Advertencia", "Debe definir un estado inicial")
            return False
            
        if not self.gui.afd.estados_aceptacion:
            messagebox.showwarning("Advertencia", "Debe definir al menos un estado de aceptación")
            return False
            
        if not self.gui.afd.alfabeto:
            messagebox.showwarning("Advertencia", "Debe definir al menos una transición para crear el alfabeto")
            return False
        
        return True
#Evalúa una cadena con el AFD actual
    def evaluar_cadena(self):
        if not self._verificar_afd_completo():
            return
            
        cadena = simpledialog.askstring("Evaluar Cadena", "Ingrese la cadena a evaluar:")
        if cadena is None:
            return
            
        try:
            es_aceptada, recorrido = self.gui.afd.procesar_cadena(cadena)
            
            resultado = "ACEPTADA ✓" if es_aceptada else "RECHAZADA ✗"
            recorrido_str = " → ".join(recorrido)
            
            # Información adicional del AFD
            info_afd = f"Estados: {len(self.gui.afd.estados)}\n"
            info_afd += f"Alfabeto: {{{', '.join(sorted(self.gui.afd.alfabeto))}}}\n"
            info_afd += f"Estado inicial: {self.gui.afd.estado_inicial}\n"
            info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.gui.afd.estados_aceptacion))}}}\n\n"
            
            mensaje = info_afd
            mensaje += f"Cadena evaluada: '{cadena}'\n"
            mensaje += f"Recorrido: {recorrido_str}\n\n"
            mensaje += f"Resultado: {resultado}"
            
            self._mostrar_ventana_resultado("Resultado de Evaluación", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar cadena: {str(e)}")

    #Permite evaluar múltiples cadenas de forma interactiva
    def evaluador_multiple(self):
        if not self._verificar_afd_completo():
            return

        # Crear ventana del evaluador múltiple
        ventana_evaluador = tk.Toplevel(self.gui.root)
        ventana_evaluador.title("🎯 Evaluador Múltiple de Cadenas")
        ventana_evaluador.geometry("700x600")
        ventana_evaluador.configure(bg=self.gui.colors['bg_primary'])

        # Frame principal
        main_frame = tk.Frame(ventana_evaluador, bg=self.gui.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Información del AFD
        info_frame = tk.Frame(main_frame, bg=self.gui.colors['bg_secondary'], relief="ridge", bd=2)
        info_frame.pack(fill="x", pady=(0, 15))

        tk.Label(info_frame, text="📊 Información del AFD", 
                font=('Segoe UI', 12, 'bold'), bg=self.gui.colors['bg_secondary'], fg='white').pack(pady=10)

        info_afd = f"Estados: {{{', '.join(sorted(self.gui.afd.estados.keys()))}}}\n"
        info_afd += f"Alfabeto: {{{', '.join(sorted(self.gui.afd.alfabeto))}}}\n"
        info_afd += f"Estado inicial: {self.gui.afd.estado_inicial}\n"
        info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.gui.afd.estados_aceptacion))}}}"

        tk.Label(info_frame, text=info_afd, font=('Consolas', 10),
                bg=self.gui.colors['bg_secondary'], fg='white', justify="left").pack(pady=(0, 10))

        # Frame de entrada
        entrada_frame = tk.Frame(main_frame, bg=self.gui.colors['bg_primary'])
        entrada_frame.pack(fill="x", pady=(0, 10))

        tk.Label(entrada_frame, text="Ingrese cadena a evaluar:", 
                font=('Segoe UI', 11, 'bold'), bg=self.gui.colors['bg_primary'], fg='white').pack(anchor="w")

        entrada_var = tk.StringVar()
        entrada_entry = tk.Entry(entrada_frame, textvariable=entrada_var, font=('Consolas', 12), width=30)
        entrada_entry.pack(side="left", pady=5)

        def evaluar_cadena_actual():
            cadena = entrada_var.get().strip()
            if not cadena:
                return

            try:
                es_aceptada, recorrido = self.gui.afd.procesar_cadena(cadena)
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
                 bg=self.gui.colors['boton_warning'], fg='white',
                 font=('Segoe UI', 10, 'bold'), padx=20).pack(side="left", padx=10)

        # Área de resultados
        tk.Label(main_frame, text="📋 Historial de Evaluaciones:", 
                font=('Segoe UI', 11, 'bold'), bg=self.gui.colors['bg_primary'], fg='white').pack(anchor="w", pady=(10, 5))

        # Frame con scroll para resultados
        resultado_frame = tk.Frame(main_frame, bg=self.gui.colors['bg_primary'])
        resultado_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=('Consolas', 10),
                               bg=self.gui.colors['canvas_bg'], fg=self.gui.colors['texto'],
                               yscrollcommand=scrollbar.set, padx=10, pady=10)
        resultado_text.pack(fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        resultado_text.insert("1.0", "💡 Ingrese cadenas para evaluar. Presione Enter o click en Evaluar.\n")
        resultado_text.config(state="disabled")

        # Botones de control
        control_frame = tk.Frame(main_frame, bg=self.gui.colors['bg_primary'])
        control_frame.pack(fill="x", pady=10)

        tk.Button(control_frame, text="🗑️ Limpiar Historial", 
                 command=lambda: self._limpiar_historial(resultado_text),
                 bg=self.gui.colors['boton_danger'], fg='white',
                 font=('Segoe UI', 10, 'bold')).pack(side="left")

        tk.Button(control_frame, text="❌ Cerrar", command=ventana_evaluador.destroy,
                 bg=self.gui.colors['bg_secondary'], fg='white',
                 font=('Segoe UI', 10, 'bold')).pack(side="right")

        # Bind Enter key
        entrada_entry.bind("<Return>", lambda e: evaluar_cadena_actual())
        entrada_entry.focus()

        # Centrar ventana
        ventana_evaluador.transient(self.gui.root)
        ventana_evaluador.grab_set()
 #Genera las primeras 10 cadenas del lenguaje
    def generar_cadenas_lenguaje(self):
        if not self._verificar_afd_completo():
            return

        try:
            # Generar cadenas
            cadenas_validas = self.gui.afd.generar_cadenas_validas(10)
            
            # Crear ventana de resultados
            ventana_cadenas = tk.Toplevel(self.gui.root)
            ventana_cadenas.title("🎲 Primeras 10 Cadenas del Lenguaje")
            ventana_cadenas.geometry("600x500")
            ventana_cadenas.configure(bg=self.gui.colors['bg_primary'])

            # Frame principal
            main_frame = tk.Frame(ventana_cadenas, bg=self.gui.colors['bg_primary'])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Título
            tk.Label(main_frame, text="🎲 Cadenas del Lenguaje L(AFD)", 
                    font=('Segoe UI', 14, 'bold'), bg=self.gui.colors['bg_primary'], fg='white').pack(pady=(0, 15))

            # Información del AFD
            info_frame = tk.Frame(main_frame, bg=self.gui.colors['bg_secondary'], relief="ridge", bd=2)
            info_frame.pack(fill="x", pady=(0, 15))

            info_afd = f"Estados: {{{', '.join(sorted(self.gui.afd.estados.keys()))}}}\n"
            info_afd += f"Alfabeto: {{{', '.join(sorted(self.gui.afd.alfabeto))}}}\n"
            info_afd += f"Estado inicial: {self.gui.afd.estado_inicial}\n"
            info_afd += f"Estados de aceptación: {{{', '.join(sorted(self.gui.afd.estados_aceptacion))}}}"

            tk.Label(info_frame, text=info_afd, font=('Consolas', 10),
                    bg=self.gui.colors['bg_secondary'], fg='white', justify="left").pack(padx=15, pady=10)

            # Área de cadenas
            cadenas_frame = tk.Frame(main_frame, bg=self.gui.colors['canvas_bg'], relief="sunken", bd=2)
            cadenas_frame.pack(fill="both", expand=True, pady=(0, 15))

            # Scroll para las cadenas
            scrollbar_cadenas = tk.Scrollbar(cadenas_frame)
            scrollbar_cadenas.pack(side="right", fill="y")

            cadenas_text = tk.Text(cadenas_frame, wrap="word", font=('Consolas', 11),
                                  bg=self.gui.colors['canvas_bg'], fg=self.gui.colors['texto'],
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
            button_frame = tk.Frame(main_frame, bg=self.gui.colors['bg_primary'])
            button_frame.pack(fill="x")

            tk.Button(button_frame, text="🔄 Regenerar", 
                     command=lambda: self._regenerar_cadenas(cadenas_text),
                     bg=self.gui.colors['boton_primary'], fg='white',
                     font=('Segoe UI', 10, 'bold')).pack(side="left")

            tk.Button(button_frame, text="❌ Cerrar", command=ventana_cadenas.destroy,
                     bg=self.gui.colors['bg_secondary'], fg='white',
                     font=('Segoe UI', 10, 'bold')).pack(side="right")

            # Centrar ventana
            ventana_cadenas.transient(self.gui.root)
            ventana_cadenas.grab_set()

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar cadenas: {str(e)}")

#Muestra la quintupla formal del AFD
    def mostrar_quintupla(self):  
        if not self.gui.estados_graficos:
            messagebox.showwarning("Advertencia", "Debe crear al menos un estado")
            return

        # Crear ventana de la quintupla
        ventana_quintupla = tk.Toplevel(self.gui.root)
        ventana_quintupla.title("📋 Quintupla del AFD")
        ventana_quintupla.geometry("700x600")
        ventana_quintupla.configure(bg=self.gui.colors['bg_primary'])

        # Frame principal
        main_frame = tk.Frame(ventana_quintupla, bg=self.gui.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text="📋 Definición Formal del AFD", 
                font=('Segoe UI', 14, 'bold'), bg=self.gui.colors['bg_primary'], fg='white').pack(pady=(0, 20))

        # Frame de contenido con scroll
        contenido_frame = tk.Frame(main_frame, bg=self.gui.colors['canvas_bg'], relief="sunken", bd=2)
        contenido_frame.pack(fill="both", expand=True, pady=(0, 15))

        scrollbar_quintupla = tk.Scrollbar(contenido_frame)
        scrollbar_quintupla.pack(side="right", fill="y")

        quintupla_text = tk.Text(contenido_frame, wrap="word", font=('Consolas', 11),
                               bg=self.gui.colors['canvas_bg'], fg=self.gui.colors['texto'],
                               yscrollcommand=scrollbar_quintupla.set, padx=20, pady=20)
        quintupla_text.pack(fill="both", expand=True)
        scrollbar_quintupla.config(command=quintupla_text.yview)

        # Construir contenido de la quintupla
        contenido = self._construir_quintupla()
        quintupla_text.insert("1.0", contenido)
        quintupla_text.config(state="disabled")

        # Botón cerrar
        tk.Button(main_frame, text="❌ Cerrar", command=ventana_quintupla.destroy,
                 bg=self.gui.colors['bg_secondary'], fg='white',
                 font=('Segoe UI', 12, 'bold'), pady=10).pack()

        # Centrar ventana
        ventana_quintupla.transient(self.gui.root)
        ventana_quintupla.grab_set()

    #Guarda el AFD en un archivo
    def guardar(self):
        if not self.gui.estados_graficos:
            messagebox.showwarning("Advertencia", "No hay estados para guardar")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                guardar_afd(self.gui.afd, filename)
                messagebox.showinfo("Éxito", f"AFD guardado en {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    #Carga un AFD desde un archivo
    def cargar(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                # Guardar estado antes de cargar (para permitir deshacer la carga)
                self.gui.save_state_for_undo()
                
                # Limpiar canvas actual
                self.gui.limpiar_canvas()
                
                # Cargar AFD
                self.gui.afd = cargar_afd(filename)
                
                # Redibujar gráficamente (posiciones automáticas)
                self.gui.drawing_manager.generar_layout_automatico()
                
                messagebox.showinfo("Éxito", f"AFD cargado desde {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {str(e)}")

    #MÉTODOS AUXILIARES
    
    #Muestra una ventana estilizada con un resultado
    def _mostrar_ventana_resultado(self, titulo, mensaje):
        """Muestra una ventana estilizada con un resultado"""
        ventana_resultado = tk.Toplevel(self.gui.root)
        ventana_resultado.title(titulo)
        ventana_resultado.geometry("500x400")
        ventana_resultado.configure(bg=self.gui.colors['bg_primary'])
        
        # Frame con scroll
        frame_scroll = tk.Frame(ventana_resultado, bg=self.gui.colors['bg_primary'])
        frame_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Texto del resultado
        texto_resultado = tk.Text(frame_scroll, wrap="word", font=("Consolas", 11),
                                bg=self.gui.colors['canvas_bg'], fg=self.gui.colors['texto'],
                                padx=15, pady=15)
        texto_resultado.pack(fill="both", expand=True)
        texto_resultado.insert("1.0", mensaje)
        texto_resultado.config(state="disabled")
        
        # Botón cerrar
        tk.Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy,
                 bg=self.gui.colors['boton_primary'], fg='white',
                 font=('Segoe UI', 10, 'bold'), pady=10).pack(pady=(10, 0))
        
        # Centrar ventana
        ventana_resultado.transient(self.gui.root)
        ventana_resultado.grab_set()

    #Limpia el historial del evaluador múltiple
    def _limpiar_historial(self, text_widget):
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", "💡 Ingrese cadenas para evaluar. Presione Enter o click en Evaluar.\n")
        text_widget.config(state="disabled")

    #Regenera las cadenas en la ventana actual
    def _regenerar_cadenas(self, text_widget):
        try:
            cadenas_validas = self.gui.afd.generar_cadenas_validas(10)
            
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

    def _construir_quintupla(self):
        contenido = "Un Autómata Finito Determinista (AFD) se define formalmente como:\n\n"
        contenido += "AFD = (Q, Σ, δ, q₀, F)\n\n"
        contenido += "Donde:\n\n"

        # Q - Estados
        estados_ordenados = sorted(self.gui.afd.estados.keys())
        contenido += "Q = Conjunto de estados\n"
        contenido += f"Q = {{{', '.join(estados_ordenados)}}}\n"
        contenido += f"   |Q| = {len(estados_ordenados)} estados\n\n"

        # Σ - Alfabeto
        alfabeto_ordenado = sorted(self.gui.afd.alfabeto) if self.gui.afd.alfabeto else []
        contenido += "Σ = Alfabeto de entrada\n"
        if alfabeto_ordenado:
            contenido += f"Σ = {{{', '.join(alfabeto_ordenado)}}}\n"
            contenido += f"   |Σ| = {len(alfabeto_ordenado)} símbolos\n\n"
        else:
            contenido += "Σ = ∅ (vacío - no hay transiciones definidas)\n\n"

        # δ - Función de transición
        contenido += "δ = Función de transición\n"
        contenido += "δ: Q × Σ → Q\n"
        if self.gui.afd.transiciones:
            contenido += "Transiciones definidas:\n"
            transiciones_ordenadas = sorted(self.gui.afd.transiciones, 
                                          key=lambda t: (t.current_state, t.symbol, t.next_state))
            for trans in transiciones_ordenadas:
                contenido += f"   δ({trans.current_state}, '{trans.symbol}') = {trans.next_state}\n"
            contenido += f"\nTotal de transiciones: {len(self.gui.afd.transiciones)}\n\n"
        else:
            contenido += "   No hay transiciones definidas\n\n"

        # q₀ - Estado inicial
        contenido += "q₀ = Estado inicial\n"
        if self.gui.afd.estado_inicial:
            contenido += f"q₀ = {self.gui.afd.estado_inicial}\n\n"
        else:
            contenido += "q₀ = ∅ (no definido)\n\n"

        # F - Estados de aceptación
        estados_finales_ordenados = sorted(self.gui.afd.estados_aceptacion)
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
        if not self.gui.afd.estado_inicial:
            problemas.append("❌ No hay estado inicial definido")
        if not self.gui.afd.estados_aceptacion:
            problemas.append("❌ No hay estados de aceptación")
        if not self.gui.afd.alfabeto:
            problemas.append("❌ No hay alfabeto definido (faltan transiciones)")
        if not self.gui.afd.transiciones:
            problemas.append("❌ No hay transiciones definidas")

        # Verificar completitud de la función de transición
        if self.gui.afd.alfabeto and self.gui.afd.estados:
            transiciones_esperadas = len(self.gui.afd.estados) * len(self.gui.afd.alfabeto)
            transiciones_existentes = len(self.gui.afd.transiciones)
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
        if self.gui.afd.estado_inicial and self.gui.afd.estados_aceptacion:
            contenido += "✅ Puede reconocer un lenguaje\n"
        if len(self.gui.afd.estados) == 1:
            contenido += "📍 AFD trivial (un solo estado)\n"
        if self.gui.afd.estado_inicial in self.gui.afd.estados_aceptacion:
            contenido += "📍 Acepta la cadena vacía (ε)\n"


        return contenido
