#!/usr/bin/env python3
"""Regenera datos/datos.js a partir de los JSON de la carpeta datos/ (ejecútalo si editas los JSON)."""
import json, os
base = os.path.dirname(os.path.abspath(__file__))
d = {k: json.load(open(os.path.join(base, "datos", k + ".json"), encoding="utf-8")) for k in ("fiscal", "catalogo", "enunciados")}
open(os.path.join(base, "datos", "datos.js"), "w", encoding="utf-8").write("window.DATOS=" + json.dumps(d, ensure_ascii=False) + ";")
print("datos/datos.js regenerado")
