import { useEffect, useRef, useState } from "react";
import Message from "./Message";

export default function ChatPanel({ messages, loading, disabled, onSend }) {
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  function submit() {
    const question = input.trim();
    if (!question || loading || disabled) return;
    setInput("");
    onSend(question);
  }

  function onKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div className="mt-20 text-center text-slate-500">
            <p className="text-lg font-medium text-slate-700">How can I help?</p>
            <p className="mt-1 text-sm">
              {disabled
                ? "Upload at least one PDF to get started."
                : "Ask a question about your company documents."}
            </p>
          </div>
        )}

        {messages.map((m, i) => (
          <Message key={i} message={m} />
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-1 rounded-2xl border bg-white px-4 py-3 shadow-sm">
              {[0, 150, 300].map((delay) => (
                <span
                  key={delay}
                  className="h-2 w-2 animate-bounce rounded-full bg-slate-400"
                  style={{ animationDelay: `${delay}ms` }}
                />
              ))}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="border-t bg-white p-3">
        <div className="mx-auto flex max-w-3xl items-end gap-2">
          <textarea
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            disabled={disabled}
            placeholder={disabled ? "Upload a PDF first..." : "Type your question..."}
            className="max-h-32 flex-1 resize-none rounded-xl border px-3 py-2 text-sm outline-none focus:border-indigo-500 disabled:bg-slate-100"
          />
          <button
            onClick={submit}
            disabled={disabled || loading || !input.trim()}
            className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
