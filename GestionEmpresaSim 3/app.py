# -*- coding: utf-8 -*-
"""
Lanzador del Simulador de Gestión Empresarial.
Abre una ventana de escritorio con el index.html y guarda las empresas en un archivo
(en la carpeta de datos del usuario), así funciona igual dentro de un .exe.

Requisitos:  pip install pywebview
Si pywebview no está instalado se abre una ventana tkinter que arranca el programa en el navegador.
"""
import base64, json, os, sys, threading, http.server, socketserver, webbrowser, functools


def recurso(ruta):
    """Ruta a un archivo incluido (funciona también empaquetado con PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, ruta)


def carpeta_datos():
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    d = os.path.join(base, "SimuladorGestion")
    os.makedirs(d, exist_ok=True)
    return d


ARCHIVO = os.path.join(carpeta_datos(), "empresas.json")


class Api:
    """Funciones que llama el JavaScript (guardar/cargar la información en un archivo)."""

    def cargar(self):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def guardar(self, texto):
        tmp = ARCHIVO + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(texto)
        os.replace(tmp, ARCHIVO)
        return True

    def guardar_archivo(self, nombre, b64):
        """Guarda facturas / CSV con un cuadro 'Guardar como'."""
        import webview
        ruta = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG, save_filename=nombre)
        if not ruta:
            return False
        ruta = ruta if isinstance(ruta, str) else ruta[0]
        with open(ruta, "wb") as f:
            f.write(base64.b64decode(b64))
        return True


def servidor_local():
    """Servidor HTTP local para servir index.html + datos/ (puerto libre)."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=recurso("."))
    handler.log_message = lambda *a, **k: None
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1]


def main():
    puerto = servidor_local()
    url = f"http://127.0.0.1:{puerto}/index.html"
    try:
        import webview
        webview.create_window("Simulador de Gestión Empresarial", url, js_api=Api(), width=1320, height=860, min_size=(1000, 650))
        webview.start()
    except ImportError:
        # Alternativa con tkinter: ventana de control que abre el programa en el navegador
        import tkinter as tk
        root = tk.Tk()
        root.title("Simulador de Gestión Empresarial")
        root.geometry("460x220")
        tk.Label(root, text="Simulador de Gestión Empresarial", font=("Segoe UI", 15, "bold")).pack(pady=18)
        tk.Label(root, text="Se abrirá en tu navegador.\nNo cierres esta ventana mientras lo uses.").pack()
        tk.Button(root, text="Abrir programa", font=("Segoe UI", 11), command=lambda: webbrowser.open(url)).pack(pady=16)
        webbrowser.open(url)
        root.mainloop()


if __name__ == "__main__":
    main()
