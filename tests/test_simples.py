import unittest
from Funciones import simples


class TestSimples(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(simples.suma(2, 3), 5)

    def test_resta(self):
        self.assertEqual(simples.resta(10, 4), 6)

    def test_multiplicacion(self):
        self.assertEqual(simples.multiplicacion(3, 5), 15)

    def test_division(self):
        self.assertEqual(simples.division(10, 2), 5)
        self.assertEqual(simples.division(5, 0), "Error: División por cero no permitida")

    def test_raiz_cuadrada(self):
        self.assertEqual(simples.raiz_cuadrada(9), 3)
        self.assertIn('Error', simples.raiz_cuadrada(-1))

    def test_porcentaje_plain(self):
        # sin operación devuelve el porcentaje absoluto
        self.assertEqual(simples.porcentaje(200, 10), 20)

    def test_porcentaje_sum(self):
        self.assertEqual(simples.porcentaje(200, 10, '+'), 220)

    def test_porcentaje_sub(self):
        res = simples.porcentaje(200, 10, '-')
        self.assertEqual(res, 180)

    def test_porcentaje_mul(self):
        self.assertEqual(simples.porcentaje(50, 10, '*'), 50 * (50 * 10 / 100))

    def test_porcentaje_div(self):
        # division por el porcentaje calculado
        res = simples.porcentaje(100, 25, '/')
        # 25% de 100 = 25, 100 / 25 = 4
        self.assertEqual(res, 4)


if __name__ == '__main__':
    unittest.main()
