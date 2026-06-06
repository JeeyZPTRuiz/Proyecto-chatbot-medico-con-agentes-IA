import sqlite3
import random
import os

# Esto obtiene la ruta exacta de la carpeta actual donde esta database.py
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(DIRECTORIO_ACTUAL, 'app.db')

# Funcion para inicializar la base de datos de la botica y sus tablas correspondientes
def inicializar_base_datos():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    # Tabla para el inventario de medicamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_medicamento TEXT NOT NULL,
            principio_activo TEXT NOT NULL,
            tipo_venta TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Tabla para relacionar sintomas con componentes sugeridos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diccionario_clinico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sintoma_reportado TEXT NOT NULL,
            componente_sugerido TEXT NOT NULL,
            nivel_gravedad TEXT NOT NULL
        )
    ''')

    # Tabla para registrar las consultas de triage del bot
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_triage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensaje_paciente TEXT NOT NULL,
            accion_bot TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
    ''')

    # Tabla para compras generales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')

    # Tabla para los detalles de las compras realizadas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compra_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (compra_id) REFERENCES compras (id),
            FOREIGN KEY (producto_id) REFERENCES inventario (id)
        )
    ''')

    conexion.commit()
    conexion.close()
    
    # Rellenar la base de datos con los medicamentos si se encuentra vacia
    poblar_inventario()

# Funcion para rellenar el inventario inicial con 100 medicamentos variados usando executemany
def poblar_inventario():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    # Verificar si el inventario ya cuenta con productos
    cursor.execute("SELECT COUNT(*) FROM inventario")
    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos == 0:
        # Arreglo con 100 medicamentos reales y variados
        medicamentos_iniciales = [
            ("Paracetamol 500mg", "Paracetamol", "Venta Libre"),
            ("Ibuprofeno 400mg", "Ibuprofeno", "Venta Libre"),
            ("Amoxicilina 500mg", "Amoxicilina", "Receta Medica"),
            ("Loratadina 10mg", "Loratadina", "Venta Libre"),
            ("Omeprazol 20mg", "Omeprazol", "Venta Libre"),
            ("Atorvastatina 20mg", "Atorvastatina", "Receta Medica"),
            ("Metformina 850mg", "Metformina", "Receta Medica"),
            ("Losartan 50mg", "Losartan", "Receta Medica"),
            ("Cetirizina 10mg", "Cetirizina", "Venta Libre"),
            ("Salbutamol Inhalador 100mcg", "Salbutamol", "Receta Medica"),
            ("Naproxeno 550mg", "Naproxeno", "Venta Libre"),
            ("Diclofenaco Sodico 75mg", "Diclofenaco", "Venta Libre"),
            ("Azitromicina 500mg", "Azitromicina", "Receta Medica"),
            ("Clonazepam 2mg", "Clonazepam", "Receta Medica"),
            ("Sertralina 50mg", "Sertralina", "Receta Medica"),
            ("Esomeprazol 40mg", "Esomeprazol", "Venta Libre"),
            ("Ranitidina 150mg", "Ranitidina", "Venta Libre"),
            ("Vitamina C 1g Efervescente", "Acido Ascorbico", "Venta Libre"),
            ("Calcio + Vitamina D3", "Calcio y Colecalciferol", "Venta Libre"),
            ("Acido Folico 5mg", "Acido Folico", "Venta Libre"),
            ("Ciprofloxacino 500mg", "Ciprofloxacino", "Receta Medica"),
            ("Clotrimazol Crema 1%", "Clotrimazol", "Venta Libre"),
            ("Hidrocortisona Crema 1%", "Hidrocortisona", "Venta Libre"),
            ("Enalapril 10mg", "Enalapril", "Receta Medica"),
            ("Amlodipino 5mg", "Amlodipino", "Receta Medica"),
            ("Ambroxol Jarabe 30mg/5ml", "Ambroxol", "Venta Libre"),
            ("Dextrometorfano Jarabe", "Dextrometorfano", "Venta Libre"),
            ("Bromhexina Jarabe", "Bromhexina", "Venta Libre"),
            ("Simeticona 80mg", "Simeticona", "Venta Libre"),
            ("Loperamida 2mg", "Loperamida", "Venta Libre"),
            ("Bismuto Subsalicilato", "Bismuto Subsalicilato", "Venta Libre"),
            ("Complejo B Tabletas", "Complejo B", "Venta Libre"),
            ("Sulfato Ferroso 200mg", "Sulfato Ferroso", "Venta Libre"),
            ("Zinc Jarabe 20mg/5ml", "Zinc", "Venta Libre"),
            ("Ketorolaco 10mg", "Ketorolaco", "Receta Medica"),
            ("Meloxicam 15mg", "Meloxicam", "Receta Medica"),
            ("Tramadol 50mg", "Tramadol", "Receta Medica"),
            ("Celecoxib 200mg", "Celecoxib", "Receta Medica"),
            ("Fluconazol 150mg", "Fluconazol", "Venta Libre"),
            ("Aciclovir 400mg", "Aciclovir", "Receta Medica"),
            ("Metronidazol 500mg", "Metronidazol", "Receta Medica"),
            ("Nitrofurantoina 100mg", "Nitrofurantoina", "Receta Medica"),
            ("Claritromicina 500mg", "Claritromicina", "Receta Medica"),
            ("Clindamicina 300mg", "Clindamicina", "Receta Medica"),
            ("Cefalexina 500mg", "Cefalexina", "Receta Medica"),
            ("Doxiciclina 100mg", "Doxiciclina", "Receta Medica"),
            ("Lansoprazol 30mg", "Lansoprazol", "Venta Libre"),
            ("Sucralfato 1g", "Sucralfato", "Receta Medica"),
            ("Clorfenamina 4mg", "Clorfenamina", "Venta Libre"),
            ("Desloratadina 5mg", "Desloratadina", "Venta Libre"),
            ("Fexofenadina 120mg", "Fexofenadina", "Venta Libre"),
            ("Pseudoefedrina 60mg", "Pseudoefedrina", "Receta Medica"),
            ("Acetilcisteina 600mg", "Acetilcisteina", "Venta Libre"),
            ("Captopril 25mg", "Captopril", "Receta Medica"),
            ("Simvastatina 20mg", "Simvastatina", "Receta Medica"),
            ("Rosuvastatina 10mg", "Rosuvastatina", "Receta Medica"),
            ("Hidroclorotiazida 25mg", "Hidroclorotiazida", "Receta Medica"),
            ("Propranolol 40mg", "Propranolol", "Receta Medica"),
            ("Carvedilol 6.25mg", "Carvedilol", "Receta Medica"),
            ("Glibenclamida 5mg", "Glibenclamida", "Receta Medica"),
            ("Glimepirida 2mg", "Glimepirida", "Receta Medica"),
            ("Sitagliptina 50mg", "Sitagliptina", "Receta Medica"),
            ("Vitamina D3 1000UI", "Colecalciferol", "Venta Libre"),
            ("Vitamina E 400UI", "Alfatocoferol", "Venta Libre"),
            ("Magnesio 400mg", "Magnesio", "Venta Libre"),
            ("Fluoxetina 20mg", "Fluoxetina", "Receta Medica"),
            ("Alprazolam 0.5mg", "Alprazolam", "Receta Medica"),
            ("Diazepam 5mg", "Diazepam", "Receta Medica"),
            ("Amitriptilina 25mg", "Amitriptilina", "Receta Medica"),
            ("Mupirocina Unguento 2%", "Mupirocina", "Receta Medica"),
            ("Ketoconazol Champu 2%", "Ketoconazol", "Venta Libre"),
            ("Nafazolina Gotas Oftalmicas", "Nafazolina", "Venta Libre"),
            ("Tobramicina Oftalmica Gotas", "Tobramicina", "Receta Medica"),
            ("Ciprofloxacino Otico Gotas", "Ciprofloxacino", "Receta Medica"),
            ("Lagrimas Artificiales Gotas", "Metilcelulosa", "Venta Libre"),
            ("Hioscina Butilbromuro 10mg", "Hioscina", "Venta Libre"),
            ("Pancreatina Enzimas Digestivas", "Pancreatina", "Venta Libre"),
            ("Mero 500 Inyectable", "Meropenem", "Receta Medica"),
            ("Ceftriaxona 1g Inyectable", "Ceftriaxona", "Receta Medica"),
            ("Prednisona 20mg", "Prednisona", "Receta Medica"),
            ("Dexametasona 4mg", "Dexametasona", "Receta Medica"),
            ("Betametasona Crema 0.05%", "Betametasona", "Receta Medica"),
            ("Salicilato de Metilo Pomada", "Salicilato de Metilo", "Venta Libre"),
            ("Gentamicina Crema 0.1%", "Gentamicina", "Receta Medica"),
            ("Terbinafina Crema 1%", "Terbinafina", "Venta Libre"),
            ("Domperidona 10mg", "Domperidona", "Receta Medica"),
            ("Metoclopramida 10mg", "Metoclopramida", "Receta Medica"),
            ("Ondansetron 8mg", "Ondansetron", "Receta Medica"),
            ("Lactulosa Jarabe", "Lactulosa", "Venta Libre"),
            ("Carbon Activado 250mg", "Carbon Activado", "Venta Libre"),
            ("Fluconazol Crema 2%", "Fluconazol", "Venta Libre"),
            ("Levotiroxina 100mcg", "Levotiroxina", "Receta Medica"),
            ("Warfarina 5mg", "Warfarina", "Receta Medica"),
            ("Clopidogrel 75mg", "Clopidogrel", "Receta Medica"),
            ("Espironolactona 25mg", "Espironolactona", "Receta Medica"),
            ("Furosemida 40mg", "Furosemida", "Receta Medica"),
            ("Finasterida 5mg", "Finasterida", "Receta Medica"),
            ("Tamsulosina 0.4mg", "Tamsulosina", "Receta Medica"),
            ("Alopurinol 300mg", "Alopurinol", "Receta Medica"),
            ("Colchicina 0.5mg", "Colchicina", "Receta Medica")
        ]

        # Preparar la lista de tuplas para la insercion masiva
        medicamentos_insertar = []
        for medicamento in medicamentos_iniciales:
            nombre = medicamento[0]
            principio = medicamento[1]
            tipo = medicamento[2]
            stock_aleatorio = random.randint(20, 200)
            medicamentos_insertar.append((nombre, principio, tipo, stock_aleatorio))

        # Realizar insercion masiva usando executemany
        cursor.executemany('''
            INSERT INTO inventario (nombre_medicamento, principio_activo, tipo_venta, stock)
            VALUES (?, ?, ?, ?)
        ''', medicamentos_insertar)

        conexion.commit()

    conexion.close()

# Funcion para obtener todos los productos del inventario
def obtener_inventario():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_medicamento, principio_activo, tipo_venta, stock FROM inventario")
    filas = cursor.fetchall()
    conexion.close()

    lista_productos = []
    for fila in filas:
        lista_productos.append({
            "id": fila[0],
            "nombre_medicamento": fila[1],
            "principio_activo": fila[2],
            "tipo_venta": fila[3],
            "stock": fila[4]
        })
    return lista_productos

# Funcion para registrar una nueva compra en la base de datos recibiendo la fecha por parametro
def registrar_compra(carrito, total, fecha):
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO compras (total, fecha) VALUES (?, ?)", (total, fecha))
    compra_id = cursor.lastrowid

    for item in carrito:
        producto_id = item.get("producto_id")
        cantidad = item.get("cantidad")
        subtotal = item.get("subtotal")

        # Insertar el detalle de la compra
        cursor.execute('''
            INSERT INTO detalle_compras (compra_id, producto_id, cantidad, subtotal)
            VALUES (?, ?, ?, ?)
        ''', (compra_id, producto_id, cantidad, subtotal))

        # Restar la cantidad del stock en la tabla inventario
        cursor.execute('''
            UPDATE inventario
            SET stock = stock - ?
            WHERE id = ?
        ''', (cantidad, producto_id))

    conexion.commit()
    conexion.close()

# Funcion para recuperar todas las compras con sus detalles
def obtener_historial_compras():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, total, fecha FROM compras ORDER BY id DESC")
    compras_filas = cursor.fetchall()

    historial_completo = []
    for compra in compras_filas:
        compra_id = compra[0]
        
        # Recuperar los detalles de los productos vinculados a la compra
        cursor.execute('''
            SELECT d.id, d.producto_id, d.cantidad, d.subtotal, i.nombre_medicamento
            FROM detalle_compras d
            JOIN inventario i ON d.producto_id = i.id
            WHERE d.compra_id = ?
        ''', (compra_id,))
        detalles_filas = cursor.fetchall()

        lista_detalles = []
        for detalle in detalles_filas:
            lista_detalles.append({
                "id": detalle[0],
                "producto_id": detalle[1],
                "cantidad": detalle[2],
                "subtotal": detalle[3],
                "nombre_medicamento": detalle[4]
            })

        historial_completo.append({
            "id": compra_id,
            "total": compra[1],
            "fecha": compra[2],
            "detalles": lista_detalles
        })

    conexion.close()
    return historial_completo

# Funcion para recuperar el historial de consultas de triage del chatbot
def obtener_historial_chat():
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, mensaje_paciente, accion_bot, fecha_registro FROM historial_triage ORDER BY id DESC")
    filas = cursor.fetchall()
    conexion.close()

    historial = []
    for fila in filas:
        historial.append({
            "id": fila[0],
            "mensaje_paciente": fila[1],
            "accion_bot": fila[2],
            "fecha_registro": fila[3]
        })
    return historial

# Funcion para guardar una nueva consulta de triage realizada
def guardar_triage(mensaje, accion, fecha):
    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()
    
    cursor.execute('''
        INSERT INTO historial_triage (mensaje_paciente, accion_bot, fecha_registro)
        VALUES (?, ?, ?)
    ''', (mensaje, accion, fecha))
    
    conexion.commit()
    conexion.close()
