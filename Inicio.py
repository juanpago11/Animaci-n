import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<body style="margin:0; background:white; font-family:sans-serif;">

<h3 style="text-align:center;">🎨 Dibujo</h3>
<canvas id="drawCanvas"></canvas>

<h3 style="text-align:center; margin-top:20px;">🎬 Dibujo con movimiento</h3>
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

// 🖱️ Detectar tecla E para borrar
window.addEventListener("keydown", (e) => {
    if (e.key === "e") eraseMode = true;
});
window.addEventListener("keyup", (e) => {
    if (e.key === "e") eraseMode = false;
});

// Iniciar trazo
drawCanvas.addEventListener("mousedown", (e) => {
    drawing = true;

    if (!eraseMode) {
        currentPath = [];
        paths.push(currentPath);
    } else {
        eraseAt(e);
    }
});

// Terminar trazo
drawCanvas.addEventListener("mouseup", () => drawing = false);

// Dibujar
drawCanvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;

    if (eraseMode) {
        eraseAt(e);
        return;
    }

    const rect = drawCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    currentPath.push({x, y});
});

// 🧽 BORRADOR (elimina trazos cercanos)
function eraseAt(e) {
    const rect = drawCanvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    paths = paths.filter(path => {
        return !path.some(p => {
            const dx = p.x - x;
            const dy = p.y - y;
            return Math.sqrt(dx*dx + dy*dy) < 15;
        });
    });
}

// 🎨 Dibujar original (arriba)
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

// 🎬 Animación Wiggly (abajo)
function animate() {
    animCtx.clearRect(0, 0, animCanvas.width, animCanvas.height);

    animCtx.lineWidth = 3;
    animCtx.strokeStyle = "black";

    for (let path of paths) {
        if (path.length < 2) continue;

        animCtx.beginPath();

        for (let i = 0; i < path.length; i++) {
            let p = path[i];

            let wiggleX = p.x + (Math.random() - 0.5) * 4;
            let wiggleY = p.y + (Math.random() - 0.5) * 4;

            if (i === 0) animCtx.moveTo(wiggleX, wiggleY);
            else animCtx.lineTo(wiggleX, wiggleY);
        }

        animCtx.stroke();
    }

    drawStatic(); // mantener dibujo original arriba
    requestAnimationFrame(animate);
}

animate();
</script>

</body>
</html>
""", height=650)
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
