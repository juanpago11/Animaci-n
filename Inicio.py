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
st.subheader("🎬 Animación estilo Wiggly")

if st.button("Animar estilo Wiggly"):
    if canvas_result.image_data is not None:

        st.write("✨ Animando...")

        image = canvas_result.image_data
        img = Image.fromarray((image).astype("uint8"))

        placeholder = st.empty()

        for i in range(40):
            arr = np.array(img)

            # Crear ruido suave (deformación tipo wiggly)
            noise_x = np.random.randint(-2, 3, arr.shape[:2])
            noise_y = np.random.randint(-2, 3, arr.shape[:2])

            new_img = np.zeros_like(arr)

            for y in range(arr.shape[0]):
                for x in range(arr.shape[1]):
                    nx = np.clip(x + noise_x[y, x], 0, arr.shape[1]-1)
                    ny = np.clip(y + noise_y[y, x], 0, arr.shape[0]-1)
                    new_img[y, x] = arr[ny, nx]

            frame = Image.fromarray(new_img)

            placeholder.image(frame, use_container_width=True)
            time.sleep(0.05)

    else:
        st.warning("⚠️ Primero dibuja algo.")
