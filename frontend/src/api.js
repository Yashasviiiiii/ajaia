import { API_URL } from "./config.js";

const TOKEN_KEY = "docs_token";

export const getToken = () => sessionStorage.getItem(TOKEN_KEY);
export const setToken = (t) => sessionStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => sessionStorage.removeItem(TOKEN_KEY);

async function request(path, { method = "GET", body, form } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let payload;
  if (form) {
    payload = form;
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const res = await fetch(`${API_URL}/api${path}`, { method, headers, body: payload });

  if (res.status === 401 && path !== "/auth/login") {
    clearToken();
    window.dispatchEvent(new Event("auth:logout"));
  }

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      if (typeof data.detail === "string") message = data.detail;
      else if (Array.isArray(data.detail)) message = data.detail.map((d) => d.msg).join(", ");
    } catch {
      /* non-JSON error body */
    }
    throw new Error(message);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  login: (email, password) => request("/auth/login", { method: "POST", body: { email, password } }),
  me: () => request("/auth/me"),
  users: () => request("/users"),
  listDocuments: () => request("/documents"),
  createDocument: (data = {}) => request("/documents", { method: "POST", body: data }),
  importDocument: (form) => request("/documents/import", { method: "POST", form }),
  getDocument: (id) => request(`/documents/${id}`),
  updateDocument: (id, patch) => request(`/documents/${id}`, { method: "PATCH", body: patch }),
  deleteDocument: (id) => request(`/documents/${id}`, { method: "DELETE" }),
  listShares: (id) => request(`/documents/${id}/shares`),
  share: (id, email, permission) =>
    request(`/documents/${id}/shares`, { method: "POST", body: { email, permission } }),
  revokeShare: (id, userId) => request(`/documents/${id}/shares/${userId}`, { method: "DELETE" }),
};