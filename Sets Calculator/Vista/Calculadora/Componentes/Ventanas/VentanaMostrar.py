import customtkinter as ctk


class VentanaMostrar(ctk.CTkToplevel):
    def __init__(self, master, titulo, texto):
        super().__init__(master=master)
        self.master = master
        self.geometry("800x600")
        self.iconbitmap("Vista//Materiales//icono.ico")
        self.title(titulo)
        self.titulo= titulo
        self.texto = texto
        
        self.crear_widgets()
        self.configurar_widgets()
        self.pack_widgets()

    def crear_widgets(self):
        self.frame_principal = ctk.CTkFrame(self)
        
        self.titulo = ctk.CTkLabel(
            self,
            text=self.titulo,
            font=("Century Gothic", 70)
            )

        self.texto_mostrado = ctk.CTkTextbox(
            self.frame_principal,
            font=("Century Gothic", 30)
            )
    
    def configurar_widgets(self):
        self.texto_mostrado.insert("end", self.texto)
        self.texto_mostrado.configure(state="disabled")
    
    def pack_widgets(self):
        self.titulo.pack(fill="x")
        self.frame_principal.pack(expand=True, fill="both", padx=40, pady=40)
        self.texto_mostrado.pack(expand=True, fill="both")
