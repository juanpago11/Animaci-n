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
st.subheader("🎬 Animación tipo trazo vivo")

if st.button("Animar trazo"):
    if canvas_result.json_data is not None:

        import copy

        data = canvas_result.json_data
        placeholder = st.empty()

        for _ in range(40):
            new_data = copy.deepcopy(data)

            # Modificar puntos de cada trazo
            for obj in new_data["objects"]:
                if obj["type"] == "path":
                    for point in obj["path"]:
                        if len(point) >= 3:
                            # punto x, y (índices 1 y 2)
                            point[1] += np.random.uniform(-2, 2)
                            point[2] += np.random.uniform(-2, 2)

            # Redibujar canvas con nuevos puntos
            placeholder.write("")  # limpiar

            st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                background_color=bg_color,
                height=canvas_height,
                width=canvas_width,
                drawing_mode="freedraw",
                initial_drawing=new_data,
                key=f"anim_{_}"
            )

            time.sleep(0.05)

    else:
        st.warning("⚠️ Primero dibuja algo.")
