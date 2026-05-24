import unittest
import tempfile
import os
import json

from main import Calculadora


class TestHistory(unittest.TestCase):
    def test_history_file_created_and_entry(self):
        tmp = tempfile.TemporaryDirectory()
        cwd = os.getcwd()
        try:
            os.chdir(tmp.name)
            app = Calculadora()
            entry = {'timestamp': '2026-05-23T00:00:00Z', 'type': 'test', 'value': 123}
            app.save_history(entry)
            # destroy the Tk instance to avoid resource leaks
            try:
                app.destroy()
            except Exception:
                pass

            path = os.path.join(os.getcwd(), 'history.json')
            self.assertTrue(os.path.exists(path), msg="history.json should exist")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertIsInstance(data, list)
            # find our entry
            found = any(d.get('type') == 'test' and d.get('value') == 123 for d in data)
            self.assertTrue(found, msg="Saved entry not found in history.json")
        finally:
            os.chdir(cwd)
            tmp.cleanup()


if __name__ == '__main__':
    unittest.main()
