import os
import unittest
from Funciones.simples import porcentaje
from main import Calculadora

class TestPercentMemory(unittest.TestCase):
    def test_porcentaje_simple(self):
        # porcentaje(base, valor, operacion=None) devuelve base*valor/100
        self.assertEqual(porcentaje(200, 10), 20)
        # con operacion aplica la operación sobre la base
        self.assertEqual(porcentaje(200, 10, '+'), 220)
        self.assertEqual(porcentaje(200, 10, '-'), 180)
        self.assertEqual(porcentaje(10, 50, '*'), 50)
        # division con porcentaje
        self.assertEqual(porcentaje(100, 10, '/'), 100 / 10)

    def test_memory_persistence(self):
        # Asegurarse de partir de limpio
        path = os.path.join(os.getcwd(), 'memory.json')
        if os.path.exists(path):
            os.remove(path)

        app = Calculadora()
        # Ocultar la ventana en entornos de prueba
        try:
            app.withdraw()
        except Exception:
            pass

        # Poner un número en la pantalla y sumar a memoria
        app.pantalla.delete(0, 'end')
        app.pantalla.insert(0, '123.5')
        app.memory_add()

        # Verificar archivo
        self.assertTrue(os.path.exists(path))
        with open(path, 'r', encoding='utf-8') as f:
            import json

            data = json.load(f)
        self.assertAlmostEqual(float(data.get('memory', 0)), 123.5)

        # Clear pantalla, llamar MR y comprobar que pantalla contiene el valor guardado
        app.pantalla.delete(0, 'end')
        app.memory_recall()
        self.assertEqual(app.pantalla.get(), '123.5')

        # Limpieza
        try:
            app.destroy()
        except Exception:
            pass
        if os.path.exists(path):
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
