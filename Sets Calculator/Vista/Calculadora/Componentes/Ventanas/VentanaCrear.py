import customtkinter as ctk
from Vista.Calculadora.Componentes.Generales.Lista import ListaConjunto

class VentanaCrear(ctk.CTkToplevel):
    def __init__(self, master, controlador, lista_conjuntos, nombre_conjunto=None, conjunto=None):
        super().__init__(master=master)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.master = master
        self.transient(master)  
        self.geometry("600x600")
        self.iconbitmap("Vista//Materiales//icono.ico")
        self.controlador = controlador
        self.lista_conjuntos = lista_conjuntos
        self.nombre_conjunto = nombre_conjunto
        self.conjunto = conjunto
        
        self.crear_widgets()
        self.configurar_widgets()
        self.pack_widgets()
        
        if self.conjunto != None:
            self.insertar_conjunto()
        
        if self.nombre_conjunto != None:
            self.bloquear_nombre()
        
        if self.nombre_conjunto == 'U':
            self.title("Crear conjunto universal")
        else:
            self.title("Crear Conjunto")

    def crear_widgets(self):

        self.titulo = ctk.CTkLabel(
            self,
            text="Crea un conjunto",
            font=("Century Gothic", 50)
            )
        
        self.nombre_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ingresa el nombre",
            font=("Century Gothic", 18),
            corner_radius=20
            )

        self.elemento_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ingresa cada elemento",
            font=("Century Gothic", 18),
            corner_radius=20
            )

        self.insertar_boton = ctk.CTkButton(
            self,
            text="Insertar elemento",
            font=("Century Gothic", 18),
            corner_radius=20
            )

        self.elementos_label = ctk.CTkLabel(
            self,
            text="Elementos",
            justify="center"
            )
        
        self.elementos_lista = ListaConjunto(self)
        
        self.crear_boton = ctk.CTkButton(
            self,
            text="Crear conjunto",
            font=("Century Gothic", 18),
            corner_radius=20
            )

    def configurar_widgets(self):
        self.nombre_entry.bind("<KeyRelease>", self.validar_entrada)
        self.nombre_entry.bind("<Return>", lambda evento: self.elemento_entry.focus())
        self.elemento_entry.bind("<Return>", self.insertar_elemento)
        self.elemento_entry.bind("<Shift-Return>", self.crear_conjunto)
        self.insertar_boton.bind("<Button-1>", self.insertar_elemento)
        self.crear_boton.bind("<Button-1>", self.crear_conjunto)

    def pack_widgets(self):
        self.titulo.pack(expand=True, fill="both", pady=20, padx=40)
        self.nombre_entry.pack(expand=True, fill="both", padx=40, pady=10)
        self.elemento_entry.pack(expand=True, fill="both", padx=40, pady=10)
        self.insertar_boton.pack(expand=True, fill="both", padx=60, pady=(5, 10))
        self.elementos_label.pack(fill="x", pady=(10,0))
        self.elementos_lista.pack(expand=True, fill="both", pady=(5, 20))
        self.crear_boton.pack(expand=True, fill="both", padx=60, pady=(5, 20))
    
    def insertar_elemento(self, evento):
        elementos = self.elementos_lista.get_elementos()
        elemento = self.elemento_entry.get()
        if elemento == "":
            self.elementos_label.configure(text="Elemento vacío", text_color="red")
            return

        if elemento in elementos:
            self.elementos_label.configure(text="Elemento ya existe", text_color="red")
            return
        
        if self.nombre_conjunto != 'U':
            if not elemento in self.controlador.get_conjunto("U"):
                self.elementos_label.configure(text="El elemento no se encuentra en el universal", text_color="red")
                return
            
        self.elemento_entry.delete(0, "end")
        self.elementos_lista.agregar_conjunto(elemento)
    
    def insertar_conjunto(self):
        self.elemento_entry.configure(state="disabled")
        self.insertar_boton.configure(state="disabled")
        lista_elementos = list(self.conjunto)
        for elemento in lista_elementos:
            self.elementos_lista.agregar_conjunto(elemento)
        
    def crear_conjunto(self, evento):
        nombre = self.nombre_entry.get()
        conjunto = self.elementos_lista.get_elementos()
        if nombre in self.lista_conjuntos.get_elementos():
            self.nombre_entry.delete(0,"end")
            self.elementos_label.configure(text="Ingrese un conjunto que no exista", text_color="red")
            return
        self.controlador.crear_conjunto(nombre, conjunto)
        self.lista_conjuntos.agregar_conjunto(nombre)
        self.master.destroy()
        self.destroy()
    
    def validar_entrada(self, event):
        texto_actual = self.nombre_entry.get()
        
        if event.keysym == "BackSpace":
            return
        
        if len(texto_actual) > 1:
            self.nombre_entry.delete(1, "end") 
            
        if texto_actual and texto_actual.islower():
            texto_actual = texto_actual.upper()
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, texto_actual)
        
        elif texto_actual.isdigit():
            self.nombre_entry.delete(0, "end")
            
            
    def bloquear_nombre(self):
        self.nombre_entry.insert(0, self.nombre_conjunto)
        self.nombre_entry.configure(state="disabled")