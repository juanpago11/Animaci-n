import streamlit as st
import numpy as np
import time
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# 🎯 Configuración
st.set_page_config(page_title="Super Tablero")

# 🎨 Título
st.title("Tablero de dibujo")
st.subheader("Pinta y dale movimiento")

# 🧱 Sidebar
with st.sidebar:
    st.subheader("⚙️ Propiedades del Tablero")

    # Dimensiones
    st.markdown("### 📐 Dimensiones")
    canvas_width = st.slider("Ancho", 300, 800, 500, 50)
    canvas_height = st.slider("Alto", 200, 600, 300, 50)

    # Herramientas
    st.markdown("### 🛠️ Herramientas")
    herramienta = st.selectbox(
        "Selecciona:",
        ("Dibujar", "Línea", "Rectángulo", "Círculo", "Mover", "Borrador"),
    )

    modos = {
        "Dibujar": "freedraw",
        "Línea": "line",
        "Rectángulo": "rect",
        "Círculo": "circle",
        "Mover": "transform",
        "Borrador": "freedraw",
    }

    drawing_mode = modos[herramienta]

    # Tamaño del trazo
    stroke_width = st.slider("✏️ Tamaño del trazo", 1, 30, 10)

    # Colores
    st.markdown("### 🎨 Colores")
    stroke_color = st.color_picker("Color de trazo", "#000000")
    bg_color = st.color_picker("Color de fondo", "#FFFFFF")

# 🧽 Borrador
if herramienta == "Borrador":
    stroke_color = bg_color

# 🎨 Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",
)

# -------------------------------
# 🎬 ANIMACIÓN
# -------------------------------
import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<body style="margin:0; overflow:hidden; background:white;">
<canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = 600;
canvas.height = 400;

let drawing = false;
let paths = [];

// Dibujar
canvas.addEventListener("mousedown", () => drawing = true);
canvas.addEventListener("mouseup", () => drawing = false);

canvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    paths.push({x, y});
});

// Animación WIGGLY REAL
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();

    for (let i = 0; i < paths.length; i++) {
        let p = paths[i];

        // 🔥 Aquí está el efecto Wiggly
        let wiggleX = p.x + (Math.random() - 0.5) * 4;
        let wiggleY = p.y + (Math.random() - 0.5) * 4;

        if (i === 0) {
            ctx.moveTo(wiggleX, wiggleY);
        } else {
            ctx.lineTo(wiggleX, wiggleY);
        }
    }

    ctx.strokeStyle = "black";
    ctx.lineWidth = 3;
    ctx.stroke();

    requestAnimationFrame(animate);
}

animate();
</script>

</body>
</html>
""", height=420)
