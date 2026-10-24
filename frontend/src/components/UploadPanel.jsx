import { useRef, useState } from "react";

export default function UploadPanel({ documents, uploading, notice, onUpload, onClear }) {
  const [selected, setSelected] = useState([]);
  const inputRef = useRef(null);

  async function submit() {
    await onUpload(selected);
    setSelected([]);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="space-y-4 p-4">
      <h1 className="hidden text-lg font-semibold text-slate-800 md:block">Support Assistant</h1>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Upload PDFs</label>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          multiple
          onChange={(e) => setSelected(Array.from(e.target.files))}
          className="block w-full text-sm text-slate-600 file:mr-3 file:rounded-md file:border-0 file:bg-slate-100 file:px-3 file:py-2 file:text-sm file:font-medium hover:file:bg-slate-200"
        />
        <button
          onClick={submit}
          disabled={selected.length === 0 || uploading}
          className="mt-3 flex w-full items-center justify-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {uploading && (
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
          )}
          {uploading ? "Processing..." : `Upload ${selected.length || ""} file(s)`}
        </button>
      </div>

      {notice && (
        <p
          className={`rounded-md p-2 text-sm ${
            notice.type === "error" ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700"
          }`}
        >
          {notice.text}
        </p>
      )}

      <div>
        <div className="mb-2 flex items-center justify-between">
          <h2 className="text-sm font-medium text-slate-700">Indexed documents</h2>
          {documents.length > 0 && (
            <button onClick={onClear} className="text-xs text-red-600 hover:underline">
              Remove all
            </button>
          )}
        </div>
        {documents.length === 0 ? (
          <p className="text-sm text-slate-500">No documents yet.</p>
        ) : (
          <ul className="space-y-2">
            {documents.map((d) => (
              <li key={d.name} className="rounded-md border bg-slate-50 px-3 py-2 text-sm">
                <p className="truncate font-medium text-slate-800">📄 {d.name}</p>
                <p className="text-xs text-slate-500">{d.chunks} chunks</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
