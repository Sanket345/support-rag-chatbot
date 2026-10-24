import { useEffect, useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ChatPanel from "./components/ChatPanel";
import { clearDocuments, getDocuments, sendChat, uploadFiles } from "./api";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState(null); // { type: "ok" | "error", text }
  const [showSidebar, setShowSidebar] = useState(false);

  useEffect(() => {
    getDocuments()
      .then(setDocuments)
      .catch(() =>
        setNotice({ type: "error", text: "Cannot reach the backend. Is it running on port 8000?" })
      );
  }, []);

  async function handleUpload(files) {
    setUploading(true);
    setNotice(null);
    try {
      const data = await uploadFiles(files);
      setDocuments(data.documents);
      const warn = data.errors.length ? ` (${data.errors.join("; ")})` : "";
      setNotice({ type: data.errors.length ? "error" : "ok", text: `Indexed ${data.indexed.length} file(s).${warn}` });
    } catch (e) {
      setNotice({ type: "error", text: e.message });
    } finally {
      setUploading(false);
    }
  }

  async function handleClear() {
    try {
      await clearDocuments();
      setDocuments([]);
      setMessages([]);
      setNotice({ type: "ok", text: "All documents removed." });
    } catch (e) {
      setNotice({ type: "error", text: e.message });
    }
  }

  async function handleSend(question) {
    // Send previous turns so the bot can understand follow-up questions.
    const history = messages
      .filter((m) => !m.error)
      .map(({ role, content }) => ({ role, content }));

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);
    try {
      const data = await sendChat(question, history);
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer, sources: data.sources }]);
    } catch (e) {
      setMessages((prev) => [...prev, { role: "assistant", content: e.message, error: true }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen flex-col md:flex-row">
      <header className="flex items-center justify-between border-b bg-white px-4 py-3 md:hidden">
        <h1 className="font-semibold text-slate-800">Support Assistant</h1>
        <button
          onClick={() => setShowSidebar((s) => !s)}
          className="rounded-md border px-3 py-1 text-sm text-slate-600"
        >
          {showSidebar ? "Hide documents" : "Documents"}
        </button>
      </header>

      <aside
        className={`${showSidebar ? "block" : "hidden"} max-h-[60vh] overflow-y-auto border-b bg-white md:block md:max-h-none md:w-80 md:border-b-0 md:border-r`}
      >
        <UploadPanel
          documents={documents}
          uploading={uploading}
          notice={notice}
          onUpload={handleUpload}
          onClear={handleClear}
        />
      </aside>

      <main className="min-h-0 flex-1">
        <ChatPanel
          messages={messages}
          loading={loading}
          disabled={documents.length === 0}
          onSend={handleSend}
        />
      </main>
    </div>
  );
}
