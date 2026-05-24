import unittest
import math
from core.evaluator import safe_eval

class TestSafeEval(unittest.TestCase):
    def setUp(self):
        self.context = {
            'pi': math.pi,
            'sin': math.sin,
            'cos': math.cos,
            'sqrt': math.sqrt,
        }

    def test_basic_ops(self):
        self.assertEqual(safe_eval('1 + 2'), 3)
        self.assertEqual(safe_eval('3 * 4'), 12)
        self.assertEqual(safe_eval('10 / 2'), 5)
        self.assertEqual(safe_eval('2 ** 3'), 8)

    def test_functions(self):
        self.assertAlmostEqual(safe_eval('sin(pi/2)', self.context), 1.0)
        self.assertEqual(safe_eval('sqrt(4)', self.context), 2.0)

    def test_prohibited_code(self):
        with self.assertRaises(NameError):
            safe_eval('__import__("os").system("echo 1")')
        with self.assertRaises(NameError):
            safe_eval('open("file.txt", "w")')
        with self.assertRaises(TypeError):
            safe_eval('[1, 2, 3]')

if __name__ == '__main__':
    unittest.main()
