import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { margin: 0; font-family: sans-serif; }
canvas { border: 1px solid #ccc; display: block; margin: 10px auto; }
h3 { text-align: center; margin: 5px; }
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

drawCanvas.width = 600;
drawCanvas.height = 300;
animCanvas.width = 600;
animCanvas.height = 300;

let drawing = false;
let paths = [];
let currentPath = [];
let eraseMode = false;

// modo borrador con tecla "e"
document.addEventListener("keydown", (e) => {
    if (e.key === "e") eraseMode = true;
});
document.addEventListener("keyup", (e) => {
    if (e.key === "e") eraseMode = false;
});

function getMousePos(canvas, evt) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

// iniciar trazo
drawCanvas.addEventListener("mousedown", (e) => {
    drawing = true;

    if (!eraseMode) {
        currentPath = [];
        paths.push(currentPath);
    } else {
        erase(e);
    }
});

// terminar trazo
drawCanvas.addEventListener("mouseup", () => {
    drawing = false;
});

// mover mouse
drawCanvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;

    if (eraseMode) {
        erase(e);
        return;
    }

    const pos = getMousePos(drawCanvas, e);
    currentPath.push(pos);
});

// borrador: elimina trazos cercanos
function erase(e) {
    const pos = getMousePos(drawCanvas, e);

    paths = paths.filter(path => {
        return !path.some(p => {
            const dx = p.x - pos.x;
            const dy = p.y - pos.y;
            return Math.sqrt(dx*dx + dy*dy) < 10;
        });
    });
}

// dibujo normal (arriba)
function drawStatic() {
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

    drawCtx.lineWidth = 3;
    drawCtx.strokeStyle = "black";

    for (let path of paths) {
        if (path.length < 2) continue;

        drawCtx.beginPath();

        for (let i = 0; i < path.length; i++) {
            let p = path[i];
            if (i === 0) drawCtx.moveTo(p.x, p.y);
            else drawCtx.lineTo(p.x, p.y);
        }

        drawCtx.stroke();
    }
}

// animación (wiggly real)
function animate() {
    animCtx.clearRect(0, 0, animCanvas.width, animCanvas.height);

    animCtx.lineWidth = 3;
    animCtx.strokeStyle = "black";

    for (let path of paths) {
        if (path.length < 2) continue;

        animCtx.beginPath();

        for (let i = 0; i < path.length; i++) {
            let p = path[i];

            let x = p.x + (Math.random() - 0.5) * 4;
            let y = p.y + (Math.random() - 0.5) * 4;

            if (i === 0) animCtx.moveTo(x, y);
            else animCtx.lineTo(x, y);
        }

        animCtx.stroke();
    }

    drawStatic();
    requestAnimationFrame(animate);
}

animate();
</script>

</body>
</html>
""", height=650)
