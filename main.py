import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import math
import re
import os
import json
from core.evaluator import safe_eval
from Funciones.cientifica import (
    seno,
    coseno,
    tangente,
    seno_inverso,
    coseno_inverso,
    tangente_inversa,
    logaritmo_base10,
    logaritmo_Natural,
    factorial,
    exponencial,
    absoluto,
    potencia,
)
from Funciones.simples import raiz_cuadrada
from Funciones.intereses import interes_simple, interes_compuesto

# Helper simple para tooltips
class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._id = None
        self.tipwindow = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._unschedule)
        widget.bind("<ButtonPress>", self._unschedule)

    def _schedule(self, event=None):
        self._unschedule()
        try:
            self._id = self.widget.after(self.delay, self.showtip)
        except Exception:
            self._id = None

    def _unschedule(self, event=None):
        if self._id:
            try:
                self.widget.after_cancel(self._id)
            except Exception:
                pass
            self._id = None
        self.hidetip()

    def showtip(self):
        if self.tipwindow:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, justify='left', background="#FFFFE0", relief='solid', borderwidth=1, font=("Segoe UI", 9))
            label.pack(ipadx=4, ipady=2)
        except Exception:
            pass

    def hidetip(self):
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None


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
        self.crear_interfaz_conversiones()
        self.crear_interfaz_figuras()
        self.crear_interfaz_calculo()
        self.crear_interfaz_estadistica()

        # Mostrar calculadora por defecto
        self.mostrar_calculadora()

    def ocultar_todas(self):
        for attr in ['frame_calc', 'frame_menu', 'frame_intereses', 'frame_conversiones', 'frame_figuras', 'frame_calculo', 'frame_estadistica']:
            if hasattr(self, attr):
                getattr(self, attr).pack_forget()

    def mostrar_calculadora(self):
        self.ocultar_todas()
        self.frame_calc.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Científica")

    def mostrar_menu(self):
        self.ocultar_todas()
        self.frame_menu.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Funciones")

    def mostrar_intereses(self):
        self.ocultar_todas()
        self.frame_intereses.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Intereses")

    def mostrar_conversiones(self):
        self.ocultar_todas()
        self.frame_conversiones.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Conversiones")

    def mostrar_figuras(self):
        self.ocultar_todas()
        self.frame_figuras.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Figuras")

    def mostrar_calculo(self):
        self.ocultar_todas()
        self.frame_calculo.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Cálculo")

    def mostrar_estadistica(self):
        self.ocultar_todas()
        self.frame_estadistica.pack(fill="both", expand=True)
        self.title("Calculadora Tocha - Estadística")

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

        # Memoria (M+, M-, MR) + indicador
        mem_frame = tk.Frame(self.frame_calc, bg="#1C1C1E")
        mem_frame.pack(fill="x", padx=20, pady=(0, 5))
        tk.Button(mem_frame, text='M+', font=("Segoe UI", 10), bg="#3A3A3C", fg="white", bd=0, width=6, command=lambda: self.memory_add()).pack(side='left', padx=2)
        tk.Button(mem_frame, text='M-', font=("Segoe UI", 10), bg="#3A3A3C", fg="white", bd=0, width=6, command=lambda: self.memory_sub()).pack(side='left', padx=2)
        tk.Button(mem_frame, text='MR', font=("Segoe UI", 10), bg="#3A3A3C", fg="white", bd=0, width=6, command=lambda: self.memory_recall()).pack(side='left', padx=2)
        self.lbl_mem = tk.Label(mem_frame, text="Mem: 0", font=("Segoe UI", 10), bg="#1C1C1E", fg="#8E8E93")
        self.lbl_mem.pack(side='left', padx=8)
        # Cargar memoria desde archivo si existe
        try:
            self.load_memory()
        except Exception:
            # Si hay cualquier problema, inicializar a 0
            self.memory = 0.0

        # Pantalla Principal
        self.pantalla = tk.Entry(self.frame_calc, font=self.custom_font, bg="#1C1C1E", fg="#FFFFFF", justify="right", bd=0, insertbackground="#FFFFFF")
        self.pantalla.pack(fill="x", padx=10, pady=10)
        
        # Frame para botones (Grid)
        grid_frame = tk.Frame(self.frame_calc, bg="#1C1C1E")
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)

        for i in range(7):
            grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            grid_frame.grid_columnconfigure(i, weight=1)

        bg_num, bg_acc, bg_op, bg_cient = "#505050", "#D4D4D2", "#FF9F0A", "#3A3A3C"
        
        botones = [
            ('C', 0, 0, bg_acc, "#000000"), ('⌫', 0, 1, bg_acc, "#000000"), ('(', 0, 2, bg_acc, "#000000"), (')', 0, 3, bg_acc, "#000000"), ('/', 0, 4, bg_op, "#FFFFFF"),
            ('sin', 1, 0, bg_cient, "#FFFFFF"), ('7', 1, 1, bg_num, "#FFFFFF"), ('8', 1, 2, bg_num, "#FFFFFF"), ('9', 1, 3, bg_num, "#FFFFFF"), ('*', 1, 4, bg_op, "#FFFFFF"),
            ('cos', 2, 0, bg_cient, "#FFFFFF"), ('4', 2, 1, bg_num, "#FFFFFF"), ('5', 2, 2, bg_num, "#FFFFFF"), ('6', 2, 3, bg_num, "#FFFFFF"), ('-', 2, 4, bg_op, "#FFFFFF"),
            ('tan', 3, 0, bg_cient, "#FFFFFF"), ('1', 3, 1, bg_num, "#FFFFFF"), ('2', 3, 2, bg_num, "#FFFFFF"), ('3', 3, 3, bg_num, "#FFFFFF"), ('+', 3, 4, bg_op, "#FFFFFF"),
            ('log', 4, 0, bg_cient, "#FFFFFF"), ('%', 4, 1, bg_cient, "#FFFFFF"), ('0', 4, 2, bg_num, "#FFFFFF"), ('.', 4, 3, bg_num, "#FFFFFF"), ('=', 4, 4, bg_op, "#FFFFFF"),
            ('ln', 5, 0, bg_cient, "#FFFFFF"), ('π', 5, 1, bg_cient, "#FFFFFF"), ('^', 5, 2, bg_cient, "#FFFFFF"), ('√', 5, 3, bg_cient, "#FFFFFF"), ('!', 5, 4, bg_cient, "#FFFFFF")
        ]

        # Fila extra de funciones científicas avanzadas
        extra = [
            ('asin', 6, 0, bg_cient, "#FFFFFF"), ('acos', 6, 1, bg_cient, "#FFFFFF"), ('atan', 6, 2, bg_cient, "#FFFFFF"), ('exp', 6, 3, bg_cient, "#FFFFFF"), ('abs', 6, 4, bg_cient, "#FFFFFF"),
        ]
        botones.extend(extra)

        for (texto, f, c, bg, fg) in botones:
            btn = tk.Button(grid_frame, text=texto, font=self.btn_font, bg=bg, fg=fg, bd=0, 
                            activebackground="#707070", activeforeground=fg, cursor="hand2",
                            command=lambda t=texto: self.click_boton(t))
            btn.grid(row=f, column=c, sticky="nsew", padx=3, pady=3)
            
        # Eventos de Teclado
        self.bind('<Return>', lambda e: self.click_boton('='))
        self.bind('<BackSpace>', lambda e: self.click_boton('⌫'))
        self.bind('<Escape>', lambda e: self.click_boton('C'))
        self.bind('<Key>', self.key_pressed)
        # Atajos para memoria
        self.bind_all('<Control-m>', lambda e: self.memory_add())
        self.bind_all('<Control-M>', lambda e: self.memory_add())
        self.bind_all('<Control-Shift-M>', lambda e: self.memory_sub())
        self.bind_all('<Control-r>', lambda e: self.memory_recall())
        self.pantalla.focus_set()

    def crear_interfaz_menu(self):
        self.frame_menu = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_menu, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_calculadora)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_menu, text="Funciones Especiales", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        # Lista de funciones (se pueden agregar más aquí)
        lista_funciones = [
            ("Conversiones", self.mostrar_conversiones),
            ("Estadística", self.mostrar_estadistica),
            ("Figuras Geométricas", self.mostrar_figuras),
            ("Integrales y Derivadas", self.mostrar_calculo),
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
        ToolTip(self.ent_capital, "Capital inicial en la moneda local, sin símbolos. Ej: 1000")

        # Tasa con flechita (Combobox)
        tk.Label(self.frame_intereses, text="Tasa de Interés (%)", **label_style).pack(pady=(15, 0))
        tasa_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        tasa_f.pack(fill="x", padx=50)
        self.ent_tasa = tk.Entry(tasa_f, **entry_style)
        self.ent_tasa.pack(side="left", fill="x", expand=True, ipady=8)
        ToolTip(self.ent_tasa, "Tasa en porcentaje (ej: 5 = 5%)")
        self.combo_tasa = ttk.Combobox(tasa_f, values=["Anual", "Mensual"], state="readonly", width=8, font=("Segoe UI", 12))
        self.combo_tasa.set("Anual")
        self.combo_tasa.pack(side="left", padx=(5, 0))
        ToolTip(self.combo_tasa, "Periodo de la tasa (Anual/Mensual)")

        # Tiempo con flechita (Combobox)
        tk.Label(self.frame_intereses, text="Tiempo", **label_style).pack(pady=(15, 0))
        tiempo_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        tiempo_f.pack(fill="x", padx=50)
        self.ent_tiempo = tk.Entry(tiempo_f, **entry_style)
        self.ent_tiempo.pack(side="left", fill="x", expand=True, ipady=8)
        ToolTip(self.ent_tiempo, "Tiempo numérico (según selección)")
        self.combo_tiempo = ttk.Combobox(tiempo_f, values=["Años", "Meses", "Días"], state="readonly", width=8, font=("Segoe UI", 12))
        self.combo_tiempo.set("Meses")
        self.combo_tiempo.pack(side="left", padx=(5, 0))
        ToolTip(self.combo_tiempo, "Unidad de tiempo (Años/Meses/Días)")
        # Frecuencia de capitalización
        tk.Label(self.frame_intereses, text="Frecuencia (n/año)", **label_style).pack(pady=(10, 0))
        freq_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        freq_f.pack(fill="x", padx=50)
        self.combo_freq = ttk.Combobox(freq_f, values=["Anual (1)", "Semestral (2)", "Trimestral (4)", "Mensual (12)", "Diaria (365)"], state="readonly", width=18, font=("Segoe UI", 12))
        self.combo_freq.set("Mensual (12)")
        self.combo_freq.pack(side="left", padx=(0, 0))
        ToolTip(self.combo_freq, "Frecuencia de capitalización por año. Ej: Mensual = 12")

        # Botones de cálculo
        btn_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        btn_f.pack(pady=40)
        tk.Button(btn_f, text="Simple", font=self.btn_font, bg="#FF9F0A", fg="white", bd=0, padx=20, pady=10, 
                  command=lambda: self.calcular_int("simple")).pack(side="left", padx=10)
        tk.Button(btn_f, text="Compuesto", font=self.btn_font, bg="#5856D6", fg="white", bd=0, padx=20, pady=10, 
                  command=lambda: self.calcular_int("compuesto")).pack(side="left", padx=10)

        self.lbl_res_int = tk.Label(self.frame_intereses, text="Resultado: $0", font=("Segoe UI", 18, "bold"), bg="#1C1C1E", fg="#32D74B", justify="center")
        self.lbl_res_int.pack(pady=10)
        # Acciones: copiar resultado y mostrar detalles
        acciones_f = tk.Frame(self.frame_intereses, bg="#1C1C1E")
        acciones_f.pack()
        tk.Button(acciones_f, text="Copiar", font=("Segoe UI", 10), bg="#3A3A3C", fg="white", bd=0, padx=12, pady=6, command=self.copy_result).pack(side='left', padx=6)
        self.show_details_var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(acciones_f, text="Mostrar detalles", variable=self.show_details_var, bg="#1C1C1E", fg="white", selectcolor="#1C1C1E", command=self._toggle_detalles)
        cb.pack(side='left', padx=6)

        # Área de detalles (oculta por defecto)
        self.txt_detalles = tk.Text(self.frame_intereses, height=6, bg="#121212", fg="#E5E5EA", bd=0, font=("Segoe UI", 10), wrap='word')
        self.txt_detalles.config(state='disabled')

    def calcular_int(self, tipo):
        # Validación de entradas
        cap_text = self.ent_capital.get().strip()
        tasa_text = self.ent_tasa.get().strip()
        tiempo_text = self.ent_tiempo.get().strip()
        if not cap_text or not tasa_text or not tiempo_text:
            self.lbl_res_int.config(text="Complete todos los campos", fg="#FF453A")
            return
        try:
            c = float(cap_text.replace(',', ''))
            rate_val = float(tasa_text) / 100
            time_val = float(tiempo_text)
        except ValueError:
            self.lbl_res_int.config(text="Valores numéricos inválidos", fg="#FF453A")
            return

        if time_val < 0 or c < 0:
            self.lbl_res_int.config(text="Valores deben ser positivos", fg="#FF453A")
            return

        rate_period = self.combo_tasa.get() or "Anual"
        time_period = self.combo_tiempo.get() or "Meses"

        # Usar tasa anual R (rate_val) y convertir tiempo a años
        try:
            R = rate_val  # tasa anual en decimal
            if time_period == "Meses":
                t_years = time_val / 12.0
            elif time_period == "Años":
                t_years = time_val
            elif time_period == "Días":
                t_years = time_val / 365.0
            else:
                t_years = time_val

            # Obtener frecuencia n desde combo
            freq_text = getattr(self, 'combo_freq', None)
            n = 1
            if freq_text is not None:
                sel = self.combo_freq.get()
                # Extraer número entre paréntesis si existe
                m = re.search(r"\((\d+)\)", sel)
                if m:
                    try:
                        n = int(m.group(1))
                    except Exception:
                        n = 1

            if tipo == "simple":
                # Interés simple usando tasa anual y tiempo en años
                res = interes_simple(c, R, t_years)
                total = c + res
                texto = f"Ganancia: ${res:,.2f}\nTotal: ${total:,.2f}"
                detalles = (
                    f"Interés simple:\n"
                    f"I = P * r * t\n"
                    f"P = {c:,.2f}, r = {R:.6f}, t(years) = {t_years:.6f}\n"
                    f"I = {res:,.2f}\nTotal = {total:,.2f}"
                )
            else:
                # Interés compuesto con frecuencia n
                total = interes_compuesto(c, R, t_years, frecuencia=n)
                ganancia = total - c
                texto = f"Ganancia: ${ganancia:,.2f}\nTotal: ${total:,.2f}"
                detalles = (
                    f"Interés compuesto:\n"
                    f"A = P * (1 + r/n)^(n*t)\n"
                    f"P = {c:,.2f}, r = {R:.6f}, n = {n}, t(years) = {t_years:.6f}\n"
                    f"A = {total:,.2f}\nGanancia = {ganancia:,.2f}"
                )

            # Mostrar resultado
            self.lbl_res_int.config(text=texto, fg="#32D74B")
            # Guardar último resultado para copiar
            try:
                self.last_int_result = str(total if tipo != "simple" else total)
            except Exception:
                self.last_int_result = texto
            # Mostrar/ocultar detalles según la selección
            try:
                if getattr(self, 'show_details_var', tk.BooleanVar()).get():
                    self.txt_detalles.config(state='normal')
                    self.txt_detalles.delete('1.0', tk.END)
                    self.txt_detalles.insert(tk.END, detalles)
                    self.txt_detalles.config(state='disabled')
                    self.txt_detalles.pack(padx=50, pady=(10, 0), fill='x')
                else:
                    self.txt_detalles.pack_forget()
            except Exception:
                pass
        except Exception:
            self.lbl_res_int.config(text="Error calculando interés", fg="#FF453A")

    def crear_interfaz_conversiones(self):
        self.frame_conversiones = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_conversiones, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_menu)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_conversiones, text="Conversiones", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        label_style = {"font": ("Segoe UI", 11), "bg": "#1C1C1E", "fg": "#8E8E93"}
        entry_style = {"font": ("Segoe UI", 16), "bg": "#2C2C2E", "fg": "white", "insertbackground": "white", "bd": 0, "justify": "center"}

        # Tipo de conversión
        tk.Label(self.frame_conversiones, text="Categoría", **label_style).pack()
        self.combo_categoria = ttk.Combobox(self.frame_conversiones, values=["Monedas", "Pesos", "Distancias"], state="readonly", font=("Segoe UI", 12))
        self.combo_categoria.set("Monedas")
        self.combo_categoria.pack(pady=5, padx=50, fill="x")
        self.combo_categoria.bind("<<ComboboxSelected>>", self.actualizar_opciones_conversion)
        ToolTip(self.combo_categoria, "Categoría de conversión: Monedas, Pesos, Distancias")

        # Contenedor De y A
        frame_opciones = tk.Frame(self.frame_conversiones, bg="#1C1C1E")
        frame_opciones.pack(fill="x", padx=50, pady=15)

        # De
        frame_de = tk.Frame(frame_opciones, bg="#1C1C1E")
        frame_de.pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Label(frame_de, text="De", **label_style).pack()
        self.combo_de = ttk.Combobox(frame_de, state="readonly", font=("Segoe UI", 12))
        self.combo_de.pack(fill="x")
        ToolTip(self.combo_de, "Unidad origen")

        # A
        frame_a = tk.Frame(frame_opciones, bg="#1C1C1E")
        frame_a.pack(side="right", fill="x", expand=True, padx=(5, 0))
        tk.Label(frame_a, text="A", **label_style).pack()
        self.combo_a = ttk.Combobox(frame_a, state="readonly", font=("Segoe UI", 12))
        self.combo_a.pack(fill="x")
        ToolTip(self.combo_a, "Unidad destino")

        # Cantidad
        tk.Label(self.frame_conversiones, text="Cantidad", **label_style).pack(pady=(10, 0))
        self.ent_cantidad = tk.Entry(self.frame_conversiones, **entry_style)
        self.ent_cantidad.pack(pady=5, padx=50, fill="x", ipady=8)
        ToolTip(self.ent_cantidad, "Cantidad numérica a convertir. Use punto para decimales")

        # Botón Calcular
        tk.Button(self.frame_conversiones, text="Convertir", font=self.btn_font, bg="#32D74B", fg="white", bd=0, padx=20, pady=10, 
                  command=self.calcular_conversion).pack(pady=20)

        # Resultado
        self.lbl_res_conv = tk.Label(self.frame_conversiones, text="Resultado: 0", font=("Segoe UI", 18, "bold"), bg="#1C1C1E", fg="#32D74B", justify="center")
        self.lbl_res_conv.pack(pady=10)

        self.tasas_monedas = None
        self.actualizar_opciones_conversion()

    def actualizar_opciones_conversion(self, event=None):
        categoria = self.combo_categoria.get()
        if categoria == "Monedas":
            if not self.tasas_monedas:
                from Funciones.conversiones import obtener_tasas_monedas
                self.tasas_monedas = obtener_tasas_monedas()
            
            if self.tasas_monedas:
                monedas = ["USD", "EUR", "COP", "MXN", "ARS", "CLP", "PEN", "BRL", "GBP", "JPY"]
                self.combo_de.config(values=monedas)
                self.combo_a.config(values=monedas)
                self.combo_de.set("USD")
                self.combo_a.set("COP")
            else:
                self.combo_de.config(values=["Error API"])
                self.combo_a.config(values=["Error API"])
                self.combo_de.set("Error API")
                self.combo_a.set("Error API")
        elif categoria == "Pesos":
            unidades = ["Kilos", "Libras", "Onzas", "Gramos", "Miligramos"]
            self.combo_de.config(values=unidades)
            self.combo_a.config(values=unidades)
            self.combo_de.set("Kilos")
            self.combo_a.set("Libras")
        elif categoria == "Distancias":
            unidades = ["Metros", "Kilómetros", "Millas", "Yardas", "Pies", "Pulgadas"]
            self.combo_de.config(values=unidades)
            self.combo_a.config(values=unidades)
            self.combo_de.set("Metros")
            self.combo_a.set("Millas")

    def calcular_conversion(self):
        cat = self.combo_categoria.get()
        val_text = self.ent_cantidad.get().strip()
        if not val_text:
            self.lbl_res_conv.config(text="Ingrese una cantidad", fg="#FF453A")
            return
        try:
            val = float(val_text.replace(',', ''))
        except ValueError:
            self.lbl_res_conv.config(text="Cantidad inválida", fg="#FF453A")
            return

        from Funciones.conversiones import convertir_moneda, convertir_peso, convertir_distancia

        try:
            de_u = self.combo_de.get()
            a_u = self.combo_a.get()
            if cat == "Monedas":
                if not self.tasas_monedas:
                    self.lbl_res_conv.config(text="No se pudieron obtener tasas", fg="#FF453A")
                    return
                if de_u not in self.tasas_monedas or a_u not in self.tasas_monedas:
                    self.lbl_res_conv.config(text="Moneda no soportada", fg="#FF453A")
                    return
                res = convertir_moneda(val, de_u, a_u, self.tasas_monedas)
                if res is None:
                    self.lbl_res_conv.config(text="Error al convertir (API)", fg="#FF453A")
                    return
                texto = f"{val:,.2f} {de_u} =\n{res:,.2f} {a_u}"
            elif cat == "Pesos":
                if not de_u or not a_u:
                    self.lbl_res_conv.config(text="Seleccione unidades", fg="#FF453A")
                    return
                res = convertir_peso(val, de_u, a_u)
                texto = f"{val:,.2f} {de_u} =\n{res:,.4f} {a_u}"
            elif cat == "Distancias":
                if not de_u or not a_u:
                    self.lbl_res_conv.config(text="Seleccione unidades", fg="#FF453A")
                    return
                res = convertir_distancia(val, de_u, a_u)
                texto = f"{val:,.2f} {de_u} =\n{res:,.4f} {a_u}"
            else:
                self.lbl_res_conv.config(text="Categoría inválida", fg="#FF453A")
                return

            self.lbl_res_conv.config(text=texto, fg="#32D74B")
        except Exception:
            self.lbl_res_conv.config(text="Error en la conversión", fg="#FF453A")

    def _toggle_detalles(self):
        if getattr(self, 'show_details_var', None) and self.show_details_var.get():
            try:
                self.txt_detalles.pack(padx=50, pady=(10, 0), fill='x')
            except Exception:
                pass
        else:
            try:
                self.txt_detalles.pack_forget()
            except Exception:
                pass

    def copy_result(self):
        try:
            text = getattr(self, 'last_int_result', None)
            if not text:
                text = self.lbl_res_int.cget('text')
            self.clipboard_clear()
            self.clipboard_append(str(text))
        except Exception:
            pass

    def crear_interfaz_figuras(self):
        self.frame_figuras = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_figuras, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_menu)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_figuras, text="Figuras Geométricas", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        label_style = {"font": ("Segoe UI", 11), "bg": "#1C1C1E", "fg": "#8E8E93"}
        entry_style = {"font": ("Segoe UI", 16), "bg": "#2C2C2E", "fg": "white", "insertbackground": "white", "bd": 0, "justify": "center"}

        # Selectores
        frame_sel = tk.Frame(self.frame_figuras, bg="#1C1C1E")
        frame_sel.pack(fill="x", padx=50, pady=10)

        self.combo_figura = ttk.Combobox(frame_sel, values=["Cuadrado", "Rectángulo", "Triángulo", "Círculo", "Cubo", "Esfera", "Cilindro", "Cono"], state="readonly", font=("Segoe UI", 12))
        self.combo_figura.set("Cuadrado")
        self.combo_figura.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.combo_figura.bind("<<ComboboxSelected>>", self.actualizar_inputs_figuras)

        self.combo_operacion = ttk.Combobox(frame_sel, values=["Área", "Perímetro"], state="readonly", font=("Segoe UI", 12))
        self.combo_operacion.set("Área")
        self.combo_operacion.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.combo_operacion.bind("<<ComboboxSelected>>", self.actualizar_inputs_figuras)

        # Contenedor de inputs dinámicos
        self.frame_inputs_fig = tk.Frame(self.frame_figuras, bg="#1C1C1E")
        self.frame_inputs_fig.pack(fill="x", padx=50, pady=10)

        self.lbl_inp1 = tk.Label(self.frame_inputs_fig, text="Lado", **label_style)
        self.ent_inp1 = tk.Entry(self.frame_inputs_fig, **entry_style)
        
        self.lbl_inp2 = tk.Label(self.frame_inputs_fig, text="Base", **label_style)
        self.ent_inp2 = tk.Entry(self.frame_inputs_fig, **entry_style)

        self.lbl_inp3 = tk.Label(self.frame_inputs_fig, text="Lado 3", **label_style)
        self.ent_inp3 = tk.Entry(self.frame_inputs_fig, **entry_style)

        # Botón Calcular
        tk.Button(self.frame_figuras, text="Calcular", font=self.btn_font, bg="#FF9F0A", fg="white", bd=0, padx=20, pady=10, 
                  command=self.calcular_figura).pack(pady=20)

        # Resultado
        self.lbl_res_fig = tk.Label(self.frame_figuras, text="Resultado: 0", font=("Segoe UI", 18, "bold"), bg="#1C1C1E", fg="#32D74B", justify="center")
        self.lbl_res_fig.pack(pady=10)

        self.actualizar_inputs_figuras()

    def actualizar_inputs_figuras(self, event=None):
        fig = self.combo_figura.get()
        
        # Opciones dinámicas
        figuras_2d = ["Cuadrado", "Rectángulo", "Triángulo", "Círculo"]
        
        if fig in figuras_2d:
            self.combo_operacion.config(values=["Área", "Perímetro"])
            if self.combo_operacion.get() not in ["Área", "Perímetro"]:
                self.combo_operacion.set("Área")
        else:
            self.combo_operacion.config(values=["Volumen", "Área Superficial"])
            if self.combo_operacion.get() not in ["Volumen", "Área Superficial"]:
                self.combo_operacion.set("Volumen")

        op = self.combo_operacion.get()

        for widget in (self.lbl_inp1, self.ent_inp1, self.lbl_inp2, self.ent_inp2, self.lbl_inp3, self.ent_inp3):
            widget.pack_forget()

        def mostrar(lbl_w, ent_w, texto):
            lbl_w.config(text=texto)
            lbl_w.pack(pady=(10, 0))
            ent_w.pack(pady=5, fill="x", ipady=8)

        if fig == "Cuadrado" or fig == "Cubo":
            mostrar(self.lbl_inp1, self.ent_inp1, "Lado")
        elif fig == "Rectángulo":
            mostrar(self.lbl_inp1, self.ent_inp1, "Base")
            mostrar(self.lbl_inp2, self.ent_inp2, "Altura")
        elif fig == "Círculo" or fig == "Esfera":
            mostrar(self.lbl_inp1, self.ent_inp1, "Radio")
        elif fig in ["Cilindro", "Cono"]:
            mostrar(self.lbl_inp1, self.ent_inp1, "Radio")
            mostrar(self.lbl_inp2, self.ent_inp2, "Altura")
        elif fig == "Triángulo":
            if op == "Área":
                mostrar(self.lbl_inp1, self.ent_inp1, "Base")
                mostrar(self.lbl_inp2, self.ent_inp2, "Altura")
            else:
                mostrar(self.lbl_inp1, self.ent_inp1, "Lado 1")
                mostrar(self.lbl_inp2, self.ent_inp2, "Lado 2")
                mostrar(self.lbl_inp3, self.ent_inp3, "Lado 3")

    def calcular_figura(self):
        try:
            fig = self.combo_figura.get()
            op = self.combo_operacion.get()
            
            from Funciones.FigurasG import (area_cuadrado, perimetro_cuadrado, area_rectangulo, 
                                            perimetro_rectangulo, area_triangulo, perimetro_triangulo, 
                                            area_circulo, perimetro_circulo,
                                            volumen_cubo, area_sup_cubo, volumen_esfera, area_sup_esfera,
                                            volumen_cilindro, area_sup_cilindro, volumen_cono, area_sup_cono)

            val1 = float(self.ent_inp1.get().replace(',', '')) if self.ent_inp1.winfo_ismapped() else 0
            val2 = float(self.ent_inp2.get().replace(',', '')) if self.ent_inp2.winfo_ismapped() else 0
            val3 = float(self.ent_inp3.get().replace(',', '')) if self.ent_inp3.winfo_ismapped() else 0

            res = 0
            # 2D
            if fig == "Cuadrado":
                res = area_cuadrado(val1) if op == "Área" else perimetro_cuadrado(val1)
            elif fig == "Rectángulo":
                res = area_rectangulo(val1, val2) if op == "Área" else perimetro_rectangulo(val1, val2)
            elif fig == "Círculo":
                res = area_circulo(val1) if op == "Área" else perimetro_circulo(val1)
            elif fig == "Triángulo":
                if op == "Área":
                    res = area_triangulo(val1, val2)
                else:
                    res = perimetro_triangulo(val1, val2, val3)
            # 3D
            elif fig == "Cubo":
                res = volumen_cubo(val1) if op == "Volumen" else area_sup_cubo(val1)
            elif fig == "Esfera":
                res = volumen_esfera(val1) if op == "Volumen" else area_sup_esfera(val1)
            elif fig == "Cilindro":
                res = volumen_cilindro(val1, val2) if op == "Volumen" else area_sup_cilindro(val1, val2)
            elif fig == "Cono":
                res = volumen_cono(val1, val2) if op == "Volumen" else area_sup_cono(val1, val2)

            unidades = "³" if op == "Volumen" else ("²" if op in ["Área", "Área Superficial"] else "")
            res_formateado = f"{res:,.4f}".rstrip('0').rstrip('.') if '.' in f"{res:,.4f}" else f"{res:,}"
            self.lbl_res_fig.config(text=f"{op}: {res_formateado}{unidades}", fg="#32D74B")
        except Exception:
            self.lbl_res_fig.config(text="Error en los datos", fg="#FF453A")

    def crear_interfaz_calculo(self):
        self.frame_calculo = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_calculo, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_menu)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_calculo, text="Cálculo Simbólico", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        label_style = {"font": ("Segoe UI", 11), "bg": "#1C1C1E", "fg": "#8E8E93"}
        entry_style = {"font": ("Segoe UI", 16), "bg": "#2C2C2E", "fg": "white", "insertbackground": "white", "bd": 0, "justify": "center"}

        tk.Label(self.frame_calculo, text="Expresión en X (ej: x**2 + 2*x)", **label_style).pack()
        self.ent_expr = tk.Entry(self.frame_calculo, **entry_style)
        self.ent_expr.pack(pady=5, padx=50, fill="x", ipady=8)

        tk.Label(self.frame_calculo, text="Operación", **label_style).pack(pady=(15, 0))
        self.combo_calculo = ttk.Combobox(self.frame_calculo, values=["Derivada", "Integral Indefinida", "Integral Definida"], state="readonly", font=("Segoe UI", 12))
        self.combo_calculo.set("Derivada")
        self.combo_calculo.pack(pady=5, padx=50, fill="x")
        self.combo_calculo.bind("<<ComboboxSelected>>", self.actualizar_inputs_calculo)

        self.frame_limites = tk.Frame(self.frame_calculo, bg="#1C1C1E")

        frame_a = tk.Frame(self.frame_limites, bg="#1C1C1E")
        frame_a.pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Label(frame_a, text="Límite Inf (a)", **label_style).pack()
        self.ent_lim_a = tk.Entry(frame_a, **entry_style)
        self.ent_lim_a.pack(fill="x")

        frame_b = tk.Frame(self.frame_limites, bg="#1C1C1E")
        frame_b.pack(side="right", fill="x", expand=True, padx=(5, 0))
        tk.Label(frame_b, text="Límite Sup (b)", **label_style).pack()
        self.ent_lim_b = tk.Entry(frame_b, **entry_style)
        self.ent_lim_b.pack(fill="x")

        tk.Button(self.frame_calculo, text="Resolver", font=self.btn_font, bg="#FF2D55", fg="white", bd=0, padx=20, pady=10, 
                  command=self.resolver_calculo).pack(pady=20)

        self.lbl_res_calculo = tk.Label(self.frame_calculo, text="Resultado: -", font=("Segoe UI", 16, "bold"), bg="#1C1C1E", fg="#32D74B", justify="center", wraplength=350)
        self.lbl_res_calculo.pack(pady=10)

    # Memoria: M+, M-, MR
    def memory_add(self):
        try:
            val = float(self.pantalla.get())
        except Exception:
            return
        if not hasattr(self, 'memory'):
            self.memory = 0.0
        self.memory += val
        self.historial.config(text=f"M+ ({self.memory})")
        mem_text = int(self.memory) if float(self.memory).is_integer() else self.memory
        try:
            self.lbl_mem.config(text=f"Mem: {mem_text}")
        except Exception:
            pass
        # Persistir memoria
        try:
            self.save_memory()
        except Exception:
            pass

    def memory_sub(self):
        try:
            val = float(self.pantalla.get())
        except Exception:
            return
        if not hasattr(self, 'memory'):
            self.memory = 0.0
        self.memory -= val
        self.historial.config(text=f"M- ({self.memory})")
        mem_text = int(self.memory) if float(self.memory).is_integer() else self.memory
        try:
            self.lbl_mem.config(text=f"Mem: {mem_text}")
        except Exception:
            pass
        # Persistir memoria
        try:
            self.save_memory()
        except Exception:
            pass

    def memory_recall(self):
        if not hasattr(self, 'memory'):
            self.memory = 0.0
        # Insertar memoria en la pantalla (reemplaza el contenido actual)
        self.pantalla.delete(0, tk.END)
        # Normalizar la representación si es entero
        mem = int(self.memory) if float(self.memory).is_integer() else self.memory
        self.pantalla.insert(tk.END, str(mem))
        try:
            self.lbl_mem.config(text=f"Mem: {mem}")
        except Exception:
            pass
        # Guardar estado también al hacer recall
        try:
            self.save_memory()
        except Exception:
            pass

    # Persistencia de memoria en workspace
    def save_memory(self):
        try:
            data = {'memory': self.memory}
            path = os.path.join(os.getcwd(), 'memory.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass

    def load_memory(self):
        path = os.path.join(os.getcwd(), 'memory.json')
        if not os.path.exists(path):
            self.memory = 0.0
            return self.memory
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.memory = float(data.get('memory', 0.0))
            mem_text = int(self.memory) if float(self.memory).is_integer() else self.memory
            try:
                self.lbl_mem.config(text=f"Mem: {mem_text}")
            except Exception:
                pass
            return self.memory
        except Exception:
            self.memory = 0.0
            return self.memory

    def _find_last_op_outside_parens(self, s: str):
        """Devuelve (index, op) del último operador + - * / que esté fuera de paréntesis, o (None, None)."""
        depth = 0
        for i in range(len(s) - 1, -1, -1):
            ch = s[i]
            if ch == ')':
                depth += 1
            elif ch == '(':
                depth -= 1
            elif depth == 0 and ch in '+-*/':
                return i, ch
        return None, None

    def actualizar_inputs_calculo(self, event=None):
        if self.combo_calculo.get() == "Integral Definida":
            self.frame_limites.pack(fill="x", padx=50, pady=15)
        else:
            self.frame_limites.pack_forget()

    def resolver_calculo(self):
        expr = self.ent_expr.get()
        op = self.combo_calculo.get()
        if not expr:
            return
        
        from Funciones.integrales_derivadas import calcular_derivada, calcular_integral_indefinida, calcular_integral_definida
        
        res = None
        if op == "Derivada":
            res = calcular_derivada(expr)
        elif op == "Integral Indefinida":
            res = calcular_integral_indefinida(expr)
        elif op == "Integral Definida":
            res = calcular_integral_definida(expr, self.ent_lim_a.get(), self.ent_lim_b.get())

        if res is None or res == "Error":
            self.lbl_res_calculo.config(text="Expresión inválida", fg="#FF453A")
        else:
            self.lbl_res_calculo.config(text=f"= {res}", fg="#32D74B")

    def crear_interfaz_estadistica(self):
        self.frame_estadistica = tk.Frame(self.container, bg="#1C1C1E")
        
        btn_back = tk.Button(self.frame_estadistica, text="Volver", font=("Segoe UI", 10, "bold"), 
                             bg="#3A3A3C", fg="white", bd=0, padx=10, pady=5, command=self.mostrar_menu)
        btn_back.pack(anchor="w", padx=20, pady=20)

        tk.Label(self.frame_estadistica, text="Estadística", font=("Segoe UI", 24, "bold"), bg="#1C1C1E", fg="white").pack(pady=(0, 20))

        label_style = {"font": ("Segoe UI", 11), "bg": "#1C1C1E", "fg": "#8E8E93"}
        entry_style = {"font": ("Segoe UI", 14), "bg": "#2C2C2E", "fg": "white", "insertbackground": "white", "bd": 0, "justify": "center"}

        tk.Label(self.frame_estadistica, text="Datos (ej: 12, 15, 12.5, 18)", **label_style).pack()
        self.ent_datos = tk.Entry(self.frame_estadistica, **entry_style)
        self.ent_datos.pack(pady=5, padx=20, fill="x", ipady=8)

        tk.Button(self.frame_estadistica, text="Analizar", font=self.btn_font, bg="#007AFF", fg="white", bd=0, padx=20, pady=10, 
                  command=self.resolver_estadistica).pack(pady=15)

        self.lbl_res_est = tk.Label(self.frame_estadistica, text="", font=("Segoe UI", 14), bg="#1C1C1E", fg="#32D74B", justify="left")
        self.lbl_res_est.pack(pady=10)

    def resolver_estadistica(self):
        datos = self.ent_datos.get()
        from Funciones.estadistica import calcular_estadistica
        res = calcular_estadistica(datos)
        
        if not res:
            self.lbl_res_est.config(text="Datos inválidos", fg="#FF453A")
        else:
            texto = ""
            for k, v in res.items():
                if isinstance(v, float):
                    texto += f"{k}: {v:,.4f}\n"
                else:
                    texto += f"{k}: {v}\n"
            self.lbl_res_est.config(text=texto, fg="#32D74B")

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
        elif texto == '%':
            exp_now = self.pantalla.get()
            if not exp_now:
                return
            # Contexto seguro para evaluar subexpresiones
            contexto = {
                'seno': seno,
                'coseno': coseno,
                'tangente': tangente,
                'logaritmo_base10': logaritmo_base10,
                'logaritmo_Natural': logaritmo_Natural,
                'factorial': factorial,
                'raiz_cuadrada': raiz_cuadrada,
                'math': math,
                'pi': math.pi,
                'e': math.e,
                'π': math.pi
            }
            idx, op = self._find_last_op_outside_parens(exp_now)
            if idx is not None:
                left_expr = exp_now[:idx]
                right_part = exp_now[idx+1:].strip()
                try:
                    if right_part.startswith('(') and right_part.endswith(')'):
                        b_val = float(safe_eval(right_part, contexto))
                    else:
                        mnum = re.match(r"^\(?\s*(\d+(?:\.\d+)?)\s*\)?$", right_part)
                        if mnum:
                            b_val = float(mnum.group(1))
                        else:
                            m2 = re.search(r"(\d+(?:\.\d+)?)\s*$", exp_now)
                            if not m2:
                                return
                            b_val = float(m2.group(1))

                    base_val = float(safe_eval(left_expr, contexto))
                    if op in ['+', '-']:
                        percent = base_val * b_val / 100.0
                    else:
                        percent = b_val / 100.0
                    if float(percent).is_integer():
                        percent = int(percent)
                    new_exp = f"{left_expr}{op}{percent}"
                    self.pantalla.delete(0, tk.END)
                    self.pantalla.insert(tk.END, str(new_exp))
                except Exception:
                    m2 = re.search(r"(\d+(?:\.\d+)?)\s*$", exp_now)
                    if m2:
                        b2 = float(m2.group(1)) / 100.0
                        self.pantalla.delete(0, tk.END)
                        self.pantalla.insert(tk.END, str(b2))
            else:
                m2 = re.search(r"(\d+(?:\.\d+)?)\s*$", exp_now)
                if m2:
                    b2 = float(m2.group(1)) / 100.0
                    if float(b2).is_integer():
                        b2 = int(b2)
                    self.pantalla.delete(0, tk.END)
                    self.pantalla.insert(tk.END, str(b2))
        elif texto == '=':
            try:
                exp_orig = self.pantalla.get()
                if not exp_orig:
                    return
                
                exp = exp_orig
                
                # Constantes
                exp = exp.replace('π', 'pi')

                # Funciones (orden importante: primero las inversas para evitar colisiones)
                exp = re.sub(r'\basin\b', 'seno_inverso', exp)
                exp = re.sub(r'\bacos\b', 'coseno_inverso', exp)
                exp = re.sub(r'\batan\b', 'tangente_inversa', exp)
                exp = re.sub(r'\bsin\b', 'seno', exp)
                exp = re.sub(r'\bcos\b', 'coseno', exp)
                exp = re.sub(r'\btan\b', 'tangente', exp)
                exp = re.sub(r'\blog\b', 'logaritmo_base10', exp)
                exp = re.sub(r'\bln\b', 'logaritmo_Natural', exp)
                exp = re.sub(r'\bexp\b', 'exponencial', exp)
                exp = re.sub(r'\babs\b', 'absoluto', exp)
                
                # Símbolos
                exp = exp.replace('^', '**')
                exp = exp.replace('√', 'raiz_cuadrada')
                
                # Factorial
                exp = re.sub(r'(\d+(?:\.\d+)?)!', r'factorial(\1)', exp)
                
                # Contexto cerrado para evaluación segura
                contexto = {
                    'seno': seno,
                    'coseno': coseno,
                    'tangente': tangente,
                    'seno_inverso': seno_inverso,
                    'coseno_inverso': coseno_inverso,
                    'tangente_inversa': tangente_inversa,
                    'logaritmo_base10': logaritmo_base10,
                    'logaritmo_Natural': logaritmo_Natural,
                    'factorial': factorial,
                    'raiz_cuadrada': raiz_cuadrada,
                    'exponencial': exponencial,
                    'absoluto': absoluto,
                    'potencia': potencia,
                    'math': math,
                    'pi': math.pi,
                    'e': math.e
                }
                res = str(safe_eval(exp, contexto))
                if res.endswith(".0"):
                    res = res[:-2]
                self.historial.config(text=exp_orig + " =")
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, res)
            except Exception:
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, "Error")
        elif texto in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'asin', 'acos', 'atan', 'exp', 'abs']:
            self.pantalla.insert(tk.END, texto + "(")
        else:
            self.pantalla.insert(tk.END, texto)

    def key_pressed(self, event):
        # Soporte de teclado: insertar dígitos y operadores permitidos
        ch = event.char
        if not ch:
            return
        allowed = '0123456789.+-*/^()%!eabcdefghijklmnopqrstuvwxyz'
        if ch in allowed:
            self.pantalla.insert(tk.END, ch)
        elif ch == '\r':
            self.click_boton('=')
        # Backspace, Escape y Return ya están enlazados

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
