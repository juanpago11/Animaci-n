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

function getMousePos(canvas, evt) {{
    const rect = canvas.getBoundingClientRect();
    return {{
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    }};
}}

drawCanvas.addEventListener("mousedown", (e) => {{
    drawing = true;

    if (!eraseMode) {{
        currentPath = [];
        paths.push(currentPath);
    }} else {{
        erase(e);
    }}
}});

drawCanvas.addEventListener("mouseup", () => drawing = false);

drawCanvas.addEventListener("mousemove", (e) => {{
    if (!drawing) return;

    if (eraseMode) {{
        erase(e);
        return;
    }}

    const pos = getMousePos(drawCanvas, e);
    currentPath.push(pos);
}});

function erase(e) {{
    const pos = getMousePos(drawCanvas, e);

    paths = paths.filter(path => {{
        return !path.some(p => {{
            const dx = p.x - pos.x;
            const dy = p.y - pos.y;
            return Math.sqrt(dx*dx + dy*dy) < {stroke_width * 2};
        }});
    }});
}}

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
""", height=canvas_height * 2 + 120)
