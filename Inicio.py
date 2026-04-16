import streamlit as st
import numpy as np
import time
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# 🎯 Configuración
st.set_page_config(page_title="Super Tablero")

# 🎨 Título
st.title("🟧 Super Tablero")
st.subheader("Dibuja en él ✏️")

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
st.subheader("🎬 Animación del dibujo")

if st.button("Animar dibujo"):
    if canvas_result.image_data is not None:

        st.write("✨ Animando...")

        image = canvas_result.image_data
        img = Image.fromarray((image).astype("uint8"))

        placeholder = st.empty()

        # Loop animación
        for i in range(30):
            dx = np.random.randint(-4, 4)
            dy = np.random.randint(-4, 4)

            frame = Image.new("RGBA", img.size, (255, 255, 255, 0))
            frame.paste(img, (dx, dy))

            placeholder.image(frame, use_container_width=True)

            time.sleep(0.07)

    else:
        st.warning("⚠️ Primero dibuja algo.")
