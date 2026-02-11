const API_BASE = process.env.NEXT_PUBLIC_API_BASE!;

export async function apiFetch(path: string, options: RequestInit = {}) {
  const userId = localStorage.getItem("userId");

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(userId ? { "X-User-ID": userId } : {}),
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "API error");
  }

  return res.json();
}
