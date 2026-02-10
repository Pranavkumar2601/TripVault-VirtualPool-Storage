const API_BASE = process.env.NEXT_PUBLIC_API_BASE!;

export async function apiFetch(
  path: string,
  options: RequestInit = {},
  userId?: string,
) {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(userId ? { "X-User-ID": userId } : {}),
    ...(options.headers || {}),
  };

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }

  return res.json();
}
