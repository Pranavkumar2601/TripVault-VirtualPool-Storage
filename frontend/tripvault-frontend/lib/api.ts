const API_BASE = "http://localhost:8000/api/v1";

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const userId =
    typeof window !== "undefined" ? localStorage.getItem("tv_user_id") : null;

  if (!userId) {
    window.location.href = "/";
    throw new Error("Not authenticated");
  }

  const headers: HeadersInit = {
    ...(options.headers || {}),
  };

  // Only set JSON content type if not FormData
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  headers["X-User-Id"] = userId;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    localStorage.removeItem("tv_user_id");
    window.location.href = "/";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Request failed");
  }

  if (res.status === 204) return null as T;
  return res.json();
}

export const api = {
  get: <T>(path: string) => apiRequest<T>(path),

  post: <T>(path: string, body?: unknown) =>
    apiRequest<T>(path, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    }),

  patch: <T>(path: string) => apiRequest<T>(path, { method: "PATCH" }),

  delete: <T>(path: string) => apiRequest<T>(path, { method: "DELETE" }),
};
