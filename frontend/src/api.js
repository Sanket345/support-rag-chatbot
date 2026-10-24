// In production, VITE_API_URL is the Render backend URL. Locally it's empty and the Vite proxy is used.
const BASE = import.meta.env.VITE_API_URL || "";

async function handle(res) {
  if (!res.ok) {
    let detail = "Request failed";
    try {
      detail = (await res.json()).detail || detail;
    } catch {}
    throw new Error(detail);
  }
  return res.json();
}

export const getDocuments = () => fetch(`${BASE}/api/documents`).then(handle);

export function uploadFiles(files) {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  return fetch(`${BASE}/api/upload`, { method: "POST", body: form }).then(
    handle,
  );
}

export const clearDocuments = () =>
  fetch(`${BASE}/api/documents`, { method: "DELETE" }).then(handle);

export const sendChat = (question, history) =>
  fetch(`${BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, history }),
  }).then(handle);
