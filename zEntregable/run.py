#!/usr/bin/env python3
"""
Startup script - runs Flask and opens the browser automatically.
Usage: python run.py
"""
import os
import threading
import time
import webbrowser
from app.main import app

URL = "http://127.0.0.1:8000"
BANNER = """
==============================================================
   BOTICA COMUNITARIA
==============================================================
   URL : http://127.0.0.1:8000
   Detener : Ctrl+C
==============================================================
"""

def _open_browser():
    time.sleep(2.0)
    webbrowser.open(URL)

if __name__ == "__main__":
    print(BANNER)
    
    # Inicia el hilo para abrir el navegador en segundo plano
    threading.Thread(target=_open_browser, daemon=True).start()
    
    # Arranca el servidor nativo de Flask
    # (use_reloader=False evita que el navegador se abra dos veces accidentalmente)
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)