# Release v1.0.0

Fecha: 2026-05-23

Cambios principales:

- feat: historial de cálculos en `history.json` con límite de 1000 entradas.
- feat: UI de `Historial` con botones para `Refrescar`, `Limpiar`, `Exportar CSV`, `Importar CSV/JSON`.
- feat: vista previa pequeña del historial en la pantalla principal y botón `Limpiar` rápido.
- feat: guardado automático del historial al calcular intereses, conversiones y al copiar resultados.
- feat: exportación a `history.csv` e importación desde CSV/JSON.
- feat: `core/evaluator.py` evaluador seguro usado en la UI (reemplaza `eval`).
- fix: compatibilidad AST para Python 3.14 (`ast.Constant`).
- tests: añadidos `tests/test_evaluator.py` y `tests/test_history.py` (suite: 20 tests OK).

Notas:
- Para crear una release en GitHub automáticamente, instala la GitHub CLI `gh` y ejecuta:

```bash
gh release create v1.0.0 -t "v1.0.0" -n "Release notes: historial + seguridad + conversiones"
```
