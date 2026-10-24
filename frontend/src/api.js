// All calls to the backend live here. No API keys: the key stays in backend/.env.

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

export const getDocuments = () => fetch("/api/documents").then(handle);

export function uploadFiles(files) {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  return fetch("/api/upload", { method: "POST", body: form }).then(handle);
}

export const clearDocuments = () =>
  fetch("/api/documents", { method: "DELETE" }).then(handle);

export const sendChat = (question, history) =>
  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, history }),
  }).then(handle);
