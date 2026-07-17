import { type NextRequest, NextResponse } from "next/server";

/**
 * Server-side reverse proxy: forwards `/api/*` to the FastAPI backend.
 *
 * The browser only ever talks to the frontend's own origin, so the backend
 * address is a *runtime* concern (`BACKEND_URL`) rather than a build-time one.
 * This means the same frontend image runs unchanged in every environment and
 * the backend can remain internal-only.
 */
const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

async function proxy(request: NextRequest, path: string[]): Promise<Response> {
  const search = request.nextUrl.search;
  const target = `${BACKEND_URL}/api/${path.join("/")}${search}`;

  const init: RequestInit = {
    method: request.method,
    headers: { "Content-Type": "application/json" },
    // Only forward a body for methods that have one.
    body: ["GET", "HEAD"].includes(request.method)
      ? undefined
      : await request.text(),
    cache: "no-store",
  };

  try {
    const upstream = await fetch(target, init);
    const contentType = upstream.headers.get("content-type") ?? "";
    if (upstream.status === 204 || !contentType.includes("application/json")) {
      return new NextResponse(null, { status: upstream.status });
    }
    const data = await upstream.json();
    return NextResponse.json(data, { status: upstream.status });
  } catch {
    return NextResponse.json({ detail: "Backend unavailable" }, { status: 502 });
  }
}

type Context = { params: Promise<{ path: string[] }> };

export async function GET(request: NextRequest, ctx: Context) {
  return proxy(request, (await ctx.params).path);
}

export async function POST(request: NextRequest, ctx: Context) {
  return proxy(request, (await ctx.params).path);
}

export async function DELETE(request: NextRequest, ctx: Context) {
  return proxy(request, (await ctx.params).path);
}

export async function PUT(request: NextRequest, ctx: Context) {
  return proxy(request, (await ctx.params).path);
}
