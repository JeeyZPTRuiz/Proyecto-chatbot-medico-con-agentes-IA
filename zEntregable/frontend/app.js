// Captura de los elementos principales del DOM para el chat
const entrada_usuario = document.getElementById("entrada_usuario");
const boton_enviar = document.getElementById("boton_enviar");
const contenedor_chat = document.getElementById("contenedor_chat");
const barra_lateral_chat = document.getElementById("barra_lateral_chat");
const boton_menu_movil = document.getElementById("boton_menu_movil");

// Captura de los elementos principales del DOM para el panel
const panel_principal = document.getElementById("panel_principal");
const lista_productos = document.getElementById("lista_productos");
const contenido_carrito = document.getElementById("contenido_carrito");
const total_compra = document.getElementById("total_compra");
const boton_procesar_compra = document.getElementById("boton_procesar_compra");

// Captura de los botones de navegacion
const boton_nav_productos = document.getElementById("boton_nav_productos");
const boton_nav_carrito = document.getElementById("boton_nav_carrito");
const boton_nav_compras = document.getElementById("boton_nav_compras");
const boton_nav_chat = document.getElementById("boton_nav_chat");

// Captura de los contenedores de las vistas
const vista_productos = document.getElementById("vista_productos");
const vista_carrito = document.getElementById("vista_carrito");
const vista_compras = document.getElementById("vista_compras");
const vista_historial_chat = document.getElementById("vista_historial_chat");

// Tablas de historial
const tabla_compras_cuerpo = document.getElementById("tabla_compras_cuerpo");
const tabla_chat_cuerpo = document.getElementById("tabla_chat_cuerpo");

// Array global del carrito de compras
let carrito = [];

// Cambia la vista activa del panel principal ocultando las demas y marcando el boton nav
function cambiar_vista(vista_id) {
    // Ocultar todas las vistas
    vista_productos.classList.add("oculto");
    vista_carrito.classList.add("oculto");
    vista_compras.classList.add("oculto");
    vista_historial_chat.classList.add("oculto");

    // Quitar clase activa a todos los botones
    boton_nav_productos.classList.remove("activo");
    boton_nav_carrito.classList.remove("activo");
    boton_nav_compras.classList.remove("activo");
    boton_nav_chat.classList.remove("activo");

    // Mostrar la vista seleccionada y activar su boton correspondiente
    if (vista_id === "vista_productos") {
        vista_productos.classList.remove("oculto");
        boton_nav_productos.classList.add("activo");
    } else if (vista_id === "vista_carrito") {
        vista_carrito.classList.remove("oculto");
        boton_nav_carrito.classList.add("activo");
        renderizar_carrito();
    } else if (vista_id === "vista_compras") {
        vista_compras.classList.remove("oculto");
        boton_nav_compras.classList.add("activo");
        cargar_historial_compras();
    } else if (vista_id === "vista_historial_chat") {
        vista_historial_chat.classList.remove("oculto");
        boton_nav_chat.classList.add("activo");
        cargar_historial_chat();
    }
}

// Carga la lista de medicamentos desde el servidor asincronamente
async function cargar_inventario() {
    try {
        const respuesta = await fetch("/api/inventario");
        if (!respuesta.ok) {
            throw new Error("Error al obtener el inventario");
        }
        const productos = await respuesta.json();
        renderizar_productos(productos);
    } catch (error) {
        console.error("Error al cargar inventario:", error);
    }
}

// Renderiza los medicamentos en la vista del inventario
function renderizar_productos(productos) {
    lista_productos.innerHTML = "";

    if (productos.length === 0) {
        lista_productos.innerHTML = '<div class="mensaje_vacio">No hay productos en el inventario</div>';
        return;
    }

    productos.forEach(function (producto) {
        const tarjeta = document.createElement("div");
        tarjeta.classList.add("tarjeta_producto");

        // Simular precio estatico determinista basado en el ID del producto
        const precio = (producto.id % 7) * 3.5 + 4.0;

        tarjeta.innerHTML = `
            <h3>${producto.nombre_medicamento}</h3>
            <p><strong>Principio Activo:</strong> ${producto.principio_activo}</p>
            <span class="badge_tipo">${producto.tipo_venta}</span>
            <div class="stock_info">
                <span>Stock:</span>
                <strong>${producto.stock} unidades</strong>
            </div>
            <div class="stock_info" style="margin-top: 4px;">
                <span>Precio:</span>
                <strong>S/. ${precio.toFixed(2)}</strong>
            </div>
            <button class="boton_agregar_carrito" onclick="anadir_al_carrito(${producto.id}, '${producto.nombre_medicamento}', ${precio}, ${producto.stock})">
                Anadir al carrito
            </button>
        `;

        lista_productos.appendChild(tarjeta);
    });
}

