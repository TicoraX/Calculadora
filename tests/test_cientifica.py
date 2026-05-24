import unittest
import math
from Funciones.cientifica import seno, coseno, tangente, seno_inverso, coseno_inverso, tangente_inversa, logaritmo_base10, logaritmo_Natural, factorial, exponencial, absoluto

class TestCientifica(unittest.TestCase):
    def test_trig(self):
        self.assertAlmostEqual(seno(90), 1.0)
        self.assertAlmostEqual(coseno(0), 1.0)
        self.assertAlmostEqual(round(tangente(45), 6), round(math.tan(math.radians(45)), 6))

    def test_trig_inversas(self):
        self.assertAlmostEqual(seno_inverso(1.0), 90.0)
        self.assertAlmostEqual(coseno_inverso(1.0), 0.0)
        self.assertAlmostEqual(round(tangente_inversa(1.0), 6), round(math.degrees(math.atan(1.0)), 6))

    def test_log_pow_abs(self):
        self.assertAlmostEqual(logaritmo_base10(100), 2.0)
        self.assertAlmostEqual(logaritmo_Natural(math.e), 1.0)
        self.assertAlmostEqual(exponencial(1), math.e)
        self.assertAlmostEqual(absoluto(-5), 5.0)

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)

if __name__ == '__main__':
    unittest.main()
