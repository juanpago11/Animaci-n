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
st.markdown("---")
st.subheader("🎬 Animación dinámica")

if st.button("Animar (modo raro)"):
    if canvas_result.image_data is not None:

        st.write("⚡ Animación activa...")

        img = canvas_result.image_data.astype("uint8")
        placeholder = st.empty()

        for i in range(60):
            arr = img.copy()

            # Movimiento exagerado por bloques
            shift_x = np.random.randint(-15, 15)
            shift_y = np.random.randint(-15, 15)

            # Movimiento rápido (tipo glitch)
            arr = np.roll(arr, shift_x, axis=1)
            arr = np.roll(arr, shift_y, axis=0)

            # Distorsión extra (efecto raro)
            if i % 2 == 0:
                arr = np.roll(arr, np.random.randint(-5, 5), axis=0)

            # Invertir colores aleatoriamente (glitch)
            if np.random.rand() > 0.8:
                arr = 255 - arr

            placeholder.image(arr, use_container_width=True)

            time.sleep(0.03)  # 🔥 mucho más rápido

    else:
        st.warning("⚠️ Primero dibuja algo.")