// Agrega un medicamento al carrito global o incrementa su cantidad
function anadir_al_carrito(producto_id, nombre, precio, stock_maximo) {
    const item_existente = carrito.find(item => item.producto_id === producto_id);

    if (item_existente) {
        if (item_existente.cantidad >= stock_maximo) {
            alert("No hay suficiente stock disponible de este medicamento");
            return;
        }
        item_existente.cantidad += 1;
        item_existente.subtotal = item_existente.cantidad * item_existente.precio;
    } else {
        if (stock_maximo <= 0) {
            alert("Este medicamento no cuenta con stock disponible");
            return;
        }
        carrito.push({
            producto_id: producto_id,
            nombre_medicamento: nombre,
            precio: precio,
            cantidad: 1,
            subtotal: precio
        });
    }

    alert("Medicamento agregado al carrito");
}

// Renderiza los medicamentos agregados en el panel del carrito
function renderizar_carrito() {
    contenido_carrito.innerHTML = "";

    if (carrito.length === 0) {
        contenido_carrito.innerHTML = '<div class="mensaje_vacio">El carrito esta vacio</div>';
        total_compra.textContent = "0.00";
        boton_procesar_compra.disabled = true;
        return;
    }

    boton_procesar_compra.disabled = false;
    let total_acumulado = 0.0;

    carrito.forEach(function (item, indice) {
        total_acumulado += item.subtotal;

        const elemento_item = document.createElement("div");
        elemento_item.classList.add("item_carrito");

        elemento_item.innerHTML = `
            <div class="info_item">
                <span class="nombre_item">${item.nombre_medicamento}</span>
                <span class="detalles_item">Precio unitario: S/. ${item.precio.toFixed(2)}</span>
            </div>
            <div class="acciones_item">
                <span class="cantidad_item">${item.cantidad} u.</span>
                <span class="nombre_item">S/. ${item.subtotal.toFixed(2)}</span>
                <button class="boton_quitar" onclick="quitar_del_carrito(${indice})">🗑️</button>
            </div>
        `;

        contenido_carrito.appendChild(elemento_item);
    });

    total_compra.textContent = total_acumulado.toFixed(2);
}

// Remueve un elemento del carrito segun su indice
function quitar_del_carrito(indice) {
    carrito.splice(indice, 1);
    renderizar_carrito();
}

// Realiza el envio de la compra del carrito al servidor asincronamente
async function procesar_compra() {
    if (carrito.length === 0) {
        return;
    }

    let total_acumulado = 0.0;
    carrito.forEach(function (item) {
        total_acumulado += item.subtotal;
    });

    const payload = {
        carrito: carrito,
        total: total_acumulado
    };

    try {
        const respuesta = await fetch("/api/comprar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!respuesta.ok) {
            throw new Error("Error al realizar la compra");
        }

        alert("Compra procesada con exito");

        // Vaciar el carrito y actualizar la interfaz del catalogo
        carrito = [];
        await cargar_inventario();
        cambiar_vista("vista_productos");
    } catch (error) {
        console.error("Error al procesar compra:", error);
        alert("Ocurrio un problema al procesar la compra");
    }
}

// Consume asincronamente el historial de compras y lo inyecta en la tabla
async function cargar_historial_compras() {
    try {
        const respuesta = await fetch("/api/historial_compras");
        if (!respuesta.ok) {
            throw new Error("Error al cargar historial de compras");
        }
        const historial = await respuesta.json();
        renderizar_tabla_compras(historial);
    } catch (error) {
        console.error("Error al cargar historial compras:", error);
    }
}

