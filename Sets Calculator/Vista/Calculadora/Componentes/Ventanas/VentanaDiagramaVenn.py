import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import close
from Modelo.venn import *
import copy

class VentanaDiagramVenn(ctk.CTkToplevel):
    def __init__(self, master, controlador):
        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title("Diagrama de Venn")
        self.geometry("800x800")
        self.controlador = controlador
        
        self.crear_widgets()
        self.pack_widgets()

    def crear_widgets(self):
        self.canvas = FigureCanvasTkAgg(
            self.get_diagrama_venn(),
            master=self
            )

    def configurar_widgets(self):
        pass
    
    def pack_widgets(self):
        self.canvas.get_tk_widget().pack(expand=True, fill="both")
        
    def get_diagrama_venn(self):
        self.diagramas = {
            2: lambda labels, nombres: venn2(labels=labels, names=nombres),
            3: lambda labels, nombres: venn3(labels=labels, names=nombres),
            4: lambda labels, nombres: venn4(labels=labels, names=nombres),
            5: lambda labels, nombres: venn5(labels=labels, names=nombres),
            6: lambda labels, nombres: venn6(labels=labels, names=nombres)
            }

        diccionario_conjuntos = copy.deepcopy(self.controlador.get_conjuntos())
        diccionario_conjuntos.pop('U', lambda: print("No existe U"))
        nombres_conjuntos = list(diccionario_conjuntos.keys())
        conjuntos = list(diccionario_conjuntos.values())
        numero_conjuntos = len(conjuntos)
        
        if numero_conjuntos == 0:
            return
        
        labels = get_labels(conjuntos, fill=["elements"], max_elements=100)
        fig, ax = self.diagramas.get(numero_conjuntos)(labels, nombres_conjuntos)
        ax.set_title("Diagrama de Venn")
        
        del diccionario_conjuntos
        del nombres_conjuntos
        del conjuntos
        
        return fig

    def close(self):
        self.canvas.get_tk_widget().destroy()
        close(self.canvas.figure)
        self.destroy()
