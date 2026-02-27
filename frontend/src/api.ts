// API utility to handle backend requests
// Uses VITE_API_URL env variable for production, falls back to relative paths for dev

const API_BASE = (import.meta as any).env?.VITE_API_URL || "";

export async function apiFetch(path: string, options?: RequestInit): Promise<Response> {
  const url = `${API_BASE}${path}`;
  return fetch(url, options);
}