// Inyecta las filas correspondientes en la tabla de historial de compras
function renderizar_tabla_compras(historial) {
    tabla_compras_cuerpo.innerHTML = "";

    if (historial.length === 0) {
        tabla_compras_cuerpo.innerHTML = '<tr><td colspan="4" style="text-align: center;">No hay compras registradas</td></tr>';
        return;
    }

    historial.forEach(function (compra) {
        const detalles_texto = compra.detalles.map(d => `${d.nombre_medicamento} (x${d.cantidad})`).join(", ");

        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${compra.id}</td>
            <td>S/. ${compra.total.toFixed(2)}</td>
            <td>${compra.fecha}</td>
            <td>${detalles_texto}</td>
        `;
        tabla_compras_cuerpo.appendChild(fila);
    });
}

// Consume asincronamente el historial de chat de triage y lo inyecta en la tabla
async function cargar_historial_chat() {
    try {
        const respuesta = await fetch("/api/historial_chat");
        if (!respuesta.ok) {
            throw new Error("Error al cargar historial del chat");
        }
        const historial = await respuesta.json();
        renderizar_tabla_chat(historial);
    } catch (error) {
        console.error("Error al cargar historial chat:", error);
    }
}

// Inyecta las filas correspondientes en la tabla de historial del chat
function renderizar_tabla_chat(historial) {
    tabla_chat_cuerpo.innerHTML = "";

    if (historial.length === 0) {
        tabla_chat_cuerpo.innerHTML = '<tr><td colspan="4" style="text-align: center;">No hay conversaciones registradas</td></tr>';
        return;
    }

    historial.forEach(function (chat) {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${chat.id}</td>
            <td>${chat.mensaje_paciente}</td>
            <td>${chat.accion_bot}</td>
            <td>${chat.fecha_registro}</td>
        `;
        tabla_chat_cuerpo.appendChild(fila);
    });
}

// Agrega un mensaje al historial del chat en la pantalla
function agregar_mensaje_interfaz(texto, remitente) {
    const div_mensaje = document.createElement("div");
    div_mensaje.classList.add("mensaje", remitente);

    const div_contenido = document.createElement("div");
    div_contenido.classList.add("contenido_mensaje");
    div_contenido.textContent = texto;

    div_mensaje.appendChild(div_contenido);
    contenedor_chat.appendChild(div_mensaje);

    // Hacer scroll automatico hacia abajo en el chat
    contenedor_chat.scrollTop = contenedor_chat.scrollHeight;

    let texto_formateado = texto.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    div_contenido.innerHTML = texto_formateado;
}

// Captura la consulta del usuario, la envia al servidor y muestra la respuesta
async function enviar_mensaje() {
    const texto = entrada_usuario.value.trim();
    if (!texto) {
        return;
    }

    // Mostrar el mensaje ingresado por el usuario
    agregar_mensaje_interfaz(texto, "usuario");

    // Limpiar el campo de entrada
    entrada_usuario.value = "";

    try {
        // Realizar la peticion post al servidor
        const respuesta = await fetch("/api/mensaje", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ mensaje_usuario: texto })
        });

        if (!respuesta.ok) {
            throw new Error("Respuesta de red incorrecta");
        }

        const datos = await respuesta.json();

        // Agregar la respuesta del bot de botica
        agregar_mensaje_interfaz(datos.respuesta, "bot");
    } catch (error) {
        // Manejar el error de conexion en la interfaz
        agregar_mensaje_interfaz("Lo sentimos, ha ocurrido un error de conexion. Por favor, intenta de nuevo.", "bot");
    }
}

// Altera la visibilidad de la barra de chat en dispositivos moviles
function alternar_vista_chat() {
    barra_lateral_chat.classList.toggle("activo");
}

// Enlace de los eventos de navegacion
boton_nav_productos.addEventListener("click", () => cambiar_vista("vista_productos"));
boton_nav_carrito.addEventListener("click", () => cambiar_vista("vista_carrito"));
boton_nav_compras.addEventListener("click", () => cambiar_vista("vista_compras"));
boton_nav_chat.addEventListener("click", () => cambiar_vista("vista_historial_chat"));

// Enlace de los eventos del chat
boton_enviar.addEventListener("click", enviar_mensaje);
entrada_usuario.addEventListener("keypress", function (evento) {
    if (evento.key === "Enter") {
        enviar_mensaje();
    }
});

// Enlace de los eventos de compras
boton_procesar_compra.addEventListener("click", procesar_compra);

// Enlace del boton movil
if (boton_menu_movil) {
    boton_menu_movil.addEventListener("click", alternar_vista_chat);
}

// Carga inicial al cargar el documento
document.addEventListener("DOMContentLoaded", function () {
    cargar_inventario();
});
