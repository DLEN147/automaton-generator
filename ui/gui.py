from .gui_base import AFDGuiBase


class AFDGui(AFDGuiBase):
    """
    Clase principal de la GUI que hereda de AFDGuiBase
    Esta clase puede extenderse con funcionalidades adicionales
    """
    
    def __init__(self, root):
        super().__init__(root)
        # Aquí se pueden agregar inicializaciones adicionales específicas
    
    # Asegurar que todos los métodos están disponibles
    def save_state_for_undo(self):
        """Guarda el estado actual para permitir deshacer - delegado al history_manager"""
        if hasattr(self, 'history_manager'):
            self.history_manager.save_state()
        else:
            print("Warning: history_manager not initialized")


def run_gui():
    """Función principal para ejecutar la GUI"""
    import tkinter as tk
    root = tk.Tk()
    app = AFDGui(root)
    root.mainloop()