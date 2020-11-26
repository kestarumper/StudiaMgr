import * as delaunay from "./Delaunay";

function randomVertices(length: number, width: number, height: number) {
  const vertices = Array.from(
    { length },
    () =>
      new delaunay.Vertex(
        Math.floor(Math.random() * width),
        Math.floor(Math.random() * height)
      )
  );

  // Vertice for each corner
  vertices.push(new delaunay.Vertex(0, 0));
  vertices.push(new delaunay.Vertex(width, 0));
  vertices.push(new delaunay.Vertex(0, height));
  vertices.push(new delaunay.Vertex(width, height));

  return vertices;
}

function draw(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  vertices: delaunay.Vertex[],
  triangles: delaunay.Triangle[]
): void {
  console.time("draw");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.lineWidth = 1;

  triangles.forEach(function (triangle) {
    // Draw triangles
    ctx.beginPath();
    ctx.moveTo(triangle.v0.x, triangle.v0.y);
    ctx.lineTo(triangle.v1.x, triangle.v1.y);
    ctx.lineTo(triangle.v2.x, triangle.v2.y);
    ctx.closePath();
    ctx.strokeStyle = "rgba(1, 1, 1, .1)";
    ctx.stroke();

    // Draw circumcircles
    // ctx.beginPath();
    // ctx.arc(triangle.center.x, triangle.center.y, triangle.radius, 0, Math.PI*2, true );
    // ctx.closePath();
    // ctx.strokeStyle = 'rgba(1, 1, 1, .1)';
    // ctx.stroke();
  });

  // Draw vertices
  vertices.forEach(function (vertex) {
    ctx.beginPath();
    ctx.arc(vertex.x, vertex.y, 2, 0, Math.PI * 2, true);
    ctx.closePath();
    ctx.fillStyle = "#999";
    ctx.fill();
  });
  console.timeEnd("draw");
}

function experiment(length: number, width: number, height: number) {
  console.time("random");
  const vertices = randomVertices(length, width, height);
  console.timeEnd("random");

  console.time("triangulation");
  const triangles = delaunay.triangulate(vertices);
  console.timeEnd("triangulation");
  return { vertices, triangles };
}

function experiments() {
  const n_vertices = 10000;
  const n_experiments = 10000;
  for (let i = 0; i < n_experiments; i++) {
    const { vertices, triangles } = experiment(n_vertices, 1000, 1000);
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
    const { vertices, triangles } = experiment(
      1000,
      canvas.width,
      canvas.height
    );
    draw(ctx, canvas, vertices, triangles);

    setTimeout(render, 1000);
  };

  render();
} else {
  experiments();
}
