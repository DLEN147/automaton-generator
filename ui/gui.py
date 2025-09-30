from .gui_base import AFDGuiBase
import tkinter as tk

class AFDGui(AFDGuiBase):
    
    def __init__(self, root):
        super().__init__(root)
    
    # Asegurar que todos los métodos están disponibles
    def save_state_for_undo(self):
        if hasattr(self, 'history_manager'):
            self.history_manager.save_state()
        else:
            print("Warning: history_manager not initialized")


def run_gui():
    root = tk.Tk()
    app = AFDGui(root)

    root.mainloop()
