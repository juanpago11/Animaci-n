import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Tablero")

st.title("Super Tablero")

# SIDEBAR
with st.sidebar:
    st.subheader("Propiedades")

    canvas_width = st.slider("Ancho", 300, 900, 600)
    canvas_height = st.slider("Alto", 200, 600, 300)

    stroke_width = st.slider("Tamaño del trazo", 1, 20, 3)

    stroke_color = st.color_picker("Color del trazo", "#000000")
    bg_color = st.color_picker("Color de fondo", "#FFFFFF")

    herramienta = st.selectbox("Herramienta", ["Dibujar", "Borrador"])

erase_mode = "true" if herramienta == "Borrador" else "false"

# BOTÓN LIMPIAR
if st.button("Limpiar dibujo"):
    components.html("""
    <script>
    localStorage.removeItem("drawing_paths");
    location.reload();
    </script>
    """, height=0)

# HTML + JS
components.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{ margin: 0; font-family: sans-serif; background: {bg_color}; }}
canvas {{ border: 1px solid #ccc; display: block; margin: 10px auto; }}
h3 {{ text-align: center; margin: 5px; }}
</style>
</head>

<body>

<h3>Dibujo</h3>
<canvas id="drawCanvas"></canvas>

<div style="height:40px; border-bottom:1px solid #ccc;"></div>

<h3>Dibujo con movimiento</h3>
<canvas id="animCanvas"></canvas>

<script>
const drawCanvas = document.getElementById("drawCanvas");
const animCanvas = document.getElementById("animCanvas");

const drawCtx = drawCanvas.getContext("2d");
const animCtx = animCanvas.getContext("2d");

drawCanvas.width = {canvas_width};
drawCanvas.height = {canvas_height};

animCanvas.width = {canvas_width};
animCanvas.height = {canvas_height};

let drawing = false;
let paths = [];
let currentPath = [];
let eraseMode = {erase_mode};

// CARGAR DESDE LOCALSTORAGE
const saved = localStorage.getItem("drawing_paths");
if (saved) {{
    paths = JSON.parse(saved);
}}

function getMousePos(canvas, evt) {{
    const rect = canvas.getBoundingClientRect();
    return {{
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    }};
}}

// INICIAR TRAZO
drawCanvas.addEventListener("mousedown", (e) => {{
    drawing = true;

    if (!eraseMode) {{
        currentPath = [];
        paths.push(currentPath);
    }} else {{
        erase(e);
    }}
}});

// TERMINAR TRAZO
drawCanvas.addEventListener("mouseup", () => drawing = false);

// DIBUJAR
drawCanvas.addEventListener("mousemove", (e) => {{
    if (!drawing) return;

    if (eraseMode) {{
        erase(e);
        return;
    }}

    const pos = getMousePos(drawCanvas, e);
    currentPath.push(pos);

    // GUARDAR
    localStorage.setItem("drawing_paths", JSON.stringify(paths));
}});

// BORRADOR
function erase(e) {{
    const pos = getMousePos(drawCanvas, e);

    paths = paths.filter(path => {{
        return !path.some(p => {{
            const dx = p.x - pos.x;
            const dy = p.y - pos.y;
            return Math.sqrt(dx*dx + dy*dy) < {stroke_width * 2};
        }});
    }});

    // GUARDAR
    localStorage.setItem("drawing_paths", JSON.stringify(paths));
}}

// DIBUJO ESTÁTICO
function drawStatic() {{
    drawCtx.fillStyle = "{bg_color}";
    drawCtx.fillRect(0, 0, drawCanvas.width, drawCanvas.height);

    drawCtx.lineWidth = {stroke_width};
    drawCtx.strokeStyle = "{stroke_color}";

    for (let path of paths) {{
        if (path.length < 2) continue;

        drawCtx.beginPath();

        for (let i = 0; i < path.length; i++) {{
            let p = path[i];
            if (i === 0) drawCtx.moveTo(p.x, p.y);
            else drawCtx.lineTo(p.x, p.y);
        }}

        drawCtx.stroke();
    }}
}}

// ANIMACIÓN WIGGLY
function animate() {{
    animCtx.fillStyle = "{bg_color}";
    animCtx.fillRect(0, 0, animCanvas.width, animCanvas.height);

    animCtx.lineWidth = {stroke_width};
    animCtx.strokeStyle = "{stroke_color}";

    for (let path of paths) {{
        if (path.length < 2) continue;

        animCtx.beginPath();

        for (let i = 0; i < path.length; i++) {{
            let p = path[i];

            let x = p.x + (Math.random() - 0.5) * 4;
            let y = p.y + (Math.random() - 0.5) * 4;

            if (i === 0) animCtx.moveTo(x, y);
            else animCtx.lineTo(x, y);
        }}

        animCtx.stroke();
    }}

    drawStatic();
    requestAnimationFrame(animate);
}}

animate();
</script>

</body>
</html>
""", height=canvas_height * 2 + 140)
