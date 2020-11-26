import Delaunay, { Point } from "./DelaunayFast";

function randomVertices(length: number, width: number, height: number) {
  const vertices: Point[] = Array.from({ length }, () => [
    Math.floor(Math.random() * width),
    Math.floor(Math.random() * height),
  ]);

  return vertices;
}

function draw(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  faces: Point[]
): void {
  console.time("draw");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Render the triangulation
  ctx.beginPath();
  ctx.strokeStyle = "#444444";
  ctx.lineWidth = 1;
  ctx.lineCap = "round";
  for (var i = 0; i < faces.length; i += 3) {
    // Drawn upside down
    ctx.moveTo(faces[i][0], faces[i][1]);
    ctx.lineTo(faces[i + 1][0], faces[i + 1][1]);
    ctx.lineTo(faces[i + 2][0], faces[i + 2][1]);
    ctx.lineTo(faces[i][0], faces[i][1]);
  }
  ctx.stroke();

  console.timeEnd("draw");
}

function experiment(length: number, width: number, height: number) {
  console.time("random");
  const vertices = randomVertices(length, width, height);
  console.timeEnd("random");

  console.time("triangulation");
  const delaunay = new Delaunay(vertices);
  const faces = delaunay.triangulate();
  console.timeEnd("triangulation");
  return faces;
}

const n_vertices = 10000;

function experiments() {
  const n_experiments = 10000;
  for (let i = 0; i < n_experiments; i++) {
    const faces = experiment(n_vertices, 1000, 1000);
  }
}

if (typeof window !== "undefined") {
  const canvas = document.createElement("canvas"),
    ctx = canvas.getContext("2d");
  document.body.appendChild(canvas);
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  if (ctx === null) {
    throw new Error("Canvas could not be created");
  }

  const render = () => {
    const faces = experiment(n_vertices, canvas.width, canvas.height);
    draw(ctx, canvas, faces);

    setTimeout(render, 10);
  };

  render();
} else {
  experiments();
}
