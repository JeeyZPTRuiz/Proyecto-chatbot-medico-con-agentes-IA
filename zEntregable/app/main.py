import os
from datetime import datetime
from flask import Flask, request, jsonify

# Importar las funciones necesarias del modulo chatbot_medico
from .chatbot_medico import configurar_chatbot, procesar_consulta_paciente

# Importar las funciones necesarias del modulo database
from .database import (
    inicializar_base_datos,
    poblar_inventario,
    guardar_triage,
    obtener_inventario,
    registrar_compra,
    obtener_historial_compras,
    obtener_historial_chat
)

# Directorio base y directorio del frontend
directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
directorio_frontend = os.path.join(directorio_base, "frontend")

# Inicializacion de la aplicacion Flask con la carpeta estatica de frontend
app = Flask(__name__, static_folder=directorio_frontend, static_url_path="")

# Inicializar la base de datos de la botica al arrancar
inicializar_base_datos()

# Asegurar que existan los 100 productos en el inventario al iniciar
poblar_inventario()

# Configurar el modelo de inteligencia artificial al arrancar
modelo_ia = configurar_chatbot()

@app.route("/")
def index():
    """
    Ruta principal que sirve la pagina index.html del frontend.
    """
    return app.send_static_file("index.html")

@app.route("/api/mensaje", methods=["POST"])
def recibir_mensaje():
    """
    Ruta que procesa el mensaje del usuario, consulta a la IA,
    guarda el registro en la base de datos y retorna la respuesta.
    """
    datos = request.get_json()
    
    # Obtener el mensaje del usuario de los datos recibidos
    mensaje_usuario = datos.get("mensaje_usuario", "")
    
    # Procesar la consulta con el modelo de inteligencia artificial
    respuesta_bot = procesar_consulta_paciente(modelo_ia, mensaje_usuario)
    
    # Obtener la fecha y hora actual del sistema
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar el registro de la consulta en la base de datos
    guardar_triage(mensaje_usuario, respuesta_bot, fecha_actual)
    
    # Retornar la respuesta del chatbot en formato JSON
    return jsonify({"respuesta": respuesta_bot})

@app.route("/api/inventario", methods=["GET"])
def recibir_inventario():
    """
    Ruta que recupera todos los productos de la base de datos y los devuelve en formato JSON.
    """
    # Obtener la lista de productos de la base de datos
    lista_productos = obtener_inventario()
    
    # Retornar la lista en formato JSON
    return jsonify(lista_productos)

@app.route("/api/comprar", methods=["POST"])
def procesar_compra():
    """
    Ruta que recibe el carrito y el total, obtiene la fecha del sistema,
    llama a registrar la compra en la base de datos y retorna exito.
    """
    datos = request.get_json()
    
    # Obtener el carrito y el total de los datos recibidos
    carrito = datos.get("carrito", [])
    total = datos.get("total", 0.0)
    
    # Obtener la fecha y hora actual del sistema
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Registrar la compra y actualizar el stock pasando el parametro de fecha
    registrar_compra(carrito, total, fecha_actual)
    
    # Retornar mensaje de exito en formato JSON
    return jsonify({"mensaje": "Compra registrada con exito"})

@app.route("/api/historial_compras", methods=["GET"])
def recibir_historial_compras():
    """
    Ruta que recupera el historial de compras realizadas con sus detalles.
    """
    # Obtener la lista de compras del historial
    historial = obtener_historial_compras()
    
    # Retornar el historial en formato JSON
    return jsonify(historial)

@app.route("/api/historial_chat", methods=["GET"])
def recibir_historial_chat():
    """
    Ruta que recupera el historial de conversaciones guardadas del chatbot.
    """
    # Obtener la lista de conversaciones guardadas del chatbot
    historial = obtener_historial_chat()
    
    # Retornar el historial en formato JSON
    return jsonify(historial)

if __name__ == "__main__":
    # Ejecutar el servidor Flask en el puerto 5000 en modo reload
    app.run(debug=True, host="127.0.0.1", port=5000)
