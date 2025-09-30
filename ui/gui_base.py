import tkinter as tk
from tkinter import messagebox
from models.afd import AFD
from .gui_events import EventHandler
from .gui_drawing import DrawingManager
from .gui_dialogs import DialogManager


class AFDGuiBase:
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Simulador de AFD - Diseñador Visual")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        #Configurar estilo moderno
        self.setup_styles()

        #Inicializar modelo
        self.afd = AFD()

        # Estados gráficos
        self.estado_counter = 0
        self.estados_graficos = {}   #nombre
        self.estado_inicial = None
        self.transiciones_graficas = []

        #Drag & Drop
        self.dragging = False
        self.drag_estado = None
        self.drag_offset = (0, 0)
        self.drag_threshold = 5
        self.drag_started = False
        self.estado_seleccionado = None
        self.hover_estado = None
        self.modo_borrador = False

        #Instanciar componentes
        self.drawing_manager = DrawingManager(self)
        self.event_handler = EventHandler(self)
        self.dialog_manager = DialogManager(self)

        self.create_interface()
        self.setup_events()
        self.setup_keyboard_shortcuts()

    def setup_styles(self):
        #estilos
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

    def create_interface(self):
        #main
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #nav
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill="x", pady=(0, 10))

        self.create_buttons(button_frame)
        self.create_info_section(main_frame)
        self.create_canvas(main_frame)

    def create_buttons(self, parent):
        #botones
        buttons_config = [
            ("💾 Guardar", self.dialog_manager.guardar, self.colors['boton_success']),
            ("📂 Cargar", self.dialog_manager.cargar, self.colors['boton_primary']),
            ("🧪 Evaluar Cadena", self.dialog_manager.evaluar_cadena, self.colors['boton_warning']),
            ("🎯 Evaluador Múltiple", self.dialog_manager.evaluador_multiple, '#8e44ad'),
            ("🎲 Generar Cadenas", self.dialog_manager.generar_cadenas_lenguaje, '#16a085'),
            ("📋 Ver Quintupla", self.dialog_manager.mostrar_quintupla, '#d35400'),
            ("🗑️ Borrador", self.toggle_borrador, self.colors['bg_secondary']),
            ("🔄 Limpiar Todo", self.limpiar_canvas, self.colors['boton_danger'])
        ]

        for text, command, color in buttons_config:
            btn = tk.Button(parent, text=text, command=command,
                           bg=color, fg='white', 
                           font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=5)
            btn.pack(side="left", padx=5)
            
            if "Borrador" in text:
                self.boton_borrador = btn

    def create_info_section(self, parent):
        info_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief="ridge", bd=1)
        info_frame.pack(fill="x", pady=(0, 10))
        
        self.info_label = tk.Label(info_frame, 
                                  text="💡 Click: crear estado | Drag: mover | Click derecho: menú contextual | Click + Click: crear transición",
                                  bg=self.colors['bg_secondary'], fg='white',
                                  font=('Segoe UI', 9), wraplength=800, justify="center")
        self.info_label.pack(pady=10)

    def create_canvas(self, parent):
        canvas_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief="sunken", bd=2)
        canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['canvas_bg'], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_events(self):
        self.canvas.bind("<Button-1>", self.event_handler.on_click)
        self.canvas.bind("<B1-Motion>", self.event_handler.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.event_handler.on_drag_stop)
        self.canvas.bind("<Button-3>", self.event_handler.on_right_click)
        self.canvas.bind("<Motion>", self.event_handler.on_hover)

    def setup_keyboard_shortcuts(self):
        self.root.bind("<Control-s>", lambda e: self.dialog_manager.guardar())
        self.root.bind("<Control-o>", lambda e: self.dialog_manager.cargar())
        self.root.bind("<F5>", lambda e: self.dialog_manager.evaluar_cadena())
        self.root.bind("<Delete>", self.event_handler.eliminar_seleccionado)

    def toggle_borrador(self):
        self.modo_borrador = not self.modo_borrador
        
        if self.modo_borrador:
            self.boton_borrador.config(bg=self.colors['boton_danger'], text="🗑️ Borrador ON")
            self.info_label.config(text="🗑️ MODO BORRADOR: Click en estados o transiciones para eliminar")
            self.canvas.configure(cursor="dotbox")
        else:
            self.boton_borrador.config(bg=self.colors['bg_secondary'], text="🗑️ Borrador")
            self.info_label.config(text="💡 Click: crear estado | Drag: mover | Click derecho: menú contextual | Click + Click: crear transición")
            self.canvas.configure(cursor="")

    def limpiar_canvas(self):
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

    def get_estado_por_coordenada(self, x, y):
        for nombre, (ex, ey, _, _, _) in self.estados_graficos.items():
            if (x-ex)**2 + (y-ey)**2 <= 30**2:
                return nombre
        return None

    def get_transicion_por_coordenada(self, x, y):
        for trans_info in self.transiciones_graficas:
            if trans_info['tipo'] == 'auto':
                # Para auto-transiciones, verificar área del bucle
                origen_x, origen_y, _, _, _ = self.estados_graficos[trans_info['origen']]
                loop_x = origen_x
                loop_y = origen_y - 55
                
                if (x - loop_x)**2 + (y - loop_y)**2 <= 30**2:
                    return trans_info
                    
            elif trans_info['tipo'] == 'normal':
                if len(trans_info['elementos']) >= 2:
                    try:
                        coords = self.canvas.coords(trans_info['elementos'][1])
                        if len(coords) >= 4:
                            x1, y1, x2, y2 = coords
                            if x1 <= x <= x2 and y1 <= y <= y2:
                                return trans_info
                    except:
                        try:
                            line_coords = self.canvas.coords(trans_info['elementos'][0])
                            if len(line_coords) >= 4:
                                x1, y1, x2, y2 = line_coords
                                mid_x = (x1 + x2) / 2
                                mid_y = (y1 + y2) / 2
                                if (x - mid_x)**2 + (y - mid_y)**2 <= 25**2:
                                    return trans_info
                        except:
                            continue

        return None
