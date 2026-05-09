import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import math
import re
from Funciones.cientifica import *
from Funciones.simples import *
from Funciones.intereses import *

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Tocha")
        self.geometry("450x750")
        self.config(bg="#1C1C1E")
        self.minsize(400, 700)
        
        # Fuentes personalizadas
        self.custom_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.btn_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.hist_font = tkfont.Font(family="Segoe UI", size=14)
        self.label_font = tkfont.Font(family="Segoe UI", size=12)

        # Estilo para los Combobox (flechitas)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground="#2C2C2E", background="#3A3A3C", foreground="black", borderwidth=0)

        # Contenedor para alternar entre vistas
        self.container = tk.Frame(self, bg="#1C1C1E")
        self.container.pack(fill="both", expand=True)

        # Crear interfaces
        self.crear_interfaz_calculadora()
        self.crear_interfaz_menu()
        self.crear_interfaz_intereses()

        # Mostrar calculadora por defecto
        self.mostrar_calculadora()

    def mostrar_calculadora(self):
        self.frame_intereses.pack_forget()
        self.frame_menu.pack_forget()
        self.frame_calc.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Científica")

    def mostrar_menu(self):
        self.frame_calc.pack_forget()
        self.frame_intereses.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Funciones")

    def mostrar_intereses(self):
        self.frame_menu.pack_forget()
        self.frame_calc.pack_forget()
        self.frame_intereses.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Intereses")

    def crear_interfaz_calculadora(self):
        self.frame_calc = tk.Frame(self.container, bg="#1C1C1E")
        
        # Botón para abrir el menú de funciones
        btn_menu = tk.Button(self.frame_calc, text="Funciones", font=("Segoe UI", 10, "bold"), 
                               bg="#3A3A3C", fg="#FF9F0A", bd=0, padx=10, pady=5, cursor="hand2",
                               command=self.mostrar_menu)
        btn_menu.pack(anchor="e", padx=20, pady=(10, 0))

        # Historial
        self.historial = tk.Label(self.frame_calc, text="", font=self.hist_font, bg="#1C1C1E", fg="#8E8E93", justify="right", anchor="e")
        self.historial.pack(fill="x", padx=20, pady=(10, 0))

        # Pantalla Principal
        self.pantalla = tk.Entry(self.frame_calc, font=self.custom_font, bg="#1C1C1E", fg="#FFFFFF", justify="right", bd=0, insertbackground="#FFFFFF")
        self.pantalla.pack(fill="x", padx=10, pady=10)
        
        # Frame para botones (Grid)
        grid_frame = tk.Frame(self.frame_calc, bg="#1C1C1E")
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)

        for i in range(6): grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(5): grid_frame.grid_columnconfigure(i, weight=1)

        bg_num, bg_acc, bg_op, bg_cient = "#505050", "#D4D4D2", "#FF9F0A", "#3A3A3C"
        
        botones = [
            ('C', 0, 0, bg_acc, "#000000"), ('⌫', 0, 1, bg_acc, "#000000"), ('(', 0, 2, bg_acc, "#000000"), (')', 0, 3, bg_acc, "#000000"), ('/', 0, 4, bg_op, "#FFFFFF"),
            ('sin', 1, 0, bg_cient, "#FFFFFF"), ('7', 1, 1, bg_num, "#FFFFFF"), ('8', 1, 2, bg_num, "#FFFFFF"), ('9', 1, 3, bg_num, "#FFFFFF"), ('*', 1, 4, bg_op, "#FFFFFF"),
            ('cos', 2, 0, bg_cient, "#FFFFFF"), ('4', 2, 1, bg_num, "#FFFFFF"), ('5', 2, 2, bg_num, "#FFFFFF"), ('6', 2, 3, bg_num, "#FFFFFF"), ('-', 2, 4, bg_op, "#FFFFFF"),
            ('tan', 3, 0, bg_cient, "#FFFFFF"), ('1', 3, 1, bg_num, "#FFFFFF"), ('2', 3, 2, bg_num, "#FFFFFF"), ('3', 3, 3, bg_num, "#FFFFFF"), ('+', 3, 4, bg_op, "#FFFFFF"),
            ('log', 4, 0, bg_cient, "#FFFFFF"), ('e', 4, 1, bg_cient, "#FFFFFF"), ('0', 4, 2, bg_num, "#FFFFFF"), ('.', 4, 3, bg_num, "#FFFFFF"), ('=', 4, 4, bg_op, "#FFFFFF"),
            ('ln', 5, 0, bg_cient, "#FFFFFF"), ('π', 5, 1, bg_cient, "#FFFFFF"), ('^', 5, 2, bg_cient, "#FFFFFF"), ('√', 5, 3, bg_cient, "#FFFFFF"), ('!', 5, 4, bg_cient, "#FFFFFF")
        ]

        for (texto, f, c, bg, fg) in botones:
            btn = tk.Button(grid_frame, text=texto, font=self.btn_font, bg=bg, fg=fg, bd=0, 
                            activebackground="#707070", activeforeground=fg, cursor="hand2",
                            command=lambda t=texto: self.click_boton(t))
            btn.grid(row=f, column=c, sticky="nsew", padx=3, pady=3)
            
        # Eventos de Teclado
        self.bind('<Return>', lambda e: self.click_boton('='))
        self.bind('<BackSpace>', lambda e: self.click_boton('⌫'))
        self.bind('<Escape>', lambda e: self.click_boton('C'))
        self.pantalla.focus_set()

    def crear_interfaz_menu(self):
        self.frame_menu = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_menu, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_calculadora)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_menu, text="Funciones Especiales", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        # Lista de funciones (se pueden agregar más aquí)
        lista_funciones = [
            ("Intereses", self.mostrar_intereses),
        ]
        # Orden alfabético
        lista_funciones.sort()

        for nombre, comando in lista_funciones:
            btn = tk.Button(self.frame_menu, text=nombre, font=self.btn_font, bg="#3A3A3C", fg="white", 
                            bd=0, pady=10, cursor="hand2", command=comando)
            btn.pack(fill="x", padx=50, pady=5)

    def crear_interfaz_intereses(self):
        self.frame_intereses = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_intereses, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_menu)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_intereses, text="Cálculo de Intereses", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        label_style = {"font": ("Segoe UI", 11), "bg": "#1C1C1E", "fg": "#8E8E93"}
        entry_style = {"font": ("Segoe UI", 16), "bg": "#2C2C2E", "fg": "white", "insertbackground": "white", "bd": 0, "justify": "center"}

        # Capital
        tk.Label(self.frame_intereses, text="Capital Inicial ($)", **label_style).pack()
        self.ent_capital = tk.Entry(self.frame_intereses, **entry_style)
        self.ent_capital.pack(pady=5, padx=50, fill="x", ipady=8)

        # Tasa con flechita (Combobox)
        tk.Label(self.frame_intereses, text="Tasa de Interés (%)", **label_style).pack(pady=(15, 0))
        tasa_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        tasa_f.pack(fill="x", padx=50)
        self.ent_tasa = tk.Entry(tasa_f, **entry_style)
        self.ent_tasa.pack(side="left", fill="x", expand=True, ipady=8)
        self.combo_tasa = ttk.Combobox(tasa_f, values=["Anual", "Mensual"], state="readonly", width=8, font=("Segoe UI", 12))
        self.combo_tasa.set("Anual")
        self.combo_tasa.pack(side="left", padx=(5, 0))

        # Tiempo con flechita (Combobox)
        tk.Label(self.frame_intereses, text="Tiempo", **label_style).pack(pady=(15, 0))
        tiempo_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        tiempo_f.pack(fill="x", padx=50)
        self.ent_tiempo = tk.Entry(tiempo_f, **entry_style)
        self.ent_tiempo.pack(side="left", fill="x", expand=True, ipady=8)
        self.combo_tiempo = ttk.Combobox(tiempo_f, values=["Años", "Meses", "Días"], state="readonly", width=8, font=("Segoe UI", 12))
        self.combo_tiempo.set("Meses")
        self.combo_tiempo.pack(side="left", padx=(5, 0))

        # Botones de cálculo
        btn_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        btn_f.pack(pady=40)
        tk.Button(btn_f, text="Simple", font=self.btn_font, bg="#FF9F0A", fg="white", bd=0, padx=20, pady=10, 
                  command=lambda: self.calcular_int("simple")).pack(side="left", padx=10)
        tk.Button(btn_f, text="Compuesto", font=self.btn_font, bg="#5856D6", fg="white", bd=0, padx=20, pady=10, 
                  command=lambda: self.calcular_int("compuesto")).pack(side="left", padx=10)

        self.lbl_res_int = tk.Label(self.frame_intereses, text="Resultado: $0", font=("Segoe UI", 18, "bold"), bg="#1C1C1E", fg="#32D74B", justify="center")
        self.lbl_res_int.pack(pady=10)

    def calcular_int(self, tipo):
        try:
            c = float(self.ent_capital.get().replace(',', ''))
            rate_val = float(self.ent_tasa.get()) / 100
            time_val = float(self.ent_tiempo.get())
            
            rate_period = self.combo_tasa.get()
            time_period = self.combo_tiempo.get()

            # Normalización: Convertir la tasa al periodo del tiempo seleccionado
            # Si el tiempo es en Meses, necesitamos la tasa mensual
            if time_period == "Meses":
                r = rate_val if rate_period == "Mensual" else rate_val / 12
                t = time_val
            elif time_period == "Años":
                r = rate_val if rate_period == "Anual" else rate_val * 12
                t = time_val
            elif time_period == "Días":
                # Asumiendo año de 365 días
                r = rate_val / 365 if rate_period == "Anual" else rate_val / 30
                t = time_val
            
            if tipo == "simple":
                res = interes_simple(c, r, t)
                total = c + res
                texto = f"Ganancia: ${res:,.2f}\nTotal: ${total:,.2f}"
            else:
                total = interes_compuesto(c, r, t)
                ganancia = total - c
                texto = f"Ganancia: ${ganancia:,.2f}\nTotal: ${total:,.2f}"
            
            self.lbl_res_int.config(text=texto, fg="#32D74B")
        except:
            self.lbl_res_int.config(text="Error en los datos", fg="#FF453A")

    def click_boton(self, texto):
        if self.pantalla.get() == "Error":
            if texto == 'C':
                self.pantalla.delete(0, tk.END)
                self.historial.config(text="")
            return

        if texto == 'C':
            self.pantalla.delete(0, tk.END)
            self.historial.config(text="")
        elif texto == '⌫':
            self.pantalla.delete(len(self.pantalla.get())-1, tk.END)
        elif texto == '=':
            try:
                exp_orig = self.pantalla.get()
                if not exp_orig: return
                
                exp = exp_orig
                
                # Constantes
                exp = exp.replace('π', 'math.pi')
                exp = re.sub(r'\be\b', 'math.e', exp)
                
                # Funciones
                exp = re.sub(r'\bsin\b', 'seno', exp)
                exp = re.sub(r'\bcos\b', 'coseno', exp)
                exp = re.sub(r'\btan\b', 'tangente', exp)
                exp = re.sub(r'\blog\b', 'logaritmo_base10', exp)
                exp = re.sub(r'\bln\b', 'logaritmo_Natural', exp)
                
                # Símbolos
                exp = exp.replace('^', '**')
                exp = exp.replace('√', 'raiz_cuadrada')
                
                # Factorial
                exp = re.sub(r'(\d+(?:\.\d+)?)!', r'factorial(\1)', exp)
                
                # Contexto cerrado para eval
                contexto = {
                    'seno': seno,
                    'coseno': coseno,
                    'tangente': tangente,
                    'logaritmo_base10': logaritmo_base10,
                    'logaritmo_Natural': logaritmo_Natural,
                    'factorial': factorial,
                    'raiz_cuadrada': raiz_cuadrada,
                    'math': math
                }
                
                res = str(eval(exp, {"__builtins__": __builtins__}, contexto))
                if res.endswith(".0"): res = res[:-2]
                self.historial.config(text=exp_orig + " =")
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, res)
            except:
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, "Error")
        elif texto in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
            self.pantalla.insert(tk.END, texto + "(")
        else:
            self.pantalla.insert(tk.END, texto)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
