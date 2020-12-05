import { Counter, makeCounter } from "./util";

export class Vertex {
  x: number;
  y: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }

  equals(vertex: Vertex): boolean {
    return this.x === vertex.x && this.y == vertex.y;
  }
}

export class Edge {
  v0: Vertex;
  v1: Vertex;

  constructor(v0: Vertex, v1: Vertex) {
    this.v0 = v0;
    this.v1 = v1;
  }

  equals(edge: Edge) {
    return (
      (this.v0.equals(edge.v0) && this.v1.equals(edge.v1)) ||
      (this.v0.equals(edge.v1) && this.v1.equals(edge.v0))
    );
  }

  inverse() {
    return new Edge(this.v1, this.v0);
  }
}

export class Triangle {
  v0: Vertex;
  v1: Vertex;
  v2: Vertex;
  radius: number = NaN;
  center: Vertex | null = null;

  constructor(v0: Vertex, v1: Vertex, v2: Vertex) {
    this.v0 = v0;
    this.v1 = v1;
    this.v2 = v2;

    this.calcCircumcircle();
  }

  calcCircumcircle() {
    // Reference: http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 1.04
    const A = this.v1.x - this.v0.x;
    const B = this.v1.y - this.v0.y;
    const C = this.v2.x - this.v0.x;
    const D = this.v2.y - this.v0.y;

    const E = A * (this.v0.x + this.v1.x) + B * (this.v0.y + this.v1.y);
    const F = C * (this.v0.x + this.v2.x) + D * (this.v0.y + this.v2.y);

    const G = 2.0 * (A * (this.v2.y - this.v1.y) - B * (this.v2.x - this.v1.x));

    let dx: number, dy: number;

    // Collinear points, get extremes and use midpoint as center
    if (Math.round(Math.abs(G)) == 0) {
      const minx = Math.min(this.v0.x, this.v1.x, this.v2.x);
      const miny = Math.min(this.v0.y, this.v1.y, this.v2.y);
      const maxx = Math.max(this.v0.x, this.v1.x, this.v2.x);
      const maxy = Math.max(this.v0.y, this.v1.y, this.v2.y);

      this.center = new Vertex((minx + maxx) / 2, (miny + maxy) / 2);

      dx = this.center.x - minx;
      dy = this.center.y - miny;
    } else {
      const cx = (D * E - B * F) / G;
      const cy = (A * F - C * E) / G;

      this.center = new Vertex(cx, cy);

      dx = this.center.x - this.v0.x;
      dy = this.center.y - this.v0.y;
    }

    this.radius = Math.sqrt(dx * dx + dy * dy);
  }

  inCircumcircle(v: Vertex) {
    ITERATION_COUNTER.inc();
    if (this.center === null) {
      throw new Error("Center is null");
    }
    const dx = this.center.x - v.x;
    const dy = this.center.y - v.y;
    return Math.sqrt(dx * dx + dy * dy) <= this.radius;
  }
}

function superTriangle(vertices: Vertex[]): Triangle {
  let miny = Infinity;
  let minx = miny;
  let maxy = -Infinity;
  let maxx = maxy;

  vertices.forEach(function (vertex) {
    minx = Math.min(minx, vertex.x);
    miny = Math.min(minx, vertex.y);
    maxx = Math.max(maxx, vertex.x);
    maxy = Math.max(maxx, vertex.y);
  });

  const dx = (maxx - minx) * 10,
    dy = (maxy - miny) * 10;

  const v0 = new Vertex(minx - dx, miny - dy * 3),
    v1 = new Vertex(minx - dx, maxy + dy),
    v2 = new Vertex(maxx + dx * 3, maxy + dy);

  return new Triangle(v0, v1, v2);
}

function addVertex(vertex: Vertex, triangles: Triangle[]) {
  const edges: Edge[] = [];
  // Remove triangles with circumcircles containing the vertex
  const trianglesFiltered = triangles.filter(function (triangle) {
    if (triangle.inCircumcircle(vertex)) {
      edges.push(new Edge(triangle.v0, triangle.v1));
      edges.push(new Edge(triangle.v1, triangle.v2));
      edges.push(new Edge(triangle.v2, triangle.v0));
      return false;
    }
    return true;
  });

  const badTriangles = triangles.length - trianglesFiltered.length;

  // Get unique edges
  const uniqEdges = uniqueEdges(edges);

  // Create new triangles from the unique edges and new vertex
  uniqEdges.forEach(function (edge) {
    ITERATION_COUNTER.inc();
    trianglesFiltered.push(new Triangle(edge.v0, edge.v1, vertex));
  });

  const newTrianglesDiff = Math.abs(
    trianglesFiltered.length - triangles.length
  );

  return { triangles: trianglesFiltered, diff: newTrianglesDiff, badTriangles };
}

function uniqueEdges(edges: Edge[]) {
  const uniqueEdges = [];
  for (let i = 0; i < edges.length; ++i) {
    let isUnique = true;

    // See if edge is unique
    for (let j = 0; j < edges.length; ++j) {
      ITERATION_COUNTER.inc();
      if (i != j && edges[i].equals(edges[j])) {
        isUnique = false;
        break;
      }
    }

    // Edge is unique, add to unique edges array
    isUnique && uniqueEdges.push(edges[i]);
  }

  return uniqueEdges;
}

let ITERATION_COUNTER: Counter;
export function triangulate(vertices: Vertex[]) {
  ITERATION_COUNTER = makeCounter();
  // Create bounding 'super' triangle
  const st = superTriangle(vertices);

  // Initialize triangles while adding bounding triangle
  let triangles = [st];
  const totalTrianglesCreated: number[] = [];
  const totalBadTriangles: number[] = [];

  // Triangulate each vertex
  vertices.forEach(function (vertex) {
    const { triangles: newTriangles, diff, badTriangles } = addVertex(
      vertex,
      triangles
    );
    triangles = newTriangles;
    totalTrianglesCreated.push(diff);
    totalBadTriangles.push(badTriangles);
  });

  // Remove triangles that share edges with super triangle
  triangles = triangles.filter(
    (triangle) =>
      !(
        triangle.v0 == st.v0 ||
        triangle.v0 == st.v1 ||
        triangle.v0 == st.v2 ||
        triangle.v1 == st.v0 ||
        triangle.v1 == st.v1 ||
        triangle.v1 == st.v2 ||
        triangle.v2 == st.v0 ||
        triangle.v2 == st.v1 ||
        triangle.v2 == st.v2
      )
  );

  return {
    triangles,
    totalTrianglesCreated,
    totalBadTriangles,
    iterations: ITERATION_COUNTER.get(),
  };
}
