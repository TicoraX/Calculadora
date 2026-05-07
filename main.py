import tkinter as tk
from Funciones.cientifica import *
from Funciones.simples import * # Asumiendo que tienes funciones simples aquí

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("350x500")
        self.config(bg="#f0f0f0")

        # Pantalla de la calculadora
        self.pantalla = tk.Entry(self, font=("Arial", 24), bg="white", fg="black", justify="right")
        self.pantalla.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, pady=10, padx=10, sticky="nsew")

        # Configuración de los botones
        botones = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('sin', 5, 2), ('cos', 5, 3),
            ('tan', 6, 0), ('log', 6, 1), ('ln', 6, 2), ('=', 6, 3)
        ]

        # Crear y posicionar botones
        for (texto, fila, columna) in botones:
            boton = tk.Button(self, text=texto, font=("Arial", 16), command=lambda t=texto: self.click_boton(t))
            boton.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

        # Configurar las filas y columnas para que se expandan
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def click_boton(self, texto):
        if texto == 'C':
            self.pantalla.delete(0, tk.END)
        elif texto == '=':
            try:
                # Obtenemos la expresión de la pantalla
                expresion = self.pantalla.get()
                
                # Reemplazamos los nombres para que coincidan con las funciones de cientifica.py
                expresion = expresion.replace('sin', 'seno')
                expresion = expresion.replace('cos', 'coseno')
                expresion = expresion.replace('tan', 'tangente')
                expresion = expresion.replace('log', 'logaritmo_base10')
                expresion = expresion.replace('ln', 'logaritmo_Natural')
                
                # Evaluamos la expresión
                resultado = str(eval(expresion))
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, resultado)
            except Exception as e:
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(tk.END, "Error")
        elif texto in ['sin', 'cos', 'tan', 'log', 'ln']:
            # Añade directamente la función con el paréntesis abierto
            self.pantalla.insert(tk.END, texto + "(")
        else:
            self.pantalla.insert(tk.END, texto)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
