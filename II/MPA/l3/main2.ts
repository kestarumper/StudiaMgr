import Delaunay, { Point } from "./DelaunayFast";
import { createExperimentStream } from "./util";

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
  // console.time("random");
  const vertices = randomVertices(length, width, height);
  // console.timeEnd("random");

  // console.time("triangulation");
  const delaunay = new Delaunay(vertices);
  const { faces, iterations } = delaunay.triangulate();
  // console.timeEnd("triangulation");
  return { faces, iterations };
}

const n_vertices = 10000;

function experiments() {
  const n_min = 100;
  const n_step = 100;
  const n_max = 10000;

  const n_experiments = 1000;
  const { write, close } = createExperimentStream(
    "delaunay_fast.csv",
    n_experiments
  );

  const size_x = 1000;
  const size_y = 1000;

  let n, i;
  try {
    for (n = n_min; n <= n_max; n += n_step) {
      console.log(`N=${n}`);
      for (i = 0; i < n_experiments; i++) {
        const { iterations } = experiment(n, size_x, size_y);
        write([n, iterations]);
      }
    }
  } catch (error) {
    console.error(
      `Error while performing experiment n=${n}, iter=${i}.`,
      error
    );
  } finally {
    close();
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
    const { faces } = experiment(n_vertices, canvas.width, canvas.height);
    draw(ctx, canvas, faces);

    setTimeout(render, 10);
  };

  render();
} else {
  experiments();
}
